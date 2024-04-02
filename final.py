import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
import os

start_time = time.time()


url = 'https://student.guc.edu.eg'
gradesURL = "https://apps.guc.edu.eg/student_ext/Grade/CheckGrade_01.aspx"
load_dotenv()
username = os.getenv("guc_username")
password = os.getenv("guc_password")
dropDownListId = "ContentPlaceHolderright_ContentPlaceHoldercontent_smCrsLst"
viewStateValue = ""

session = requests.Session()
session.auth = HttpNtlmAuth(username, password)

response = session.get(gradesURL)

soup = BeautifulSoup(response.text, 'html.parser')

fields = {
    'viewStateValue': soup.find('input', {'id': '__VIEWSTATE'}).get('value') if soup.find('input', {'id': '__VIEWSTATE'}) else '',
    'hiddenFieldStudentValue': soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldstudent'}).get('value') if soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldstudent'}) else '',
    'hiddenFieldSeasonValue': soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldseason'}).get('value') if soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldseason'}) else '',
    'hiddenFieldDivPositionValue': soup.find('input', {'id': 'div_position'}).get('value') if soup.find('input', {'id': 'div_position'}) else '',
    'viewStateGeneratorValue': soup.find('input', {'id': '__VIEWSTATEGENERATOR'}).get('value') if soup.find('input', {'id': '__VIEWSTATEGENERATOR'}) else '',
    'eventValidationValue': soup.find('input', {'id': '__EVENTVALIDATION'}).get('value') if soup.find('input', {'id': '__EVENTVALIDATION'}) else '',
    'hiddenFieldEvalMethIdValue': soup.find('input', {'id': 'ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$rptrNtt$ctl02$evalMethId'}).get('value') if soup.find('input', {'id': 'ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$rptrNtt$ctl02$evalMethId'}) else ''
}

dropdown = soup.find('select', {'id': f'{dropDownListId}'})



options = dropdown.find_all('option')

# print(options)

for i,option in enumerate(options):

    if(i == 0):
        continue



    soup = BeautifulSoup(response.text, 'html.parser')

    option_value = option['value']


    payload = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": fields['viewStateValue'],
        "__VIEWSTATEGENERATOR": fields['viewStateGeneratorValue'],
        "__EVENTVALIDATION": fields['eventValidationValue'],
        "ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$smCrsLst": option_value,
        "ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$HiddenFieldstudent": fields['hiddenFieldStudentValue'],
        "ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$HiddenFieldseason": fields['hiddenFieldSeasonValue'],
        "ctl00$ctl00$div_position": fields['hiddenFieldDivPositionValue'],
    }
   

    # response = requests.post(gradesURL, data=payload,auth = HttpNtlmAuth(username, password))
    
    response = session.post(gradesURL, data=payload)

    # tempSession = requests.Session()
    # tempSession.auth = HttpNtlmAuth(username, password)
    # response = tempSession.post(gradesURL, data=payload)
  
    # print(response.status_code)


    soup_response = BeautifulSoup(response.text, 'html.parser')
    
    with open(f"gradepage{i}.html", "w") as file:
        file.write(response.text)
        print(option.text)

    table = soup_response.find('table', class_='table table-bordered')
    

end_time = time.time()

elapsed_time = end_time - start_time

print("Elapsed time: {:.6f} seconds".format(elapsed_time))