from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import re
import math

def sn_read(file_str):  # read sn from file(sn.txt),return sn list
    sn_list=[]
    with open(file_str,'r') as f:
        sn_text=f.read()
        sn_list=re.findall(r'\S+',sn_text)   # find all sn
    return sn_list

def log(username,password,proc="1272849679634128896"):
    URL="http://192.168.8.34:8950/login-view.html"
    browser.get(URL)
    sel = Select(browser.find_element_by_css_selector("#workStation"))
    sel.select_by_value(proc)
    browser.find_element_by_css_selector("#username").send_keys(username)
    pw=browser.find_element_by_css_selector("#password")
    pw.send_keys(password)
    pw.send_keys(Keys.ENTER)
    browser.implicitly_wait(5)

def load(sn):
    # browser.switch_to.default_content()
    # sel = Select(browser.find_element_by_css_selector('select[id="workStationSelect"]'))
    # # proc="1272849679634128896"
    # sel.select_by_value(proc)
    # browser.implicitly_wait(5)
    browser.switch_to.frame("frame")
    input_name=browser.find_element_by_css_selector('input[id="barcode"]')
    input_name.send_keys(sn)
    input_name.send_keys(Keys.ENTER)
    browser.find_element_by_css_selector('button[onclick="doSave()"]').click()
    time.sleep(3)
    browser.switch_to.default_content()
    status=0
    n=browser.find_elements_by_css_selector('div>p:nth-last-child(3)>font')
    if n==10:
        status=1000
        x=browser.find_elements_by_css_selector('div>p:nth-last-child(3)>font[color="#00AA00"]')
        y=browser.find_elements_by_css_selector('div>p:nth-last-child(3)>font[color="#0000FF"]')
        if x>=3 and x<=7:
            status=status+x*100+y*10
        else:
            status=4000
        finish=browser.find_element_by_css_selector("#log>p:nth-last-child(3)").text
        if "完工" in finish:
            status=status+1
        elif "前工序" in finish:
            status=status+2
        else:
            status=4000
    else:
        status=4000

    # finish=browser.find_element_by_css_selector("#log>p:nth-last-child(1)").text
    # if "完工" in finish:
    #     f=True
    # else:
    #     f=False
    # x=browser.find_elements_by_css_selector('div>p:nth-child(2)>font[color="#00AA00"]')
    # y=browser.find_elements_by_css_selector('div>p:nth-child(2)>font[color="#0000FF"]')
    # z=browser.find_elements_by_css_selector('div>p:nth-child(2)>font[color="#000000"]')
    # return (len(x),len(y),len(z),f)

def finish(sn):
    browser.switch_to.default_content()
    browser.find_element_by_css_selector('a[target="frame"]').click()
    time.sleep(1)
    browser.switch_to.frame("frame")
    in_sn=browser.find_element_by_css_selector('input[id="barcode"]')
    in_sn.send_keys(sn)
    in_sn.send_keys(Keys.ENTER)
    time.sleep(5)
    browser.find_element_by_css_selector('onclick="doSave()"]').click()
    text=browser.find_element_by_css_selector("#log>p:nth-last-child(1)").text
    if "成功" in text:
        return True
    else:
        return False

if __name__ == "__main__":
    username="7711"
    password="7711"
    browser=webdriver.Chrome() 
    sn_list=sn_read("sn.txt")
    process=["1272015079198396416","1272015655940362240","1272015794260119552",\
    "1272015911050514432","1272849679634128896"]
    log(username,password)

browser.quit()

