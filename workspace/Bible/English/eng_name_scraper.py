#!/usr/bin/env python3
# -*- coding:utf8 -*-

import json
import random
import re
from bs4 import BeautifulSoup
from pprint import pprint
from requests import get
from time import sleep

def scrape_page(url, categoryINT, i):
    """"""
    nameLIST = []
    
    resp = get(url)
    wait = random.uniform(1, 10)
    sleep(wait)
    print("等待時間：", wait, "秒")
    soup = BeautifulSoup(resp.text, "lxml")
    
    h4LIST = soup.find_all('h4')                  #找網頁中所有h4
    for a in h4LIST:
        nameSTR = a.get_text()
        nameSTR = re.split(r'\s', nameSTR)[3]     #取得英文名字
        if categoryINT == 7 and i <= 116:
            if re.split(r'\s', nameSTR)[4] == "or":
                nameLIST.append(re.split(r'\s', nameSTR)[3])
                nameLIST.append(re.split(r'\s', nameSTR)[5])            
            #nameSTR = re.split(r'\s', nameSTR)[3]     
            #nameLIST.append(nameSTR)
        if categoryINT == 7 and i == 117:
            if re.split(r'\s', nameSTR)[3] == "or":
                nameLIST.append(re.split(r'\s', nameSTR)[2])
                nameLIST.append(re.split(r'\s', nameSTR)[4])
            #nameSTR = re.split(r'\s', nameSTR)[2]     
            #nameLIST.append(nameSTR)
        elif categoryINT == 6 and i <= 165:
            if re.split(r'\s', nameSTR)[4] == "or":
                nameLIST.append(re.split(r'\s', nameSTR)[3])
                nameLIST.append(re.split(r'\s', nameSTR)[5])            
            #nameSTR = re.split(r'\s', nameSTR)[3]     
            #nameLIST.append(nameSTR)
        elif categoryINT == 6 and i > 165:
            if re.split(r'\s', nameSTR)[3] == "or":
                nameLIST.append(re.split(r'\s', nameSTR)[2])
                nameLIST.append(re.split(r'\s', nameSTR)[4])
            #nameSTR = re.split(r'\s', nameSTR)[2]     
            #nameLIST.append(nameSTR)
        else:
            print("Check categoryINT:", categoryINT, ",page", i) 
    
    pprint(nameLIST)
    return nameLIST

def main(categoryINT, lastINT):
    """"""
    nameLIST = []
    for i in range(0, lastINT, 1):
        url = f"http://www.ch.fhl.net/xoops/modules/wordbook/category.php?categoryID={categoryINT}&start={i}0"
        nameLIST.extend(scrape_page(url))
        if categoryINT == 7 :
            print("目前位置: LOCATION 第", i+1, "頁")
        if categoryINT == 6 :
            print("目前位置: PERSONS 第", i+1, "頁")        
    return nameLIST


if __name__ == "__main__":
    #地名
    locLIST = main(categoryINT=7, lastINT=117)
    with open("../../../data/Bible/English/names/places.json", "w", encoding="utf-8") as f:
        json.dump({"LOCATION": locLIST}, f, ensure_ascii=False, indent=4)
    
    #人名
    perLIST = main(categoryINT=6, lastINT=187)
    with open("../../../data/Bible/English/names/persons.json", "w", encoding="utf-8") as f:
        json.dump({"ENTITY_person": perLIST}, f, ensure_ascii=False, indent=4)

