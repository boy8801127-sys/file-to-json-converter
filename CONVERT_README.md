# 檔案轉換為 JSON 格式使用說明

## 功能說明

此腳本會將資料夾內的所有檔案（PDF、TXT、MD）轉換成適合 Open WebUI 知識庫使用的 JSON 格式，用於模型微調和 RAG 應用。

## 安裝依賴

在虛擬環境中安裝所需套件：

```bash
# 啟動虛擬環境（Windows）
env\Scripts\activate

# 安裝依賴
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
python convert_to_json.py --root "D:\find_a_job"

# 指定輸出檔案名稱
python convert_to_json.py --output my_training_data.json

# 同時輸出個別 JSON 檔案到資料夾
python convert_to_json.py --output-dir output

# 只輸出個別檔案，不輸出單一 JSON
python convert_to_json.py --no-single --output-dir output
```

## 輸出格式

### 單一 JSON 檔案格式

預設會產生 `training_data.json`，包含所有檔案的陣列：

```json
[
  {
    "id": "resume_abc12345",
    "file_path": "生平簡介/履歷書.pdf",
    "file_name": "履歷書.pdf",
    "file_type": "pdf",
    "category": "生平簡介",
    "subcategory": null,
    "content": "提取的文字內容...",
    "metadata": {
      "title": "履歷書",
      "summary": "摘要內容...",
      "keywords": ["履歷", "學歷", "技能"],
      "extracted_date": "2025-01-XX",
      "file_size": 12345
    }
  }
]
```

### 個別 JSON 檔案

如果指定 `--output-dir`，每個檔案會產生一個獨立的 JSON 檔案，檔名為 `{id}.json`。

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

## 注意事項

1. **PDF 處理**：需要安裝 `pdfplumber` 或 `PyPDF2`，腳本會自動嘗試使用可用的套件
2. **編碼問題**：文字檔案會嘗試多種編碼（UTF-8、Big5、GB2312 等）
3. **虛擬環境**：腳本會自動排除 `env/` 資料夾中的檔案
4. **檔案大小**：大檔案會完整提取，建議確保有足夠記憶體

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

如果處理大量大檔案時遇到記憶體問題，可以分批處理或增加系統記憶體。

