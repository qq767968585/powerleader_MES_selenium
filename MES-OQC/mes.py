from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

username="7711"
password="7711"

def log(username,password,proc):
    URL="http://192.168.8.34:8950/login-view.html"
    browser.get(URL)
    browser.find_element_by_name("username").send_keys(username)
    browser.find_element_by_name("password").send_keys(password)
    s1 = Select(browser.find_element_by_id("workStation"))
    s1.select_by_value(proc)       # SQ102   OQC功能检验
    # s1.select_by_value("1272014207798185984")     # CT101   安规测试（CT）
    time.sleep(1)
    browser.find_element_by_class_name("button").click()
    time.sleep(3)

def load(snNumber):   # 上料
    browser.switch_to.frame("frame")
    browser.find_element_by_xpath('//button[@class="btn btn-default btn-success"]').click()
    time.sleep(1)
    browser.switch_to.default_content()
    text=browser.find_element_by_css_selector("#log>p:nth-last-child(1)").text
    if "成功" in text:
        return True
    else:
        return False

def finish(snNumber,username):      #  完工
    browser.find_element_by_css_selector("a[onclick=\"$f.open(this,'/finish-work.html','完工')\"]").click()
    time.sleep(1)
    browser.switch_to.frame("frame")
    browser.find_element_by_xpath('//input[@id="barcode"]').send_keys(snNumber)
    time.sleep(1)
    # browser.find_element_by_xpath('//input[@id="wbs"]').send_keys(1)
    # browser.find_element_by_xpath('//input[@id="wbs"]').send_keys(Keys.ENTER)
    # time.sleep(1)
    # browser.find_element_by_xpath('//input[@id="completeEmpName"]').send_keys(username)
    browser.find_element_by_xpath('//input[@id="completeEmpName"]').send_keys(Keys.ENTER)
    time.sleep(1)
    double_click=browser.find_element_by_xpath('//button[@class="btn btn-default btn-success"]')
    time.sleep(2)
    ActionChains(browser).click(double_click).perform()
    time.sleep(1)
    browser.switch_to.default_content()
    text=browser.find_element_by_css_selector("#log>p:nth-last-child(1)").text
    if "成功" in text:
        return True
    else:
        return False

def sn_read():
    filename = 'sn.txt'
    with open(filename,'r') as f:
        str_txt=f.read()
    str_txt=str_txt.replace('\n','')
    str_list=str_txt.split('LC')
    sn_list=[]
    for item in str_list:
        if item:
            sn_list.append('LC'+item)
    return sn_list 

def get(snNumber):
    browser.find_element_by_css_selector("a[onclick=\"$f.open(this,'/receive.html','上料')\"]").click()
    time.sleep(1)
    browser.switch_to.frame("frame")
    browser.find_element_by_xpath('//input[@id="barcode"]').send_keys(snNumber)
    browser.find_element_by_xpath('//input[@id="barcode"]').send_keys(Keys.ENTER)
    time.sleep(1)
    # browser.find_element_by_xpath('//input[@id="quantity"]').send_keys("1")
    browser.find_element_by_xpath('//input[@id="quantity"]').send_keys(Keys.ENTER)
    time.sleep(3)
    browser.switch_to.default_content()
    text=browser.find_element_by_css_selector("#log>p:nth-last-child(1)").text
    if "完工" in text:
        return (10,10)       
    else:
        eles=browser.find_elements_by_css_selector('div>p:nth-last-child(1)>font[color="#00AA00"]')
        if len(eles):
            eles_f=browser.find_elements_by_css_selector('div>p:nth-last-child(1)>font[color="#0000FF"]')
            return (len(eles),len(eles_f))
        else:
            eles=browser.find_elements_by_css_selector('div>p:nth-last-child(3)>font[color="#00AA00"]')
            eles_f=browser.find_elements_by_css_selector('div>p:nth-last-child(3)>font[color="#0000FF"]')
            return (len(eles),len(eles_f))

browser=webdriver.Chrome()
sn_list=sn_read()
process=["1272015079198396416","1272015655940362240","1272015794260119552",\
    "1272015911050514432","1272849679634128896","1273943582261088256","1272849925290319872"]
log(username,password,process[4])
i=0
for sn in sn_list:
    work_nub=get(sn)
    m=work_nub[0]
    n=work_nub[1] 
    while True:
        if m==3 and n==0:
            log(username,password,process[0])
            m=get(sn)[0]
            if load(sn):
                m=3
                n=1
            if finish(sn,username):
                m=4
                n=0
        elif m==3 and n==1:
            log(username,password,process[0])
            if finish(sn,username):
                m=4
            n=0

        elif m==4 and n==0:
            log(username,password,process[1])
            m=get(sn)[0]
            if load(sn):
                m=4
                n=1
            if finish(sn,username):
                m=5
                n=0
        elif m==4 and n==1:
            log(username,password,process[1])
            if finish(sn,username):
                m=5
            n=0

        elif m==5 and n==0:
            log(username,password,process[2])
            m=get(sn)[0]
            if load(sn):
                m=5
                n=1
            if finish(sn,username):
                m=6
                n=0
        elif m==5 and n==1:
            log(username,password,process[2])
            if finish(sn,username):
                m=6
            n=0

        elif m==6 and n==0:
            log(username,password,process[3])
            m=get(sn)[0]
            if load(sn):
                m=6
                n=1
            if finish(sn,username):
                m=7
                n=0
        elif m==6 and n==1:
            log(username,password,process[3])
            if finish(sn,username):
                m=7
            n=0
        
        elif m==7 and n==0:
            log(username,password,process[4])
            m=get(sn)[0]
            if load(sn):
                m=7
                n=1
            if finish(sn,username):
                m=10
                n=0
        elif m==7 and n==1:
            log(username,password,process[4])
            if finish(sn,username):
                m=10
            n=0

        # elif m==8 and n==0:
        #     log(username,password,process[5])
        #     m=get(sn)[0]
        #     if load(sn):
        #         m=8
        #         n=1
        #     if finish(sn,username):
        #         m=9
        #         n=0
        # elif m==8 and n==1:
        #     log(username,password,process[5])
        #     if finish(sn,username):
        #         m=9
        #     n=0

        # elif m==9 and n==0:
        #     log(username,password,process[6])
        #     m=get(sn)[0]
        #     if load(sn):
        #         m=9
        #         n=1
        #     if finish(sn,username):
        #         m=10
        #         n=0
        # elif m==9 and n==1:
        #     log(username,password,process[6])
        #     if finish(sn,username):
        #         m=10
        #     n=0    

        elif m==10:
            print(sn+" is OK")
            i+=1
            break
        else:
            print(sn+" is NO_pass")
            break
print("Total: {} is NO_pass".format(len(sn_list)-i))
browser.quit()

