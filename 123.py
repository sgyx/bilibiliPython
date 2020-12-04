import asyncio
from aiohttp import ClientSession
import time
import json
import MySQLdb
import aiohttp

MidUrl = 'http://api.bilibili.com/x/relation/stat?vmid='
NameUrl = 'http://api.bilibili.com/x/space/acc/info?mid='
urll = 'http://www.baidu.com/s?wd=ip'
db = MySQLdb.connect("localhost", "root", "20001101", "bilibiliuser", charset='utf8' )
cursor = db.cursor()
print("1")

#
#
#
# async def getBiliList(mid):
#     print('{}\t{}'.format(mid, time.time()))
#     async with ClientSession() as session:
#         proxy = getProxyIp()
#         for proxyip in proxy:
#             print(proxyip[0])
#             async with session.get(url + str(mid),proxy='http://' + proxyip[0],verify_ssl=False) as response:
#                 try:
#                     response = await response.text()
#                     data = json.loads(response)
#                 except:
#                     print("Requests uMid and uFans error!")
#                     continue
#                 if data['data'] is None:
#                     raise print("Not Data Return!")
#                 if data['data']['follower'] >= 100000:
#                     uMid = str(data['data']['mid'])
#                     uFans = int(data['data']['follower'])
#                     async with session.get(url + str(mid), proxy=proxyip[0], verify_ssl=False) as responseName:
#                         try:
#                             UserName = await responseName.text()
#                             data2 = json.loads(UserName)
#                         except:
#                             print("Requests uName and uFace error!")
#                             continue
#                         if data['data'] is None:
#                             raise print("Request Error,Not Data Return!")
#                         uName = str(data2['data']['name'])
#                         uFace = str(data2['data']['face'])
#                         try:
#                             sql = "INSERT INTO biliUser(Uid,Uname, Ufans, Uface) VALUES ('{}', '{}', {},'{}')".format(uMid, uName,uFans,uFace)
#                             cursor.execute(sql)
#                             db.commit()
#                             print("Insert Success!")
#                         except:
#                             db.rollback()
#                             print("Insert Fail")

# 获取代理IP池
def getProxyIp():
    searchIpSql = "SELECT Ip FROM proxyip"
    cursor.execute(searchIpSql)
    proxy = cursor.fetchall()
    return proxy

# 读取用户ID和粉丝数
async def getuMid(session,mid, ip):
    try:
        print(ip[0])
        async with session.get(MidUrl + str(mid), proxy='http://' + ip[0]) as response:
            return await response.read()
    except:
        print("getuMid failed")
        return False


# 读取用户名和用户头像
async def getuName(session,mid, ip):
    try:
        print(ip[0])
        async with session.get(NameUrl + str(mid), proxy='http://' + ip[0]) as response:
            return await response.read()
    except:
        print("getuName failed")
        return False


# 将读取到的数据写入数据库
async def insertDB(data1,data2):
    uMid = str(data1['data']['mid'])
    uFans = int(data1['data']['follower'])
    uName = str(data2['data']['name'])
    uFace = str(data2['data']['face'])
    try:
        sql = "INSERT INTO biliUser(Uid,Uname, Ufans, Uface) VALUES ('{}', '{}', {},'{}')".format(uMid, uName,uFans,uFace)
        cursor.execute(sql)
        db.commit()
        print("Insert Success!")
    except:
        db.rollback()
        print("Insert Fail")



# 总体控制
async def getBiliWeb(mid):
    proxy = getProxyIp()
    for ip in proxy:
        i = True
        while i:
            async with aiohttp.ClientSession() as session:
                html1 = await getuMid(session, mid, ip)
                html2 = await getuName(session, mid, ip)
                print(html1)
                print(html2)
                if html1 and html2:
                    data1 = json.loads(html1)
                    data2 = json.loads(html2)
                    await insertDB(data1, data2)
                else:
                    i = False
        else:
            print("This Proxy is Dead!")

if __name__ == '__main__':
    N = 2
    loop = asyncio.get_event_loop()
    future = [asyncio.ensure_future(getBiliWeb(mid)) for mid in range(1, N)]
    res = loop.run_until_complete(asyncio.gather(*future))
