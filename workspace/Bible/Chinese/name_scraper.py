#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from urllib.parse import unquote

bookPAT = re.compile(r"(?<=《).*?(?=》)")

def get_names(url):
    """
    從指定的 URL 擷取表格中的帶有 <u> 標籤的專有名詞，以及《》內的書名，並返回一個不重複的名稱集合。

    參數:
        url (str): 目標網頁的 URL。

    返回:
        nameSET (set): 單一章節內所有專有名詞的集合。
    """
    #driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    
    driver.get(url)
    
    # 等待頁面加載完成
    driver.implicitly_wait(10)
    
    # 獲取頁面原始碼
    htmlSTR = driver.page_source
    driver.quit()
    soup = BeautifulSoup(htmlSTR, "lxml")       
    
    nameSET = set()
    trTag = soup.find_all("tr")
    if trTag:
        for tr in trTag[1:]:
            #拿內文
            tdTag = tr.find_all("td")
            for h2 in tdTag[1].find_all("h2"):
                h2.decompose()
            for b in tdTag[1].find_all("b"):
                b.decompose()

            senSTR = tdTag[1].get_text().strip()
            booknameSTR = re.search(bookPAT, senSTR)    #《》的書名
            if booknameSTR:
                nameSET.add(booknameSTR.group(0))
                
            nameTag = tdTag[1].find_all("u")    #有 underlined 的專有名詞
            if nameTag:
                for n in nameTag:
                    nameSTR = n.get_text().strip()
                    nameSTR = nameSTR.replace("‧", "")
                    nameSET.add(nameSTR)
    return nameSET

def get_BookLIST(url):
    """
    使用 Selenium 驅動 Chrome 瀏覽器來訪問指定的 URL，並抓取 HTML 原始碼。
    使用 BeautifulSoup 解析 HTML，從 `<select>` 標籤中提取所有書籍的選項值，並返回這些值作為書籍列表。

    參數:
        url (str): 目標網頁的 URL。

    返回:
        list: 包含所有書籍選項值的列表。
    """    
    #driver = webdriver.Chrome()
    driver = webdriver.Firefox()  
    driver.get(url)
    driver.implicitly_wait(10)
    htmlSTR = driver.page_source
    driver.quit()
    soup = BeautifulSoup(htmlSTR, "lxml")
    sbTag = soup.find("select", attrs={"name": "sb", "onchange": "setchap(1)"})    
    valueTag = sbTag.find_all("option")
    bookLIST = [v["value"] for v in valueTag]
    print(f"bookLIST = {bookLIST}")    
    return bookLIST

def get_ChapterLIST(bk_url):
    """
    使用 Selenium 驅動 Chrome 瀏覽器來訪問指定的 URL，並抓取 HTML 原始碼。
    使用 BeautifulSoup 解析 HTML，從 `<select>` 標籤中提取所有書籍中的最後一章的選項值，並返回最後一章的數值。

    參數:
        url (str): 目標網頁的 URL。

    返回:
        int: 包含所有書籍中的最後一章的選項值。
    """    
    #driver = webdriver.Chrome()
    driver = webdriver.Firefox()  
    driver.get(bk_url)
    driver.implicitly_wait(10)
    htmlSTR = driver.page_source
    driver.quit()
    soup = BeautifulSoup(htmlSTR, "lxml")
    scTag = soup.find("select", attrs={"name": "sc", "onchange": "gotochap()"})
    valueTag = scTag.find_all("option")
    chapterLIST = [v["value"] for v in valueTag]
    chapterINT = int(chapterLIST[-1])
    print(f"last chapter = {chapterINT}")    
    return chapterINT

def main(url):
    """
    從指定的 URL 獲取書籍列表，並遍歷每本書的所有章節，擷取經文中的名稱。

    參數:
        url (str): 包含書籍列表的目標網頁的 URL。

    返回:
        all_nameSET (set): 所有 book 的名稱集合。

    功能:
        1. 取得 bookLIST。
        2. 依序處理每本書，根據章節數量建立 ch_url。
        3. 擷取每章的名稱並存入集合，確保名稱不重複。
        4. 每次擷取新名稱後，將其儲存至 `fhl_names.json`。

    """    
    bookLIST = get_BookLIST(url)
    all_nameSET = set()
    
    for idx, b in enumerate(bookLIST):
        bookname = unquote(b)
        bk_url = f"https://bible.fhl.net/new/read.php?VERSION4=tcv95&strongflag=0&TABFLAG=1&chineses={b}&chap=1&submit1=%E9%96%B1%E8%AE%80"
        
        chapterINT = get_ChapterLIST(bk_url)
        for i in range(1, chapterINT + 1):  #根據每個 book 有的章節數量做迴圈
            print(f"正在處理 idx: {idx} 的 '{bookname}' 的 '第{i}章'")            
            ch_url = f"https://bible.fhl.net/new/read.php?VERSION4=tcv95&strongflag=0&TABFLAG=1&chineses={b}&chap={i}&submit1=%E9%96%B1%E8%AE%80"
            nameSET = get_names(ch_url)
            pprint(nameSET)
            
            all_nameSET.update(nameSET)
            names_folder = "../../../data/Bible/Chinese/names"
            os.makedirs(names_folder, exist_ok=True)
            with open("../../../data/Bible/Chinese/names/fhl_names.json", "w", encoding="utf-8") as f:
                json.dump(list(all_nameSET), f, ensure_ascii=False, indent=4)
            
    pprint(all_nameSET)
    return all_nameSET

if __name__ == "__main__":
    url = "https://bible.fhl.net/new/read.php?VERSION4=tcv95&strongflag=0&TABFLAG=1&chineses=%E5%89%B5&chap=1&submit1=%E9%96%B1%E8%AE%80"
    
    jsonFILE = "../../../data/Bible/Chinese/names/fhl_names.json"
    if not os.path.exists(jsonFILE):    #如果還不存在檔案才呼叫 main() 爬蟲
        userDefinedDICT = {}
        all_nameSET = main(url)
        nameLIST = sorted(list(all_nameSET), key=len)   #轉成列表後，依照元素長度排序
        userDefinedDICT["ENTITY_person"] = nameLIST     #再轉成 dict type for articut
                        
                           
        with open(jsonFILE, "w", encoding="utf-8") as f:    #寫出檔案並印出
            json.dump(userDefinedDICT, f, ensure_ascii=False, indent=4)
            pprint(userDefinedDICT)
    
    else:   #檔案存在就印出來看看
        with open(jsonFILE, "r", encoding="utf-8") as f:
            userDefinedDICT = json.load(f)       
            pprint(userDefinedDICT)
        
    
