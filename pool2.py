import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
import time
import concurrent.futures
from dotenv import load_dotenv
import os

def fetchGrades():
    def process_option(option, gradesURL, session, fields, i):
        option_value = option['value']
        fields['ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$smCrsLst'] = option_value
        
        response = requests.post(gradesURL, data=fields, auth=authentication)
    
        with open(f"gradepage{i}.html", "w") as file:
            file.write(response.text)
            print(option.text)


    gradesURL = "https://apps.guc.edu.eg/student_ext/Grade/CheckGrade_01.aspx"

    load_dotenv()
    username = os.getenv("guc_username")
    password = os.getenv("guc_password")
    print(username, password)
    dropDownListId = "ContentPlaceHolderright_ContentPlaceHoldercontent_smCrsLst"
    # viewStateValue = ""

    authentication = HttpNtlmAuth(username, password)
    # session = requests.Session()
    # session.auth = authentication
    # response = session.get(gradesURL)
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
        # session = requests.Session()
        # session.auth = authentication
        for i, option in enumerate(options):
            if i == 0:
                continue
            futures.append(executor.submit(process_option, option, gradesURL, authentication, fields, i))
        
        for future in concurrent.futures.as_completed(futures):
            pass  # You can handle any cleanup or result processing here if needed



# start_time = time.time()
# fetchGrades()

# end_time = time.time()
# elapsed_time = end_time - start_time
# print("Elapsed time: {:.6f} seconds".format(elapsed_time))
        

# Number of times to run the function
num_runs = 15

# Measure the total elapsed time
total_elapsed_time = 0
for _ in range(num_runs):
    start_time = time.time()
    fetchGrades()
    end_time = time.time()
    total_elapsed_time += end_time - start_time

# Calculate average elapsed time
average_elapsed_time = total_elapsed_time / num_runs

print("Average elapsed time for {} runs: {:.6f} seconds".format(num_runs, average_elapsed_time))


# 4.83