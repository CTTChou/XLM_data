#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from pprint import pprint

def main():
    """
    比對 `UserDefinedFile.json` 中的 `ENTITY_person` 和 `LOCATION` 列表，找出重複的名稱並返回。

    這個函數執行以下步驟：
    1. 讀取 `UserDefinedFile.json` 文件，提取 `ENTITY_person` 和 `LOCATION` 列表。
    2. 對 `UserDefinedFile.json` 內的所有列表按照字串長度進行排序，並將結果寫回原文件。    
    3. 檢查 `ENTITY_person` 列表中的每個名稱是否也存在於 `LOCATION` 列表中。
    4. 如果名稱重疊，將其加入到 `overlapLIST` 中並返回這個列表。

    回傳:
        overlapLIST (list): 包含重疊的名稱列表，這些名稱同時出現在 `ENTITY_person` 和 `LOCATION` 中。
    """
    overlapLIST = []
    
    with open("../../../data/Bible/Chinese/UserDefinedFile.json", "r", encoding="utf-8") as f:
        userdefinedDICT = json.load(f)
        perLIST = userdefinedDICT["ENTITY_person"]
        locLIST = userdefinedDICT["LOCATION"]
    
    # 對每個 key 的 list 按長度排序    
    for keySTR in userdefinedDICT:
        userdefinedDICT[keySTR] = sorted(userdefinedDICT[keySTR], key=len)
    
    # 寫回 JSON 檔案
    with open("../../../data/Bible/Chinese/UserDefinedFile.json", "w", encoding="utf-8") as f:
        json.dump(userdefinedDICT, f, ensure_ascii=False, indent=4)    
        
    for nameSTR in perLIST:
        if nameSTR in locLIST:
            overlapLIST.append(nameSTR)
        
    return overlapLIST


if __name__ == "__main__":
    overlapLIST = main()
    pprint(overlapLIST)
    print(f"人名地名重疊數量：{len(overlapLIST)}")