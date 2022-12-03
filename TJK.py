# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 18:41:34 2022

@author: Savage33
"""
from selenium import webdriver
import selenium.webdriver.common.keys
import time
import pandas as pd
import os
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import keyboard
import pyautogui as gw
import shutil
from bs4 import BeautifulSoup

chrome_options = Options()
prefs={"excludeSwitches": ["enable-automation"],'credentials_enable_service': False,
       'profile.password_manager_enabled':False,'useAutomationExtension': False}
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome("C://Users//Savage33//OneDrive//programlama//eklentiler//chromedriver.exe",chrome_options=chrome_options)
driver.get("https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisSonuclari?SehirId=82&SehirAdi=Keeneland+ABD")
action = webdriver.ActionChains(driver)
geriBakilacakGunSayisi=100
driver.maximize_window()
time.sleep(6)

def kaydetKapat():
    driver.close()
    driver.quit()
    
yarisbilgisi=driver.find_element_by_class_name("gunluk-tabs")
yarislistesi=yarisbilgisi.find_elements_by_tag_name("li")
len(yarislistesi)
yarislistesi[0].click()

oncekigun=driver.find_element_by_xpath("//a[@title='Önceki Gün']")



tabloBasliklari=["Forma","S" ,"At İsmi" ,"Yaş", "Orijin(Baba - Anne)" ,"Sıklet" ,"Jokey", "Sahip",
                 "Antrenörü" ,"Derece" ,"Gny" ,"AGF" ,"St" ,"Fark", "G." ,"Çık." ,"HP"]
df = pd.DataFrame(columns=tabloBasliklari)
for i in range(geriBakilacakGunSayisi):
    oncekigun.click()
    time.sleep(5)
    tables=driver.find_elements_by_xpath("//table[@summary='Kosular']")
    

    for table in tables:
        df2 = pd.read_html(table.get_attribute('outerHTML'))
        df = df.append(df2, ignore_index = True)
    
df.to_excel(r"C:\Users\Savage33\OneDrive\Masaüstü\TJK.xlsx")
kaydetKapat()