import requests

url = 'http://api.bilibili.com/x/relation/stat?vmid=1'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
res = requests.get(url=url,headers=header,proxies={'http':'http://180.250.12.10:80'})
# if res.status_code == 200:
#     print("1")
print(res.status_code)