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
        pattern_start = r'(\d+)\xa0'
        match = re.findall(pattern_start, j)
        print(match[0])
        lineLIST.append(match[0])
        outputLIST[i] = re.sub(r'\d+\xa0|\[\w\]|\(\w\)|\(|\)|\“|\‘|\’|\”|\s$', "", j)
    lineLIST[0] = "1"   
      
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
    resultLIST.append(sentenceDICT)
    print(resultLIST)
    
    return resultLIST


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
        chapterIntLIST = [int(m.getText()) for m in nums]    #取得每一卷的章節數量
        for i, count in enumerate(chapterIntLIST): 
            for j in range(count):                
                try:
                    url = f"https://www.biblegateway.com/passage/?search={n}%20{j}&version=GNT"
                    resultLIST.append(main(url, j))
                    print(resultDICT)            
                except Exception:
                   pass                
        #for j in range(1,151):           #還可以加上怎麼找有幾個章節的部分
            #try:
                #url = f"https://www.biblegateway.com/passage/?search={n}%20{j}&version=GNT"
                #resultLIST.append(main(url, j))
                #print(resultDICT)            
            #except Exception:
                #pass
        resultDICT = {}
        resultDICT[n] = resultLIST

        with open("../../../data/Bible/English/book/genesis.json", "r", encoding="utf-8") as f:
            dataLIST = json.load(f)
            dataLIST.append(resultDICT)        
        with open("../../../data/Bible/English/book/genesis.json", "w", encoding="utf-8") as f:
            json.dump(dataLIST, f, ensure_ascii=False, indent=4)      
