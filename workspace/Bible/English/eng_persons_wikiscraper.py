#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import requests
import re
from bs4 import BeautifulSoup

def NameScrape():
    """
    從維基百科抓取聖經人名，按字母 A-Z 遍歷，擷取列表中的名字並回傳。
    
    回傳:
        eng_nameLIST (list): 聖經人名的列表。
    """    
    
    AtoZLIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'Y', 'Z']
    
    eng_nameLIST = []
    for a in AtoZLIST:
        AtoZ_url = f"https://en.wikipedia.org/wiki/List_of_biblical_names_starting_with_{a}"
        resp = requests.get(AtoZ_url)
        soup = BeautifulSoup(resp.text, "lxml")
        div = soup.find('div', class_="mw-body-content")
        ulLIST = div.find_all('ul')
        liLIST = ulLIST[0].find_all('li')
        
        for j in liLIST:
            outSTR = j.get_text(strip=True)            
            outSTR = re.sub(r",.*|-|\[\d+\]", "", j.get_text())
            eng_nameLIST.append(outSTR)
    
    print(eng_nameLIST)
    return eng_nameLIST


def main():
    """
    爬取聖經人名並將其儲存為 JSON 文件。
    """
    eng_nameLIST = NameScrape()
    
    folder_path = "../../../data/Bible/English/names"
    os.makedirs(folder_path, exist_ok=True)  # 確保資料夾存在
    with open("../../../data/Bible/English/names/english_person_wiki_nameLIST.json", "w", encoding="utf-8") as f:
        json.dump(eng_nameLIST, f, ensure_ascii=False, indent=4)   


if __name__ == "__main__":
    main()
