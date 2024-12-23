import requests
import httpx

# 定义 URL 和请求头
url = "https://www.hao6v.tv/e/search/index.php"

# 请求头信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=GB2312'
}

# 关键字
keyword = "凡人歌".encode('gb2312')  # 将关键字转换为 GB2312 编码

# 表单数据
data = {
    'show': 'title,smalltext',
    'tempid': '1',
    'keyboard': keyword,  # 转换后的关键字
    'tbname': 'article',
    'x': '42',
    'y': '11',
}

# 使用 Requests 发送请求
response = requests.post(url, data=data)

print(response.text)