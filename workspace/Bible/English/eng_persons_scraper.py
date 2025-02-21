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
    eng_personLIST = []
    
    for i in line:
        pattern_ch = r'（(.*)）'
        pattern_eng = r' ?(.*) （'
        ch_person = re.findall(pattern_ch, i.get_text())
        ch_personLIST.append(ch_person[0])
        eng_person = re.findall(pattern_eng, i.get_text())  
        eng_personLIST.append(eng_person[0])
    
    return ch_personLIST, eng_personLIST


def main(url): 
    response = requests.get(url)
    response.encoding = 'Big5'
    html_doc = response.text  
    searched_results = search(html_doc)    
    engLIST = searched_results[1]
    chLIST = searched_results[0]
    return engLIST, chLIST
    

if __name__ == "__main__":
    letterLIST = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    for i in letterLIST:
        url_main = f"http://www.christianstudy.com/biography_names_{i}.html"
        results = main(url_main)
        engLIST = results[0]
        chLIST = results[1]
        
        with open("../../../data/Bible/English/english_persons.json", "r", encoding="utf-8") as f:
            old_engLIST = json.load(f)    
        with open("../../../data/Bible/English/english_persons.json", "w", encoding="utf-8") as f:
            for i in engLIST:
                old_engLIST.append(i)            
            json.dump(old_engLIST, f, ensure_ascii=False, indent=4)   
        
        with open("../../../data/Bible/Chinese/chinese_persons.json", "r", encoding="utf-8") as f:
            old_chLIST = json.load(f)       
        with open("../../../data/Bible/Chinese/chinese_persons.json", "w", encoding="utf-8") as f:
            for i in chLIST:
                    old_chLIST.append(i)  
            json.dump(old_chLIST, f, ensure_ascii=False, indent=4)