import requests

from xiaoqiangclub import get_response

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.hao6v.tv",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://www.hao6v.tv/",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
cookies = {
    "9310_4001_217.142.251.127": "1",
    "9313_3862_217.142.251.127": "1",
    "sqh6Dlastsearchtime": "1734924224",
    "9310_3588_217.142.251.127": "1",
    "9313_3992_217.142.251.127": "1",
    "richviews_9313": "t%252Bfvh5p0k%252FypAvv5NxyJrjAm1MtnRCOm7%252Bi%252BY1WtahtwxlHZJqrwvbnYe8xQGnis2P07au1NR8vwDbbXxqnPANy54F5FJfRNgsyf5xYTO60L3p6AwCs2n5phj9Gc3cbA2Cn4cwMR53aMW5%252Bs8dPDvUUvx2kXNhnjdkXn1EOQihAY6ovfFaGwjfNzleUX5lFz08ueMGCndyR8qVHk9%252FVXWLpeeQW7mvHR9GpUd4zsvO3YiC1LgoC8IE3RoDTCQW8Wv6AfxpT%252FKSk72NpzdrkSWE1aNgjJ%252BO%252BhzqMElKqP4zw9TXaLzheD3nW5eVoC56V2qsQcSB20CDsAJ0G%252F%252FoKWSA%253D%253D",
    "9313_3922_217.142.251.127": "1",
    "beitouviews_9310": "vuJQOCHRk7aCCStNr2A9ehw3oMQO7uzq6l2%252BvrbY1VyNga87%252B3NxU%252FWLoJaI022EGf9HjkDjlaCULKEIxgtNcuCkjN602dTk1jboK40bi0I9pC23N6JGXWjLXIxk1V9AufCXEwHUrAAOq91GvYFWKcnmR3c%252Fvj%252BsPF0AjTU3eWArOUplAyvdVdzsHu6M96pVkbDytyg4qgxt1rp%252FAzWGuBNqnrhncs%252FAIpmicxGd%252F9V86l4Zi2z5ih9lq7g%252BOABAR99oPthU53m5aQm2C2g%252BSK8fhu2RCyLRKmip2h9TFo7mfZi8zuVQ0I77SNYvNSflBLNhiUx%252BNmeW6IIwlX1SPA%253D%253D",
    "9310_3698_217.142.251.127": "1"
}
url = "https://www.hao6v.tv/e/search/index.php"
data = {
    "show": "title,smalltext",
    "tempid": "1",
    "keyboard": "凡人歌",
    "tbname": "article",
    "x": "41",
    "y": "15"
}
# response = requests.post(url,  data=data)

response = get_response(url,  data=data)

print(response.text)
print(response)