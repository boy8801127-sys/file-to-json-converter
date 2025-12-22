#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
檔案轉換為訓練用 JSON 格式
將資料夾內的所有檔案（PDF、TXT、MD）轉換成適合 Open WebUI 知識庫使用的 JSON 格式
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import uuid

try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    try:
        import PyPDF2
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False
        print("警告：未安裝 PDF 處理套件，PDF 檔案將被跳過")


class FileConverter:
    """檔案轉換器主類別"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.supported_extensions = {'.pdf', '.txt', '.md'}
        self.results = []
        
    def scan_files(self) -> List[Path]:
        """掃描所有支援的檔案"""
        files = []
        for ext in self.supported_extensions:
            files.extend(self.root_dir.rglob(f"*{ext}"))
        # 排除虛擬環境資料夾
        files = [f for f in files if 'env' not in str(f)]
        return sorted(files)
    
    def classify_file(self, file_path: Path) -> Tuple[str, Optional[str]]:
        """根據路徑分類檔案"""
        path_str = str(file_path)
        relative_path = file_path.relative_to(self.root_dir)
        path_parts = relative_path.parts
        
        if '生平簡介' in path_parts:
            category = "生平簡介"
            subcategory = None
        elif '程式編寫' in path_parts:
            category = "程式編寫"
            # 提取專案名稱（第二層資料夾名稱）
            if len(path_parts) > 2:
                subcategory = path_parts[1]  # 例如：景氣燈號策略
            else:
                subcategory = None
        elif '職訓班課程' in path_parts:
            category = "職訓班課程"
            subcategory = None
        else:
            category = "其他"
            subcategory = None
            
        return category, subcategory
    
    def extract_pdf_text(self, file_path: Path) -> str:
        """提取 PDF 文字內容"""
        if not PDF_AVAILABLE:
            return f"[PDF 處理套件未安裝，無法提取內容]"
        
        text_content = []
        
        try:
            # 優先使用 pdfplumber
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
            except:
                # 備用方案：使用 PyPDF2
                try:
                    with open(file_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        for page in pdf_reader.pages:
                            text = page.extract_text()
                            if text:
                                text_content.append(text)
                except Exception as e:
                    return f"[PDF 提取失敗: {str(e)}]"
        except Exception as e:
            return f"[PDF 處理錯誤: {str(e)}]"
        
        return "\n\n".join(text_content)
    
    def extract_text_file(self, file_path: Path) -> str:
        """提取文字檔案內容"""
        encodings = ['utf-8', 'utf-8-sig', 'big5', 'gb2312', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                return f"[讀取檔案失敗: {str(e)}]"
        
        return "[無法解碼檔案內容]"
    
    def extract_text(self, file_path: Path) -> str:
        """根據檔案類型提取文字內容"""
        ext = file_path.suffix.lower()
        
        if ext == '.pdf':
            return self.extract_pdf_text(file_path)
        elif ext in ['.txt', '.md']:
            return self.extract_text_file(file_path)
        else:
            return ""
    
    def extract_title_from_content(self, content: str, file_name: str) -> str:
        """從內容中提取標題（簡單規則）"""
        # 嘗試從 Markdown 檔案提取標題
        if file_name.endswith('.md'):
            # 尋找第一個 # 標題
            lines = content.split('\n')
            for line in lines[:20]:  # 只檢查前20行
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
                elif line.startswith('## '):
                    return line[3:].strip()
        
        # 從檔案名稱提取（移除副檔名）
        title = Path(file_name).stem
        # 移除常見的檔案名稱前綴
        title = re.sub(r'^(README|readme|README_|readme_)', '', title, flags=re.IGNORECASE)
        if not title:
            title = file_name
        
        return title
    
    def extract_summary(self, content: str, file_type: str) -> str:
        """提取摘要（簡單規則）"""
        # 取前200字作為摘要
        content_clean = re.sub(r'\s+', ' ', content.strip())
        if len(content_clean) <= 200:
            return content_clean
        
        # 嘗試在句號處截斷
        summary = content_clean[:200]
        last_period = summary.rfind('。')
        if last_period > 100:  # 確保摘要不會太短
            summary = summary[:last_period + 1]
        else:
            summary = summary[:200] + "..."
        
        return summary
    
    def extract_keywords(self, content: str, category: str, subcategory: Optional[str]) -> List[str]:
        """提取關鍵字（簡單規則）"""
        keywords = []
        
        # 根據分類添加關鍵字
        if category == "程式編寫":
            keywords.extend(["Python", "程式設計", "專案"])
            if subcategory:
                keywords.append(subcategory)
        elif category == "生平簡介":
            keywords.extend(["履歷", "自我推薦", "個人資料"])
        elif category == "職訓班課程":
            keywords.extend(["課程", "學習", "職訓"])
        
        # 從內容中提取常見技術關鍵字
        tech_keywords = [
            "Python", "SQL", "MySQL", "API", "GitHub", "Docker", 
            "量化交易", "回測", "資料分析", "機器學習", "Orange",
            "雲端部署", "爬蟲", "資料庫", "視覺化", "Power BI"
        ]
        
        content_lower = content.lower()
        for keyword in tech_keywords:
            if keyword.lower() in content_lower:
                if keyword not in keywords:
                    keywords.append(keyword)
        
        # 限制關鍵字數量
        return keywords[:10]
    
    def enhance_metadata(self, file_path: Path, content: str, category: str, 
                        subcategory: Optional[str]) -> Dict:
        """使用簡單規則增強 metadata"""
        file_name = file_path.name
        
        title = self.extract_title_from_content(content, file_name)
        summary = self.extract_summary(content, file_name.split('.')[-1])
        keywords = self.extract_keywords(content, category, subcategory)
        
        return {
            "title": title,
            "summary": summary,
            "keywords": keywords,
            "extracted_date": datetime.now().strftime("%Y-%m-%d"),
            "file_size": file_path.stat().st_size
        }
    
    def convert_file(self, file_path: Path) -> Optional[Dict]:
        """轉換單一檔案為 JSON 格式"""
        try:
            # 提取文字內容
            content = self.extract_text(file_path)
            if not content or content.startswith("["):
                print(f"警告：無法提取 {file_path} 的內容")
                if content.startswith("["):
                    # 如果是錯誤訊息，仍然記錄
                    pass
                else:
                    return None
            
            # 分類檔案
            category, subcategory = self.classify_file(file_path)
            
            # 生成 ID
            file_id = f"{category.lower()}_{uuid.uuid4().hex[:8]}"
            
            # 獲取相對路徑
            relative_path = str(file_path.relative_to(self.root_dir))
            
            # 增強 metadata
            metadata = self.enhance_metadata(file_path, content, category, subcategory)
            
            # 構建 JSON 物件
            json_obj = {
                "id": file_id,
                "file_path": relative_path.replace("\\", "/"),  # 統一使用斜線
                "file_name": file_path.name,
                "file_type": file_path.suffix[1:].lower(),  # 移除點號
                "category": category,
                "subcategory": subcategory,
                "content": content,
                "metadata": metadata
            }
            
            return json_obj
            
        except Exception as e:
            print(f"錯誤：處理 {file_path} 時發生錯誤: {str(e)}")
            return None
    
    def convert_all(self, output_file: str = "training_data.json", 
                   output_dir: Optional[str] = None) -> None:
        """轉換所有檔案"""
        print("開始掃描檔案...")
        files = self.scan_files()
        print(f"找到 {len(files)} 個檔案")
        
        print("\n開始轉換檔案...")
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] 處理: {file_path.name}")
            json_obj = self.convert_file(file_path)
            if json_obj:
                self.results.append(json_obj)
        
        print(f"\n成功轉換 {len(self.results)} 個檔案")
        
        # 輸出單一 JSON 檔案
        if output_file:
            output_path = self.root_dir / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"已輸出單一 JSON 檔案: {output_path}")
        
        # 輸出個別 JSON 檔案
        if output_dir:
            output_path_dir = self.root_dir / output_dir
            output_path_dir.mkdir(exist_ok=True)
            
            for json_obj in self.results:
                file_name = json_obj['id'] + '.json'
                file_path = output_path_dir / file_name
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(json_obj, f, ensure_ascii=False, indent=2)
            
            print(f"已輸出 {len(self.results)} 個個別 JSON 檔案到: {output_path_dir}")


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='將檔案轉換為訓練用 JSON 格式')
    parser.add_argument('--root', type=str, default='.', 
                       help='根目錄路徑（預設：當前目錄）')
    parser.add_argument('--output', type=str, default='training_data.json',
                       help='輸出 JSON 檔案名稱（預設：training_data.json）')
    parser.add_argument('--output-dir', type=str, default=None,
                       help='輸出個別 JSON 檔案的資料夾（選填）')
    parser.add_argument('--no-single', action='store_true',
                       help='不輸出單一 JSON 檔案')
    
    args = parser.parse_args()
    
    converter = FileConverter(args.root)
    
    output_file = None if args.no_single else args.output
    converter.convert_all(output_file=output_file, output_dir=args.output_dir)
    
    print("\n轉換完成！")


if __name__ == "__main__":
    main()

