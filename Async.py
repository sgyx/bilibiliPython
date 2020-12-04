import time
import asyncio
from aiohttp import ClientSession
import requests
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
tasks = []
url = "https://www.baidu.com/{}"
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
tasks = []
url = "https://movie.douban.com/top250?start={}"
async def hello(url):
    async with ClientSession() as session:
        try:

            async with session.get('http://www.ipip.net/',headers=header,proxy='http://221.122.91.65:80',verify_ssl=False) as response:
                print('Hello World:%s' % time.time())
                response = await response.text()
                print(response)
        except:
            print("1")
            pass


def run():
    for i in range(0,101,25):
        print(i)
        task = asyncio.ensure_future(hello(url.format(i)))
        tasks.append(task)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run()
    loop.run_until_complete(asyncio.wait(tasks))
# def getWeb(urll):
#     req = requests.get(url=urll, headers=header).text
#     print('Hello World:%s' % time.time())
#
# if __name__ == '__main__':
#     for i in range(5):
#         getWeb(url.format(i))