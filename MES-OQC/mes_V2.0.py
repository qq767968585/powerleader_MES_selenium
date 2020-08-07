from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import re

class SnFileIsNone(Exception):
    def __str__(self):
        return "Error:sn.txt文件为空"
class LoadFail(Exception):
    def __init__(self,page):
        self.page=page
    def __str__(self):
        return "Error:{}加载失败".format(self.page)

class Mes():
    NO={
        "D01":"1272015079198396416",
        "D02":"1272015655940362240",
        "D03":"1272015794260119552",
        "D04":"1272015911050514432",
        "C02":"1272849679634128896",
        "H01":"1285508455294021632",
    }
    nopass=0
    def __init__(self,browser,username,password):
        self.browser=browser
        self.username=username
        self.password=password
    def run(self):
        sn_list=self.sn()
        self.index_load()
        for sn in sn_list:
            m=0
            n="C02"
            while(True):
                if m==0:
                    m,n=self.up_material(m,n,sn)         # m is status,n is oprNO
                elif m==1:
                    m,n=self.finish(m,n,sn)
                elif m==2:
                    break
                else:
                    raise LoadFail("上料,完工")
        print("未完成数:{}".format(self.nopass))

    def sn(self):       #read sn from sn.txt file,return sn list 
        filename="sn.txt"
        sn_list=[]  
        with open(filename,'r') as f:
            text=f.read()
            sn_list=re.findall(r'\S+',text)
        if not sn_list:
            raise SnFileIsNone
        return sn_list

    def index_load(self,oprNO=NO["C02"]):
        # self.browser.implicitly_wait(3)
        URL="http://192.168.8.34:8950/login-view.html"   
        self.browser.get(URL)
        workStation=Select(browser.find_element_by_css_selector("#workStation"))
        workStation.select_by_value(oprNO)
        self.browser.find_element_by_css_selector("#username").send_keys(username)
        pw=self.browser.find_element_by_css_selector("#password")
        pw.send_keys(password)
        pw.send_keys(Keys.ENTER)
        WebDriverWait(self.browser,3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'a[id="clearLog"]'))
            )

    def up_material(self,m,n,sn):           # return next oprNO
        if n=='F10':
            oprNO=None
            status=2
            return (status,oprNO)
        self.browser.refresh()
        self.browser.switch_to.default_content()
        # clearLog=WebDriverWait(self.browser,3).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR,'a[id="clearLog"]'))
        #         )
        # clearLog.click()
        workStationSelect=Select(self.browser.find_element_by_css_selector('select[id="workStationSelect"]'))
        workStationSelect.select_by_value(self.NO[n])
        self.browser.switch_to.frame("frame")
        input_name=self.browser.find_element_by_css_selector('input[id="barcode"]')
        input_name.send_keys(sn)
        input_name.send_keys(Keys.ENTER)
        self.browser.switch_to.default_content()
        # parent_element=WebDriverWait(self.browser,3).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR,'div>p:nth-child(2)'))
        #         )
        # self.browser.implicitly_wait(3)
        try:
            hint=WebDriverWait(self.browser,3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'div[id="log"]>p:nth-child(4)'))
                    )
        except TimeoutException:
            oprNO=None
            self.nopass+=1
            status=2
            return (status,oprNO)
        verbose=hint.text
        oprNO_total=self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font')
        # oprNO_total=parent_element.find_elements_by_css_selector('font')
        oprNO_list=[]
        for i in oprNO_total:
            oprNO_list.append(i.text)
        finish_index=len(self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font[color="#00AA00"]'))
        try:
            oprNO=oprNO_list[finish_index-1]
        except IndexError:
            oprNO=None
            self.nopass+=1
            status=2
            return (status,oprNO)
        # verbose=self.browser.find_element_by_css_selector('div>p:nth-child(4)').text
        if "完成" in verbose:
            status=1
        elif "半成品" in verbose:
            status=1
        elif "当前工序不能收料" in verbose:
            status=0
        else:
            self.nopass+=1
            status=2
        return (status,oprNO)
        
    def finish(self,m,n,sn):
        if n=='F10':
            oprNO=None
            status=2
            return (status,oprNO)
        self.browser.refresh()
        self.browser.switch_to.default_content()
        browser.find_element_by_css_selector("a[onclick=\"$f.open(this,'/finish-work.html','完工')\"]").click()
        # clearLog=WebDriverWait(self.browser,3).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR,'a[id="clearLog"]'))
        #         )
        # clearLog.click()
        workStationSelect=Select(self.browser.find_element_by_css_selector('select[id="workStationSelect"]'))
        workStationSelect.select_by_value(self.NO[n])
        self.browser.switch_to.frame("frame")
        input_name=self.browser.find_element_by_css_selector('input[id="barcode"]')
        input_name.send_keys(sn)
        input_name.send_keys(Keys.ENTER)
        # self.browser.implicitly_wait(3)
        # input_number=self.browser.find_element_by_css_selector('input[id="thisQty"]')
        # input_number.send_keys('1')
        # input_name.send_keys(Keys.ENTER)
        # try:
        #     WebDriverWait(self.browser,3).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR,'input[id="thisQty"]'))
        #         )
        # except TimeoutException:
        #     oprNO=None
        #     self.nopass+=1
        #     status=2
        #     return (status,oprNO)
        self.browser.switch_to.default_content()
        try:
            WebDriverWait(self.browser,3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'div[id="log"]>p:nth-child(2)'))
                )
            # time.sleep(3)
        except TimeoutException:
            oprNO=None
            self.nopass+=1
            status=2
            return (status,oprNO)
        self.browser.switch_to.frame("frame")
        self.browser.find_element_by_css_selector('button[onclick="doSave()"]').click()
        self.browser.switch_to.default_content()
        try:
            hint=WebDriverWait(self.browser,3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'div[id="log"]>p:nth-child(4)'))
                )
        except TimeoutException:
            oprNO=None
            self.nopass+=1
            status=2
            return (status,oprNO)
        verbose=hint.text
        oprNO_total=self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font')
        # oprNO_total=parent_element.find_elements_by_css_selector('font')
        oprNO_list=[]
        for i in oprNO_total:
            oprNO_list.append(i.text)
        # finish_index=len(parent_element.find_elements_by_css_selector('font[color="#00AA00"]'))
        finish_index=len(self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font[color="#00AA00"]'))
        oprNO=oprNO_list[finish_index]
        # verbose=self.browser.find_element_by_css_selector('div>p:nth-last-child(1)').text
        noFinish=self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font[color="#0000FF"]')
        if len(noFinish)==1:
            if "完成" in verbose:
                oprNO=oprNO_list[finish_index+1]
                status=0
            elif "报工不允许数量与工时同时为0" in verbose:
                status=1
            else:
                self.nopass+=1
                status=2
        else:
            status=0      
        return (status,oprNO)

if __name__ == "__main__":
    # option=webdriver.ChromeOptions()      # option:run browser in the background
    # option.add_argument('headless')   
    # browser=webdriver.Chrome(chrome_options=option)
    options=webdriver.ChromeOptions()      # option:run browser no error in command
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser=webdriver.Chrome(chrome_options=options)
    browser.implicitly_wait(3)
    # browser.maximize_window()
    username="7711"
    password="7711"
    auto=Mes(browser,username,password)
    auto.run()
    browser.quit()