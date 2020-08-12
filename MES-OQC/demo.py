from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time
import re

# dic={
#         "D01":"1272015079198396416",
#         "D02":"1272015655940362240",
#         "D03":"1272015794260119552",
#         "D04":"1272015911050514432",
#         "C02":"1272849679634128896",
#         "H01":"1285508455294021632",
#     }
# try:
#     raise KeyError
# except KeyError:
#     print('error')

options=webdriver.ChromeOptions()      # option:run browser no error in command
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser=webdriver.Chrome(chrome_options=options)
URL="https://www.baidu.com/"   
browser.get(URL)
NO_list=[font_ele.text for font_ele in browser.find_elements_by_css_selector('input[id="barcode"]')]
print(NO_list)
print(not NO_list)