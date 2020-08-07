from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import re

class Mes():
    NO=[None,None,None,None,
        "1272015079198396416",
        "1272015655940362240",
        "1272015794260119552",
        "1272015911050514432",
        "1272849679634128896",
        "1285508455294021632",
        "1272849679634128896",
    ]
    def __init__(self,browser,username,password):
        self.browser=browser
        self.username=username
        self.password=password
    def run(self):
        sn_list=self.sn()
        self.index_load()
        for sn in sn_list:
            m=8
            n=0
            while(True):
                if n==0:
                    m,n=self.up_material(m,n,sn)
                    continue
                elif n==1:
                    m,n=self.finish(m,n,sn)
                    continue
                elif n==2:
                    break
                elif n==3:
                    print("{} is nopass".format(sn))
                    break       

    def sn(self):          #read sn from sn.txt file,return sn list 
        filename="sn.txt"
        sn_list=[]
        with open(filename,'r') as f:
            text=f.read()
            sn_list=re.findall(r'\S+',text)
        return sn_list

    def index_load(self,oprNO="1272849679634128896"):
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
            EC.presence_of_element_located((By.CSS_SELECTOR,'select[id="workStationSelect"]'))
            )

    def up_material(self,m,n,sn): 
        self.browser.refresh()          
        self.browser.switch_to.default_content()
        self.browser.find_element_by_css_selector("a[onclick=\"$f.open(this,'/receive.html','上料')\"]").click()
        time.sleep(1)
        workStationSelect=Select(self.browser.find_element_by_css_selector('select[id="workStationSelect"]'))
        workStationSelect.select_by_value(self.NO[m])
        self.browser.switch_to.frame("frame")
        input_name=self.browser.find_element_by_css_selector('input[id="barcode"]')
        input_name.send_keys(sn)
        input_name.send_keys(Keys.ENTER)
        time.sleep(2)
        self.browser.switch_to.default_content()
        try:
            WebDriverWait(self.browser,3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'div[id="log"]>p:nth-child(4)'))
                )
        except TimeoutException:
            verbose=self.browser.find_element_by_css_selector('div[id="log"]>p:nth-last-child(1)').text
            if '不存在' in verbose:
                return (m,3)
            elif '无任务' in verbose:
                return (m,2)
            else:
                return (m,0)
        total=len(self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font'))
        x=len(self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font[color="#00AA00"]'))
        y=len(self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font[color="#0000FF"]'))
        verbose=self.browser.find_element_by_css_selector('div[id="log"]>p:nth-last-child(1)').text
        if total==11:
            if "成功" in verbose:
                return(x,1)
            else:
                if x>=3 and x<9:
                    return(x,y)
                elif x>=9:
                    return (x,2)
                else:
                    return (m,3)
        elif total>11:
            if "成功" in verbose:
                return(x,1)
            else:
                if x>=3 and x<10:
                    return(x,y)
                elif x>=10:
                    return (x,2)
                else:
                    return (m,3)
        else:
            return (m,3)

        
    def finish(self,m,n,sn):
        self.browser.refresh()
        self.browser.switch_to.default_content()
        self.browser.find_element_by_css_selector("a[onclick=\"$f.open(this,'/finish-work.html','完工')\"]").click()
        time.sleep(1)
        workStationSelect=Select(self.browser.find_element_by_css_selector('select[id="workStationSelect"]'))
        workStationSelect.select_by_value(self.NO[m])
        self.browser.switch_to.frame("frame")
        try:
            WebDriverWait(self.browser,3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'input[id="completeEmpName"]'))
                )
        except TimeoutException:
            return (m,n)
        input_name=self.browser.find_element_by_css_selector('input[id="barcode"]')
        input_name.send_keys(sn)
        input_name.send_keys(Keys.ENTER)
        time.sleep(3)
        self.browser.find_element_by_css_selector('button[onclick="doSave()"]').click()
        time.sleep(2)
        self.browser.switch_to.default_content()
        try:
            WebDriverWait(self.browser,3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'div[id="log"]>p:nth-child(4)'))
                )
        except TimeoutException:
            verbose=self.browser.find_element_by_css_selector('div[id="log"]>p:nth-last-child(1)').text
            if '不存在' in verbose:
                return (m,3)
            else:
                return (m,0)
        total=len(self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font'))
        x=len(self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font[color="#00AA00"]'))
        y=len(self.browser.find_elements_by_css_selector('div[id="log"]>p:nth-child(2)>font[color="#0000FF"]'))
        verbose=self.browser.find_element_by_css_selector('div[id="log"]>p:nth-last-child(1)').text
        if total==11:
            if "成功" in verbose:
                if x<8:
                    return(x+1,0)
                else:
                    return(x,2)
            else:
                if x>=3 and x<9:
                    return(x,y)
                elif x>=9:
                    return (x,2)
                else:
                    return (m,3)
        elif total>11:
            if "成功" in verbose:
                if x<11:
                    return(x+1,0)
                else:
                    return(x,2)
            else:
                if x>=3 and x<11:
                    return(x,y)
                elif x>=11:
                    return (x,2)
                else:
                    return (m,3)
        else:
            return (m,3)

      

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