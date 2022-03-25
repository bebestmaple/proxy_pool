# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

import os.path
import re
import urllib
from time import sleep

import pytesseract

from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        米扑代理 https://proxy.mimvp.com/
        :return:
        """
        url_list = [
            'https://proxy.mimvp.com/freeopen?proxy=in_hp',
            'https://proxy.mimvp.com/freeopen?proxy=out_hp'
        ]
        for url in url_list:
            html_tree = WebRequest().get(url).tree
            for tr in html_tree.xpath(".//table[@class='mimvp-tbl free-proxylist-tbl']/tbody/tr"):
                try:
                    ip = ''.join(tr.xpath('./td[2]/text()'))
                    port_img_url = 'https://proxy.mimvp.com' + ( ''.join(tr.xpath('./td[3]/img/@src')))
                    port_img_name = port_img_url.split('port=')[-1]
                    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../cache/freeopen_port_image/%s.png" % port_img_name))
                    if not os.path.exists(img_path):
                        urllib.request.urlretrieve(port_img_url, filename=img_path)
                    port = pytesseract.image_to_string(img_path)
                    if port:
                        yield '%s:%s' % (ip, port)
                except Exception as e:
                    print(e)

    @staticmethod
    def freeProxy02():
        """
        代理66 http://www.66ip.cn/
        :return:
        """
        url = "http://www.66ip.cn/mo.php"

        resp = WebRequest().get(url, timeout=10)
        proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})', resp.text)
        for proxy in proxies:
            yield proxy

    @staticmethod
    def freeProxy03(page_count=10):
        """ 开心代理 """
        target_urls = ["http://www.kxdaili.com/dailiip.html"]

        for url in target_urls:
            tree = WebRequest().get(url).tree
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                yield "%s:%s" % (ip, port)

        page = 1
        while page < page_count:
            url = "http://www.kxdaili.com/dailiip/2/%d.html" % page
            tree = WebRequest().get(url).tree
            trs = tree.xpath("//table[@class='active']//tr")[1:]
            if not trs:
                break
            for tr in trs:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                yield "%s:%s" % (ip, port)
            sleep(1)
            page += 1

    @staticmethod
    def freeProxy04(page_count=10):
        """ 蝶鸟IP """
        page = 1
        while page < page_count:
            url = "https://www.dieniao.com/FreeProxy/%d.html" % page
            tree = WebRequest().get(url, verify=False).tree
            trs = tree.xpath("//div[@class='free-main col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li")[1:]
            if not trs:
                break
            for li in trs:
                ip = "".join(li.xpath('./span[1]/text()')).strip()
                port = "".join(li.xpath('./span[2]/text()')).strip()
                if ip and port:
                    yield "%s:%s" % (ip, port)
            sleep(1)
            page += 1

    @staticmethod
    def freeProxy05(page_count=1):
        """ 快代理 https://www.kuaidaili.com """
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxy06():
        """ PROXY11 https://proxy11.com """
        url = "https://proxy11.com/api/demoweb/proxy.json?country=hk&speed=2000"
        try:
            resp_json = WebRequest().get(url).json
            for each in resp_json.get("data", []):
                yield "%s:%s" % (each.get("ip", ""), each.get("port", ""))
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy07(page_count=10):
        """ 云代理 """
        page = 1
        while page < page_count:
            url = "http://www.ip3366.net/free/?page=%d" % 1
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            if not proxies:
                break
            for proxy in proxies:
                yield ":".join(proxy)
            sleep(1)
            page += 1

    @staticmethod
    def freeProxy08():
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        }
        base_url = 'https://free-proxy-list.com/?search=1&port=&type[]=http&speed[]=2&speed[]=3&connect_time[]=2&connect_time[]=3&up_time=0&search=Search&page='
        page = 1
        while True:
            url = base_url + str(page)
            try:
                resp = WebRequest().get(url, headers=headers)
                resp.raise_for_status()
                proxies = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', resp.text)
                if proxies is not None and len(proxies) > 0:
                    for proxy in proxies:
                        yield proxy
                else:
                    break
            except:
                pass

            page += 1

    @staticmethod
    def freeProxy09(page_count=10):
        """ 免费代理库 """
        page = 1
        while page <= page_count:
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(page)
            html_tree = WebRequest().get(url).tree
            trs = html_tree.xpath("//table//tr")
            if len(trs) <= 1:
                break
            for index, tr in enumerate(trs):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()
            sleep(1)
            page += 1

    @staticmethod
    def freeProxy10(page_count=10):
        """ 89免费代理 """
        page = 1
        while page < page_count:
            url = "https://www.89ip.cn/index_%d.html" % page
            r = WebRequest().get(url, timeout=3)
            proxies = re.findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                r.text)
            if not proxies:
                break
            for proxy in proxies:
                yield ':'.join(proxy)
            sleep(1)
            page += 1

    @staticmethod
    def wallProxy11():
        """
        PzzQz https://pzzqz.com/
        """
        from requests import Session
        from lxml import etree
        session = Session()
        try:
            index_resp = session.get("https://pzzqz.com/", timeout=20, verify=False).text
            x_csrf_token = re.findall('X-CSRFToken": "(.*?)"', index_resp)
            if x_csrf_token:
                data = {"http": "on", "ping": "300", "country": "us", "ports": ""}
                proxy_resp = session.post("https://pzzqz.com/", verify=False,
                                          headers={"X-CSRFToken": x_csrf_token[0]}, json=data).json()
                tree = etree.HTML(proxy_resp["proxy_html"])
                for tr in tree.xpath("//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()"))
                    port = "".join(tr.xpath("./td[2]/text()"))
                    yield "%s:%s" % (ip, port)
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy12():
        urls = [
            'https://free-proxy-list.net/',
            'https://www.us-proxy.org/',
            'https://free-proxy-list.net/uk-proxy.html',
            'https://www.sslproxies.org/',
            'https://free-proxy-list.net/anonymous-proxy.html',
        ]

        for url in urls:
            resp = WebRequest().get(url, timeout=10, proxies={
                "http": "socks5://host.docker.internal:10808",
                "https": "socks5://host.docker.internal:10808",
            })
            proxies = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', resp.text)
            for proxy in proxies:
                yield proxy

    @staticmethod
    def freeProxy13():
        base_url = 'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-'
        page = 1
        while True:
            url = base_url + str(page)
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            if len(proxies) == 0:
                break
            for proxy in proxies:
                yield ':'.join(proxy)
            page += 1


# if __name__ == '__main__':
#     p = ProxyFetcher()
#     for _ in p.freeProxy11():
#         print(_)

# http://nntime.com/proxy-list-01.htm
