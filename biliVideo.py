import requests
from bs4 import BeautifulSoup
from bilibili_api import video
from bilibili_api import user
from bilibili_api import live
import MySQLdb
import time

db = MySQLdb.connect("localhost", "root", "20001101", "bilibiliuser", charset='utf8' )
cursor = db.cursor()

for i in range(31203,1000000):
    try:
        time.sleep(0.5)
        print(i)
        userInfo = user.get_relation_info(i)
        if userInfo['follower'] >= 100000:
            uMid = str(userInfo['mid'])
            uName = str(user.get_user_info(i)['name'])
            uFans = int(userInfo['follower'])
            try:
                sql = """INSERT INTO biliUser(Uid,Uname, Ufans) VALUES ('{}', '{}', {})""".format(uMid,uName,uFans)
                cursor.execute(sql)
                db.commit()
                print("yes")
            except:
                db.rollback()
                print("no")
    except:
        print("Requests error")
        i -= 1
        time.sleep(5)
        continue
db.close()
print("It's end!")
exit(0)