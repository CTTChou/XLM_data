from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests import post
import json
import requests

def llm_translation(ls):
    url = "https://api.droidtown.co/Loki/Call/"
    ls1 = ls
    translated_list = []
    
    for i in ls1:
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
        translated_list.append(result['result'][0]['message']['content'])
    
    return translated_list   

    
def search_spec(htmlSTR, a, b):
    ls = []
    soup = BeautifulSoup(htmlSTR, "lxml")
    aLIST = soup.find_all(a, class_=b)
    for a in aLIST:
        aSTR = a.get_text()
        ls.append(aSTR)    
    return ls

def search(htmlSTR, a):
    ls = []
    soup = BeautifulSoup(htmlSTR, "lxml")
    aLIST = soup.find_all(a)
    for a in aLIST:
        aSTR = a.get_text()
        ls.append(aSTR)    
    return ls


def main(): 
    
    return None


if __name__ == "__main__":
    url = "https://focustaiwan.tw/politics/202501030001" 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }    
    response = requests.get(url, headers=headers) 
    html_doc = response.text
    ls = search(html_doc, "p")
    print("english news: ", ls)
    translatedLIST = llm_translation(ls)
    print("translated: ", translatedLIST)
    