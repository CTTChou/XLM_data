#!/user/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests import post
import json
import requests
import re


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
            #"user": "依上文，翻譯成台灣新聞常見的台灣繁體中文，不要出現中文以外的語言文字，請依照輸入的句子回傳句子內容的翻譯即可，不需額外加入註解，遇到名字時，如果後面已經有括號加入中文名稱，請直接使用原文括號內提供的中文，不需要繼續附上括號。", # required            
            "user": "依上文，全部翻譯成台灣新聞常見的台灣繁體中文，不要回覆繁體中文以外的內容，名字國名也都要翻譯成繁體中文。", # required
          }
        }
        try:
            result = post(url, json=payload).json()
            resultSTR = result['result'][0]['message']['content']
            processedSTR = re.sub("Note.*|[(.*)]|[(.*]]|\n|[（.*）]", '', resultSTR)
            translatedLIST.append(processedSTR)
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
    engLIST = search_para(html_doc)
    for i in engLIST:
        engLIST[engLIST.index(i)] = re.sub(".*[(CNA)]\s", '', i)    
    print("english news: ", engLIST)
    translatedLIST = llm_translate(engLIST)
    print("translated: ", translatedLIST)
    
    resultDICT = {}
    sentenceDICT = {}
    sentenceLIST = []
    for i in range(len(engLIST)):
        tempDICT = {}
        tempDICT[engLIST[i]] = translatedLIST[i]
        sentenceLIST.append(tempDICT)  
    resultDICT["src"] = url
    resultDICT["sentence"] = sentenceLIST
      
    return resultDICT


if __name__ == "__main__":
    url = "https://focustaiwan.tw/politics/202501060006" 
    resultDICT = main(url)
    
    with open('../../data/cna_news/english/eng_results.json', 'r') as file:
        dataLIST = json.load(file)
        dataLIST.append(resultDICT)
    
    with open("../../data/cna_news/english/eng_results.json", "w", encoding="utf-8") as f:
        json.dump(dataLIST, f, ensure_ascii=False, indent=4)     