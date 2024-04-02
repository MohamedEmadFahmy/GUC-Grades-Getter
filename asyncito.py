import asyncio
import requests
# from requests_negotiate_sspi import HttpNegotiateAuth
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
import os

from requests_ntlm import HttpNtlmAuth

async def fetch_and_process_grades(authentication):

    gradesURL = "https://apps.guc.edu.eg/student_ext/Grade/CheckGrade_01.aspx"
    

    dropDownListId = "ContentPlaceHolderright_ContentPlaceHoldercontent_smCrsLst"

    # Fetch the initial page
    response = requests.get(gradesURL, auth=authentication)
    # response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    fields = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": soup.find('input', {'id': '__VIEWSTATE'}).get('value', ''),
        "__VIEWSTATEGENERATOR": soup.find('input', {'id': '__VIEWSTATEGENERATOR'}).get('value', ''),
        "__EVENTVALIDATION": soup.find('input', {'id': '__EVENTVALIDATION'}).get('value', ''),
        "ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$HiddenFieldstudent": soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldstudent'}).get('value', ''),
        "ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$HiddenFieldseason": soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldseason'}).get('value', ''),
        "ctl00$ctl00$div_position": soup.find('input', {'id': 'div_position'}).get('value', ''),
        # "hiddenFieldEvalMethIdValue": soup.find('input', {'id': 'ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$rptrNtt$ctl02$evalMethId'})['value']
    }

    dropdown = soup.find('select', {'id': dropDownListId})
    options = dropdown.find_all('option')

    tasks = []
    for i, option in enumerate(options):
        if i == 0:
            continue
        tasks.append(process_option(option, gradesURL, authentication ,fields, i))

    await asyncio.gather(*tasks)

async def process_option(option, gradesURL,authentication,fields, i):
    option_value = option['value']
    fields['ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$smCrsLst'] = option_value

    # Post request for each option
    response = requests.post(gradesURL, data=fields,auth=authentication)
    response.raise_for_status()
    html = response.text
    with open(f"gradepage{i}.html", "w") as file:
        file.write(html)
    print(option.text)

start_time = time.time()

load_dotenv()
username = os.getenv("guc_username")
password = os.getenv("guc_password")
authentication  = HttpNtlmAuth(username=username, password=password)

asyncio.run(fetch_and_process_grades(authentication=authentication))

end_time = time.time()
elapsed_time = end_time - start_time

print("Elapsed time: {:.6f} seconds".format(elapsed_time))
