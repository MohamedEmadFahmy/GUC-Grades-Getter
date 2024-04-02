import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
import time
import concurrent.futures
from dotenv import load_dotenv
import os

def process_option(option, gradesURL, authentication, fields, i):
    option_value = option['value']
    fields['ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$smCrsLst'] = option_value
        
    response = requests.post(gradesURL, data=fields, auth=authentication)
    
    with open(f"gradepage{i}.html", "w") as file:
        file.write(response.text)
        print(option.text)



def fetchGrades(username, password):


    gradesURL = "https://apps.guc.edu.eg/student_ext/Grade/CheckGrade_01.aspx"

    dropDownListId = "ContentPlaceHolderright_ContentPlaceHoldercontent_smCrsLst"


    authentication = HttpNtlmAuth(username, password)

    response = requests.get(gradesURL, auth=authentication)
    soup = BeautifulSoup(response.text, 'html.parser')

    fields = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": soup.find('input', {'id': '__VIEWSTATE'}).get('value', '') if soup.find('input', {'id': '__VIEWSTATE'}) else '',
        "__VIEWSTATEGENERATOR": soup.find('input', {'id': '__VIEWSTATEGENERATOR'}).get('value', '') if soup.find('input', {'id': '__VIEWSTATEGENERATOR'}) else '',
        "__EVENTVALIDATION": soup.find('input', {'id': '__EVENTVALIDATION'}).get('value', '') if soup.find('input', {'id': '__EVENTVALIDATION'}) else '',
        "ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$HiddenFieldstudent": soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldstudent'}).get('value', '') if soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldstudent'}) else '',
        "ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$HiddenFieldseason": soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldseason'}).get('value', '') if soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldseason'}) else '',
        "ctl00$ctl00$div_position": soup.find('input', {'id': 'div_position'}).get('value', '') if soup.find('input', {'id': 'div_position'}) else '',
        "hiddenFieldEvalMethIdValue": soup.find('input', {'id': 'ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$rptrNtt$ctl02$evalMethId'})['value'] if soup.find('input', {'id': 'ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$rptrNtt$ctl02$evalMethId'}) else ''
    }

    dropdown = soup.find('select', {'id': f'{dropDownListId}'})
    options = dropdown.find_all('option')

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []

        for i, option in enumerate(options):
            if i == 0:
                continue
            futures.append(executor.submit(process_option, option, gradesURL, authentication, fields, i))
        
        for future in concurrent.futures.as_completed(futures):
            pass  # You can handle any cleanup or result processing here if needed



load_dotenv()
username = os.getenv("guc_username")
password = os.getenv("guc_password")

start_time = time.time()
fetchGrades(username, password)

end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time: {:.6f} seconds".format(elapsed_time))
        

