import requests
import re
from urllib import parse
header ={
    'sina':{
        'Host': parse.quote('api.xiaomingming.org'),
        'User-Agent':parse.quote('Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'),
        'Accept': parse.quote('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        'Accept-Language': parse.quote('zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
        'Accept-Encoding': parse.quote('gzip, deflate, br'),
        'Cookie': parse.quote('UM_distinctid=16cf5594a72449-0649633ba1f78a-396b4645-1fa400-16cf5594a7435b; CNZZDATA1261531716=73060751-1567484300-null%7C1567911270'),
        'Connection': parse.quote('keep-alive'),
        'Upgrade-Insecure-Requests':parse.quote('1'),
    },
    'zw':{
        'Cookie': parse.quote('PHPSESSID=eh57e62qhi0flhlc4e6nquu2l2')
    },
    'hd_iask':{
        'Host': parse.quote('api.xiaomingming.org'),
        'User-Agent':parse.quote('Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'),
        'Accept': parse.quote('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        'Accept-Language': parse.quote('zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
        'Accept-Encoding': parse.quote('gzip, deflate, br'),
        'Cookie': parse.quote('UM_distinctid=16cf5594a72449-0649633ba1f78a-396b4645-1fa400-16cf5594a7435b; CNZZDATA1261531716=73060751-1567484300-null%7C1567911270'),
        'Connection': parse.quote('keep-alive'),
        'Upgrade-Insecure-Requests':parse.quote('1'),
    }
}
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
proxies = {'http': '120.236.128.201:8060',
           'https': '120.236.128.201:8060'
           }
deplayer = {
    'sina':'https://api.xiaomingming.org/cloud/sina.php?vid={}',
    'hd_iask':'https://api.xiaomingming.org/cloud/sina.php?vid={}',
    'zw':'{}'
}
def mv(uid,type):
    try:
        if type in deplayer:
            url = deplayer[type].format(uid)
            response = requests.get(url, headers=header[type])
            if response.status_code == 200:
                if type == 'zw':
                    return innerText.first(response.text, r'url: \'(http.*?)\'', '')
                url_res = innerText.first(response.text, r'video =  \'(.*?)\'', '')
                res = requests.get(url_res,allow_redirects=False)
                return res.headers["location"]
        # response = requests.head(uid,allow_redirects=False)
        # if response.status_code == 302:
        #     url_real = response.headers["location"]
        #     return url_real
        return uid
    except:
        return uid