#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from glob import glob
from pprint import pprint

def replace_tag(d, tagSTR, nameSTR):
    """
    遞迴替換 JSON 結構中的 <UserDefined> 標籤為指定的標籤名稱。
    
    此函式會遍歷輸入的 JSON 結構 (dict 或 list)，
    並將其中的 `<UserDefined>{nameSTR}</UserDefined>` 替換為 `<{tagSTR}>{nameSTR}</{tagSTR}>`。

    參數:
        d (dict | list | str): JSON 結構 (可以是字典、列表或字串)。
        tagSTR (str): 要替換成的新標籤名稱 (不包含 `< >`)。
        nameSTR (str): 需要匹配的標籤內容。

    回傳:
        dict | list | str: 替換標籤後的 JSON 結構，結構與輸入相同。    
    """
    
    if isinstance(d, dict):
        return {k: replace_tag(v, tagSTR, nameSTR) for k, v in d.items()}
    
    elif isinstance(d, list):
        return [replace_tag(item, tagSTR, nameSTR) for item in d]
    
    elif isinstance(d, str):
        return d.replace(f"<UserDefined>{nameSTR}</UserDefined>", f"<{tagSTR}>{nameSTR}</{tagSTR}>")

def main(jsonFILE, userDefined):
    """
    遞迴遍歷 JSON 檔案，根據 `userDefined` 內的標籤名稱，替換 `<UserDefined>` 標籤為指定的新標籤。

    參數:
        jsonFILE (str): 要進行標籤替換的 JSON 檔案路徑。
        userDefined (str): 包含標籤對應資訊的 JSON 檔案路徑。
    
    回傳:
        None: 此函式不回傳值，而是直接修改並覆寫 `jsonFILE` 的內容。

    執行步驟:
        1. 讀取 `jsonFILE` 為 `ChiBibleLIST`。
        2. 讀取 `userDefined` 為 `userDefinedDICT`，格式如下:
            {
                "ENTITY_Person": ["Jesus", "Peter", "John"],
                "ENTITY_Location": ["Jerusalem", "Bethlehem"]
            }
        3. 遍歷 `userDefinedDICT` 中的每個標籤 (例如 `"ENTITY_Person"`)，並逐一替換 `ChiBibleLIST` 內的
           `<UserDefined>name</UserDefined>` 為 `<ENTITY_Person>name</ENTITY_Person>`。
        4. 替換完成後，將 `ChiBibleLIST` 覆寫回 `jsonFILE`。
        5. 輸出處理結果的前兩個元素以供檢查。    
    """
    
    with open(jsonFILE, "r", encoding="utf-8") as f:
        ChiBibleLIST = json.load(f)
    
    with open(userDefined, "r", encoding="utf-8") as f:
        userDefinedDICT = json.load(f)
    
    pprint(f"{jsonFILE} 標籤替換中...")
    
    #遍歷所有標籤和對應的名稱
    for tagSTR, nameLIST in userDefinedDICT.items():   #e.g. tagSTR= "ENTITY_Person"
        for nameSTR in nameLIST:
            ChiBibleLIST = replace_tag(ChiBibleLIST, tagSTR, nameSTR)
          
    #完成處理後，寫回 JSON
    with open(jsonFILE, "w", encoding="utf-8") as f:
        json.dump(ChiBibleLIST, f, ensure_ascii=False, indent=4)            
        pprint(ChiBibleLIST[:2])    #只印出處理檔案的前兩個元素看一下
        
    pprint(f"{jsonFILE} tag changed")
      
    return None


if __name__ == "__main__":
    userDefined = "../../../data_phase2/Bible/Chinese/UserDefinedFile.json"    
    
    all_Bible = "../../../data_phase2/Bible/Chinese/POS_all_ChiBible.json"
    
    folderLIST = ["../../../data_phase2/Bible/Chinese/POS"]
    
    # 先將 all_Bible 和 lv2_all_Bible 加入 jsonFILE_LIST
    jsonFILE_LIST = [all_Bible, lv2_all_Bible]
    
    # 然後遍歷 folderLIST，將所有 JSON 檔案加入 jsonFILE_LIST
    for folder in folderLIST:
        # 過濾掉檔名中包含"tmpLIST"的檔案
        files = glob(f"{folder}/*.json")
        files = [f for f in files if "tmpLIST" not in f]        
        jsonFILE_LIST += files
        
    for jsonFILE in jsonFILE_LIST:
        main(jsonFILE, userDefined)        