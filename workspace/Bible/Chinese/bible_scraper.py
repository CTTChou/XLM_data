#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from urllib.parse import unquote

def get_ChiBibleDICT(url):
    """
    爬取指定網址的中文聖經資料，並將其整理成字典格式。
    參數:
    url (str): 需要爬取的網頁地址，通常為中文聖經的閱讀頁面。

    回傳:
    dict: 返回包含爬取資料的字典，格式如下：

    字典格式範例:
    ChiBibleDICT={ 
    "創世紀": {
        "第1章": [
            {"1:1": "ChiSentence"},
            {"1:2": "ChiSentence"}
            ],
        "第40章": [
            {"40:1": "ChiSentence"},
            {"40:2": "ChiSentence"}]
        }
    }
    """
    ChiBibleDICT = {}
    driver = webdriver.Chrome()
    driver.get(url)
    
    # 等待頁面加載完成
    driver.implicitly_wait(10)
    
    # 獲取頁面原始碼
    htmlSTR = driver.page_source
    driver.quit()
    soup = BeautifulSoup(htmlSTR, "lxml")    

    #第幾章
    scTag = soup.find("select", attrs={"name": "sc", "onchange": "gotochap()"})
    chapterTag = scTag.find("option", selected="selected")
    chSTR = chapterTag.get_text()
    #拿 Book
    sbTag = soup.find("select", attrs={"name": "sb", "onchange": "setchap(1)"})
    bookTag = sbTag.find("option", selected="selected")
    bookSTR = bookTag.get_text()    
    
    trTag = soup.find_all("tr")
    if trTag:
        for tr in trTag[1:]:
            #章節 (e.g. 1:1)            
            tdTag = tr.find("td", align="center").find("b")
            secSTR = tdTag.get_text()
            #拿內文
            tdTag = tr.find_all("td")
            for h2 in tdTag[1].find_all("h2"):
                h2.decompose()
            senSTR = tdTag[1].get_text().strip()
            
            if bookSTR not in ChiBibleDICT:
                ChiBibleDICT[bookSTR] ={}
            if chSTR not in ChiBibleDICT[bookSTR]:
                ChiBibleDICT[bookSTR][chSTR] = []
            ChiBibleDICT[bookSTR][chSTR].append({secSTR: senSTR})
    return ChiBibleDICT

def get_BookLIST(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)
    htmlSTR = driver.page_source
    driver.quit()
    soup = BeautifulSoup(htmlSTR, "lxml")
    sbTag = soup.find("select", attrs={"name": "sb", "onchange": "setchap(1)"})    
    valueTag = sbTag.find_all("option")
    bookLIST = [v["value"] for v in valueTag]
    return bookLIST

def main(url):
    bookLIST = get_BookLIST(url)
    all_ChiBibleLIST = []
    for b in bookLIST:
        ChiBibleLIST = []
        bookname = unquote(b)
        try:
            for i in range(1, 151):
                ch_url = f"https://bible.fhl.net/new/read.php?VERSION4=tcv95&strongflag=0&TABFLAG=1&chineses={b}&chap={i}&submit1=%E9%96%B1%E8%AE%80"
                ChiBibleDICT = get_ChiBibleDICT(ch_url)
                pprint(ChiBibleDICT)
                ChiBibleLIST.append(ChiBibleDICT)
        except IndexError:
            pass
        
        book_jsonFILE = f"{bookname}.json"
        with open(book_jsonFILE, "w", encoding="utf-8") as f:
            json.dump(ChiBibleLIST, f, ensure_ascii=False, indent=4)
            all_ChiBibleLIST.extend(ChiBibleLIST)
    
    with open("./ChiBible.json", "w", encoding="utf-8") as f:
        json.dump(all_ChiBibleLIST, f, ensure_ascii=False, indent=4)
    
    return all_ChiBibleLIST

if __name__ == "__main__":
    url = f"https://bible.fhl.net/new/read.php?VERSION4=tcv95&strongflag=0&TABFLAG=1&chineses=%E5%89%B5&chap=1&submit1=%E9%96%B1%E8%AE%80"
    all_ChiBibleLIST = main(url)
    pprint(all_ChiBibleLIST)
  