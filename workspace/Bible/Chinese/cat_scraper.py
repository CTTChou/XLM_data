#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import re
import random
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from time import sleep

delPAT = re.compile(r"(?<= ).+畫(?= )|\([^\)]+\)")
namePAT = re.compile(r"(?<=[a-z] )[^a-z]+(?= )")

def scrape_page(url):
    """
    擷取指定網址的名稱列表。

    參數:
        url (str): 目標網址。

    回傳:
        list: 從該頁面擷取的名稱列表。    
    """
    nameLIST = []    
    
    response = requests.get(url)
    sleep(random.randrange(1, 10))
    htmlSTR = response.text
    soup = BeautifulSoup(htmlSTR, "lxml")
    
    h4LIST = soup.find_all("h4")    #找 h4 中的 <a href>
    for h4 in h4LIST:
        a = h4.find("a", href=True, string=True)
        if a and a["href"].startswith("http://www.ch.fhl.net/xoops/modules/wordbook/entry.php?"):
            aSTR = a.text.strip()
            aSTR = re.sub(delPAT, "", aSTR) #去除不需要的部分，像是 xx畫、(英文名)
            nameSTR = re.search(namePAT, aSTR).group() if re.search(namePAT, aSTR) else None    #找到中文名
            print(nameSTR)
            if nameSTR: #找到的話，添加到 nameLIST
                nameLIST.append(nameSTR.strip())
            
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
    
    #找地名
    for i in range(0, lastINT, 10):
        url = f"http://www.ch.fhl.net/xoops/modules/wordbook/category.php?categoryID={categoryINT}&start={i}"
        print(i)
        nameLIST.extend(scrape_page(url))  

    return nameLIST



if __name__ == "__main__":
    #找地名
    locLIST = main(categoryINT=7, lastINT=1170)
    with open("../../../data/Bible/Chinese/names/places.json", "w", encoding="utf-8") as f:
        json.dump({"LOCATION": locLIST}, f, ensure_ascii=False, indent=4)
        
    #找人名        
    perLIST = main(categoryINT=6, lastINT=1870)
    with open("../../../data/Bible/Chinese/names/persons.json", "w", encoding="utf-8") as f:
        json.dump({"ENTITY_person": perLIST}, f, ensure_ascii=False, indent=4)     