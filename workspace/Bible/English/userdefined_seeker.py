#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import re
from pprint import pprint

UserDictPAT = r"<UserDefined>(.+?)</UserDefined>"

def searchEngName():
    """
    遍歷經POS處理過後的英文聖經，找到以UserDefined標記的名詞。
    
    回傳：
        dictionary: 找到的所有以UserDefined標記的名詞，返回 EngcheckDICT 內容。
    """
    jsonFILE = f"./data/POS_all_EngBible.json"
    with open (jsonFILE, "r", encoding="utf-8") as f:
        dataLIST = json.load(f)     
    
    for bookDICT in dataLIST:
        bookNameSTR = next(iter(bookDICT))   # 每次拿一個書名
        EngcheckDICT[f"{bookNameSTR}"] = []
        EngVersesLIST = EngcheckDICT[f"{bookNameSTR}"]
        
        for chapter_idx, chapterDICT in enumerate(bookDICT[bookNameSTR]):

            global chapterNums
            chapterNums = next(iter(chapterDICT))        #找到chapter
            versesLIST = chapterDICT[chapterNums]
            
            for verseDICT in versesLIST:
                global verseNums
                verseNums = next(iter(verseDICT))        #找到verse
                EngVerseDICT = {}
                EngVersesLIST.append(EngVerseDICT)
                
                contentLIST = []
                for verseLIST in verseDICT[verseNums]:
                    if verseNums:
                        for contentSTR in verseLIST:
                        
                            if re.search(UserDictPAT, contentSTR):             #依regex pattern找UserDefined
                                udLIST = re.findall(UserDictPAT, contentSTR)
                            
                                for udSTR in udLIST:
                                    contentLIST.append(udSTR)
                                
                for i in range(len(verseDICT)):                                #每個verse找到的結果不重複加入EngcheckDICT
                    if verseNums[i+1] != verseNums[i]:
                        EngVerseDICT[f"{verseNums}"] = contentLIST 
        
    #pprint(EngcheckDICT)
    return EngcheckDICT

def searchChiName():
    """
    
    遍歷經POS處理過後的中文聖經，找到以UserDefined標記的名詞。

    回傳：
        dictionary: 找到的所有以UserDefined標記的名詞，返回 ChicheckDICT 內容。
    """
    jsonFILE = f"../../../data/Bible/English/lv2_POS_all_ChiBible_UDtag.json"
    with open (jsonFILE, "r", encoding="utf-8") as f:
        dataLIST = json.load(f)     
    
    
    for bookDICT in dataLIST:
        bookNameSTR = next(iter(bookDICT))   # 每次拿一個書名
        ChicheckDICT[f"{bookNameSTR}"] = []
        ChiVersesLIST = ChicheckDICT[f"{bookNameSTR}"]
        
        for chapter_idx, chapterDICT in enumerate(bookDICT[bookNameSTR]):

            global chapterNums
            chapterNums = next(iter(chapterDICT))        #找到chapter
            versesLIST = chapterDICT[chapterNums]
            
            for verseDICT in versesLIST:
                global verseNums
                verseNums = next(iter(verseDICT))        #找到verse
                ChiVerseDICT = {}
                ChiVersesLIST.append(ChiVerseDICT)
                
                contentLIST = []
                for verseLIST in verseDICT[verseNums]:
                    if verseNums:
                        for contentSTR in verseLIST:
                        
                            if re.search(UserDictPAT, contentSTR):             #依regex pattern找UserDefined
                                udLIST = re.findall(UserDictPAT, contentSTR)
                                
                                for udSTR in udLIST:
                                    contentLIST.append(udSTR)
                                
                for i in range(len(verseDICT)):                                #每個verse找到的結果不重複加入EngcheckDICT
                    if verseNums[i+1] != verseNums[i]:
                        ChiVerseDICT[f"{verseNums}"] = contentLIST 
        
    #pprint(ChicheckDICT)
    return ChicheckDICT

def comapareUD():
    """
    比較中英聖經每個verse找到的UserDefined數量是否相同。

    回傳：
        dictionary: 中英文UserDefined數量不一致的verse，返回CompareLIST內容。
    """
    
    global bookname, chbookname, EngVNum, ChVNum
    
    for bookname in EngcheckDICT:                         #找英文checkDICT的key(bookname)
        EngVsLIST = EngcheckDICT[f"{bookname}"]
        for chbookname in ChicheckDICT:                   #找中文checkDICT的key(chbookname)
            ChVsLIST = ChicheckDICT[f"{chbookname}"]
            if bookname == chbookname:
                for evDICT in EngVsLIST:                  #找英文checkDICT的key(verse)
                    for chvDICT in ChVsLIST:              #找中文checkDICT的key(verse)
                        #if chvDICT == {} and evDICT == {}:
                            #EngVNum = evDICT.keys()
                            #print(f"Skipped!!{bookname}-{EngVNum}--{evDICT} vs. {chvDICT}")
                        #elif evDICT == {}:
                            #pass
                        #elif chvDICT == {}:
                            #pass
                        if chvDICT == {} or evDICT == {}:
                            pass
                        else:
                            EngVNum = list(evDICT.keys())[0]
                            ChVNum = list(chvDICT.keys())[0]

                            if EngVNum == ChVNum:         #確認在同個verse
                                #print("here!!")
                                if len(evDICT[f"{EngVNum}"]) != len(chvDICT[f"{ChVNum}"]):    #比較中英文每個verse中UserDefined個數是否相同
                                    CompareLIST.append(f"{bookname}--{evDICT} vs. {chvDICT}")
    pprint(CompareLIST)
    return CompareLIST


def main():
    
    searchEngName()
    searchChiName()
    comapareUD()
    
    return None


if __name__ == "__main__":
    
    EngcheckDICT ={}
    ChicheckDICT ={}    
    CompareLIST = []
    main()
    
    with open(f"../../../data/Bible/English/names/POSCheckList.json", "w", encoding="utf-8") as f:
        json.dump(CompareLIST, f, ensure_ascii=False, indent=4)
    
    #with open(f"./data/EngPOSCheckList.json", "w", encoding="utf-8") as f:
        #json.dump(EngcheckDICT, f, ensure_ascii=False, indent=4)     

    #with open(f"./data/ChPOSCheckList.json", "w", encoding="utf-8") as f:
        #json.dump(ChicheckDICT, f, ensure_ascii=False, indent=4) 
