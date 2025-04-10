#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import re
from pprint import pprint

splitPAT = re.compile(r"\sor\s|\，\s|\s\(")

#def main(personsDICT, processLIST):
def main(placesDICT, processLIST):
    """
    將同個string中包含兩個以上名字的stirng切開，並處理字典中多餘標點符號。
    
    """
    
    processLIST = []
    
    #for nameSTR in personsDICT["ENTITY_person"]:
    for nameSTR in placesDICT["LOCATION"]:
        split_namesSTR = re.split(splitPAT, nameSTR)     #將名字切開為獨立string
        nameSTR = re.sub(r"\)", "", nameSTR)         
        processLIST.extend([s.strip() for s in split_namesSTR if s.strip()])
    
    #personsDICT["ENTITY_person"] = processLIST           #更新原始檔案
    #pprint(personsDICT["ENTITY_person"])
    placesDICT["LOCATION"] = processLIST           #更新原始檔案
    pprint(placesDICT["LOCATION"])    
    
    with open(jsonFILE, "w", encoding="utf-8") as f:
        #personsDICT = json.dump(personsDICT, f, ensure_ascii=False, indent=4)
        placesDICT = json.dump(placesDICT, f, ensure_ascii=False, indent=4)
    
    #return personsDICT
    return placesDICT

if __name__ == "__main__":
    #jsonFILE = "../../../data/Bible/English/names/persons.json"
    jsonFILE = "../../../data/Bible/English/names/places.json"
    
    with open(jsonFILE, "r", encoding="utf-8") as f:
        #personsDICT = json.load(f)
        #personsDICT = main(personsDICT, jsonFILE)
        placesDICT = json.load(f)
        placesDICT = main(placesDICT, jsonFILE)        
     





