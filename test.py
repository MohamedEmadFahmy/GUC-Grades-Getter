import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Replace the placeholders with your actual values
url = 'https://student.guc.edu.eg'
gradesURL = "https://apps.guc.edu.eg/student_ext/Grade/CheckGrade_01.aspx"
load_dotenv()
username = os.getenv("guc_username")
password = os.getenv("guc_password")
dropDownListId = "ContentPlaceHolderright_ContentPlaceHoldercontent_smCrsLst"
viewStateValue = ""

# Create a session with NTLM authentication
session = requests.Session()
session.auth = HttpNtlmAuth(username, password)

# Make the NTLM request
# response = session.get(url)
response = session.get(gradesURL)

soup = BeautifulSoup(response.text, 'html.parser')


# Find the dropdown list element
dropdown = soup.find('select', {'id': f'{dropDownListId}'})


# print(dropdown)

options = dropdown.find_all('option')

print(options)

# Iterate through each option
for i,option in enumerate(options):

    if(i == 0):
        continue

    if i > 3:
        break

    # session2 = requests.Session()
    # session2.auth = HttpNtlmAuth(username, password)

    # Make the NTLM request
    # response = session.get(url)
    # response = session.get(gradesURL)

    soup = BeautifulSoup(response.text, 'html.parser')



    viewstate_div = soup.find('input', {'id': '__VIEWSTATE'})

    if viewstate_div:
        viewStateValue = viewstate_div['value']
    else:
        print("Error")

    hidden_field_student = soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldstudent'})
    if hidden_field_student:
        hidden_field_student_value = hidden_field_student.get('value')
    else:
        print("Error")



    hidden_field_season = soup.find('input', {'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldseason'})

    # Extract the value attribute
    if hidden_field_season:
        hidden_field_season_value = hidden_field_season.get('value')
    else:
        print("Error")

    hidden_field_div_position = soup.find('input', {'id': 'div_position'})

    # Extract the value attribute
    if hidden_field_div_position:
        hidden_field_div_position_value = hidden_field_div_position.get('value')
    else:
        print("Error")



    hidden_field_viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})
    hidden_field_eventvalidation = soup.find('input', {'id': '__EVENTVALIDATION'})

    # Extract the value attributes
    if hidden_field_viewstategenerator:
        viewstategenerator_value = hidden_field_viewstategenerator.get('value')
    else:
        print("Error")

    if hidden_field_eventvalidation:
        eventvalidation_value = hidden_field_eventvalidation.get('value')
    else:
        print("Error")



    hidden_field_eval_meth_id = soup.find('input', {'id': 'ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$rptrNtt$ctl02$evalMethId'})

    # Extract the value attribute
    if hidden_field_eval_meth_id:
        hidden_field_eval_meth_id_value = hidden_field_eval_meth_id.get('value')
    else:
        hidden_field_eval_meth_id_value = ""
        # print("Error")




    # Get the value of the option
    option_value = option['value']
    # Set the payload with the selected option
    payload = {
        # "__EVENTTARGET": "ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$smCrsLst",
        # "__EVENTARGUMENT": "",
        # "__LASTFOCUS": "",
        "__VIEWSTATE": viewStateValue,
        # "__VIEWSTATEGENERATOR": viewstategenerator_value,
        # "__EVENTVALIDATION": eventvalidation_value,
        # "'ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$smCrsLst'": option_value,
        # # "'ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$rptrNtt$ctl02$evalMethId'":hidden_field_eval_meth_id_value,
        # "ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldstudent": hidden_field_student_value,
        # "ContentPlaceHolderright_ContentPlaceHoldercontent_HiddenFieldseason": hidden_field_season_value,
        # "ctl00$ctl00$div_position": hidden_field_div_position_value
    }


    # javascript:setTimeout('__doPostBack(\'ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$smCrsLst\',\'\')', 0)

    # Send a POST request with the payload

   

    # requests.get(gradesURL)
    response = session.post("https://apps.guc.edu.eg/student_ext/Grade/CheckGrade_01.aspx", data=payload)
  
    print(response.status_code)

    # print(payload)
    # print(payload["ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$smCrsLst"])

    # Parse the response
    soup_response = BeautifulSoup(response.text, 'html.parser')
    
    # if i == 4:
        # print(soup_response)
    with open(f"gradepage{i}.html", "w") as file:
        # Write the content to the file
        file.write(response.text)
        print(option.text)

    table = soup_response.find('table', class_='table table-bordered')
    
    # Print the table contents if found
    # if table:
    #     print(table)
    #     print("-------")
    # else:
    #     print("Table not found on the page")


# Print the response content
# print(response.text)