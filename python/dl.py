# coding=utf-8
import urllib
import random
import time
import requests


def dl():
    a1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'}
    o_g = ['114.239.3.149:808', '61.232.254.39:3128', '218.18.232.29:8080']
    a = 0
    for a in range(0, 3):
        proxies_l = {'http': o_g[a]}
        print(proxies_l['http'])

        try:
            req = requests.get('http://httpbin.org/ip', headers=a1, proxies=proxies_l)
            print('finish')
            print(req.text)
        except:
            print('no proxies')
        sleep_time = random.randint(1, 3)
        time.sleep(sleep_time)
        print('Wait%ds' % sleep_time)


dl()
