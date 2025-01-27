#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
from ArticutAPI import Articut
from glob import glob
from time import sleep

def main(jsonFILE, filename, articut):
    """
    處理指定的 JSON 聖經檔案，將經文分段並使用 Articut 進行分詞與詞性標註，最後將結果儲存為新的 JSON 檔案。。

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
    if os.path.exists(f"../../../data/Bible/Chinese/POS/{filename}tmpLIST.json"):
        with open(f"../../../data/Bible/Chinese/POS/{filename}tmpLIST.json", "r", encoding="utf-8") as f:
            tmpLIST = json.load(f)
            tmp_index = len(tmpLIST)  # 取得已經處理過的資料的數量            
    
    with open (jsonFILE, "r", encoding="utf-8") as f:
        ChiBibleLIST = json.load(f)

    processed_LIST = []
    all_split_senLIST = []
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
                        
                        for secSTR, split_senLIST in secDICT.items():
                            parseLIST = []
                            print(split_senLIST)
                            all_split_senLIST.append(split_senLIST)
                            tmp_index = len(tmpLIST)
                            for s_l in (all_split_senLIST[tmp_index:]):
                                for item_s in s_l:                                   
                                    resultDICT = articut.parse(item_s, level="lv1")
                                    result_posLIST = resultDICT["result_pos"]
                                    print(result_posLIST)   
                                    parseLIST.append(result_posLIST)
                                    sleep(1.5)
                            print(parseLIST)
                            
                            if parseLIST:
                                tmpLIST.append(parseLIST)
                                # 每次處理完後就儲存到 JSON 檔案
                                with open(f"../../../data/Bible/Chinese/POS/{filename}tmpLIST.json", "w", encoding="utf-8") as f:
                                    json.dump(tmpLIST, f, ensure_ascii=False, indent=4)                                    
                                                                                
                            processed_secDICT[secSTR] = parseLIST
                        processed_secLIST.append(processed_secDICT)
                    processed_chDICT[chSTR] = processed_secLIST
                processed_chLIST.append(processed_chDICT)
            processed_bookDICT[bookSTR] = processed_chLIST
        processed_LIST.append(processed_bookDICT)
    
    # 最後將 tmpLIST 中的資料放回 processed_secDICT[secSTR]
    tmp_index = 0  # 重設索引，這樣後續的處理可以正確填入
    for bookDICT in processed_LIST:
        for bookSTR, chLIST in bookDICT.items():
            for chDICT in chLIST:
                for chSTR, secLIST in chDICT.items():
                    for secDICT in secLIST:
                        for secSTR in secDICT:
                            if tmp_index < len(tmpLIST):
                                secDICT[secSTR] = tmpLIST[tmp_index]
                                tmp_index += 1
                                
    return processed_LIST

if __name__ == "__main__":
    accountDICT = json.load(open("account.info",encoding="utf-8"))
    articut = Articut(username=accountDICT["username"],apikey=accountDICT["api_key"])
   
    segment_folder = "../../../data/Bible/Chinese/segment" #read here
    jsonFILE_LIST = glob(f"{segment_folder}/*.json")
    sorted_LIST = sorted(jsonFILE_LIST)
    
    POS_folder = "../../../data/Bible/Chinese/POS"  #write here
    os.makedirs(POS_folder, exist_ok=True)  # 確保資料夾存在    
    
    LIST1 = sorted_LIST[:33]
    for jsonFILE in LIST1:  #first 33 books
        filename = os.path.splitext(os.path.basename(jsonFILE))[0]  # 拿到中文檔名
        print(filename)
    
    #LIST2 = sorted_LIST[-33:]  #last 33 books
    #for FILE in LIST2:
        #filename = os.path.splitext(os.path.basename(FILE))[0]  # 拿到中文檔名
    
        output_jsonFILE = f"../../../data/Bible/Chinese/POS/{filename}.json"        
        if not os.path.exists(output_jsonFILE):
            with open(jsonFILE, "r", encoding="utf-8") as f:
                processed_LIST = main(jsonFILE, filename, articut)
                
                with open(output_jsonFILE, "w", encoding="utf-8") as f:
                    json.dump(processed_LIST, f, ensure_ascii=False, indent=4)            
