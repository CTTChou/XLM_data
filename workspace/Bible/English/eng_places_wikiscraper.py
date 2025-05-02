#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import requests
import re
from bs4 import BeautifulSoup

def PlaceScrape(): 
    
    AtoZLIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'Y', 'Z']
    
    url_places = "https://en.wikipedia.org/wiki/List_of_biblical_places"
    resp = requests.get(url_places)
    soup = BeautifulSoup(resp.text, "lxml")
    divLIST = soup.find('div', class_="mw-content-ltr mw-parser-output")
    ulLIST = divLIST.find_all('ul')
    
    for index in range(len(AtoZLIST)-1):
        liLIST = ulLIST[index+1].find_all('li')
        for j in liLIST:
            out = j.get_text()
            out = re.sub(r",.*", "", out)
            out = re.sub(r"\s\–.*", "", out)
            out = re.sub(r"\s\(Bible\)","", out)               
            out = re.split(r"\/", out)
            eng_placeLIST.extend(out)
    
    print(eng_placeLIST)
    return eng_placeLIST



def main(eng_placeLIST):
    PlaceScrape()
    with open("../../../data/Bible/English/english_place_wiki_nameLIST.json", "w", encoding = "utf-8") as f:
        json.dump(eng_placeLIST, f, ensure_ascii=False, indent=4)    


if __name__ == "__main__":
    eng_placeLIST = []
    main(eng_placeLIST)
    
    
