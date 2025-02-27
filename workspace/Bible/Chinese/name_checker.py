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
    with open("../../../data/Bible/Chinese/chinese_persons.json", "r", encoding="utf-8") as f:    
        nameLIST = json.load(f)
        print(f"可檢查的人名數量：{len(nameLIST)}")
        
        not_haveLIST = []
        for name in nameLIST:
            if name not in versesSTR:   #比對 chinese_persons.json 裡的人名是否在 all_ChiBible.json
                not_haveLIST.append(name)  #不需要的人名 
        print(f"不需要的人名數量：{len(not_haveLIST)}")
        pprint(not_haveLIST)