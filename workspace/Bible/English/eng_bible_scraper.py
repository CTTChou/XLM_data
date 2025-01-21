#!/user/bin/env python
# -*- coding: utf-8 -*-


from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
import re
    
    
def search(htmlSTR):
    """
    Searches the the htmlSTR and returns the content and line number list.
    
    Parameters:
        htmlSTR (str): The HTML string.
    
    Returns:
        list: The list of searched content.
        list: The list of line numbers.
    """
    soup = BeautifulSoup(htmlSTR, 'lxml')
    tempLIST = []
    paragraph_div = soup.find('div', class_="version-GNT result-text-style-normal text-html")
    ps = paragraph_div.find_all('p')
    for j in ps:
        result = j.find_all('span', recursive=False)
        for i in result:
            tempLIST.append(i.get_text())
    outputLIST = []
    for i in tempLIST:
        if "\xa0" in i:
            outputLIST.append(i)
        else:
            outputLIST[-1] += " "
            outputLIST[-1] += i  
    lineLIST = []
    for i, j in enumerate(outputLIST):
        pattern_start = r'(\d+)\xa0|(\d\-\d)\xa0'
        match = re.findall(pattern_start, j)
        print(match)
        if match[0][0] != "":
            lineLIST.append(match[0][0])
        else:
            lineLIST.append(match[0][1])
        outputLIST[i] = re.sub(r'\d+\xa0|\[\w\]|\(\w\)|\(|\)|\“|\‘|\’|\”|\s$|\d\-\d\xa0', "", j)
    lineLIST[0] = "1"
    
    for i, j in enumerate(lineLIST):
        if "-" in lineLIST[i]:
            pattern1 = r'(\d)\-\d'
            pattern2 = r'\d\-(\d)'
            num1 = re.findall(pattern1, j)    
            num2 = re.findall(pattern2, j)
      
    return outputLIST, lineLIST


def main(url, chapter_num): 
    """
    Fetches a web page from the provided URL, extracts the html string, calls the 
    search() function to obtain content of the specified chapter, and returns the result list.
    
    Parameters:
        url (str): The input url string.
        chapter_num (int): The specified Bible chapter.
    
    Returns:
        list: A list containing the dictionary of the content of the searched chapter.
    """
    response = requests.get(url)
    html_doc = response.text  
    searched_results = search(html_doc)
    engLIST = searched_results[0]
    lineLIST = searched_results[1]
    
    resultLIST = []
    sentenceDICT ={}
    sentenceLIST = []
    for i in range(len(lineLIST)):
        tempDICT = {}              
        tempSTR = f"{chapter_num}:{lineLIST[i]}"
        tempDICT[tempSTR] = engLIST[i]        
        sentenceLIST.append(tempDICT)
    sentenceDICT[f"Chapter {chapter_num}"] = sentenceLIST
    #resultLIST.append(sentenceDICT)
    print(resultLIST)
    
    return sentenceDICT


if __name__ == "__main__":
    
    bookLIST = []
    url_main = "https://www.biblegateway.com/versions/Good-News-Translation-GNT-Bible/#booklist"
    response = requests.get(url_main)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    for span in soup.find_all('span'):
        span.decompose()
    book = soup.find_all('td', class_="toggle-collapse2 book-name")
    for i in book:
        name = i.get_text()
        name = re.sub("\s", "", name)
        bookLIST.append(name)
    
    for n in bookLIST:
        resultLIST = []
        pattern_start = r'\/passage\/\?search='+n+r'%20(\d+)&amp;version=GNT'
        match = re.findall(pattern_start, str(html))
        print(match)
        for m in match:
            try:
                url = f"https://www.biblegateway.com/passage/?search={n}%20{m}&version=GNT"
                resultLIST.append(main(url, m))
                print(resultLIST)      
            except Exception:
                pass
        
        resultDICT = {}
        resultDICT[n] = resultLIST

        with open("../../../data/Bible/English/all_EngBible.json", "r", encoding="utf-8") as f:
            dataLIST = json.load(f)
            dataLIST.append(resultDICT)        
        with open("../../../data/Bible/English/all_EngBible.json", "w", encoding="utf-8") as f:
            json.dump(dataLIST, f, ensure_ascii=False, indent=4)      
