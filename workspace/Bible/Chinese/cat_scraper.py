#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import re
import random
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from time import sleep

delPAT = re.compile(r"(?<= ).+畫(?= )|\([^\)]+\)")
namePAT = re.compile(r"(?<=[a-z] )[^a-z]+(?= )")

def main(url):
    """"""
    nameLIST = []    
    
    response = requests.get(url)
    sleep(random.randrange(1, 10))
    htmlSTR = response.text
    soup = BeautifulSoup(htmlSTR, "lxml")
    
    h4LIST = soup.find_all("h4")    #找 h4 中的 <a href>
    for h4 in h4LIST:
        a = h4.find("a", href=True, string=True)
        if a and a["href"].startswith("http://www.ch.fhl.net/xoops/modules/wordbook/entry.php?"):
            aSTR = a.text.strip()
            aSTR = re.sub(delPAT, "", aSTR) #去除不需要的部分，像是 xx畫、(英文名)
            nameSTR = re.search(namePAT, aSTR).group() if re.search(namePAT, aSTR) else None    #找到中文名
            print(nameSTR)
            if nameSTR: #找到的話，添加到 nameLIST
                nameLIST.append(nameSTR.strip())
            
    pprint(nameLIST)
    return nameLIST


if __name__ == "__main__":
    locDICT = {"LOCATION": []}
    personDICT = {"ENTITY_person": []}
    
    #找地名
    #for i in range(0, 1170, 10):
        #url = f"http://www.ch.fhl.net/xoops/modules/wordbook/category.php?categoryID=7&start={i}"
        #print(i)        
        #locLIST = main(url)
        #locDICT["LOCATION"].extend(locLIST)
        
    #print(locDICT)
    #with open("../../../data/Bible/Chinese/names/places.json", "w", encoding="utf-8") as f:
        #json.dump(locDICT, f, ensure_ascii=False, indent=4)

    #找人名
    for i in range(0, 1870, 10):
        url = f"http://www.ch.fhl.net/xoops/modules/wordbook/category.php?categoryID=6&start={i}"
        print(i)        
        personLIST = main(url)
        personDICT["ENTITY_person"].extend(personLIST)
    
    print(personDICT)
    with open("../../../data/Bible/Chinese/names/persons.json", "w", encoding="utf-8") as f:
        json.dump(personDICT, f, ensure_ascii=False, indent=4)    