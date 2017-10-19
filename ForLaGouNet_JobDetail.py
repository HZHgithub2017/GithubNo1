# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 13:54:06 2017

@author: HEZHAOHUI
"""

##拉钩网 job详情页面
import requests
from bs4 import BeautifulSoup
import json
import time
def getjobdetails(jobdetailURL):
    headers={'Cookie':'user_trace_token=20171011221929-317fc5fb-ae8f-11e7-8b4a-525400f775ce; LGUID=20171011221929-317fc9fa-ae8f-11e7-8b4a-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAAAGGABCB5CBA6EC7A34CB24BF038618A2CC2D908; _gat=1; PRE_UTM=; PRE_HOST=www.sogou.com; PRE_SITE=https%3A%2F%2Fwww.sogou.com%2Flink%3Furl%3DDSOYnZeCC_qqU75nxClpCQDydjxbYhws; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; SEARCH_ID=f2727c934f73480f80def968aa8144da; _gid=GA1.2.2047759544.1507731572; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1507731572,1507801198,1507801207,1507873851; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1507873886; _ga=GA1.2.1526983715.1507731572; LGSID=20171013135048-7644fee2-afda-11e7-9526-5254005c3644; LGRID=20171013135122-8af07a89-afda-11e7-9526-5254005c3644',
                     'Host':'www.lagou.com',
                     'Referer':'https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=Python',
                     'Upgrade-Insecure-Requests':'1',
                     'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
                    }
    res = requests.get(jobdetailURL,headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    job_info = {}
    job_info['jobname'] = soup.select('.job-name')[0]['title']
    job_info['company'] = soup.select('.company')[0].text
    job_info['salary'] = soup.select('.job_request p')[0].contents[1].text
    job_info['experience'] = soup.select('.job_request p')[0].contents[5].text.rstrip(' /')
    job_info['education'] = soup.select('.job_request p')[0].contents[7].text.rstrip(' /')
    article = []
    for p in soup.select('.job_bt p'):
        article.append(p.text)
    job_info['requests'] = '\n'.join(article)
    job_info['addres'] = soup.select('.work_addr')[0].contents[-3].strip().lstrip('- ')
    return job_info
    print('+')
#
#b = getjobdetails('https://www.lagou.com/jobs/3447959.html')

##z找到得到jobid的方法
def getalldetails(x):
    JobURL = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false&isSchoolJob=0'
    URL = 'https://www.lagou.com/jobs/{}.html'
    net_headers = {'Cookie':'user_trace_token=20171011221929-317fc5fb-ae8f-11e7-8b4a-525400f775ce; LGUID=20171011221929-317fc9fa-ae8f-11e7-8b4a-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAAAGGABCB5CBA6EC7A34CB24BF038618A2CC2D908; X_HTTP_TOKEN=7f301410e85ff164023ce46cba8190a3; _gid=GA1.2.2047759544.1507731572; _ga=GA1.2.1526983715.1507731572; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1507731572,1507801198,1507801207,1507873851; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1507879223; LGSID=20171013145226-129afc89-afe3-11e7-9528-5254005c3644; LGRID=20171013152019-f7c93fa3-afe6-11e7-9528-5254005c3644; TG-TRACK-CODE=search_code; SEARCH_ID=790aa03f93104a8bae9c87d7d59b13d6',
                           'Host':'www.lagou.com',
                           'Referer':'https://www.lagou.com/jobs/list_PYTHON?labelWords=&fromSearch=true&suginput=',
                           'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
                           'X-Anit-Forge-Code':'0',
                           'X-Anit-Forge-Token':None,
                           'X-Requested-With':'XMLHttpRequest'
                           }
    net_data = {'first':'true',
                        'pn':x,
                        'kd':'PYTHON'
                        }
    res = requests.post(JobURL,headers=net_headers,data=net_data)
    res.encoding = 'utf-8'
    jd = json.loads(res.text)
    URL_pg = []
    job_pg = []
    for i in jd['content']['positionResult']['result']:
        idnumber = i['positionId']
        newURL = URL.format(idnumber)
        URL_pg.append(newURL)
#    for j in URL_pg:
#        print(j)
    job_pg.append(getjobdetails(URL_pg[0]))
    time.sleep(20)   
    return job_pg
##这就很尴尬，操作过于频繁！！！暂时不知道怎么解决
alldetails = []
for x in range(0,5):
    alldetails.append(getalldetails(x))
        