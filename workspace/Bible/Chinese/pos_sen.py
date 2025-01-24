#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
from ArticutAPI import Articut
from time import sleep

def main(jsonFILE, articut):
    """
    從指定的 JSON 檔案讀取聖經內容，將經文按標點符號（如：問號、逗號等）進行分割，並將結果進行處理後寫回新的 JSON 檔案。

    參數:
    jsonFILE (str): 包含聖經資料的 JSON 檔案路徑。
    articut (Articut): 透過 Articut API 進行中文分詞和詞性標註的實例。

    程式流程：
    1. 嘗試讀取已有的 tmpLIST 資料，如果不存在則初始化為空，並取得已經處理過的資料的數量。
    2. 讀取傳入的 JSON 檔案並解析成 `ChiBibleLIST` 變數，該變數包含聖經的書卷、章節和小節資料。
    3. 遍歷 `ChiBibleLIST` 中的所有書卷、章節和小節資料，對每個小節中的每個句子進行分詞和詞性標註。
    4. 每處理完一個句子，就將結果暫時儲存在 `tmpLIST` 中並寫回檔案，確保處理過程的進度不會丟失。
    5. 最後，將處理後的資料寫入新的 JSON 檔案 `創.json` 中，保存在指定的資料夾中。

    輸出：
    - 處理後的經文資料會寫入新的 JSON 檔案，並存儲於指定資料夾。
    - `tmpLIST` 檔案用來儲存已經處理過的資料，以便下次繼續處理未完成的部分。
    """
    # 嘗試讀取已有的 tmpLIST 資料，如果不存在則初始化為空
    tmpLIST = []
    tmp_index = 0  # 預設從頭開始，但會從 tmpLIST 中讀取上次處理的位置
    if os.path.exists("../../../data/Bible/Chinese/POS/出tmpLIST.json"):
        with open("../../../data/Bible/Chinese/POS/出tmpLIST.json", "r", encoding="utf-8") as f:
            tmpLIST = json.load(f)
            tmp_index = len(tmpLIST)  # 取得已經處理過的資料的數量            
    
    with open (jsonFILE, "r", encoding="utf-8") as f:
        ChiBibleLIST = json.load(f)

    POS_folder = "../../../data/Bible/Chinese/POS"
    os.makedirs(POS_folder, exist_ok=True)  # 確保資料夾存在
    output_jsonFILE = "../../../data/Bible/Chinese/POS/出.json"

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
                                with open("../../../data/Bible/Chinese/POS/出tmpLIST.json", "w", encoding="utf-8") as f:
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

    with open(output_jsonFILE, "w", encoding="utf-8") as f:
        json.dump(processed_LIST, f, ensure_ascii=False, indent=4)   

if __name__ == "__main__":
    accountDICT = json.load(open("account.info",encoding="utf-8"))
    articut = Articut(username=accountDICT["username"],apikey=accountDICT["api_key"])

    jsonFILE = "../../../data/Bible/Chinese/segment/出.json"    
    main(jsonFILE, articut)
   