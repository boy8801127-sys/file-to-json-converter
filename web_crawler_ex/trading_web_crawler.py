'''
開始
  ↓
找到所有 news_blocks（例如：30 個區塊）
  ↓
第 1 次迴圈：block = 第 1 個區塊
  ↓
找到父層的 <a> 標籤 → link
  ↓
取得連結網址 → href = "/news/xxx.aspx"
  ↓
補齊網址 → href = "https://www.cna.com.tw/news/xxx.aspx"
  ↓
在 block 裡面找 <h2> → h2
  ↓
在 h2 裡面找 <span> → span
  ↓
取得標題文字 → title = "新聞標題"
  ↓
顯示：標題和連結
  ↓
第 2 次迴圈：block = 第 2 個區塊
  ↓
...（重複以上步驟）
  ↓
結束
'''

import requests
from bs4 import BeautifulSoup

# 取得網頁
response = requests.get("https://www.cna.com.tw/list/aall.aspx")
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有新聞區塊（div class="listInfo"）
news_blocks = soup.find_all('div', class_='listInfo')

# 提取每一則新聞
for block in news_blocks:
    # 找到父層的 <a> 標籤（連結）
    link = block.find_parent('a')
    
    if link:
        # 取得連結網址
        href = link.get('href')
        
        # 補齊完整網址（如果是相對路徑）
        if href and not href.startswith('http'):
            href = 'https://www.cna.com.tw' + href
        
        # 取得標題（在 h2 > span 裡面）
        h2 = block.find('h2')
        if h2:
            span = h2.find('span')
            if span:
                title = span.text.strip()
                
                # 顯示結果
                print(f"標題：{title}")
                print(f"連結：{href}")
                print("-" * 60)