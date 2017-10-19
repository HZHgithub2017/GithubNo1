# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:03:53 2017

@author: HEZHAOHUI
"""
##自己爬取猫眼Top100
import requests
from bs4 import BeautifulSoup
import json
from requests.exceptions import RequestException
def get_one_page(offset):
    try:
        url = 'http://maoyan.com/board/4?offset={}'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
                }
        response = requests.get(url.format(offset),headers=headers)
        soup = BeautifulSoup(response.text,'html.parser')
        listonepage = []
        dic = {}
        for li in soup.select('.board-item-content'):
            dic['name'] = li.select('a')[0]['title']
            dic['actor'] = li.select('.star')[0].text.strip()
            dic['time'] = li.select('.releasetime')[0].text
            dic['score'] = li.select('.score')[0].contents[0].text+li.select('.score')[0].contents[1].text
            listonepage.append(dic.copy())
            with open ('top100.txt','a',encoding='utf-8') as f:
                f.write(json.dumps(dic,ensure_ascii=False)+'\n')
                f.close()
    except RequestException: 
        None
def main():
    for i in range(0,10):
        get_one_page(i*10)

if __name__ =='__main__':
    main()