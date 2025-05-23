#!/usr/bin/env python3
# -*- coding:utf8 -*-

import json
import random
import re
from bs4 import BeautifulSoup
from pprint import pprint
from requests import get
from time import sleep

namePAT = re.compile(r"[A-Za-z][A-Za-z \，()\-]*")

def scrape_page(url, categoryINT, i):
    """
    擷取指定網址的名稱列表。

    參數:
        url (str): 目標網址。
        categoryINT (int): 網頁分類 ID (6: 人名, 7: 地名)。
        i (int): 網頁頁數。

    回傳:
        list: 從該頁面擷取的名稱列表。  
    """
    nameLIST = []
    
    resp = get(url)
    wait = random.uniform(1, 10)
    sleep(wait)
    print("等待時間：", wait, "秒")
    soup = BeautifulSoup(resp.text, "lxml")
    
    h4LIST = soup.find_all('h4')                  #找網頁中所有h4
    for a in h4LIST:

        aSTR = a.get_text()
        aLIST = []
        aLIST.append(aSTR)
        for nameSTR in aLIST:
            nameSTR = ''.join(re.findall(namePAT, nameSTR))  #找到英文部分
            nameSTR = re.sub(r"\s+$", "", nameSTR)           #添加到nameLIST
            nameLIST.append(nameSTR)
    
    pprint(nameLIST)
    return nameLIST

def main(categoryINT, lastINT):
    """
    爬取指定類別 (地名/人名) 的名稱並返回列表。

    參數:
        categoryINT (int): 網頁分類 ID (6: 人名, 7: 地名)。
        lastINT (int): 類別的總數量 (用於控制迴圈範圍)。

    回傳:
        list: 取得的名稱列表。
    """
    nameLIST = []
    for i in range(0, lastINT, 1):
        url = f"http://www.ch.fhl.net/xoops/modules/wordbook/category.php?categoryID={categoryINT}&start={i}0"
        nameLIST.extend(scrape_page(url, categoryINT, i))
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

