import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
import MySQLdb
db = MySQLdb.connect("localhost", "root", "20001101", "bilibiliuser", charset='utf8' )
cursor = db.cursor()
try:
    sqqll = """TRUNCATE TABLE proxyIp"""
    cursor.execute(sqqll)
    db.commit()
    print("Initiation Success")
except:
    db.rollback()
    print("Initiation Failed")
class proxyIp:
    def __init__(self):
        self.url = 'http://www.xiladaili.com/gaoni/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        self.list1 = []
        self.okList1 = []

    def get_url(self):
        for index in range(50):               #此处设置为要爬多少页的代理IP
            time.sleep(3)
            try:
                res = requests.get(self.url if index == 0 else self.url + str(index) + "/",headers=self.headers,timeout=10).text
            except:
                print("Request IpWeb error!")
                continue
            ip_data = etree.HTML(res).xpath("//*[@class='mt-0 mb-2 table-responsive']/table/tbody/tr/td[1]")
            score_data = etree.HTML(res).xpath("//*[@class='mt-0 mb-2 table-responsive']/table/tbody/tr/td[8]")
            for i, j in zip(ip_data, score_data):
                score = int(j.text)
                if score > 10000:
                    self.list1.append(i.text)
            set(self.list1)
        for i in self.list1:
            try:
                res = requests.get(url='http://api.bilibili.com/x/relation/stat?vmid=1',proxies={'http':'http://' + i},timeout=10)
                if res.status_code == 200:
                    try:
                        sql = """INSERT INTO proxyIp(Ip) VALUES ('{}')""".format(i)
                        cursor.execute(sql)
                        db.commit()
                        print("Insert Success")
                        # print(requests.get(url='https://www.baidu.com/s?wd=ip',headers=self.headers,proxies={'http':'http://' + i}).text)
                        # exit()
                    except:
                        db.rollback()
                        print("Insert Failed")
            except:
                print("This Ip is dead")
                continue
        return 1
    def run(self):
        return self.get_url()


if __name__ == '__main__':
    findIp = proxyIp()
    print(findIp.run())