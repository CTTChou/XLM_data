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
        if i[0].isdigit(): 
            outputLIST.append(i)
        else:
            if len(outputLIST) !=0:
                outputLIST[-1] += " "
                outputLIST[-1] += i
    
    lineLIST = []
    for i, j in enumerate(outputLIST):
        outputLIST[i] = re.sub(r"(\xa0)|\[\w\]|\(\w\)|\(|\)|\“|\‘|\’|\”|\s$", "", j)
        pattern_start = r"^(\d+-\d+)|^(\d+)"
        match = re.findall(pattern_start, j)
        print(match)
        if match[0][0] != "":
            lineLIST.append(match[0][0])
        else:
            lineLIST.append(match[0][1])
        outputLIST[i] = re.sub(r"^(\d+)", "", outputLIST[i])
        outputLIST[i] = re.sub(r"^(\-\d+)", "", outputLIST[i])
    lineLIST[0] = "1"
    
    for i, j in enumerate(lineLIST):
        if "-" in lineLIST[i]:
            pattern1 = r'(\d+)\-\d+'
            pattern2 = r'\d+\-(\d+)'
            num1 = re.findall(pattern1, j)    
            num2 = re.findall(pattern2, j)
            lineLIST[i] = num1[0]
            lineLIST.insert(i+1, num2[0])
            outputLIST.insert(i+1, outputLIST[i])
            n = int(num2[0])-int(num1[0])
            if n > 1:
                for m in range(n-1):
                    lineLIST.insert(i+1, str(int(num1[0])+n-m-1))
                    outputLIST.insert(i+1, outputLIST[i])
    
    footnotes_div = soup.find('div', class_="footnotes")
    try:
        ft = footnotes_div.find_all('span')  
        for i in ft:
            footnotes = i.get_text()
            ft_pattern = r'verse\s(\d+):\s(.*)'
            ft_result = re.findall(ft_pattern, footnotes)
            if ft_result != []:
                print("ft_result:", ft_result)
                if ft_result[0][0] not in lineLIST:
                    lineLIST.insert(int(ft_result[0][0])-1, ft_result[0][0])
                    outputLIST.insert(int(ft_result[0][0])-1, ft_result[0][1])
    except Exception:
        pass
    #print(len(lineLIST), lineLIST)
    #print(len(outputLIST), outputLIST)
    return outputLIST, lineLIST

##########################here#######################
#catch versenum & verse contents
url_Ezra6 = "https://www.biblegateway.com/passage/?search=Ezra%206&version=GNT" #Ezra6

response = requests.get(url_Ezra6)
html = response.text
soup = BeautifulSoup(html, "lxml")

resultDICT = {}

verse_spans_text = soup.find_all("span", class_=re.compile(r"text"))
verse_spans_poetry = soup.find_all("span", class_=re.compile(r"poetry"))

for span in verse_spans_text:
    # 提取章節-經文號碼 (來自 <sup class="versenum"> 或其他文本)
    sup = span.find("sup", class_="versenum")
    
    if sup :       
        chapter_verse = sup.get_text(strip=True)
        text = span.get_text(strip=True)
        if sup:
            text = text.replace(sup.get_text(strip=True), "")
        
        resultDICT[chapter_verse] = text
#####################################################


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
    
    bookLIST = []                                                                       # find list of all books
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
    
    for n in bookLIST:                                                                  # loop through all books
        resultLIST = []
        
        temp_n = n                                                     
        if n[0].isdigit():                                                             # for special book names (e.g. 1 Samuel)
            temp_n = re.sub(r'^\d+', lambda m: m.group(0) + '%20', n)
        if " " in n:
            temp_n = re.sub(r"\s", "%20", n)   
        if temp_n == "SongofSolomon":
            temp_n = "Song%20of%20Solomon"        
            
        pattern_start = r'\/passage\/\?search='+temp_n+r'%20(\d+)&amp;version=GNT'      # find all chapters
        chapter_match = re.findall(pattern_start, str(html))
        print(chapter_match)
   
        for m in chapter_match:
            try:
                url = f"https://www.biblegateway.com/passage/?search={temp_n}%20{m}&version=GNT"
                resultLIST.append(main(url, m))
                print(resultLIST)      
            except Exception as e:
                print(e)
                pass
        
        resultDICT = {}
        resultDICT[n] = resultLIST

        with open("../../../data/Bible/English/all_EngBible.json", "r", encoding="utf-8") as f:
            dataLIST = json.load(f)
            dataLIST.append(resultDICT)        
        with open("../../../data/Bible/English/all_EngBible.json", "w", encoding="utf-8") as f:
            json.dump(dataLIST, f, ensure_ascii=False, indent=4)      
