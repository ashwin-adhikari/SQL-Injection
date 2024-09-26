"""
SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

import os


driver = webdriver.Firefox('C:/Users/Ripple/Downloads/geckodriver-v0.35.0-win64/geckodriver.exe')
driver.get("https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data")
