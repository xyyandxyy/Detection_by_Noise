"""
这个代码是用来获取所有设备的url
"""

import requests
from bs4 import BeautifulSoup

# 定义目标网页的URL
url = "https://www.dpreview.com/sample-galleries"

# 发送GET请求获取网页内容
response = requests.get(url)

# 使用Beautiful Soup解析网页内容
soup = BeautifulSoup(response.content, 'html.parser')

# 找到所有<tr>元素，其中class="gallery"
gallery_elements = soup.find_all("tr", class_="gallery")

# 创建一个空列表来存储链接
links = []

# 遍历每个<tr>元素，提取其中的链接
for gallery in gallery_elements:
    # 找到包含链接的<a>元素
    link_element = gallery.find("a")
    
    # 提取链接的href属性值
    link = link_element.get("href")
    
    # 添加链接到列表中
    links.append(link)

# 打印链接列表
print(links)
