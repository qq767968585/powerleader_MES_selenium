from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time
import re

class Mes():
    NO={
        "D01":"1272015079198396416",
        "D02":"1272015655940362240",
        "D03":"1272015794260119552",
        "D04":"1272015911050514432",
        "C02":"1272849679634128896",
        "H01":"1285508455294021632",
    }

    def __init__(self,browser,username,password):
        self.browser=browser
        self.username=username
        self.password=password

    def run(self):
        sn_list=self.sn()
        self.index_load()
        for sn in sn_list:
            m="C02"
            n=0
            while(True):
                if m=='F10':
                    break     # 正常完成退出
                try:
                    work_NO=self.NO[m]
                except KeyError:
                    print("{} is nopass".format(sn))
                    break
                if n==0:
                    m,n=self.up_material(work_NO,sn)
                    continue
                else:
                    m,n=self.finish(work_NO,sn)
                    continue

    def sn(self):          #read sn from sn.txt file,return sn list 
        filename="sn.txt"
        sn_list=[]
        with open(filename,'r') as f:
            text=f.read()
            sn_list=re.findall(r'\S+',text)
        return sn_list

    def index_load(self,oprNO=NO["C02"]):
        # self.browser.implicitly_wait(3)
        URL="http://192.168.8.34:8950/login-view.html"   
        self.browser.get(URL)
        self.browser.implicitly_wait(3)
        workStation=Select(self.browser.find_element_by_css_selector("#workStation"))
        workStation.select_by_value(oprNO)
        self.browser.find_element_by_css_selector("#username").send_keys(self.username)
        pw=self.browser.find_element_by_css_selector("#password")
        pw.send_keys(self.password)
        pw.send_keys(Keys.ENTER)
        WebDriverWait(self.browser,3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'select[id="workStationSelect"]'))
            )

    def up_material(self,work_NO,sn):
        try:
            self.browser.refresh()          
            self.browser.switch_to.default_content()
            self.browser.find_element_by_css_selector("a[onclick=\"$f.open(this,'/receive.html','上料')\"]").click()
            WebDriverWait(self.browser,3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'iframe[src="/receive.html"]'))
            )
            workStationSelect=Select(self.browser.find_element_by_css_selector('select[id="workStationSelect"]'))
            workStationSelect.select_by_value(work_NO)
            self.browser.switch_to.frame("frame")
            input_name=self.browser.find_element_by_css_selector('input[id="barcode"]')
            input_name.send_keys(sn)
            input_name.send_keys(Keys.ENTER)
            self.browser.switch_to.default_content()
            hint_ele=WebDriverWait(self.browser,3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'div[id="log"]>p:nth-child(2)'))
                    )
            hint_text=hint_ele.text
            if '不存在' in hint_text:
                m=None
                n=0
                return m,n    
            NO_list=[font_ele.text for font_ele in hint_ele.find_elements_by_css_selector('font')]
            if not NO_list:
                raise NoSuchElementException
            NO_index=len(hint_ele.find_elements_by_css_selector('font[color="#00AA00"]'))
            m=NO_list[NO_index]
            try:
                n=len(hint_ele.find_elements_by_css_selector('font[color="#0000FF"]'))
            except NoSuchElementException:
                n=0
            return m,n
        except (NoSuchElementException,TimeoutException):
            m=list(self.NO.keys())[list(self.NO.values()).index(work_NO)]
            n=0
            return m,n

    def finish(self,work_NO,sn):
        try:
            self.browser.refresh()          
            self.browser.switch_to.default_content()
            self.browser.find_element_by_css_selector("a[onclick=\"$f.open(this,'/finish-work.html','完工')\"]").click()
            WebDriverWait(self.browser,3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'iframe[src="/finish-work.html"'))
            )
            workStationSelect=Select(self.browser.find_element_by_css_selector('select[id="workStationSelect"]'))
            workStationSelect.select_by_value(work_NO)
            self.browser.switch_to.frame("frame")
            input_name=self.browser.find_element_by_css_selector('input[id="barcode"]')
            input_name.send_keys(sn)
            input_name.send_keys(Keys.ENTER)
            self.browser.switch_to.default_content()
            hint_ele=WebDriverWait(self.browser,3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'div[id="log"]>p:nth-child(2)'))
                    )
            hint_text=hint_ele.text
            if '不存在' in hint_text:
                m=None
                n=0
                return m,n    
            NO_list=[font_ele.text for font_ele in hint_ele.find_elements_by_css_selector('font')]
            if not NO_list:
                raise NoSuchElementException
            NO_index=len(hint_ele.find_elements_by_css_selector('font[color="#00AA00"]'))
            m=NO_list[NO_index]
            try:
                n=len(hint_ele.find_elements_by_css_selector('font[color="#0000FF"]'))
            except NoSuchElementException:
                n=0
            self.browser.switch_to.frame("frame")
            try:
                changeWorkStep=Select(self.browser.find_element_by_css_selector('select[id="rowNum"]'))
                changeWorkStep.select_by_index(1)
            except NoSuchElementException:
                pass
            self.browser.find_element_by_css_selector('button[onclick="doSave()"]').click()
            self.browser.switch_to.default_content()
            try:
                WebDriverWait(self.browser,3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'div[id="log"]>p:nth-child(4)'))
                        )
            except TimeoutException:
                pass
            return m,n
        except (NoSuchElementException,TimeoutException):
            m=list(self.NO.keys())[list(self.NO.values()).index(work_NO)]
            n=0
            return m,n



if __name__ == "__main__":
    options=webdriver.ChromeOptions()      # option:run browser no error in command
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser=webdriver.Chrome(chrome_options=options)
    username="7711"
    password="7711"
    auto=Mes(browser,username,password)
    auto.run()
    browser.quit()