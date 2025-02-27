#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import re

def main(jsonFILE, secPat):
    """
    從 JSON 檔案中讀取聖經數據，檢查每一章的經文是否有缺失的小節。

    參數:
        jsonFILE (str): JSON 檔案的路徑，包含所有聖經書卷的資料。
        secPat (str): 正則表達式，用來從經文標題中提取節數。

    輸出:
        會列印出缺失節數的經文書名、章號。
    """

    with open(jsonFILE, "r", encoding="utf-8") as f:
        dataLIST = json.load(f)
    
    for bookDICT in dataLIST:
        booknameSTR = next(iter(bookDICT))  # 每次拿一個書名
        
        for ch_idx, chapterDICT in enumerate(bookDICT[booknameSTR]):
            versesLIST = list(chapterDICT.values())[0]  # 取得 values 的第一個元素（列表）
            
            checkLIST = []
            for verseDICT in versesLIST:
                verseNum_s = list(verseDICT.keys())[0]  #verse 小節
                existingNum_LIST = re.findall(secPat, verseNum_s)   #已成功抓到的小節 e.g. "1:2" 的 "2"
                checkLIST.append(int(existingNum_LIST[0]))          #已有的小節放入 checkLIST
            
            if checkLIST and checkLIST[len(checkLIST)-1] != len(checkLIST):
                missingLIST = [n for n in range(1, checkLIST[len(checkLIST)-1]) if n not in checkLIST]
                print(booknameSTR, list(chapterDICT.keys())[0], checkLIST, "有大問題", f"缺{missingLIST}", )
                    

if __name__ == "__main__":
    jsonFILE = f"../../../data/Bible/English/all_EngBible.json"
    secPat = re.compile(r":(.*)")    
    main(jsonFILE, secPat)