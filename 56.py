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



def getProxyIp():
    searchIpSql = "SELECT Ip FROM proxyip"
    cursor.execute(searchIpSql)
    proxy = cursor.fetchall()
    return proxy

# 读取用户ID和粉丝数
async def getuMid(session,mid):
    async with session.get(MidUrl + str(mid),proxy="http://80.241.222.138:80") as response:
        print(response.status)
        return await response.text()


# 读取用户名和用户头像
async def getuName(session,mid):
    async with session.get(NameUrl + str(mid),proxy="http://80.241.222.138:80") as response:
        print(response.status)
        return await response.text()

# 将读取到的数据写入数据库
async def insertDB(data1,data2):
    uMid = str(data1['data']['mid'])
    uFans = int(data1['data']['follower'])
    uName = str(data2['data']['name'])
    uFace = str(data2['data']['face'])
    if uFans > 100000:
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
    i = True
    while i:
        async with aiohttp.ClientSession() as session:
            html1 = await getuMid(session, mid)
            html2 = await getuName(session, mid)
            print(html1)
            print(html2)
            if html1 and html2:
                data1 = json.loads(html1)
                data2 = json.loads(html2)
                await insertDB(data1, data2)
            else:
                i = False
            i = False
    else:
        print("This Proxy is Dead!")

if __name__ == '__main__':
    N = 3
    loop = asyncio.get_event_loop()
    future = [asyncio.ensure_future(getBiliWeb(mid)) for mid in range(2, N)]
    res = loop.run_until_complete(asyncio.gather(*future))