from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from diffpng import diffpng
import os

chrome_options = Options()
chrome_options.add_argument('headless')
driver = webdriver.Chrome("F:/googlechromedriver/96/chromedriver_win32/chromedriver.exe",chrome_options=chrome_options)

def get_url(url, dataSource):
    driver.get(url)
    time.sleep(waitingElement)
    driver.set_window_size(1366, 768)
    time.sleep(waitingElement)
    elementUser = driver.find_element_by_id("username")
    elementPassword = driver.find_element_by_id("password")
    elementSubmit = driver.find_element_by_class_name("btn-info")

    elementUser.send_keys("admin")
    elementPassword.send_keys("admin123")
    elementSubmit.click()

    time.sleep(waitingElement)
    elementSelect = driver.find_element_by_xpath("//div[@class='page-content-wrapper']/main[@id='js-page-content']/smart-page-breadcrumb/ol[@class='breadcrumb page-breadcrumb ng-star-inserted']/li[@class='position-absolute pos-top pos-right d-none d-sm-block ng-star-inserted']/div[@class='form-group']/select[@id='example-select']")
    elementSelect.click()
    time.sleep(waitingElement)

    elementSelectOption = driver.find_elements_by_xpath("//div[@class='page-content-wrapper']/main[@id='js-page-content']/smart-page-breadcrumb/ol[@class='breadcrumb page-breadcrumb ng-star-inserted']/li[@class='position-absolute pos-top pos-right d-none d-sm-block ng-star-inserted']/div[@class='form-group']/select[@id='example-select']/option")
    for option in elementSelectOption:
        if (option.text == dataSource):
            option.click()

def get_image(save_pic_path):
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.set_window_size(width, height)
    time.sleep(waitingElement)
    driver.save_screenshot(save_pic_path)

def nav_toggle():
    nav = driver.find_elements_by_xpath("//div[@class='page-inner']/smart-sidebar[@id='yyh']/aside[@class='page-sidebar ng-star-inserted']/smart-navigation[@class='d-flex flex-column flex-fill ']/nav[@id='js-primary-nav']/smart-nav/ul[@id='js-nav-menu']/li")
    nav[0].click()
    time.sleep(waitingElement)
    save_pic_name = "name"
    for li in nav:
        li.click()
        time.sleep(waitingElement)
        secondaryNav = li.find_elements_by_tag_name("li")
        for secondaryLi in secondaryNav:
            save_pic_name = li.text[0:2] + '-' + secondaryLi.text.strip().replace(' ', '')
            secondaryLi.click()
            time.sleep(waitingElement)
            thirdNav = secondaryLi.find_elements_by_tag_name("li")
            if 0 == len(thirdNav):
                time.sleep(waitingData)
                get_image("./pic/new/" + save_pic_name + ".png")
            else:
                for thirdLi in thirdNav:
                    save_pic_name = li.text[0:2] + '-' + secondaryLi.text[0:2] + '-' + thirdLi.text.strip().replace(' ', '')
                    thirdLi.click()
                    time.sleep(waitingData)
                    get_image("./pic/new/" + save_pic_name + ".png")


def diffFiles(file_dir, new_dir):
    for root, dirs, files in os.walk(file_dir):
        print("files", files)
        for file in files:
            print(file)
            diffpng(file_dir + file, new_dir + file, file)


url = "http://192.168.0.110:8007"
dataSource = "Monitor History"
save_pic_path = "C:/Users/DELL/Desktop/新建文件夹 (2)/8009.png"
waitingElement = 2
waitingData = 5

get_url(url, dataSource)
nav_toggle()
driver.quit()
diffFiles("./pic/origin/", "./pic/new/")
