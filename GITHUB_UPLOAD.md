# GitHub 上傳指南

## 上傳前的準備

### 1. 確認 .gitignore 已正確設定

已建立的 `.gitignore` 會自動排除：
- ✅ 虛擬環境資料夾 (`env/`)
- ✅ 個人資料 JSON 檔案 (`training_data.json`)
- ✅ 生平簡介資料夾（包含履歷）
- ✅ Python 快取檔案
- ✅ IDE 設定檔

### 2. 檢查要上傳的檔案

**會上傳的檔案：**
- ✅ `convert_to_json.py` - 主轉換腳本
- ✅ `test_convert.py` - 測試腳本
- ✅ `requirements.txt` - 依賴套件清單
- ✅ `README.md` - 專案說明
- ✅ `CONVERT_README.md` - 詳細使用說明
- ✅ `.gitignore` - Git 忽略規則
- ✅ `程式編寫/` 資料夾（專案文件）
- ✅ `職訓班課程/` 資料夾（課程資料，不含個人資訊）

**不會上傳的檔案：**
- ❌ `training_data.json` - 個人資料 JSON
- ❌ `生平簡介/` - 個人履歷資料
- ❌ `env/` - 虛擬環境
- ❌ `output/` - 輸出資料夾（如果有的話）

## Git 初始化與上傳步驟

### 1. 初始化 Git 倉庫（如果尚未初始化）

```bash
git init
```

### 2. 檢查檔案狀態

```bash
git status
```

確認沒有個人資料檔案被加入追蹤。

### 3. 加入檔案

```bash
# 加入所有檔案（.gitignore 會自動過濾）
git add .

# 或手動加入特定檔案
git add convert_to_json.py
git add test_convert.py
git add requirements.txt
git add README.md
git add CONVERT_README.md
git add .gitignore
git add 程式編寫/
git add 職訓班課程/
```

### 4. 提交變更

```bash
git commit -m "feat: 新增檔案轉換為 JSON 格式工具

- 實作 PDF、TXT、MD 檔案轉換功能
- 支援自動分類和 metadata 提取
- 產生適合 Open WebUI 知識庫的 JSON 格式
- 包含完整的使用說明和測試腳本"
```

### 5. 在 GitHub 建立新倉庫

1. 前往 [GitHub](https://github.com) 登入
2. 點擊右上角 "+" → "New repository"
3. 輸入倉庫名稱（例如：`file-to-json-converter`）
4. 選擇公開或私有
5. **不要**勾選 "Initialize this repository with a README"（因為本地已有）
6. 點擊 "Create repository"

### 6. 連接遠端倉庫並推送

```bash
# 加入遠端倉庫（將 YOUR_USERNAME 和 REPO_NAME 替換為實際值）
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 推送程式碼
git branch -M main
git push -u origin main
```

## Commit Message 範例

### 初始提交

```
feat: 新增檔案轉換為 JSON 格式工具

功能：
- 支援 PDF、TXT、Markdown 檔案格式轉換
- 自動分類檔案（生平簡介、程式編寫、職訓班課程）
- 智能提取標題、摘要和關鍵字
- 產生標準化 JSON 格式輸出

技術：
- 使用 pdfplumber/PyPDF2 處理 PDF
- 支援多種文字編碼自動檢測
- 簡單規則的 metadata 提取

文件：
- 完整的 README.md 說明文件
- 詳細的使用指南（CONVERT_README.md）
- 測試腳本（test_convert.py）
```

### 後續更新

```
docs: 更新 README 說明文件

fix: 修正 PDF 提取錯誤處理

refactor: 優化檔案分類邏輯
```

## 專案描述建議（GitHub 倉庫設定）

**倉庫描述：**
```
將 PDF、TXT、MD 檔案轉換為適合 Open WebUI 知識庫使用的 JSON 格式，用於模型微調和 RAG 應用
```

**主題標籤（Topics）：**
- `python`
- `json-converter`
- `pdf-extraction`
- `rag`
- `open-webui`
- `knowledge-base`
- `file-processing`
- `nlp`

## 注意事項

1. **個人資料保護**：確保 `.gitignore` 已正確設定，避免上傳個人敏感資料
2. **檢查檔案**：上傳前使用 `git status` 確認沒有意外加入個人資料
3. **測試**：上傳前建議先測試腳本功能是否正常
4. **授權**：考慮加入 LICENSE 檔案（MIT、Apache 2.0 等）

## 後續維護

### 更新程式碼

```bash
# 修改檔案後
git add .
git commit -m "描述變更內容"
git push
```

### 新增功能

建議使用分支開發：
```bash
git checkout -b feature/new-feature
# 開發新功能
git add .
git commit -m "feat: 新增功能描述"
git push origin feature/new-feature
# 在 GitHub 建立 Pull Request
```

## 參考資源

- [Git 官方文件](https://git-scm.com/doc)
- [GitHub 指南](https://guides.github.com/)
- [如何寫好 Commit Message](https://www.conventionalcommits.org/)

