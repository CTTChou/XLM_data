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
            "system": "你是一個專業的台灣繁體中文至英文新聞翻譯人員", # optional
            "assistant": i, # optional
            "user": "依上文，翻譯成新聞用英語", # required
          }
        }
        try:
            result = post(url, json=payload).json()
            translatedLIST.append(result["result"][0]["message"]["content"])
        except Excption as e:
            print(f"input: {i}, Error: {e}")
    
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
    """
    Fetches a web page from the provided URL, extracts news content, 
    translates the content, and returns the result dictionary.
    
    Parameters:
        url (str): The input url string.
    
    Returns:
        dict: A dictionary with the following keys:
            - "src": The original URL of the web page.
            - "sentence": A list of dictionaries containing the original and translated news content.
    """    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }    
    response = requests.get(url, headers=headers) 
    html_doc = response.text
    chLIST = search_para(html_doc)
    print("chinese news: ", chLIST)
    translatedLIST = llm_translate(chLIST)
    print("translated: ", translatedLIST)
    
    resultDICT = {}
    sentenceDICT = {}
    sentenceLIST = []
    for i in range(len(chLIST)):
        tempDICT = {}
        tempDICT[chLIST[i]] = translatedLIST[i]
        sentenceLIST.append(tempDICT)
    resultDICT["src"] = url
    resultDICT["sentence"] = sentenceLIST
    
    return resultDICT


if __name__ == "__main__":
    url = "https://www.cna.com.tw/news/aipl/202501060065.aspx" 
    resultDICT = main(url)
    
    with open("../../data/cna_news/chinese/ch_results.json", "r", encoding="utf-8") as file:
        dataLIST = json.load(file)
        dataLIST.append(resultDICT)
    
    with open("../../data/cna_news/chinese/ch_results.json", "w", encoding="utf-8") as f:
        json.dump(dataLIST, f, ensure_ascii=False, indent=4)    

