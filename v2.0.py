import time
import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import  Options
import datetime

PROXY = ['','',''] # your proxyes
counter = 0

chromeOptions = webdriver.ChromeOptions() 
prefs = {"profile.managed_default_content_settings.images":2} 
chromeOptions.add_extension('') # path to anticaptcha extension
chromeOptions.add_experimental_option("prefs",prefs) 
chromeOptions.add_argument('--proxy-server=%s' % PROXY[counter]) 
driver = webdriver.Chrome(chrome_options=chromeOptions) 


time_ = time.strftime("%d.%m", time.localtime())
file = open("C:\\Users\\grove\\Desktop\\Scripts\\Smmok\\answ_"+time_+".csv", 'w')

accounts = ['','',
'', '']   # your accounts ['login', 'pass', 'login', 'pass']
i = 0
j = 1

def check_proxy():
    global counter
    if counter == len(PROXY) - 1:
        counter = 0
        reconnection()
    else:
        counter = counter + 1
        reconnection()
        

def reconnection():
    global driver
    driver.quit()
    chromeOptions = webdriver.ChromeOptions() 
    prefs = {"profile.managed_default_content_settings.images":2} 
    chromeOptions.add_extension(' ') # path to anticaptcha extension
    chromeOptions.add_experimental_option("prefs",prefs) 
    chromeOptions.add_argument('--proxy-server=%s' % PROXY[counter]) 
    driver = webdriver.Chrome(chrome_options=chromeOptions) 
    logining()

def logining():
    driver.get("https://whoer.net")
    time.sleep(10)
    driver.get("https://smmok14.ru/")
    driver.find_element_by_xpath("//a[@x-ulogin-button='vkontakte']").click()
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    driver.find_element_by_xpath("//input[@type='text']").send_keys(accounts[i])
    driver.find_element_by_xpath("//input[@type='password']").send_keys(accounts[j])
    driver.find_element_by_class_name("oauth_button").click()
    window_before = driver.window_handles[0]
    driver.switch_to.window(window_before)
    driver.get("https://smmok14.ru/offer/index")
    driver.implicitly_wait(3)
    driver.find_element_by_class_name("ui-dialog-buttonset").click() 
    working()

def working():
    global i
    global j
    driver.get("https://smmok14.ru/offer/index")
    try:
        driver.implicitly_wait(3)
        project_name = driver.find_element_by_xpath("//span[@class='project_name']").text
    except:
        balance = driver.find_element_by_id("user_balance").text
        print(accounts[i] + "|" + balance)
        print(datetime.datetime.now())
        money = driver.find_element_by_id("user_balance").text
        money = balance.split('.')
        print(money)
        if int(money[0]) > 75:
            print("vohoo")
            driver.find_element_by_class_name('color2').click()
            driver.find_element_by_name('withdraw_sum').send_keys('75')
            driver.find_element_by_name('withdraw_wmr').send_keys('Z792976401629')
            driver.find_element_by_class_name('submitBtn').click()
            time.sleep(120)
        driver.get("https://api.telegram.org/&text="+accounts[i] + "|" + balance)
        # file = open("C:\\Users\\grove\\Desktop\\Scripts\\Smmok\\answ_"+time_+'.csv', 'a')
        # file.write(accounts[i]+"|"+balance+'\n')
        # file.close()
        if j == len(accounts) - 1:
            i = 0
            j = 1
            time.sleep(750)
            check_proxy()
        else:
            i = i+2
            j = j+2
            check_proxy()
    if project_name == "Добавить в друзья":
        add_friend()
    elif project_name == "Подписка":
        subscribe()
    elif project_name == "Просмотр страницы":
        look()
    elif project_name == "Мне нравится":
        like()
    elif project_name == "Лайк + рассказать друзьям":
        like_repost()
    else:
        time.sleep(300)
        working()
        
def opening(func):
    def wrapper():
        driver.find_element_by_xpath("//a[@class='button projectDetails']").click()
        driver.implicitly_wait(3)
        driver.find_element_by_xpath("//button[@type='button']").click()
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        func()
        driver.close()
        window_before = driver.window_handles[0]
        driver.switch_to.window(window_before)
        driver.implicitly_wait(3)
        driver.find_element_by_xpath("//button[@type='button']").click()
        working()
    return wrapper
    
@opening
def add_friend():
    try:
        driver.implicitly_wait(3)
        driver.find_element_by_xpath("//button[@class='flat_button button_wide']").click()
        driver.implicitly_wait(3)
        captcha = driver.find_elements_by_xpath("//a[@class='status']")
        if len(captcha) > 0:
            time.sleep(100)
    except:
        driver.close()
        window_before = driver.window_handles[0]
        driver.switch_to.window(window_before)
        driver.find_element_by_xpath("//button[2]").click()
        working()
    time.sleep(2)

@opening
def subscribe():
    try:
        driver.find_element_by_xpath("//button[@id='join_button']").click()
        driver.implicitly_wait(3)
        captcha = driver.find_elements_by_xpath("//a[@class='status']")
        if len(captcha) > 0:
            time.sleep(100)
    except:
        second_chance()

def second_chance():
    try:
        driver.find_element_by_xpath("//button[@id='public_subscribe']").click()
        driver.implicitly_wait(3)
        captcha = driver.find_elements_by_xpath("//a[@class='status']")
        if len(captcha) > 0:
            time.sleep(100)
    except:
        driver.close()
        window_before = driver.window_handles[0]
        driver.switch_to.window(window_before)
        driver.find_element_by_xpath("//button[2]").click()
        working()
    driver.close()
    window_before = driver.window_handles[0]
    driver.switch_to.window(window_before)
    driver.implicitly_wait(3)
    driver.find_element_by_xpath("//button[@type='button']").click()
    working()

def look():
    driver.find_element_by_xpath("//a[@class='button projectDetails']").click()
    driver.implicitly_wait(3)
    driver.find_element_by_xpath("//button[@type='button']").click()
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    time.sleep(3)
    driver.close()
    window_before = driver.window_handles[0]
    driver.switch_to.window(window_before)
    try:
        driver.implicitly_wait(3)
        driver.find_element_by_xpath("//button[@type='button']").click()
    except:
        driver.close()
        window_before = driver.window_handles[0]
        driver.switch_to.window(window_before)
        driver.implicitly_wait(3)
        driver.find_element_by_xpath("//button[2]").click()
        working()
    working()

@opening
def like():
    try:
        driver.find_element_by_xpath("//a[@class='like_btn like _like']").click()
        driver.implicitly_wait(3)
        captcha = driver.find_elements_by_xpath("//a[@class='status']")
        if len(captcha) > 0:
            time.sleep(100)
    except:
        driver.close()
        window_before = driver.window_handles[0]
        driver.switch_to.window(window_before)
        driver.find_element_by_xpath("//button[2]").click()
        working()

@opening    
def like_repost():  
    try:
        driver.implicitly_wait(3)
        driver.find_element_by_xpath("//a[@class='like_btn share _share']").click()
        driver.implicitly_wait(3)
        driver.find_element_by_class_name("radiobtn").click()
        driver.find_element_by_xpath("//button[@class='like_share_btn flat_button']").click()
    except:
        driver.close()
        window_before = driver.window_handles[0]
        driver.switch_to.window(window_before)
        driver.find_element_by_xpath("//button[2]").click()
        working()

def out_():
    driver.get("https://smmok14.ru/welcome/logout")
    driver.get("https://vk.com/")
    driver.implicitly_wait(3)
    driver.find_element_by_xpath("//a[@id='top_profile_link']").click()
    driver.implicitly_wait(3)
    driver.find_element_by_xpath("//a[@id='top_logout_link']").click()
    check_proxy()

if __name__ == '__main__':
    try:
        logining()
    except:
        pass
