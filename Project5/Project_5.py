from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-f","--filename",type=str)  

args=parser.parse_args()

options = Options()

service = Service('chromedriver.exe')

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.zara.com/pl/')

button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
button.click()
time.sleep(10)

home=driver.find_element(By.XPATH,'//*[@id="main"]/article/div[2]/ul[2]/li[4]/button')
home.click()
time.sleep(10)
scents = driver.find_element(By.XPATH, '//*[@id="theme-app"]/div/div/div[1]/div/div/div[2]/nav/div[1]/ul[4]/li[1]/ul/li[9]/a/span')
scents.click()
time.sleep(10)

view = driver.find_element(By.XPATH, '//*[@id="theme-app"]/div/div/header/div[4]/div/button[2]')
view.click()
time.sleep(10)

for _ in range(10):
   driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
   time.sleep(1)

main_div = driver.find_element(By.CLASS_NAME, 'product-grid__product-list')

item=[]
for results in main_div.find_elements(By.CSS_SELECTOR, 'h2'):
    item.append(results.text.strip())

prize=[]
for results in main_div.find_elements(By.CLASS_NAME, 'money-amount__main'):
    prize.append(results.text.strip())

zara=list(zip(item,prize))

with open(args.filename+'.json', 'w') as f:
    json.dump(zara, f, indent=4)

with open(args.filename+'.json', 'r') as f:
    ranking_json = json.load(f)

print(ranking_json)
