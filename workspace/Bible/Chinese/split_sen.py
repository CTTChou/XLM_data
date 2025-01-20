#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re

def main(jsonFILE):
    """
    從指定的 JSON 檔案讀取聖經內容，將經文按標點符號（如：問號、逗號等）進行分割，並將結果寫回同一個 JSON 檔案。

    參數:
    jsonFILE (str): 包含聖經資料的 JSON 檔案路徑。

    程式流程：
    1. 讀取 JSON 檔案並加載內容到 `ChiBibleLIST`。
    2. 逐層遍歷 `ChiBibleLIST` 中的書卷、章節及小節資料。
    3. 對每一小節的內容進行分割，根據正則表達式將句子按標點符號進行拆分。
    4. 將拆分後的句子清除前後空格後，存儲到新的結構中。
    5. 最後將處理過的資料寫入新的 JSON 檔案，保存在指定資料夾。
    
    輸出：
    - 處理後的經文資料會寫入新的 JSON 檔案，並存儲於指定的資料夾中。
    """
    with open (jsonFILE, "r", encoding="utf-8") as f:
        ChiBibleLIST = json.load(f)
    processed_LIST = []
    for bookDICT in ChiBibleLIST:
        processed_bookDICT = {}
        
        for bookSTR, chLIST in bookDICT.items():
            processed_chLIST = []
            
            for chDICT in chLIST:
                processed_chDICT = {}
                
                for chSTR, secLIST in chDICT.items():
                    processed_secLIST = []
                    
                    for secDICT in secLIST:
                        processed_secDICT = {}
                        
                        for secSTR, senSTR in secDICT.items():
                            split_senLIST = []
                            print(senSTR)                        
                            split_senLIST = [s.strip() for s in re.split(r"[？！。，；：、「」『』（）─]", senSTR) if s ]
                            print(split_senLIST)                            
                    
                            processed_secDICT[secSTR] = split_senLIST
                        processed_secLIST.append(processed_secDICT)
                    processed_chDICT[chSTR] = processed_secLIST
                processed_chLIST.append(processed_chDICT)
            processed_bookDICT[bookSTR] = processed_chLIST
        processed_LIST.append(processed_bookDICT)
    
    segment_folder = "../../../data/Bible/Chinese/segment"
    os.makedirs(segment_folder, exist_ok=True)  # 確保資料夾存在
    output_jsonFILE = "../../../data/Bible/Chinese/segment/創.json"
    with open(output_jsonFILE, "w", encoding="utf-8") as f:
        json.dump(processed_LIST, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    jsonFILE = "../../../data/Bible/Chinese/book/創.json"    
    main(jsonFILE)