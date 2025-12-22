#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速測試腳本 - 測試檔案轉換功能
"""

from convert_to_json import FileConverter
from pathlib import Path

def test_basic_functionality():
    """測試基本功能"""
    print("=" * 50)
    print("測試檔案轉換功能")
    print("=" * 50)
    
    converter = FileConverter(".")
    
    # 測試檔案掃描
    print("\n1. 測試檔案掃描...")
    files = converter.scan_files()
    print(f"   找到 {len(files)} 個檔案")
    if files:
        print(f"   範例檔案: {files[0].name}")
    
    # 測試檔案分類
    print("\n2. 測試檔案分類...")
    if files:
        category, subcategory = converter.classify_file(files[0])
        print(f"   檔案: {files[0].name}")
        print(f"   分類: {category}")
        print(f"   子分類: {subcategory}")
    
    # 測試文字提取（僅測試第一個文字檔案）
    print("\n3. 測試文字提取...")
    text_files = [f for f in files if f.suffix.lower() in ['.txt', '.md']]
    if text_files:
        test_file = text_files[0]
        print(f"   測試檔案: {test_file.name}")
        content = converter.extract_text(test_file)
        print(f"   內容長度: {len(content)} 字元")
        if len(content) > 0:
            print(f"   前100字: {content[:100]}...")
    
    print("\n" + "=" * 50)
    print("測試完成！")
    print("=" * 50)

if __name__ == "__main__":
    test_basic_functionality()

