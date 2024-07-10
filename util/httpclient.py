#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: albert
:date: 02/28/2019
:desc: http 请求工具类
"""
import logging

import requests

from config import GLOBAL_PROXY, PROXY_POOL_URL


class Request:
    def __init__(self, url, method=None, params=None, proxy=True, **kwargs):
        self.proxy = proxy
        self.url = url
        self.params = params
        self.data = None
        self.method = method
        if self.method == 'post':
            self.post(**kwargs)
        else:
            self.get(**kwargs)

    def get(self, **kwargs):
        p = proxy() if GLOBAL_PROXY and self.proxy else None
        resp = requests.get(self.url, params=self.params, verify=False, proxies=p, **kwargs)
        if resp and resp.status_code == 200:
            self.data = resp.text
        else:
            logging.warning(resp)

    def post(self, **kwargs):
        p = proxy() if GLOBAL_PROXY and self.proxy else None
        resp = requests.post(self.url, verify=False, proxies=p, **kwargs)
        if resp and resp.status_code == 200:
            self.data = resp.text
        else:
            logging.warning(resp)


def proxy():
    import json
    r = requests.get(f"{PROXY_POOL_URL}/get")
    if r and r.status_code == 200:
        p = json.loads(r.text)
        if p['https']:
            return {"http": "https://%s" % p.get("proxy")}
        else:
            return {"http": "http://%s" % p.get("proxy")}


if __name__ == '__main__':
    print(proxy())
    
