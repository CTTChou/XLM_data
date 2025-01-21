#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
from ArticutAPI import Articut

def main(jsonFILE):
    """
    從指定的 JSON 檔案讀取聖經內容，將經文按標點符號（如：問號、逗號等）進行分割，並將結果寫回同一個 JSON 檔案。

    參數:
    jsonFILE (str): 包含聖經資料的 JSON 檔案路徑。

    程式流程：
    1. 讀取 JSON 檔案並加載內容到 `EngBibleLIST`。
    2. 逐層遍歷 `EngBibleLIST` 中的書卷、章節及小節資料。
    3. 對每一小節的內容進行分割，根據正則表達式將句子按標點符號進行拆分。
    4. 將拆分後的句子清除前後空格後，存儲到新的結構中。
    5. 最後將處理過的資料寫入新的 JSON 檔案，保存在指定資料夾。
    
    輸出：
    - 處理後的經文資料會寫入新的 JSON 檔案，並存儲於指定的資料夾中。
    """
    with open (jsonFILE, "r", encoding="utf-8") as f:
        EngBibleLIST = json.load(f)
    processed_LIST = []
    for bookDICT in EngBibleLIST:
        processed_bookDICT = {}
        
        for bookSTR, enLIST in bookDICT.items():
            processed_enLIST = []
            
            for enDICT in enLIST:
                processed_enDICT = {}
                
                for enSTR, secLIST in enDICT.items():
                    processed_secLIST = []
                    
                    for secDICT in secLIST:
                        processed_secDICT = {}
                        
                        for secSTR, senSTR in secDICT.items():
                            split_senLIST = []
                            print(senSTR)                        
                            split_senLIST = [s.strip() for s in re.split(r"[?!.,;;、""()-]", senSTR) if s ]
                            print(split_senLIST)
                    
                            processed_secDICT[secSTR] = split_senLIST
                        processed_secLIST.append(processed_secDICT)
                    processed_enDICT[enSTR] = processed_secLIST
                processed_enLIST.append(processed_enDICT)
            processed_bookDICT[bookSTR] = processed_enLIST
        processed_LIST.append(processed_bookDICT)
    
    segment_folder = "../../../data/Bible/English/segment"
    os.makedirs(segment_folder, exist_ok=True)  # 確保資料夾存在
    output_jsonFILE = "../../../data/Bible/English/segment/genesis.json"
    with open(output_jsonFILE, "w", encoding="utf-8") as f:
        json.dump(processed_LIST, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    accountDICT = json.load(open("account.info",encoding="utf-8"))
    articut = Articut(username=accountDICT["username"],apikey=accountDICT["api_key"])
    
    jsonFILE = "../../../data/Bible/English/book/genesis.json"    
    main(jsonFILE)