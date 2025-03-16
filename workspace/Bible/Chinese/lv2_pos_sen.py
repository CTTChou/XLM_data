#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
from ArticutAPI import Articut
from glob import glob
from pprint import pprint
from time import sleep

def main(jsonFILE, filename, articut):
    """
    處理指定的 JSON 聖經檔案，將經文分段並使用 Articut 進行分詞與詞性標註，最後將結果儲存為新的 JSON 檔案。

    參數:
    jsonFILE (str): 包含聖經資料的 JSON 檔案路徑。
    filename (str): 處理過程中臨時檔案的 basename（用於保存中途結果的 tmpLIST）。
    articut (Articut): 透過 Articut API 進行中文分詞和詞性標註的實例。

    功能描述:
    1. 嘗試讀取指定目錄下的臨時檔案 `tmpLIST`，該檔案用於保存已處理的經文片段，以便程序中斷後能從上次進度繼續。
    2. 讀取原始 JSON 聖經檔案，提取每一書卷、章節、小節的經文資料。
    3. 遍歷每一經文段落，按句子逐一進行分詞與詞性標註。
    4. 每處理完成一段經文後，將結果即時追加至 `tmpLIST`，並寫回臨時檔案，確保資料已保存。
    5. 經文處理完成後，整理成包含分詞結果的完整 JSON 結構，最終保存為新檔案。

    輸出：
    - processed_LIST (list): 處理過斷句，放回原格式。
    - 一個名為 `lv2_{filename}tmpLIST.json` 的臨時檔案，保存中途處理進度。
    """
    tmpLIST = []    # 嘗試讀取已有的 tmpLIST 資料，如果不存在則初始化為空
    tmp_index = 0   # 預設從頭開始，但會從 tmpLIST 中讀取上次處理的位置
    if os.path.exists(f"../../../data/Bible/Chinese/lv2_POS/lv2_{filename}tmpLIST.json"):
        with open(f"../../../data/Bible/Chinese/lv2_POS/lv2_{filename}tmpLIST.json", "r", encoding="utf-8") as f:
            tmpLIST = json.load(f)
            tmp_index = len(tmpLIST)  # 取得已經處理過的資料的數量            
    
    processed_LIST = []
    all_senLIST = []
    with open (jsonFILE, "r", encoding="utf-8") as f:
        ChiBibleLIST = json.load(f)

        for bookDICT in ChiBibleLIST:
            booknameSTR = next(iter(bookDICT))  # 每次拿一個書名
            for ch_idx, chapterDICT in enumerate(bookDICT[booknameSTR]):
                chapterSTR = next(iter(chapterDICT))    #拿章節
                for v_idx, verseDICT in enumerate(chapterDICT[chapterSTR]):                    
                    parseLIST = []                                                                                    
                    senLIST = list(verseDICT.values())[0]    #已 segment 的內文
                    all_senLIST.append(senLIST)                    
                    tmp_index = len(tmpLIST)                    
                    for senLIST in (all_senLIST[tmp_index:]):
                        for s in senLIST:
                            resultLIST = (articut.parse(s, level="lv2"))["result_pos"]  #單一內文 articut 結果
                            pprint(resultLIST)   
                            parseLIST.append(resultLIST)
                            sleep(1.5)
                            
                    if parseLIST:                            
                        tmpLIST.append(parseLIST)
                        # 每次處理完後就儲存到 JSON 檔案
                        with open(f"../../../data/Bible/Chinese/lv2_POS/lv2_{filename}tmpLIST.json", "w", encoding="utf-8") as f:
                            json.dump(tmpLIST, f, ensure_ascii=False, indent=4)
                      
        processed_LIST.append(bookDICT)
                      
                                
        tmp_index = 0  # 重設索引，這樣後續的處理可以正確填入
        for bookDICT in processed_LIST:
            bookLIST = list(bookDICT.keys())   #拿到書名 
            for v_idx, chapterDICT in enumerate(bookDICT[bookLIST[0]]):
                versesLIST = list(chapterDICT.values())[0]  # 取得 values 的第一個元素（列表）
                for verseDICT in versesLIST:        
                    for key in verseDICT:
                        if tmp_index < len(tmpLIST):                        
                            verseDICT[key] = tmpLIST[tmp_index] #最後將 tmpLIST 中的資料放回
                            tmp_index += 1
                                
    return processed_LIST

def to_POS_LIST(POS_folder):
    """
    從指定資料夾中的所有 JSON 檔案讀取資料，將其合併到一個列表中，並將合併後的資料寫入新的 JSON 檔案。

    參數:
    pos_folder (str): 包含 JSON 檔案的資料夾路徑。

    程式流程：
    1. 遍歷指定資料夾中的非tmpLIST的 `.json` 檔案。
    2. 對每個 JSON 檔案，將其內容讀取並追加到 `pos_LIST` 列表中。
    3. 最後，將合併後的資料寫入一個名為 `lv2_POS_all_ChiBible.json` 的檔案，並儲存在指定路徑中。
    
    輸出：
    - 一個新的 JSON 檔案 `lv2_POS_all_ChiBible.json`，包含了資料夾中所有 JSON 檔案合併後的內容。
    """    
    POS_LIST = []
    POS_jsonFILE = [file for file in glob(f"{POS_folder}/*.json") if "tmpLIST" not in file]
    for jsonFILE in POS_jsonFILE:
        with open(jsonFILE, "r", encoding="utf=8") as f:
            POS_LIST.extend(json.load(f))
            
    filename ="../../../data/Bible/Chinese/lv2_POS_all_ChiBible.json"        
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(POS_LIST, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    accountDICT = json.load(open("account.info",encoding="utf-8"))
    articut = Articut(username=accountDICT["username"],apikey=accountDICT["api_key"])
   
    segment_folder = "../../../data/Bible/Chinese/segment" #read here
    jsonFILE_LIST = glob(f"{segment_folder}/*.json")
    sorted_LIST = sorted(jsonFILE_LIST)
    
    POS_folder = "../../../data/Bible/Chinese/lv2_POS"  #write here
    os.makedirs(POS_folder, exist_ok=True)  # 確保資料夾存在    
    
    LIST1 = sorted_LIST[:33]
    for jsonFILE in LIST1:  #first 33 books
        filename = os.path.splitext(os.path.basename(jsonFILE))[0]  # 拿到中文檔名
        print(f"處理：'lv2_{filename}'中")
    
    #LIST2 = sorted_LIST[-33:]  #last 33 books
    #for FILE in LIST2:
        #filename = os.path.splitext(os.path.basename(FILE))[0]  # 拿到中文檔名
        #print(f"處理：'lv2_{filename}'中")    
    
        output_jsonFILE = f"../../../data/Bible/Chinese/lv2_POS/lv2_{filename}.json"        
        if not os.path.exists(output_jsonFILE):
            with open(jsonFILE, "r", encoding="utf-8") as f:
                processed_LIST = main(jsonFILE, filename, articut)
                
                with open(output_jsonFILE, "w", encoding="utf-8") as f:
                    json.dump(processed_LIST, f, ensure_ascii=False, indent=4)            
    
    #統整在一個 JSON
    to_POS_LIST(POS_folder)