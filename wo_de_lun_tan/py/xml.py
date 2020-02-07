import time
def sitemap(data):
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:mobile="http://www.baidu.com/schemas/sitemap-mobile/1/">
    <url>
     <loc>https://xn--by-6y6c831p.cn/sitemap</loc>
     <mobile:mobile type="pc,mobile"/>
     <priority>0.5</priority>
     <lastmod>{time_but}</lastmod>
     <changefreq>always</changefreq>
    </url>
    <url>
     <loc>https://www.xn--by-6y6c831p.cn/</loc>
     <mobile:mobile type="pc,mobile"/>
     <priority>0.5</priority>
     <lastmod>{time_but}</lastmod>
     <changefreq>always</changefreq>
    </url>
    <url>
     <loc>https://www.xn--by-6y6c831p.cn/</loc>
     <mobile:mobile type="pc,mobile"/>
     <priority>0.5</priority>
     <lastmod>{time_but}</lastmod>
     <changefreq>always</changefreq>
    </url>
    <url>
     <loc>https://www.xn--by-6y6c831p.cn/zi_yuan/time_tb</loc>
     <mobile:mobile type="pc,mobile"/>
     <priority>0.5</priority>
     <lastmod>{time_but}</lastmod>
     <changefreq>always</changefreq>
    </url>
    <url>
     <loc>https://www.xn--by-6y6c831p.cn/zi_yuan/fen_lei</loc>
     <mobile:mobile type="pc,mobile"/>
     <priority>0.5</priority>
     <lastmod>{time_but}</lastmod>
     <changefreq>always</changefreq>
    </url>
    <url>
     <loc>https://www.xn--by-6y6c831p.cn/</loc>
     <mobile:mobile type="pc,mobile"/>
     <priority>0.5</priority>
     <lastmod>{time_but}</lastmod>
     <changefreq>always</changefreq>
    </url>
    <url>
     <loc>https://www.xn--by-6y6c831p.cn/index</loc>
     <mobile:mobile type="pc,mobile"/>
     <priority>0.5</priority>
     <lastmod>{time_but}</lastmod>
     <changefreq>always</changefreq>
    </url>
    <url>
     <loc>https://xn--by-6y6c831p.cn/user/1</loc>
     <mobile:mobile type="pc,mobile"/>
     <priority>0.5</priority>
     <lastmod>{time_but}</lastmod>
     <changefreq>always</changefreq>
    </url>
    <url>
     <loc>https://www.xn--by-6y6c831p.cn/deng_lu</loc>
     <mobile:mobile type="pc,mobile"/>
     <priority>0.5</priority>
     <lastmod>{time_but}</lastmod>
     <changefreq>{time_but}</changefreq>
    </url>
    {other}
    </urlset>'''
    res = ''
    time_cur = time.strftime("%Y-%m-%d", time.localtime())
    if data:
        for i in data:
            try:
                num = len(data[i]['path0'].split('@@'))-1
                res += '''<url>
                    <loc>https://www.xn--by-6y6c831p.cn/ziYuanDetail/{}/0/{}</loc>
                    <mobile:mobile type="pc,mobile"/>
                    <priority>0.5</priority>
                    <lastmod>{}</lastmod>
                    <changefreq>always</changefreq>
                    </url>'''.format(data[i]['id'],num,time_cur)
            except:
                continue
    return xml.format(time_but = time_cur,other = res)
