import os
import requests
from requests.exceptions import RequestException
import re
import random
def get_one_page(url):
    a = random.randint(10, 180)
    b = random.randint(1, 227)
    c = random.randint(11, 128)
    d = random.randint(11, 253)
    header = {
        'Host': parse.quote('api.xiaomingming.org'),
        'User-Agent': parse.quote('Mozilla/5.0 (Android 8.1.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0'),
        'Accept': parse.quote('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        'Accept-Language': parse.quote('zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
        'Accept-Encoding': parse.quote('gzip, deflate, br'),
        'Cookie': parse.quote(
            'UM_distinctid=16cf5594a72449-0649633ba1f78a-396b4645-1fa400-16cf5594a7435b; CNZZDATA1261531716=73060751-1567484300-null%7C1567911270'),
        'Connection': parse.quote('keep-alive'),
        'Upgrade-Insecure-Requests': parse.quote('1'),
    }
    proxies = {
        'http': '{}.{}.{}.{}'.format(a,b,c,d),
        'https': '{}.{}.{}.{}'.format(a,b,c,d)
    }
    try:
        response=requests.get(url = url,header = header,proxies = proxies)
        if response.status_code == 200:
            r=response.text
            a=r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
            return a
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
        html_show = get_one_page(url)
        if html_show:
            up_ip = innerText.first(html_show, '<a target="_blank" href="(.*?)".*?>https://www.xn--by-6y6c831p.cn/', '')
            a = get_one_page(up_ip)
            print(a)