#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from pprint import pprint

def replace_tag(d, tag, name):
    if isinstance(d, dict):
        return {k: replace_tag(v, tag, name) for k, v in d.items()}
    
    elif isinstance(d, list):
        return [replace_tag(item, tag, name) for item in d]
    
    elif isinstance(d, str):
        return d.replace(f"<UserDefined>{name}</UserDefined>", f"<{tag}>{name}</{tag}>")

def main():
    """"""
    with open(jsonFile, "r", encoding="utf-8") as f:
        ChiBibleLIST = json.load(f)
    
    with open(userDefined, "r", encoding="utf-8") as f:
        userDefinedDICT = json.load(f)
    
    #對每個tag進行處理
    pprint(f"tag changing")    
    for tag in userDefinedDICT.keys():  #tag= "_asPerson"
        for name in userDefinedDICT[tag]:
            #在 ChiBibleLIST 中進行標籤替換
            ChiBibleLIST = replace_tag(ChiBibleLIST, tag, name)
    pprint(f"tag changed")
          
    #完成處理後，寫回更新過的資料
    with open(jsonFile, "w", encoding="utf-8") as f:
        json.dump(ChiBibleLIST, f, ensure_ascii=False, indent=4)            
        pprint(ChiBibleLIST)
        
    return None


if __name__ == "__main__":
    jsonFile = "../../../data/Bible/Chinese/POS/創.json"
    userDefined = "../../../data/Bible/Chinese/names/fhl_names.json"
    main()
        