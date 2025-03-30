#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from pprint import pprint

def load_verseSTR():
    """
    讀取 JSON 格式的英文聖經數據，並提取所有經文內容。
    
    此函式會執行以下步驟：
    1. 從指定路徑 ("../../../data/Bible/Chinese/all_ChiBible.json") 讀取 JSON 數據。
    2. 遍歷 JSON 數據結構，提取每卷書的所有經文。
    3. 將經文內容存入列表 `all_versesLIST`，並返回該列表。

    回傳:
        versesSTR (str): 包含所有經文內容的字串，所有經文以空格分隔。
    """   
    with open("../../../data/Bible/Chinese/all_ChiBible.json", "r", encoding="utf-8") as f:            
        dataLIST = json.load(f)     
    all_versesLIST =[]
    for bookDICT in dataLIST:
        booknameSTR = next(iter(bookDICT))  # 每次拿一個書名
        for ch_idx, chapterDICT in enumerate(bookDICT[booknameSTR]):
            versesLIST = list(chapterDICT.values())[0]  # 取得 values 的第一個元素（列表）
            for verseDICT in versesLIST:
                all_versesLIST.append(next(iter(verseDICT.values())))  # 加入 verse 內文
    
    versesSTR = " ".join(all_versesLIST) #把所有內文接在一起

    return versesSTR

def extract_overlapping(comparedLIST, targetLIST, category):
    """
    比較 `comparedLIST` 中的項目，找出與 fhl_names.json 中的重複項目，並將重複項目加入到 `targetLIST` 中。

    這個函數會執行以下步驟：
    1. 讀取 fhl_names.json，獲取所有名稱列表。
    2. 遍歷 `comparedLIST`，找到在 fhl_names.json 中也存在的項目。
    3. 將這些重複項目加入到 `targetLIST` 中。

    參數:
        comparedLIST (list): 用來比對的列表，例如： places.json 或 persons.json。
        targetLIST (list): 要更新的目標列表，例如： `locLIST` 或 `perLIST`。
        category (str): 類別，用於區分是處理地名 (`"place"`) 還是人名 (`"person"`)。
    """
    overlapLIST = []
    
    with open("../../../data/Bible/Chinese/names/fhl_names.json", "r", encoding="utf-8") as f:
        fhlDICT = json.load(f)
        fhlLIST = list(fhlDICT.values())[0]
        #如果 places.json 裡的也在 fhl_names.json
        overlapLIST = [nameSTR for nameSTR in comparedLIST if nameSTR in fhlLIST]
    
    pprint(f"和 fhl_names.json 重疊的名字：{overlapLIST}")
    pprint(f"和 fhl_names.json 的重疊數量：{len(overlapLIST)}")
    
    for nameSTR in overlapLIST:
        if nameSTR not in targetLIST:  
            targetLIST.append(nameSTR)
    
    
def adding_names(comparedLIST, locLIST, nounLIST):
    """
    根據聖經經文檢查 `comparedLIST` 中的名稱是否應該加到 `locLIST` 或 `nounLIST` 中。

    這個函數會執行以下步驟：
    1. 定義地名和名詞可能的後綴詞。
    2. 遍歷 `comparedLIST`，檢查每個名稱與後綴組合是否出現在聖經經文中。
    3. 如果匹配，將結果加入 `locLIST` 或 `nounLIST`。

    參數:
        comparedLIST (list): 用來比對的名稱列表，來自於 places.json。
        locLIST (list): 儲存地名的列表。
        nounLIST (list): 儲存名詞的列表。
    """
    versesSTR = load_verseSTR()
           
    # 定義 location & noun 可能的後綴詞
    suffixDICT = {
        "loc": ["鎮", "城", "河", "海", "山", "山脈", "平原", "谷"],
        "noun": ["人", "王"]
    }    
    
    # 儲存匹配到的名字
    havingDICT = {
        "loc": set(),
        "noun": set()
    }
    
    #遍歷所有 "地名 + suffix"，檢查是否匹配聖經經文
    for nameSTR in comparedLIST:
        for key, suffixLIST in suffixDICT.items():
            #如果 "地名"+"鎮" 也在 all_ChiBible.json，將 "xxx鎮" 放入 LOCATION                        
            #如果 "地名"+"人" 也在 all_ChiBible.json，將 "xxx人" 放入 ENTITY_noun
            havingDICT.update(nameSTR + suffixSTR for suffixSTR in suffixLIST if (nameSTR + suffixSTR) in versesSTR)
                
    pprint(f"須添加的：{havingLIST}")    
    print(f"和 all_ChiBible.json 的重疊數量：{len(havingLIST)}")

    locLIST.extend(havingDICT["loc"] - set(locLIST))    #如果 location 還不存在於 UserDefinedFile.json 就添加
    nounLIST.extend(havingDICT["noun"] - set(nounLIST)) #如果 noun 還不存在於 UserDefinedFile.json 就添加        

if __name__ == "__main__":
    with open("../../../data/Bible/Chinese/UserDefinedFile.json", "r", encoding="utf-8") as f:
        userdefinedDICT = json.load(f)
        locLIST = userdefinedDICT["LOCATION"]
        perLIST = userdefinedDICT["ENTITY_person"]
        nounLIST = userdefinedDICT["ENTITY_noun"]
    
    # 統一處理 places.json 和 persons.json
    mappingDICT = {
        "place": locLIST,
        "person": perLIST
    }
    
    for category, targetLIST in mappingDICT.items():        
        with open(f"../../../data/Bible/Chinese/names/{category}s.json", "r", encoding="utf-8") as f:  
            comparedDICT = json.load(f)
            comparedLIST = list(comparedDICT.values())[0]
            extract_overlapping(comparedLIST, targetLIST, category)
                
            if category == "place": #是地名的話，才檢查是否有 "地名"+"鎮" 類似的詞彙需添加
                adding_names(comparedLIST, locLIST, nounLIST)
                
    
    with open("../../../data/Bible/Chinese/UserDefinedFile.json", "w", encoding="utf-8") as f:
        json.dump(userdefinedDICT, f, ensure_ascii=False, indent=4)