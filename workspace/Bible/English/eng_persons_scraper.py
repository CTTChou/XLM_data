#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import json
import os
import requests
import re

engPAT = re.compile(r" ?(.*) （")

def search(htmlSTR):
    soup = BeautifulSoup(htmlSTR, "lxml")
    lineLIST = soup.find_all("li")
    eng_personLIST = []
    
    for i in lineLIST:
        eng_person = re.findall(engPAT, i.get_text())
        eng_personLIST.append(eng_person[0])
    
    return eng_personLIST


def main(url): 
    response = requests.get(url)
    response.encoding = "Big5"
    htmlSTR = response.text
    searched_results = search(htmlSTR)    
    engLIST = searched_results
    return engLIST
    

if __name__ == "__main__":
    letterLIST = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    for i in letterLIST:
        url_main = f"http://www.christianstudy.com/biography_names_{i}.html"
        engLIST = main(url_main)
        
        names_folder = "../../../data/Bible/English/names"
        os.makedirs(names_folder, exist_ok=True)         
        with open("../../../data/Bible/English/names/english_persons.json", "r", encoding="utf-8") as f:
            old_engLIST = json.load(f)    
        with open("../../../data/Bible/English/names/english_persons.json", "w", encoding="utf-8") as f:
            for i in engLIST:
                old_engLIST.append(i)            
            json.dump(old_engLIST, f, ensure_ascii=False, indent=4) 