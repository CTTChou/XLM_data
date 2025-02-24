#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import requests
import re
from bs4 import BeautifulSoup

def NameScrape():
    
    AtoZLIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'Y', 'Z']
    
    for a in AtoZLIST:
        AtoZ_url = f"https://en.wikipedia.org/wiki/List_of_biblical_names_starting_with_{a}"
        resp = requests.get(AtoZ_url)
        soup = BeautifulSoup(resp.text, "lxml")
        div = soup.find('div', class_="mw-body-content")
        ul = div.find_all('ul')
        li = ul[0].find_all('li')
        
        for j in li:
            out = re.sub(r",.*", "", j.get_text())
            out = re.sub(r"-", "", out)
            out = re.sub(r"\[\d\]", "", out)
            eng_nameLIST.append(out)
    
    print(eng_nameLIST)
    return eng_nameLIST


def main(eng_nameLIST):
    NameScrape()
    with open("../../../data/Bible/English/english_person_wiki_nameLIST.json", "w", encoding = "utf-8") as f:
        json.dump(eng_nameLIST, f, ensure_ascii=False, indent=4)    


if __name__ == "__main__":
    eng_nameLIST = []
    main(eng_nameLIST)
