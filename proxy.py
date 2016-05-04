#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import re

try:
    # python 2
    from urllib2 import Request, urlopen
except ImportError:
    # python 3
    from urllib.request import Request, urlopen


def _process(content):
    proxies = []
    proxies_raw = re.findall(
        r'<tr\s+class=\"(|odd)\">(.*?)</tr>', content, re.M | re.I | re.S)
    for proxy_raw in proxies_raw:
        if len(proxy_raw) == 2:
            field = re.findall(
                r'<td(|\s+class="country")>(.*?)</td>', proxy_raw[1], re.M | re.I | re.S)
        else:
            field = re.findall(
                r'<td(|\s+class="country")>(.*?)</td>', proxy_raw, re.M | re.I | re.S)
        proxies.append(_convert_to_object(field))
    return proxies


def _convert_to_object(data):
    item = {}
    country = re.findall(r'\w+?.png', data[0][1])
    item['country'] = ''.join(country).split('.')[0]
    item['ip'] = data[1][1]
    item['port'] = data[2][1]
    item['location'] = data[3][1]
    item['is_anonymous'] = data[4][1]
    item['type'] = data[5][1]
    item['last_check_date'] = data[6][1]
    return item


def _to_json(data=[]):
    return json.dumps(data, ensure_ascii=False)


def _request(url):
    req = Request(url)
    req.add_header(
        'User-Agent', "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0")
    req.add_header(
        'Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    req.add_header('Accept-Language', "en-US,en;q=0.5")
    resp = urlopen(req)

    return resp.read()


def main():
    url = 'http://www.xicidaili.com/'
    content = _request(url)
    proxies = _process(content)
    jsonstr = _to_json(proxies)
    with open('proxy_data.json', 'w+') as f:
        f.write(jsonstr)


if __name__ == '__main__':
    main()
