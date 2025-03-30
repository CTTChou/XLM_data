#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from pprint import pprint

def main():
    """
    比對 `UserDefinedFile.json` 中的 `ENTITY_person` 和 `LOCATION` 列表，找出重複的名稱並返回。

    這個函數執行以下步驟：
    1. 讀取 `UserDefinedFile.json` 文件，提取 `ENTITY_person` 和 `LOCATION` 列表。
    2. 檢查 `ENTITY_person` 列表中的每個名稱是否也存在於 `LOCATION` 列表中。
    3. 如果名稱重疊，將其加入到 `overlapLIST` 中並返回這個列表。

    回傳:
        overlapLIST (list): 包含重疊的名稱列表，這些名稱同時出現在 `ENTITY_person` 和 `LOCATION` 中。
    """
    overlapLIST = []
    
    with open("../../../data/Bible/Chinese/UserDefinedFile.json", "r", encoding="utf-8") as f:
        userdefinedDICT = json.load(f)
        perLIST = userdefinedDICT["ENTITY_person"]
        locLIST = userdefinedDICT["LOCATION"]
        
    for nameSTR in perLIST:
        if nameSTR in locLIST:
            overlapLIST.append(nameSTR)
        
    return overlapLIST


if __name__ == "__main__":
    overlapLIST = main()
    pprint(overlapLIST)
    print(f"人名地名重疊數量：{len(overlapLIST)}")