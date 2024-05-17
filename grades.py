import os
# import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
import concurrent.futures
from dotenv import load_dotenv
import time

def fetchCourseTable(option, gradesURL, authentication, fields, i):
    option_value = option['value']
    fields['ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$smCrsLst'] = option_value
        
    # response = requests.post(gradesURL, data=fields, auth=authentication)

    # Construct the path to the HTML file
    file_path = os.path.join(os.getcwd(), 'pages', f'gradepage{i}.html')

    # Check if the file exists
    if os.path.exists(file_path):
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            response = file.read()

        soup = BeautifulSoup(response, 'html.parser')

        # Find the table within the div
        table = soup.select('#ContentPlaceHolderright_ContentPlaceHoldercontent_nttTr table')

        if len(table) == 0:
            return None

        return table[0]
    
    return None

def fetchGrades(username, password):
    gradesURL = "https://apps.guc.edu.eg/student_ext/Grade/CheckGrade_01.aspx"
    dropDownListId = "ContentPlaceHolderright_ContentPlaceHoldercontent_smCrsLst"
    authentication = HttpNtlmAuth(username, password)

    file_path = os.path.join(os.getcwd(), 'pages', 'gradepage1.html')

    # Check if the file exists
    if os.path.exists(file_path):
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            response = file.read()

        soup = BeautifulSoup(response, 'html.parser')

    # response = requests.get(gradesURL, auth=authentication)
    # soup = BeautifulSoup(response.text, 'html.parser')

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
            futures.append(executor.submit(fetchCourseTable, option, gradesURL, authentication, fields, i))
        
        for future in concurrent.futures.as_completed(futures):
            # You can handle any cleanup or result processing here if needed
            table = future.result()
            parseTable(table)

def parseTable(table):
    if table is None:
        print("Table is None")
        return []

    ''' Extract Data from html table of grades '''
    datasets = []
    for row in table.find_all("tr")[1:]:
        element = []
        for item in row.find_all('td'):
            element.append(item.text.strip())
        datasets.append(element)

    # Fix grades format
    for element in datasets:
        grades = element[2].split()
        element[2] = ''.join(grades)


    print(datasets)
    print()
    # print("\n\n\n")

load_dotenv()
username = os.getenv("guc_username")
password = os.getenv("guc_password")

start_time = time.time()
fetchGrades(username, password)
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time: {:.6f} seconds".format(elapsed_time))
