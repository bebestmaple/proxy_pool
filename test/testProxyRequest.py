import requests


def get_proxy():
    return requests.get("http://127.0.0.1:8010/get?type=https").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:8010/delete/?proxy={}".format(proxy))


# your spider code

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get('https://www.example.com',
                                proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
            # 删除代理池中代理
            delete_proxy(proxy)
    return None


if __name__ == '__main__':
    success_proxy_count = 0
    for i in range(0, 10):
        html = getHtml()
        print("try times %d,status code: %d" % (i, 4003 if html is None else html.status_code))
        if html and html.status_code == 200:
            success_proxy_count += 1

    print(success_proxy_count)
