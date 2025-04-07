#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
from glob import glob
from pprint import pprint

delPAT = re.compile(r"\([^()]*?（見.?\d+）.*?\)|\([^()]*?\)|（(?:[^\d（）]+?\d+:\d+(?:-?\d*)?)+(?:-\d+(?:,\d+)+:?-?\d+)?）|（\d+:\d+-\d+:\d+）|（.\d+:\d+-\d+,\d+-\d+）|（..\d+）|（（[^（）]*?(?:從前叫|希伯來文)）")   #刪除的內容
re_delPAT = re.compile(r"\d+-|[\u4e00-\u9fff]+\d+|\d+|22節由本章末段移到此段|詩篇四十二～七十二篇|詩篇七十三～八十九篇|詩篇九十～一零六篇|詩篇一零七～一五零篇|第五卷")    #刪除的內容
zeroPAT = re.compile(r"○")  #改成國字「零」
splitPAT = re.compile(r"[？！!。，；：、「」『』（）()─〕……]")  #斷句符號

def main(jsonFILE):
    """
    從指定的 JSON 檔案讀取聖經內容，將經文按標點符號（如：問號、逗號等）進行分割，並將結果寫回同一個 JSON 檔案。

    參數:
    jsonFILE (str): 包含聖經資料的 JSON 檔案路徑。

    程式流程：
    1. 讀取 JSON 檔案並加載內容到 `ChiBibleLIST`。
    2. 對每一小節的內容進行分割，根據正則表達式將句子按標點符號進行拆分。
    3. 返回處理後的資料結構 `ChiBibleLIST`，該資料結構與原始資料格式相同，只是其中的句子已經被分割並清理過。    
    
    輸出：
    ChiBibleLIST (list): 將每節經文的內容拆分為句子列表。
    """
    with open (jsonFILE, "r", encoding="utf-8") as f:
        ChiBibleLIST = json.load(f)
    
    for bookDICT in ChiBibleLIST:
        booknameSTR = next(iter(bookDICT))  # 每次拿一個書名
        for ch_idx, chapterDICT in enumerate(bookDICT[booknameSTR]):
            versesLIST = list(chapterDICT.values())[0]  #取得該章節所有 verse
            for verseDICT in versesLIST:
                senSTR = list(verseDICT.values())[0]    #內文
                
                #post-processing after scraping
                senSTR = re.sub(delPAT, "", senSTR)      #需刪除的內容
                senSTR = re.sub(zeroPAT, "零", senSTR)   #圓形符號改成國字
 
                split_senLIST = [s.strip() for s in re.split(splitPAT, senSTR) if s.strip() ]   #split sentence
                filtered_senLIST = [s for s in split_senLIST if not re.search(re_delPAT, s)]    #re-postprocessing
                pprint(filtered_senLIST)
                
                for key in verseDICT:
                    verseDICT[key] = filtered_senLIST
    
    return ChiBibleLIST

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