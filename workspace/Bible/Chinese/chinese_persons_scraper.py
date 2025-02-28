#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import json
import os
import requests
import re

chPAT = re.compile(r"（(.*)）")

def search(htmlSTR):
    soup = BeautifulSoup(htmlSTR, "lxml")
    lineLIST = soup.find_all("li")
    ch_personLIST = []
    
    for i in lineLIST:
        ch_person = re.findall(chPAT, i.get_text())
        ch_personLIST.append(ch_person[0])
    
    return ch_personLIST


def main(url): 
    response = requests.get(url)
    response.encoding = "Big5"
    htmlSTR = response.text  
    searched_results = search(htmlSTR)    
    chLIST = searched_results
    return chLIST
    

if __name__ == "__main__":
    letterLIST = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    for i in letterLIST:
        url_main = f"http://www.christianstudy.com/biography_names_{i}.html"
        chLIST = main(url_main)
        
        names_folder = "../../../data/Bible/Chinese/names"
        os.makedirs(names_folder, exist_ok=True)        
        with open("../../../data/Bible/Chinese/names/chinese_persons.json", "r", encoding="utf-8") as f:
            old_chLIST = json.load(f)       
        with open("../../../data/Bible/Chinese/names/chinese_persons.json", "w", encoding="utf-8") as f:
            for i in chLIST:
                    old_chLIST.append(i)  
            json.dump(old_chLIST, f, ensure_ascii=False, indent=4)