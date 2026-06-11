from turtle import title
import requests
from bs4 import BeautifulSoup


    url = "https://www.cna.com.tw/list/aall.aspx"
    response = requests.get(url, timeout=10)
    response.encoding = 'utf-8'  # 確保中文正確顯示
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到所有即時新聞區塊
    news_blocks = soup.find_all('div', class_='listInfo')
    print(news_blocks) #看是否能找到即時新聞的標題頁面

    # 提取標題和連結
    news_list = []
    for block in news_blocks:
        title = block.find('span')
        
    print(title)