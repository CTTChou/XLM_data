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
    
for n in bookLIST:                                                                  # loop through all books
    resultLIST = []
    
    temp_n = n                                                     
    if n[0].isdigit():                                                             # for special book names (e.g. 1 Samuel)
        temp_n = re.sub(r'^\d+', lambda m: m.group(0) + '%20', n)
    if " " in n:
        temp_n = re.sub(r"\s", "%20", n)   
    if temp_n == "SongofSolomon":
        temp_n = "Song%20of%20Solomon"        
        
    pattern_start = r'\/passage\/\?search='+temp_n+r'%20(\d+)&amp;version=GNT'      # find all chapters
    chapter_match = re.findall(pattern_start, str(html))

    for m in chapter_match:
        if int(m) == 1:
            print("start", temp_n)
        url = f"https://www.biblegateway.com/passage/?search={temp_n}%20{m}&version=GNT"
        response = requests.get(url)
        html_doc = response.text
        sp = BeautifulSoup(html_doc, 'html.parser')
        paragraph_div = sp.find('div', class_="version-GNT result-text-style-normal text-html")
        tb = paragraph_div.find_all('table')
        if len(tb) != 0:
            print(temp_n, "ch", m, tb)