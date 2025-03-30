#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from pprint import pprint

def main(jsonFILE):
    """
    讀取 JSON 格式的英文聖經數據，並提取所有經文內容。
    
    此函式會執行以下步驟：
    1. 從指定路徑 ("../../../data/Bible/Chinese/all_ChiBible.json") 讀取 JSON 數據。
    2. 遍歷 JSON 數據結構，提取每卷書的所有經文。
    3. 將經文內容存入列表 `all_versesLIST`，並返回該列表。

    參數:
    jsonFILE (str): JSON 檔案的路徑，包含所有聖經書卷的資料。

    回傳:
        list: 包含所有經文內容的列表，每個元素為一節經文的文字內容。
    """   
    with open(jsonFILE, "r", encoding="utf-8") as f:            
        dataLIST = json.load(f)     
    all_versesLIST =[]
    for bookDICT in dataLIST:
        booknameSTR = next(iter(bookDICT))  # 每次拿一個書名
        for ch_idx, chapterDICT in enumerate(bookDICT[booknameSTR]):
            versesLIST = list(chapterDICT.values())[0]  # 取得 values 的第一個元素（列表）
            for verseDICT in versesLIST:
                all_versesLIST.append(next(iter(verseDICT.values())))  # 加入 verse 內文
        #pprint(all_versesLIST)
    return all_versesLIST


if __name__ == "__main__":
    jsonFILE = f"../../../data/Bible/Chinese/all_ChiBible.json"
    all_versesLIST = main(jsonFILE)
    
    versesSTR = " ".join(all_versesLIST) #把所有內文接在一起
    
    with open("../../../data/Bible/Chinese/names/places.json", "r", encoding="utf-8") as f:    
    #with open("../../../data/Bible/Chinese/names/persons.json", "r", encoding="utf-8") as f:        
        comparedDICT = json.load(f)
        comparedLIST = list(comparedDICT.values())[0]
        
    
    #定義 noun 可能的後綴詞
    #suffixLIST = ["人", "王"]  
            
    # 定義 location 可能的後綴詞
    suffixLIST = ["鎮", "城", "河", "海", "山", "山脈", "平原", "谷"]
    
    # 儲存匹配到的地名
    havingLIST = []
    
    # 遍歷所有地名，檢查是否匹配聖經經文
    for nameSTR in comparedLIST:
        for suffixSTR in suffixLIST:
            #如果 "地名"+"人" 也在 all_ChiBible.json，將 "xxx人" 放入 ENTITY_noun
            combinedSTR = nameSTR + suffixSTR
            if combinedSTR in versesSTR:
                havingLIST.append(combinedSTR)
    
    print(f"和 all_ChiBible.json 的重疊數量：{len(havingLIST)}")
    pprint(havingLIST)


    overlapLIST = []
    with open("../../../data/Bible/Chinese/names/fhl_names.json", "r", encoding="utf-8") as f:
        fhlDICT = json.load(f)
        fhlLIST = list(fhlDICT.values())[0]
        #如果 places.json 裡的也在 fhl_names.json
        overlapLIST = [nameSTR for nameSTR in comparedLIST if nameSTR in fhlLIST]
    #pprint(overlapLIST)
    pprint(f"和 fhl_names.json 的重疊數量：{len(overlapLIST)}")
    
    with open("../../../data/Bible/Chinese/UserDefinedFile.json", "r", encoding="utf-8") as f:
        userdefinedDICT = json.load(f)
        locLIST = userdefinedDICT["LOCATION"]
        perLIST = userdefinedDICT["ENTITY_person"]
        nounLIST = userdefinedDICT["ENTITY_noun"]

    #for nameSTR in overlapLIST:
        #if nameSTR not in locLIST:
            #locLIST.append(nameSTR)
    #pprint(locLIST)
    
    #for nameSTR in overlapLIST:
        #if nameSTR not in perLIST:
            #perLIST.append(nameSTR)
    #pprint(perLIST)    
    
    #for peopleSTR in havingLIST:
    #if peopleSTR not in nounLIST:  #如果 noun 還不存在於 UserDefinedFile.json 就添加
            #nounLIST.append(peopleSTR)
            
    for nameSTR in havingLIST:
        if nameSTR not in locLIST:  #如果 location 還不存在於 UserDefinedFile.json 就添加
            locLIST.append(nameSTR)    
    
    with open("../../../data/Bible/Chinese/UserDefinedFile.json", "w", encoding="utf-8") as f:
        json.dump(userdefinedDICT, f, ensure_ascii=False, indent=4)