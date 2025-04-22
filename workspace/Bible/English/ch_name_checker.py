#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import re
from pprint import pprint

PerPAT = r"<ENTITY_person>(.+?)</ENTITY_person>"
LocPAT = r"<LOCATION>(.+?)</LOCATION>"

def main():
    """
    遍歷經POS處理過後的中文聖經，找到以ENTITY_person與LOCATION標記的人名、地名。
    """
    with open (jsonFILE, "r", encoding="utf-8") as f:
        dataLIST = json.load(f)     
    checkDICT ={}
    checkDICT["PERSON"] = []
    checkDICT["LOCATION"] = []
    
    for bookDICT in dataLIST:
        bookNameSTR = next(iter(bookDICT))   # 每次拿一個書名
        checkDICT["PERSON"].append(bookNameSTR)
        checkDICT["LOCATION"].append(bookNameSTR)
        
        for chapter_idx, chapterDICT in enumerate(bookDICT[bookNameSTR]):

            global chapterNums
            chapterNums = next(iter(chapterDICT))         #找到chapter
            versesLIST = chapterDICT[chapterNums]
            
            for verseDICT in versesLIST:
                global verseNums
                verseNums = (next(iter(verseDICT)))        #找到verse
                checkDICT["PERSON"].append(verseNums)
                checkDICT["LOCATION"].append(verseNums)
                
                for verseLIST in verseDICT[verseNums]:
                    for contentSTR in verseLIST:
                        
                        if re.search(PerPAT, contentSTR):             #依regex pattern找人名、地名
                            PerSTR = re.findall(PerPAT, contentSTR)
                            checkDICT["PERSON"].append(PerSTR)
                        elif re.search(LocPAT, contentSTR):
                            LocSTR = re.findall(LocPAT, contentSTR)
                            checkDICT["LOCATION"].append(LocSTR)
                        else:
                            checkDICT["PERSON"].append("--No names--")
                            checkDICT["LOCATION"].append("--No names--")
                        
        
    with open(f"../../../data/Bible/English/ChNamePOS_checklist", "w", encoding="utf-8") as f:
        json.dump(checkDICT, f, ensure_ascii=False, indent=4)       
        
    pprint(checkDICT)
    return checkDICT

if __name__ == "__main__":
    jsonFILE = f"../../../data/Bible/Chinese/lv2_POS_all_ChiBible.json"
    main()
    
    




