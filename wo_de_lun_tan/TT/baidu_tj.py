import js2py
import requests
from urllib import parse
import random
import time
def header(i):
    headers = {
            'Host': parse.quote('sp0.baidu.com'),
            'User-Agent':parse.quote('Mozilla/5.0 (X11; Linux x86_64…) Gecko/20100101 Firefox/69.0'),
            'Accept': parse.quote('image/webp,*/*'),
            'Accept-Language': parse.quote('zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
            'Accept-Encoding': parse.quote('gzip, deflate, br'),
            'Cookie': parse.quote('BAIDUID=8EA3197B6BBA827AA4881F9DC9F18717:FG=1; BIDUPSID=8EA3197B6BBA827AA4881F9DC9F18717; PSTM=1568003583; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDUSS=I4RHVVRWJBTWdFbi15UDIwZTdBbktDbkVFZkZINGQyNzN0WjZUN0NKQm5DYkJkRVFBQUFBJCQAAAAAABAAAAEAAABW6gP9AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGd8iF1nfIhdNj; H_PS_PSSID=1450_21099_29523_29568_29221; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a03194698733; delPer=0; PSINO=2; BDRCVFR[gltLrB7qNCt]=mk3SLVN4HKm; BDSFRCVID=ActsJeCCxG3jBnJwZK4-EtIllD084lzbh8Ef3J; H_BDCLCKID_SF=tRk8oI0aJDvjDb7GbKTMbtCSbfTJetJyaROhQJ7E-b7hqRONHtJb24tWqGKHJ6DDtJkXoD_htDDKMTu4D6LKDjjWJloJ2lRL5Cn0LRCBK-Jf245mhqnEb5us5p62-KCHtJCHoC_5HD_KhD_lD6t_D6jLDGLHt5nCK5neaJ5n0-nnhncthx6bWxn3qtoJB47Q3n4O_nRLKJPWsJLRy66jK4JKDH8eJTvP; uc_login_unique=09838f0c5b9a563d2294ad7153c9c15a; uc_recom_mark=cmVjb21tYXJrXzI4OTQ5MDk4'),
            'Connection': parse.quote('keep-alive'),
            'Referer': parse.quote('https://xn--by-6y6c831p.cn/ziYuanDetail/{}/0/0'.format(i))
        }
url = 'https://sp0.baidu.com/9_Q4simg2RQJ8t7jm9iCKT-xh_/s.gif?r=https%3A%2F%2Fxn--by-6y6c831p.cn%2F&l=https://xn--by-6y6c831p.cn/ziYuanDetail/{}/0/0'
#tj = js2py.eval_js(js)
for i in range(1,200):
    sleep_time = random.randint(1, 3)
    time.sleep(sleep_time)
    response = requests.get(url.format(i),headers = header(i))
    if response.status_code == 200:
        print(response.headers)
