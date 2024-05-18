import os
# import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
import concurrent.futures
from dotenv import load_dotenv
from time import sleep

from rich.console import Console
from rich.progress import Progress
from rich.table import Table

import keyboard
import time

console = Console()

allGrades = []


def fetchCourseTable(option,courseName, gradesURL, authentication, fields, i):
    option_value = option['value']
    fields['ctl00$ctl00$ContentPlaceHolderright$ContentPlaceHoldercontent$smCrsLst'] = option_value

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

        return [courseName, table[0]]
    
    # response = requests.post(gradesURL, data=fields, auth=authentication)
    # soup = BeautifulSoup(response.text, 'html.parser')

    # # Find the table within the div
    # table = soup.select('#ContentPlaceHolderright_ContentPlaceHoldercontent_nttTr table')

    # if len(table) == 0:
    #     return None

    # return [courseName, table[0]]



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
        
        with Progress() as progress:
            task = progress.add_task("[bold green]Fetching grades...", total=len(options) - 1)

            for i, option in enumerate(options):
                if i == 0:
                    continue
                futures.append(executor.submit(fetchCourseTable, option, option.text.strip(),  gradesURL, authentication, fields, i))
            
            for future in concurrent.futures.as_completed(futures):
                # You can handle any cleanup or result processing here if needed
                [courseName, table] = future.result()
                parseTable(courseName, table)
                progress.update(task, advance=1)
                sleep(0.1)
            
                

def parseTable(courseName, table):
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
        
    
    allGrades.append([courseName, datasets])


    # print(datasets)
    # print()
    # print("\n\n\n")

load_dotenv()
username = os.getenv("guc_username")
password = os.getenv("guc_password")

# start_time = time.time()
# end_time = time.time()
# elapsed_time = end_time - start_time
# print("Elapsed time: {:.6f} seconds".format(elapsed_time))

fetchGrades(username, password)
console.clear()
# console.log("Hi there!")
# console.log("Here are your grades:")
# console.log(allGrades)




# table = Table(title="Courses" ,box=None)

# for course in allGrades:
#     table.add_row(course[0], style="cyan")


# console.print(table)

# while True:
#     3+3

def update_table(selected_index):
    table = Table(title="Courses", box=None)
    for i, course in enumerate(allGrades):
        if i == selected_index:
            table.add_row(course[0], style="cyan")
        else:
            table.add_row(course[0])
    console.clear()
    console.print(table)
    
def print_grades(courseIndex):
    console.clear()
    table = Table(title=allGrades[courseIndex][0], box=None)
    for grade in allGrades[courseIndex][1]:
        table.add_row(grade[0], grade[1], grade[2], grade[3])
    
    if len(allGrades[courseIndex][1]) == 0:
        table.add_row("No grades available for this course!")
        
    console.print(table)

    
    
        

def handle_key_press():
    selected_index = 0
    update_table(selected_index)
    
    while True:
        if keyboard.is_pressed('up'):
            selected_index = (selected_index - 1) % len(allGrades)
            update_table(selected_index)
        elif keyboard.is_pressed('down'):
            selected_index = (selected_index + 1) % len(allGrades)
            update_table(selected_index)
        elif keyboard.is_pressed('enter'):
            print_grades(selected_index)
            while True:
                if keyboard.is_pressed('backspace'):
                    break
            
            update_table(selected_index)
            # time.sleep(0.1)
            
        time.sleep(0.1)

handle_key_press()
