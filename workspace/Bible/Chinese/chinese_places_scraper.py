#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
import re

def search(htmlSTR):
    soup = BeautifulSoup(htmlSTR, 'lxml')
    line = soup.find_all('li')
    ch_personLIST = []
    
    for i in line:
        pattern_ch = r'（(.*)）'
        ch_person = re.findall(pattern_ch, i.get_text())
        ch_personLIST.append(ch_person[0])
    
    return ch_personLIST


def main(url): 
    try:
        response = requests.get(url)   
        response.encoding = 'Big5'
        html_doc = response.text
        searched_results = search(html_doc)    
        chLIST = searched_results
        return chLIST        
    except Exception as e:
        print(e)
        pass 
    

if __name__ == "__main__":
    letterLIST = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    for i in letterLIST:
        url_main = f"http://www.christianstudy.com/biography_places_{i}.html"
        results = main(url_main)
        chLIST = results
        
        if chLIST != None:
            with open("../../../data/Bible/Chinese/chinese_places.json", "r", encoding="utf-8") as f:
                old_chLIST = json.load(f)       
            with open("../../../data/Bible/Chinese/chinese_places.json", "w", encoding="utf-8") as f:
                for i in chLIST:
                    old_chLIST.append(i)  
                json.dump(old_chLIST, f, ensure_ascii=False, indent=4)