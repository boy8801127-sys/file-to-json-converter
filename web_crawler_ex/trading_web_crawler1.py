import requests
from bs4 import BeautifulSoup

# 取得網頁
url = "http://tw.people.com.cn/GB/104510/index.html"
response = requests.get(url)

# 設定編碼（人民網使用 GB2312/GBK）
response.encoding = 'utf-8'  # 或 'gbk'

# 解析 HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有新聞區塊
news_blocks = soup.find_all('li')

# 提取每一則新聞
for block in news_blocks:
    link = block.find('a')
    
    if link:
        # 取得連結
        href = link.get('href')
        if href and not href.startswith('http'):
            href = 'http://tw.people.com.cn' + href
        
        # 取得標題
        title = link.text.strip()
        
        if title:
            print(f"標題：{title}")
            print(f"連結：{href}")
            print("-" * 60)