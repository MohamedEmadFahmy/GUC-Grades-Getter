import os
from dotenv import load_dotenv
import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup

def make_grades_request(payload):
    # URL for the POST request
    gradesURL = "https://apps.guc.edu.eg/student_ext/Grade/CheckGrade_01.aspx"

    load_dotenv()
    username = os.getenv("guc_username")
    password = os.getenv("guc_password")

    session = requests.Session()
    session.auth = HttpNtlmAuth(username, password)

    # Make a GET request to obtain the initial __VIEWSTATE
    response = session.get(gradesURL)
    if response.status_code != 200:
        return f"Error: {response.status_code}"

    # Parse the response HTML to extract the __VIEWSTATE value
    soup = BeautifulSoup(response.text, 'html.parser')
    viewstate_element = soup.find('input', {'id': '__VIEWSTATE'})
    if not viewstate_element:
        return "Error: __VIEWSTATE not found in response"

    viewstate_value = viewstate_element.get('value')

    # Update the payload with the extracted __VIEWSTATE value
    payload['__VIEWSTATE'] = viewstate_value

    # Make a POST request with the updated payload and NTLM authentication
    response = session.post(gradesURL, data=payload)

    if response.status_code == 200:
        # Save the response content to the specified file
        with open("temp.html", "w") as file:
            file.write(response.text)
        return "Response saved to test.html"
    else:
        # Return an error message
        return f"Error: {response.status_code}"

# Example payload data (replace with actual values)
example_payload = {
    # Include other form data parameters as needed
}

# Make the request using the example payload
print(make_grades_request(example_payload))
