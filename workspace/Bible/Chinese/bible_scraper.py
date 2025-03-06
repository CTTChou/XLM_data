#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from urllib.parse import unquote

delPAT = re.compile(r"\n|『|』|「|」|‧|\s|第[一二三四]卷|•[^•]+•|\[|\]|《|》|\u3000")   #刪除的內容

def get_ChiBibleDICT(url):
    """
    爬取指定網址的中文聖經資料，並將其整理成字典格式。
    
    參數:
    url (str): 需要爬取的網頁地址，通常為中文聖經的閱讀頁面。

    回傳:
    dict: 返回包含爬取資料的字典，格式如下：

    字典格式範例:
    ChiBibleDICT={ 
    "創世紀": [{
        "第1章": [
            {"1:1": "ChiSentence"},
            {"1:2": "ChiSentence"}
            ],
        "第40章": [
            {"40:1": "ChiSentence"},
            {"40:2": "ChiSentence"}]
            }]
    }
    """
    ChiBibleDICT = {}
    #driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    
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
        prev_senSTR = ""  # 用來保存上一個內文
        for tr in trTag[1:]:
            #章節 (e.g. 1:1)            
            tdTag = tr.find("td", align="center").find("b")
            secSTR = tdTag.get_text()
            #拿內文
            tdTag = tr.find_all("td")
            for h2 in tdTag[1].find_all("h2"):
                h2.decompose()
            for b in tdTag[1].find_all("b"):
                b.decompose()
            senSTR = tdTag[1].get_text().strip()
            senSTR = re.sub(delPAT, "", senSTR)
            
            while senSTR in {"【併於上節】", "a"}:  # 如果是 "【併於上節】" 或是 "a"，持續回溯到上一個非 "【併於上節】" 或非 "a" 的內文
                senSTR = prev_senSTR
            if senSTR not in {"【併於上節】", "a"}:   # 如果不是 "【併於上節】"，更新 prev_senSTR
                prev_senSTR = senSTR

            if bookSTR not in ChiBibleDICT:
                ChiBibleDICT[bookSTR] = [{}]
            if chSTR not in ChiBibleDICT[bookSTR][0]:
                ChiBibleDICT[bookSTR][0][chSTR] = []
            # 添加 secSTR 和 senSTR 到對應的章節
            ChiBibleDICT[bookSTR][0][chSTR].append({secSTR: senSTR})
            
    return ChiBibleDICT, bookSTR

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
    獲取指定 URL 的書籍列表，並對每本書進行處理，抓取每章的中文聖經內容。
    將每本書的內容存儲為單獨的 JSON 文件，最後將所有書的內容匯總為一個 JSON 文件。

    參數:
        url (str): 包含書籍列表的目標網頁的 URL。

    返回:
        list: 包含所有書籍中文聖經內容的列表。
    """    
    bookLIST = get_BookLIST(url)
    print(f"book 總數為： {len(bookLIST)}")
    all_ChiBibleLIST = []
    for b in bookLIST:
        ChiBibleLIST = []
        bookname = unquote(b)
        book_jsonFILE = f"../../../data/Bible/Chinese/book/{bookname}.json"        
        if os.path.exists(book_jsonFILE):
            with open(book_jsonFILE, "r", encoding="utf-8") as f:   #讀取已存在的 chapter，並從還未抓取的章節開始
                ChiBibleLIST = json.load(f)
            bookSTR = list(ChiBibleLIST[0].keys())[0]
            exist_chapter = len(ChiBibleLIST[0][bookSTR])
        else:
            exist_chapter = 0
        
        bk_url = f"https://bible.fhl.net/new/read.php?VERSION4=tcv95&strongflag=0&TABFLAG=1&chineses={b}&chap=1&submit1=%E9%96%B1%E8%AE%80"
        print(f"processing {bookname}...")
        chapterINT = get_ChapterLIST(bk_url)
        for i in range(exist_chapter + 1, chapterINT + 1):  #根據每個 book 有的章節數量做迴圈
            ch_url = f"https://bible.fhl.net/new/read.php?VERSION4=tcv95&strongflag=0&TABFLAG=1&chineses={b}&chap={i}&submit1=%E9%96%B1%E8%AE%80"
            ChiBibleDICT, bookSTR = get_ChiBibleDICT(ch_url)
            pprint(ChiBibleDICT)
            book_folder = "../../../data/Bible/Chinese/book"
            if not os.path.exists(book_folder):
                os.makedirs(book_folder)
            with open(book_jsonFILE, "w", encoding="utf-8") as f:   #每次抓取新章節都更新 jsonFILE
                json.dump(ChiBibleLIST, f, ensure_ascii=False, indent=4)
            
            existing_bookDICT = None
            for bookDICT in ChiBibleLIST:
                if bookSTR in bookDICT:
                    existing_bookDICT = bookDICT
                    break
            if existing_bookDICT:   # 合併 chapter
                existing_bookDICT[bookSTR].append(ChiBibleDICT[bookSTR][0])
            else:   #合併 book
                ChiBibleLIST.append(ChiBibleDICT)             
            pprint(ChiBibleLIST)

        with open(book_jsonFILE, "w", encoding="utf-8") as f:   #抓取完所有章節更新 jsonFILE
            json.dump(ChiBibleLIST, f, ensure_ascii=False, indent=4)
        
    book_folder = "../../../data/Bible/Chinese/book"
    for FILEname in os.listdir(book_folder):
        if FILEname.endswith(".json"):
            filepath = os.path.join(book_folder, FILEname)
            with open(filepath, "r", encoding="utf-8") as f:    #整合所有 book_jsonFILE
                all_ChiBibleLIST.extend(json.load(f))
                
    with open("../../../data/Bible/Chinese/all_ChiBible.json", "w", encoding="utf-8") as f:
        json.dump(all_ChiBibleLIST, f, ensure_ascii=False, indent=4)
        
    return all_ChiBibleLIST

if __name__ == "__main__":
    url = "https://bible.fhl.net/new/read.php?VERSION4=tcv95&strongflag=0&TABFLAG=1&chineses=%E5%89%B5&chap=1&submit1=%E9%96%B1%E8%AE%80"
    
    all_ChiBibleLIST = main(url)
    pprint(all_ChiBibleLIST)    
        
    
  