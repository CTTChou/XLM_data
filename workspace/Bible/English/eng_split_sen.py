#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
from glob import glob

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
    -回傳processed_LIST(list)
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
                            split_senLIST = [s.strip() for s in re.split(r"[?!.,:;、""()-]", senSTR) if s ]
                            print(split_senLIST)
                    
                            processed_secDICT[secSTR] = split_senLIST
                        processed_secLIST.append(processed_secDICT)
                    processed_enDICT[enSTR] = processed_secLIST
                processed_enLIST.append(processed_enDICT)
            processed_bookDICT[bookSTR] = processed_enLIST
        processed_LIST.append(processed_bookDICT)
    
    return processed_LIST
    
def to_segment_LIST(segment_folder):
    """
    從指定資料夾中的所有 JSON 檔案讀取資料，將其合併到一個列表中，並將合併後的資料寫入新的 JSON 檔案。

    參數:
    segment_folder (str): 包含 JSON 檔案的資料夾路徑。

    程式流程：
    1. 遍歷指定資料夾中的所有 `.json` 檔案。
    2. 對每個 JSON 檔案，將其內容讀取並追加到 `segment_LIST` 列表中。
    3. 最後，將合併後的資料寫入一個名為 `segment_all_English.json` 的檔案，並儲存在指定路徑中。
    
    輸出：
    - 一個新的 JSON 檔案 `segment_all_English.json`，包含了資料夾中所有 JSON 檔案合併後的內容。
    """    
    segment_LIST = []
    segment_jsonFILE = glob(f"{segment_folder}/*.json")
    for jsonFILE in segment_jsonFILE:
        with open(jsonFILE, "r", encoding="utf=8") as f:
            segment_LIST.extend(json.load(f))
            
    filename ="../../../data/Bible/English/segment_all_EngBible.json"        
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(segment_LIST, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    book_folder = "../../../data/Bible/English/book"
    segment_folder = "../../../data/Bible/English/segment"
    os.makedirs(segment_folder, exist_ok=True)
    for json_file in os.listdir(book_folder):
        jsonFILE = os.path.join(book_folder, json_file)
        if os.path.isfile:
            with open(jsonFILE, "r", encoding="utf-8") as f:
                processed_LIST = main(jsonFILE)
                output_jsonFILE = os.path.join(segment_folder, os.path.basename(jsonFILE))
                with open(output_jsonFILE, "w", encoding="utf-8") as f:
                    json.dump(processed_LIST, f, ensure_ascii=False, indent=4)            
    
    #統整在一個 JSON            
    to_segment_LIST(segment_folder)
    