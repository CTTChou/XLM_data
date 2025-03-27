#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from glob import glob
from pprint import pprint

def replace_tag(d, tag, name):
    """遞迴替換 JSON 結構中的 <UserDefined> 標籤"""
    
    if isinstance(d, dict):
        return {k: replace_tag(v, tag, name) for k, v in d.items()}
    
    elif isinstance(d, list):
        return [replace_tag(item, tag, name) for item in d]
    
    elif isinstance(d, str) and "<UserDefined>" in d:
        return d.replace(f"<UserDefined>{name}</UserDefined>", f"<{tag}>{name}</{tag}>")

def main(jsonFILE, userDefined):
    """處理單個 JSON 檔案"""
    
    with open(jsonFILE, "r", encoding="utf-8") as f:
        ChiBibleLIST = json.load(f)
    
    with open(userDefined, "r", encoding="utf-8") as f:
        userDefinedDICT = json.load(f)
    
    pprint(f"{jsonFILE} 標籤替換中...")
    
    #遍歷所有標籤和對應的名稱
    for tag, nameLIST in userDefinedDICT.items():   #tag= "_asPerson"
        for name in nameLIST:
            ChiBibleLIST = replace_tag(ChiBibleLIST, tag, name)
          
    #完成處理後，寫回 JSON
    with open(jsonFILE, "w", encoding="utf-8") as f:
        json.dump(ChiBibleLIST, f, ensure_ascii=False, indent=4)            
        pprint(ChiBibleLIST[:2])    #只印出處理檔案的前兩個元素看一下
        
    pprint(f"{jsonFILE} tag changed")
      
    return None


if __name__ == "__main__":
    userDefined = "../../../data/Bible/Chinese/names/fhl_names.json"    
    
    folderLIST = ["../../../data/Bible/Chinese/POS", "../../../data/Bible/Chinese/lv2_POS"]
    for folder in folderLIST:
        jsonFILE_LIST = glob(f"{folder}/*.json")
        for jsonFILE in jsonFILE_LIST:
            main(jsonFILE, userDefined)        