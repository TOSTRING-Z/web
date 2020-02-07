import os
import requests
from requests.exceptions import RequestException
import re
import random
from urllib import parse
headers =[{
        'Host': 'www.baidu.com',
        'User-Agent': parse.quote('Mozilla/5.0 (Android 8.1.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0'),
        'Accept': parse.quote('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        'Accept-Language': parse.quote('zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
        'Accept-Encoding': parse.quote('gzip, deflate, br'),
        'Cache - Control': parse.quote('max - age = 0'),
        'Cookie': parse.quote(
            'BAIDUID=8EA3197B6BBA827AA4881F9DC9F18717:FG=1; BIDUPSID=8EA3197B6BBA827AA4881F9DC9F18717; PSTM=1568003583; BD_UPN=133352; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; H_PS_PSSID=1450_21099_29523_29568_29221; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a03192491211; BDUSS=I4RHVVRWJBTWdFbi15UDIwZTdBbktDbkVFZkZINGQyNzN0WjZUN0NKQm5DYkJkRVFBQUFBJCQAAAAAABAAAAEAAABW6gP9AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGd8iF1nfIhdNj; H_PS_645EC=50e9RFHqC%2FloskL%2FOU36%2BuFuMyP3PGSMzKmudY7P1biXNytI7e5KcZ8ZyXpFnxQLh8%2BL; BDRCVFR[gltLrB7qNCt]=mk3SLVN4HKm; delPer=0; BD_CK_SAM=1; PSINO=2; COOKIE_SESSION=2563_0_7_4_10_5_0_0_6_2_0_1_2721_0_161_0_1569247296_0_1569247135%7C9%230_1_1568181477%7C1'),
        'Connection': parse.quote('keep-alive'),
        'Upgrade-Insecure-Requests': parse.quote('1'),
        },{
                'Host': parse.quote('www.xn--by-6y6c831p.cn'),
                'User-Agent': parse.quote('Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'),
                'Accept': parse.quote('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                'Accept-Language': parse.quote('zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
                'Accept-Encoding': parse.quote('gzip, deflate, br'),
                'Referer': parse.quote('{}'.format('')),
                'Connection': parse.quote('keep-alive'),
                'Cookie': parse.quote('wordpress_logged_in_e4d9fd6fd0c2eaccb652e324dd159e22=root%7C1570106119%7CV3hRFlLsZbrj1BDubT4Na0THVlqMIv1VK79LDx1YKp8%7C0094cbe6d8fbf5905b31a79593fbe8e1ff8e33501114aa9d0f5f700d20b6853d'),
                'Upgrade-Insecure-Requests': parse.quote('1')
            }]
proxies = {
    'http': '112.250.107.37:53281',
    'https': '112.250.107.37:53281'
}
def get_one_page(url,h):

    try:
        response=requests.get(url,headers = h)
        if response.status_code == 200:
            r=response.text
            #a=r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
            return r
        return None
    except RequestException:
        return None
class innerText:
    def first(html_in,pattern,split_sel):
        result = re.search(r'{0}'.format(pattern), html_in, re.DOTALL)
        if result:
            result_groups = result.groups()
            return split_sel.join(result_groups)
        return None
    def all(html_in,pattern,split_sel):
        result = re.findall(r'{0}'.format(pattern), html_in, re.DOTALL)
        if result:
            return split_sel.join(result)
        return None
if __name__ == '__main__':
    for t in range(0,10000):
        url = 'https://www.baidu.com/baidu?wd=site%3Axn--by-6y6c831p.cn&tn=monline_4_dg&ie=utf-8'.format(t)
        html_show = get_one_page(url,headers[0])
        if html_show:
            up_ip = innerText.first(html_show, '"title":"萌咔萌咔 ","url":"(.*?)"', '')
            a = get_one_page(up_ip,headers[0])
            print(a)