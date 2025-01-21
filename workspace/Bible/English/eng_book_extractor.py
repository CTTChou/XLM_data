#!/user/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
import re

def content_extractor(bookLIST):
    for i in bookLIST:
        book = i
        resultLIST = []
        with open("../../../data/Bible/English/all_EngBible.json", "r", encoding="utf-8") as f:
            dataLIST = json.load(f)
            dic = dataLIST[0]
            resultLIST.append(dic)
        with open(f"../../../data/Bible/English/book/{book}.json", "w", encoding="utf-8") as f:
            json.dump(resultLIST, f, ensure_ascii=False, indent=4)
        print(f"{book} done!")
    return None
    
def main(): 
    bookLIST = []
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
    content_extractor(bookLIST)
    return None
    
if __name__ == "__main__":
    main()
    