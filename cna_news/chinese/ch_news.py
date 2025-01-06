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
            "system": "你是一個專業的台灣繁體中文至英文新聞翻譯人員", # optional
            "assistant": i, # optional
            "user": "依上文，翻譯成新聞用英語", # required
          }
        }
        result = post(url, json=payload).json()
        translated_list.append(result['result'][0]['message']['content'])
    
    return translated_list


def search_paragraphs_in_paragraph_div(htmlSTR):
    """<p> tags inside <div class='paragraph'> and not <div class='author'>."""
    ls = []
    soup = BeautifulSoup(htmlSTR, "lxml")
    paragraph_div = soup.find('div', class_='paragraph')
    result = paragraph_div.find_all('p', recursive=False)
    for i in result:
        ls.append(i.get_text())
    return ls


def main(): 
    
    return None


if __name__ == "__main__":
    url = "https://www.cna.com.tw/news/asoc/202501060183.aspx" 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }    
    response = requests.get(url, headers=headers) 
    html_doc = response.text
    #print(html_doc)
    ls = search_paragraphs_in_paragraph_div(html_doc)
    print("chinese news: ", ls)
    translatedLIST = llm_translation(ls)
    print("translated: ", translatedLIST)
    
    resultDICT = {}
    for i in range(len(ls)):
        resultDICT[ls[i]] = translatedLIST[i]
    print(resultDICT)
    with open("ch_results.json", "a", encoding="utf-8") as f:
        f.write(url+"\n")
        json.dump(resultDICT, f, ensure_ascii=False, indent=4)
        f.write("\n")
    
    
    
'''def search_spec(htmlSTR, a, b):
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
    return ls'''

