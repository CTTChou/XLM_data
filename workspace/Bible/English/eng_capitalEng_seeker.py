#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import re
from pprint import pprint

CapitalPAT = r"\b[A-Z][a-z]+\b"
deleteLIST = ["God", "Lord", "I", "You", "He", "She", "It", "We", "They", "Our", "Ours", "Your","Yours", "Their","My", "His", "Her", "All", "Everyone", "With", "Also", "Again", "Once", "One", "Two", "Three", "Some", "Day", "Night", "Evening", 
              "This", "That", "These", "Those", "There", "The", "Then","Even", "Now", "Before", "After", "And", "Or", "But", "So", "To", "From", "Of", "For", "As", "At", "Are", "Am", "Is", "Among", "Between", "Yes", "No", "Each", "Every", "Everything", "Something", "Nothing", 
              "Do", "Does", "Did", "Have", "Has", "Had", "Can", "May", "Will", "What", "Where", "When","Why", "Who","Which", "How", "In", "On","Since", "During", "By","If", "Please", "Let", "New", "Next", "Whenever", "Whoever", "Until", "Still", "Though", "While", "Most", 
              "Make", "Go", "Come", "Look", "Listen", "Give"]

def main():
    """
    讀取JSON格式英文數據，找大寫英文並到字母開頭的單字。
    """
    with open (jsonFILE, "r", encoding="utf-8") as f:
        dataLIST = json.load(f)     
    checkLIST = []
    
    for bookDICT in dataLIST:
        bookNameSTR = next(iter(bookDICT))   # 每次拿一個書名
        
        for chapter_idx, chapterDICT in enumerate(bookDICT[bookNameSTR]):

            global chapterNums
            chapterNums = next(iter(chapterDICT))         #找到chapter
            versesLIST = chapterDICT[chapterNums]
            
            for verseDICT in versesLIST:
                global verseNums
                verseNums = str(next(iter(verseDICT)))        #找到verse

                for contentSTR in verseDICT.values():
                        
                    if re.search(CapitalPAT, contentSTR):             #依regex pattern找所有大寫字
                        CapitalLIST = re.findall(CapitalPAT, contentSTR)
                        for CapitalSTR in CapitalLIST:
                            resultDICT = {}
                            if CapitalSTR not in deleteLIST:          #如果CapitalSTR是在deleteLIST裡的詞就不加入字典
                            #print(f"{bookNameSTR}<{verseNums}>", CapitalSTR)                                
                                resultDICT[f"{bookNameSTR}<{verseNums}>"] = CapitalSTR
                                capitalLIST = []
                                capitalLIST.append(CapitalSTR)
                                if resultDICT == None:
                                    del resultDICT
                                else:
                                    checkLIST.append(resultDICT)
                            print(resultDICT)                        #{"Genesis<2:8>": "Eden"}
                            
    with open(f"../../../data/Bible/English/names/EngCapital_checklist.json", "w", encoding="utf-8") as f:
        json.dump(checkLIST, f, ensure_ascii=False, indent=4)       
        
    pprint(checkLIST)
    return checkLIST, capitalLIST


if __name__ == "__main__":
    jsonFILE = f"../../../data/Bible/English/all_EngBible.json"
    main()
    
    personDictFILE = f"../../../data/Bible/English/names/persons.json"
    with open(personDictFILE, "r", encoding="utf-8") as f:
        personDICT = json.load(f)
        
    placeDictFILE = f"../../../data/Bible/English/names/places.json"
    with open(placeDictFILE, "r", encoding="utf-8") as f:
        placeDICT = json.load(f)
    
    nameLIST = []
    nameLIST.append(personDICT["ENTITY_person"])
    nameLIST.append(placeDICT["LOCATION"])
    
    #for CapitalSTR in CapitalLIST:
    
