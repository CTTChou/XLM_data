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
    1. 讀取 JSON 檔案並加載內容到 `ChiBibleLIST`。
    2. 逐層遍歷 `ChiBibleLIST` 中的書卷、章節及小節資料。
    3. 對每一小節的內容進行分割，根據正則表達式將句子按標點符號進行拆分。
    4. 返回處理後的資料結構 `processed_LIST`，該資料結構與原始資料格式相同，只是其中的句子已經被分割並清理過。    
    
    輸出：
    processed_LIST (list): 處理過斷句，放回原格式
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
    
    return processed_LIST

def to_segment_LIST(segment_folder):
    """
    從指定資料夾中的所有 JSON 檔案讀取資料，將其合併到一個列表中，並將合併後的資料寫入新的 JSON 檔案。

    參數:
    segment_folder (str): 包含 JSON 檔案的資料夾路徑。

    程式流程：
    1. 遍歷指定資料夾中的所有 `.json` 檔案。
    2. 對每個 JSON 檔案，將其內容讀取並追加到 `segment_LIST` 列表中。
    3. 最後，將合併後的資料寫入一個名為 `segment_all_ChiBible.json` 的檔案，並儲存在指定路徑中。
    
    輸出：
    - 一個新的 JSON 檔案 `segment_all_ChiBible.json`，包含了資料夾中所有 JSON 檔案合併後的內容。
    """    
    segment_LIST = []
    segment_jsonFILE = glob(f"{segment_folder}/*.json")
    for jsonFILE in segment_jsonFILE:
        with open(jsonFILE, "r", encoding="utf=8") as f:
            segment_LIST.extend(json.load(f))
            
    filename ="../../../data/Bible/Chinese/segment_all_ChiBible.json"        
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(segment_LIST, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    #分別處理每個 book
    book_folder = "../../../data/Bible/Chinese/book"
    jsonFILE_LIST = glob(f"{book_folder}/*.json")
    
    segment_folder = "../../../data/Bible/Chinese/segment"
    os.makedirs(segment_folder, exist_ok=True)  # 確保資料夾存在
    
    for jsonFILE in jsonFILE_LIST:
        with open(jsonFILE, "r", encoding="utf-8") as f:
            processed_LIST = main(jsonFILE)
            
            output_jsonFILE = os.path.join(segment_folder, os.path.basename(jsonFILE))
            with open(output_jsonFILE, "w", encoding="utf-8") as f:
                json.dump(processed_LIST, f, ensure_ascii=False, indent=4)
    
    #統整在一個 JSON            
    to_segment_LIST(segment_folder)