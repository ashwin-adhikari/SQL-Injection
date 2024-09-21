"""
SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By


# url = r'https://portswigger.net/academy/labs/launch/13e48d1949abb8793e11da34ed06a5811ea3a9b2be0501a5e9f0deb255d37406?referrer=%2fweb-security%2fsql-injection%2fexamining-the-database%2flab-querying-database-version-mysql-microsoft'

# soup = BeautifulSoup(html, 'lxml')
# filters = soup.find('section', class_ = "search-filters")
# print(filters)

driver = webdriver.Edge()

driver.get('https://portswigger.net/academy/labs/launch/13e48d1949abb8793e11da34ed06a5811ea3a9b2be0501a5e9f0deb255d37406?referrer=%2fweb-security%2fsql-injection%2fexamining-the-database%2flab-querying-database-version-mysql-microsoft')

element = driver.find_element(By.ID, 'sb_form_q')
element.send_keys('WebDriver')
element.submit()
print(element)
time.sleep(5)
driver.quit()