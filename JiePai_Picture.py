# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 18:52:33 2017

@author: HEZHAOHUI
"""
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlencode
import re

def get_page_index(offset,keyword):
    data = {'offset':offset,
            'format':'json',
            'keyword':keyword,
            'autoload':'true',
            'count':20,
            'cur_tab':3
            }
    url = 'http://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response = requests.get(url,data=data)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except:
        print('请求索引页出错')
        return None

def get_parse_page(html):
    try:
        jd = json.loads(html)
        #print(jd)
        piclist = []
        picdic = {}
        for item in jd['data']:
            if 'title' in item:
                picdic['title'] = item['title']
                picdic['url'] = item['article_url']
                piclist.append(picdic.copy())
        return piclist
    except:
        print('解析页面出错')
        return None

def pic_page_index(pic_url):    
    try:
        pic_response = requests.get(pic_url)
        soup = BeautifulSoup(pic_response.text,'html.parser')
        patern = re.compile('gallery: {(.*)height".*?}',re.S)
        items = re.findall(patern,soup.text)
        patern2 = re.compile('{"url":"(.*?)",',re.S)
        items2 = re.findall(patern2,items[0])
        pic_request = items2[::2]
        imagelist = []
        for image in pic_request:
            resimage = image.replace('\\','')
            imagelist.append(resimage)
        return imagelist
    except:
        print('获取照片详情页出错：'+pic_url)
        return None
            
def save_pic(title,url):
    try:
        resimag = requests.get(url)
        with open(title+url[-6:-1]+'.jpg','wb') as f:
            f.write(resimag.content)
    except:
        print('保存到本地出错：'+url)
        None
        
def main(offset,keyword):
    html = get_page_index(offset,keyword)
    pic_url_list = get_parse_page(html)
    for pic_url in pic_url_list:
        url = pic_url['url']
        imagelist = pic_page_index(url)
        if imagelist:
            print('图片title: '+pic_url['title'])
            for imageurl in imagelist:
                save_pic(pic_url['title'],imageurl)
                print('正在保存: '+imageurl)

if __name__ == '__main__':
    keyword = '美女'
    pagenumber = 2
    for i in range(0,pagenumber):
        try:
            main(i*20,keyword)
        except:
            print('解析主函数出错')
            None
    
    