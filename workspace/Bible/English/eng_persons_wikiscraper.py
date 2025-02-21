#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import requests
import re
from bs4 import BeautifulSoup

url_list = "https://en.wikipedia.org/wiki/List_of_biblical_names"
resp_list = requests.get(url_list)
soup_list = BeautifulSoup(resp_list.text, "lxml")

azLIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'Y', 'Z']

eng_nameLIST = []
for a in azLIST:

    az_url = f"https://en.wikipedia.org/wiki/List_of_biblical_names_starting_with_{a}"
    resp = requests.get(az_url)
    soup = BeautifulSoup(resp.text, "lxml")
    div = soup.find('div', class_="mw-body-content")
    ul = div.find_all('ul')
    d = ul[0].find_all('li')
    
    for a in d:
        out = re.sub(r",.*", "", a.get_text())
        out = re.sub(r"-", "", out)
        out = re.sub(r"\[\d\]", "", out)
        #print(out)
        eng_nameLIST.append(out)
print(eng_nameLIST)

with open("../../../data/Bible/English/english_person_wiki_nameLIST.json", "w", encoding = "utf-8") as f:
    json.dump(eng_nameLIST, f, ensure_ascii=False, indent=4)
    
    
    