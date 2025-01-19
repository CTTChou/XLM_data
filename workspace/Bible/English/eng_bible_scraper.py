#!/user/bin/env python
# -*- coding: utf-8 -*-


from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
import re


def find_lines(html_doc):
    pattern_start = r'id="[^"]*-([0-9]+)"'
    match_start = re.findall(pattern_start, html_doc)
    end_line_num = int(match_start[0]) + len(match_start) -1
    return match_start[0], end_line_num
    
    
def search(htmlSTR, chapter):
    """
    Searches the specified chapter in the htmlSTR by obtaining the starting and ending lines and returns the result list.
    
    Parameters:
        htmlSTR (str): The HTML string.
        chapter (int): The specified chapter.
    
    Returns:
        list: The list of searched content.
    """
    outputLIST = []
    lineLIST = []
    start_line = find_lines(htmlSTR)[0]         #calls the find_lines(html_doc) function to get starting and ending lines.
    end_line = find_lines(htmlSTR)[1]
    htmlSTR = re.sub(r'<h3[^>]*>.*?</h3>', "", htmlSTR)
    soup = BeautifulSoup(htmlSTR, "lxml")
    
    first_line = soup.find_all('span', class_= f"text Gen-{chapter}-1")  
    for l in first_line:
        tempSTR = l.get_text()
        tempSTR = re.sub("\[\w\]|\(\w\)|^(\d|-|\)){1,5}\s", "", tempSTR)
        outputLIST.append(tempSTR)
        lineLIST.append(1)
    for start_line in range(end_line+1):
        result = soup.find_all('span', id= f"en-GNT-{start_line}")  
        for k in result:
            tempSTR = k.get_text()
            pattern = r'(\d+-\d+|\d+)'
            line = re.findall(pattern, tempSTR)   
            tempSTR2 = re.sub("\[\w\]|\(\w\)|^(\d|-|\)){1,5}\s", "", tempSTR)
            outputLIST.append(tempSTR2)
            lineLIST.append(line[0])
    '''for j in outputLIST:
        if chapter < 10:
            outputLIST[outputLIST.index(j)] = re.sub("\[\w\]|\(\w\)|^..", "", j)   
        else:
            outputLIST[outputLIST.index(j)] = re.sub("\[\w\]|\(\w\)|^...", "", j)  '''    
    return outputLIST, lineLIST


def main(url, chapter_num): 
    """
    Fetches a web page from the provided URL, extracts content, 
    calls the search() function to obtain content of the specified chapter, and returns the result dictionary.
    
    Parameters:
        url (str): The input url string.
        chapter_num (int): The specified Bible chapter.
    
    Returns:
        dict: A dictionary with the following keys:
            - "Genesis": The book of the extracted content.
            - "Chapter": A list of dictionaries containing the chapter content.
    """
    response = requests.get(url)
    html_doc = response.text
    if f"text Gen-{chapter_num}-1" in str(html_doc):
        print(f"text Gen-{chapter_num}-1")    

    engLIST = search(html_doc, chapter_num)[0]
    lineLIST = search(html_doc, chapter_num)[1]
    
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
    resultLIST = []
    for i in range(1,51):           #還需加上怎麼找有幾個章節的部分
        try:
            url = f"https://www.biblegateway.com/passage/?search=Genesis%20{i}&version=GNT"
            resultLIST.append(main(url, i))
            print(resultDICT)            
        except Exception:
            pass
    resultDICT = {}
    dataLIST = []
    resultDICT["Genesis"] = resultLIST
    dataLIST.append(resultDICT)
    with open("../../../data/Bible/English/book/genesis.json", "w", encoding="utf-8") as f:
        json.dump(dataLIST, f, ensure_ascii=False, indent=4)      
