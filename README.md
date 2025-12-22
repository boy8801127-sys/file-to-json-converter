# 檔案轉換為訓練用 JSON 格式工具

一個 Python 工具，用於將資料夾內的所有檔案（PDF、TXT、MD）轉換成適合 Open WebUI 知識庫使用的 JSON 格式，用於模型微調和 RAG（檢索增強生成）應用。

## 功能特色

- 📄 **多格式支援**：支援 PDF、TXT、Markdown 檔案格式
- 🏷️ **自動分類**：根據檔案路徑自動分類（生平簡介、程式編寫、職訓班課程等）
- 🔍 **智能提取**：自動提取標題、摘要和關鍵字
- 📊 **結構化輸出**：產生標準化的 JSON 格式，適合向量資料庫索引
- 🔧 **簡單易用**：命令列工具，支援多種輸出選項

## 安裝

### 1. 建立虛擬環境（建議）

```bash
python -m venv env

# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate
```

### 2. 安裝依賴

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```bash
# 轉換當前目錄的所有檔案，輸出為 training_data.json
python convert_to_json.py
```

### 進階選項

```bash
# 指定根目錄
python convert_to_json.py --root "D:\your_folder"

# 指定輸出檔案名稱
python convert_to_json.py --output my_training_data.json

# 同時輸出個別 JSON 檔案到資料夾
python convert_to_json.py --output-dir output

# 只輸出個別檔案，不輸出單一 JSON
python convert_to_json.py --no-single --output-dir output
```

## 輸出格式

每個檔案會轉換為以下 JSON 格式：

```json
{
  "id": "unique_id",
  "file_path": "相對路徑",
  "file_name": "檔案名稱",
  "file_type": "pdf|txt|md",
  "category": "分類",
  "subcategory": "子分類",
  "content": "檔案文字內容",
  "metadata": {
    "title": "標題",
    "summary": "摘要",
    "keywords": ["關鍵字1", "關鍵字2"],
    "extracted_date": "2025-01-XX",
    "file_size": 12345
  }
}
```

## 檔案分類規則

腳本會根據檔案路徑自動分類：

- **生平簡介**：`生平簡介/` 資料夾下的檔案
- **程式編寫**：`程式編寫/` 資料夾下的檔案
  - 子分類：專案資料夾名稱（如：景氣燈號策略）
- **職訓班課程**：`職訓班課程/` 資料夾下的檔案

## Metadata 提取規則

### 標題提取
- Markdown 檔案：提取第一個 `#` 或 `##` 標題
- 其他檔案：從檔案名稱提取（移除副檔名和常見前綴）

### 摘要提取
- 取內容前 200 字
- 嘗試在句號處截斷，保持完整性

### 關鍵字提取
- 根據分類自動添加相關關鍵字
- 從內容中掃描常見技術關鍵字（Python、SQL、量化交易等）
- 最多提取 10 個關鍵字

## 專案結構

```
find_a_job/
├── convert_to_json.py      # 主轉換腳本
├── test_convert.py          # 測試腳本
├── requirements.txt         # Python 依賴套件
├── CONVERT_README.md       # 詳細使用說明
└── README.md               # 本檔案
```

## 技術細節

### 依賴套件

- `pdfplumber` 或 `PyPDF2`：PDF 文字提取
- `pathlib2`：檔案路徑處理（Python < 3.4）

### PDF 處理

腳本會自動嘗試使用可用的 PDF 處理套件：
1. 優先使用 `pdfplumber`（更準確）
2. 備用方案：`PyPDF2`

### 編碼處理

文字檔案會自動嘗試多種編碼：
- UTF-8
- UTF-8 with BOM
- Big5（繁體中文）
- GB2312（簡體中文）
- Latin-1

## 使用案例

### Open WebUI 知識庫

將轉換後的 JSON 檔案匯入 Open WebUI 知識庫，用於：
- RAG 應用（檢索增強生成）
- 模型微調資料準備
- 向量資料庫索引

### 模型微調

產生的 JSON 格式適合用於：
- 語言模型微調
- 問答對生成
- 文件檢索系統

## 注意事項

1. **PDF 處理**：需要安裝 `pdfplumber` 或 `PyPDF2`
2. **編碼問題**：腳本會自動嘗試多種編碼，但某些特殊編碼可能無法處理
3. **虛擬環境**：腳本會自動排除 `env/` 資料夾中的檔案
4. **檔案大小**：大檔案會完整提取，建議確保有足夠記憶體
5. **個人資料**：請確保 `.gitignore` 已正確設定，避免上傳個人敏感資料

## 疑難排解

### PDF 無法提取

確保已安裝 PDF 處理套件：
```bash
pip install pdfplumber
# 或
pip install PyPDF2
```

### 編碼錯誤

如果遇到編碼問題，腳本會自動嘗試多種編碼。如果仍然失敗，檔案內容會標記為 `[無法解碼檔案內容]`。

### 記憶體不足

如果處理大量大檔案時遇到記憶體問題，可以：
- 分批處理檔案
- 增加系統記憶體
- 使用 `--output-dir` 選項分開處理

## 授權

本專案僅供學習和研究使用。

## 貢獻

歡迎提出 Issue 或 Pull Request！

## 聯絡方式

如有問題或建議，請透過 GitHub Issues 提出。

