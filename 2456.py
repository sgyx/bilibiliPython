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
async def getuMid(session,mid,ip):
    try:
        async with session.get(MidUrl + str(mid),proxy="http://" + ip[0]) as response:
            if response.status != 200:
                return False
            return await response.text()
    except:
        return False


# 读取用户名和用户头像
async def getuName(session,mid,ip):
    try:
        async with session.get(NameUrl + str(mid),proxy="http://" + ip[0]) as response:
            if response.status != 200:
                return False
            return await response.text()
    except:
        return False
def deleProxy(ip):
    sql = "DELETE FROM proxyip WHERE Ip='{}'".format(str(ip[0]))
    try:
        cursor.execute(sql)
        db.commit()
        print("dele success")
    except:
        db.rollback()
        print("dele failed")

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
            return True
        except:
            db.rollback()
            print("Insert Fail")
            return False

# 总体控制
async def getBiliWeb(mid):
    proxy = getProxyIp()
    print(proxy)
    for ip in proxy:
        i = True
        while i:
            async with aiohttp.ClientSession() as session:
                print(ip[0])
                html1 = await getuMid(session, mid, ip)
                html2 = await getuName(session, mid, ip)
                # print(html1)
                # print(html2)
                if html1 and html2:
                    try:
                        data1 = json.loads(html1)
                        data2 = json.loads(html2)
                        isOk = await insertDB(data1, data2)
                        if isOk:
                            return 0
                    except:
                        print("Json is Filed!")
                        i = False
                else:
                    i = False
        else:
            print("This Proxy is Dead!")
            deleProxy(ip)

if __name__ == '__main__':
    N = 10
    loop = asyncio.get_event_loop()
    future = [asyncio.ensure_future(getBiliWeb(mid)) for mid in range(1, N)]
    res = loop.run_until_complete(asyncio.gather(*future))