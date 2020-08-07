# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# import re
# class LoadFail(Exception):
#     def __init__(self,page):
#         self.page=page
#     def __str__(self):
#         return "Error:{}加载失败".format(self.page)

# NO={
#     "ST101":"1272015079198396416",
#     "ST102":"1272015655940362240",
#     "ST103":"1272015794260119552",
#     "ST104":"1272015911050514432",
#     "SQ102":"1272849679634128896",
# }
# browser=webdriver.Chrome()
# browser.maximize_window()
# browser.implicitly_wait(5)
# username="7711"
# password="7711"
# URL="http://192.168.8.34:8950/login-view.html"    
# browser.get(URL)
# workStation=Select(browser.find_element_by_css_selector("#workStation"))
# oprNO="SQ102"
# workStation.select_by_value(NO[oprNO])
# browser.find_element_by_css_selector("#username").send_keys(username)
# pw=browser.find_element_by_css_selector("#password")
# pw.send_keys(password)
# pw.send_keys(Keys.ENTER)
# status=WebDriverWait(browser,3).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR,'a[id="clearLog"]'))
#         )
# browser.switch_to.frame("frame")
# input_name=browser.find_element_by_css_selector('input[id="barcode"]')
# sn="11111111111111"
# input_name.send_keys(sn)
# input_name.send_keys(Keys.ENTER)
# browser.switch_to.default_content()
# WebDriverWait(browser,3).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR,'div>p:nth-child(2)'))
#                 )
# clearLog=WebDriverWait(browser,3).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR,'a[id="clearLog"]'))
#         )
# clearLog.click()
from selenium import webdriver
options=webdriver.ChromeOptions()      # option:run browser in the background
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser=webdriver.Chrome(chrome_options=options)
# browser.maximize_window()
browser.implicitly_wait(5)
URL="https://www.baidu.com/"     
browser.get(URL)