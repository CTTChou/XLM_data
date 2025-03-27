#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
#from time import sleep
from requests import post
from glob import glob

#url = "https://nlu.droidtown.co/Articut_EN/API/"
url = "http://127.0.0.1:8999"


def articutEN(inputSTR: str) -> list:
    """
    使用 Articut 英文版 StandardAPI 對輸入的文字進行詞性標記 (POS)。
    
    參數:
        inputSTR (str): 需要進行詞性標記的英文文字。
    
    回傳:
        list: 詞性標記後的結果，返回 result_pos 內容。
    """
    payload = {
       "username":"",
       "api_key": "",
       "input_str": inputSTR
    }    
   
    #response = post(url, json=payload).json()
    response = post("{}/Articut_EN/API/".format(url), json=payload).json()
    print(response)
    return response


def main(jsonFILE, flename, articut):
    """
    處理指定的 JSON 聖經檔案，將經文分段並使用 英文版Articut 進行分詞與詞性標註，最後將結果儲存為新的 JSON 檔案。。

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
    - 一個名為 `{filename}tmpLIST.json` 的臨時檔案，保存中途處理進度。
    """
    # 嘗試讀取已有的 tmpLIST 資料，如果不存在則初始化為空
    tmpLIST = []
    tmp_index = 0  # 預設從頭開始，但會從 tmpLIST 中讀取上次處理的位置
    if os.path.exists(f"../../../data/Bible//POS/{filename}tmpLIST.json"):
        with open(f"../../../data/Bible/English/POS/{filename}tmpLIST.json", "r", encoding="utf-8") as f:
            tmpLIST = json.load(f)
            tmp_index = len(tmpLIST)  # 取得已經處理過的資料的數量            
    
    with open (jsonFILE, "r", encoding="utf-8") as f:
        EngBibleLIST = json.load(f)

    processed_LIST = []
    all_split_senLIST = []
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
                        
                        for secSTR, split_senLIST in secDICT.items():
                            parseLIST = []
                            print(split_senLIST)
                            all_split_senLIST.append(split_senLIST)
                            tmp_index = len(tmpLIST)
                            for s_l in (all_split_senLIST[tmp_index:]):
                                for item_s in s_l:                                   
                                    resultDICT = articutEN(item_s)
                                    result_posLIST = resultDICT["result_pos"]
                                    print(result_posLIST)   
                                    parseLIST.append(result_posLIST)
                                    #sleep(1.5)
                            print(parseLIST)
                            
                            if parseLIST:
                                tmpLIST.append(parseLIST)
                                # 每次處理完後就儲存到 JSON 檔案
                                with open("../../../data/Bible/English/POS/tmpLIST.json", "w", encoding="utf-8") as f:
                                    json.dump(tmpLIST, f, ensure_ascii=False, indent=4)                                    
                                                                                
                            processed_secDICT[secSTR] = parseLIST
                        processed_secLIST.append(processed_secDICT)
                    processed_enDICT[enSTR] = processed_secLIST
                processed_enLIST.append(processed_enDICT)
            processed_bookDICT[bookSTR] = processed_enLIST
        processed_LIST.append(processed_bookDICT)
    
    # 最後將 tmpLIST 中的資料放回 processed_secDICT[secSTR]
    tmp_index = 0  # 重設索引，這樣後續的處理可以正確填入
    for bookDICT in processed_LIST:
        for bookSTR, enLIST in bookDICT.items():
            for enDICT in enLIST:
                for enSTR, secLIST in enDICT.items():
                    for secDICT in secLIST:
                        for secSTR in secDICT:
                            if tmp_index < len(tmpLIST):
                                secDICT[secSTR] = tmpLIST[tmp_index]
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
    3. 最後，將合併後的資料寫入一個名為 `pos_all_ChiBible.json` 的檔案，並儲存在指定路徑中。
    
    輸出：
    - 一個新的 JSON 檔案 `pos_all_ChiBible.json`，包含了資料夾中所有 JSON 檔案合併後的內容。
    """    
    POS_LIST = []
    POS_jsonFILE = [file for file in glob(f"{POS_folder}/*.json") if "tmpLIST" not in file]
    for jsonFILE in POS_jsonFILE:
        with open(jsonFILE, "r", encoding="utf=8") as f:
            POS_LIST.extend(json.load(f))
            
    filename ="../../../data/Bible/English/POS_all_EngBible.json"        
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(POS_LIST, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    
    #try:
        #with open("./account.info", encoding="utf-8") as f:
            #accountDICT = json.load(f)
    #except:
        #accountDICT = {"username":"", "apikey":""}    
    

    #jsonFILE = "../../../data/Bible/English/segment/Ezra.json"    
    #main(jsonFILE, articutEN)
    
    segment_folder = "../../../data/Bible/English/segment" #read here
    jsonFILE_LIST = glob(f"{segment_folder}/*.json")
    sorted_LIST = sorted(jsonFILE_LIST)
    
    POS_folder = "../../../data/Bible/English/POS"  #write here
    os.makedirs(POS_folder, exist_ok=True)  # 確保資料夾存在    
    
    LIST2 = sorted_LIST[-33:]  #last 33 books
    for jsonFILE in LIST2:
        filename = os.path.splitext(os.path.basename(jsonFILE))[0]  # 拿到英文檔名
    
        output_jsonFILE = f"../../../data/Bible/English/POS/{filename}.json"        
        if not os.path.exists(output_jsonFILE):
            with open(jsonFILE, "r", encoding="utf-8") as f:
                processed_LIST = main(jsonFILE, filename, articutEN)
                
                with open(output_jsonFILE, "w", encoding="utf-8") as f:
                    json.dump(processed_LIST, f, ensure_ascii=False, indent=4)            
    
    #統整在一個 JSON
    to_POS_LIST(POS_folder)   