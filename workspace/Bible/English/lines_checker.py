#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
import re


bookLIST = []                                                                       # find list of all books
url_main = "https://www.biblegateway.com/versions/Good-News-Translation-GNT-Bible/#booklist"
response = requests.get(url_main)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
for span in soup.find_all('span'):
    span.decompose()
book = soup.find_all('td', class_="toggle-collapse2 book-name")
for i in book:
    name = i.get_text()
    name = re.sub("\s", "", name)
    bookLIST.append(name)
    
with open("../../../data/Bible/English/all_EngBible.json", "r", encoding="utf-8") as f:
    dataLIST = json.load(f)

for i, j in enumerate(dataLIST):
    #for j in bookLIST:
    #print(j[bookLIST[i]])
    for k in j[bookLIST[i]]:
        #print("k", list(k.values())[0])
        checkLIST = []
        for l in list(k.values())[0]:
            li = list(l.keys())[0]
            pt = r':(.*)'
            num = re.findall(pt, li)   
            #print(num)
            checkLIST.append(int(num[0]))
        if checkLIST[len(checkLIST)-1] != len(checkLIST):
            missingLIST = []
            multipleLIST = []
            for n in range(1, checkLIST[len(checkLIST)-1]):
                if n not in checkLIST:
                    missingLIST.append(n)
            print(bookLIST[i], list(k.keys())[0], checkLIST, "有大問題", f"缺{missingLIST}", )
