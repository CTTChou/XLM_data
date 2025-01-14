#!/user/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests import post
import json
import requests


def llm_translate(inputLIST):
    """
    Translates the input list and returns the translated list.
    
    Parameters:
        inputLIST (list): The input list.
    
    Returns:
        list: The translation of a.
    """
    url = "https://api.droidtown.co/Loki/Call/"
    translatedLIST = []
    
    for i in inputLIST:
        payload = {
          "username": "ganpeijie3@gmail.com",
          "func": "call_llm",
          "data": {
            "model": "Llama3-8B", # [Gemma2-9B, Llama3-8B]
            "system": "你是一個專業的英文至台灣繁體中文新聞翻譯人員", # optional
            "assistant": i, # optional
            "user": "依上文，翻譯成台灣新聞常見的台灣繁體中文", # required
          }
        }
        result = post(url, json=payload).json()
        translatedLIST.append(result['result'][0]['message']['content'])
    
    return translatedLIST


def search_para(htmlSTR):
    """
    Searches <p> tags in the input HTML string and returns the results list.
    
    Parameters:
        htmlSTR (str): The HTML string.
    
    Returns:
        list: The list of searched paragraphs.
    """
    outputLIST = []
    soup = BeautifulSoup(htmlSTR, "lxml")
    paragraph_div = soup.find('div', class_='paragraph')
    result = paragraph_div.find_all('p', recursive=False)
    for i in result:
        outputLIST.append(i.get_text())
    return outputLIST


def main(url): 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }    
    response = requests.get(url, headers=headers) 
    html_doc = response.text
    ls = search_para(html_doc)
    print("english news: ", ls)
    translatedLIST = llm_translate(ls)
    print("translated: ", translatedLIST)
    
    resultDICT = {}
    sentenceDICT = {}
    sentenceLIST = []
    for i in range(len(ls)):
        tempDICT = {}
        tempDICT[ls[i]] = translatedLIST[i]
        sentenceLIST.append(tempDICT)
    #print(sentenceLIST)    
    resultDICT["src"] = url
    resultDICT["sentence"] = sentenceLIST
      
    return resultDICT


if __name__ == "__main__":
    url = "https://focustaiwan.tw/politics/202501060006" 
    resultDICT = main(url)
    
    with open('eng_results.json', 'r') as file:
        dataLIST = json.load(file)
        dataLIST.append(resultDICT)
    
    with open("eng_results.json", "w", encoding="utf-8") as f:
        json.dump(dataLIST, f, ensure_ascii=False, indent=4)     