# # -*- coding: utf-8 -*-
# '''
# @Created on 2017-11-25 16:31:36

# @author: 许瑞锐
# '''
# import random,requests,time,re
# from spider import user_agent,database


# def get_random_header():
#     headers={'User-Agent':random.choice(user_agent.list),'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",'Accept-Encoding':'gzip'}
#     return headers

# def   scraw_proxies(page_num,scraw_url="http://www.xicidaili.com/nt/"):
#     scraw_ip=list()
#     available_ip=list()
#     for page in range(1,page_num):
#         print("抓取第%d页代理IP" %page)
#         url=scraw_url+str(page)
#         r=requests.get(url,headers=get_random_header())
#         r.encoding='utf-8'
#         pattern = re.compile('<td class="country">.*?alt="Cn" />.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', re.S)
#         scraw_ip= re.findall(pattern, r.text)
#         for ip in scraw_ip:
#             if(test_ip(ip)==True):
#                 print('%s:%s通过测试，添加进可用代理列表' %(ip[0],ip[1]))
#                 available_ip.append(ip)
#             else:
#                 pass    
#         print("代理爬虫暂停10s")
#         time.sleep(10)
#         print("爬虫重启")
#     print('抓取结束')
#     return available_ip

# def test_ip(ip,time_out,test_url='http://2017.ip138.com/ic.asp'):
#     proxies={'http': ip[0]+':'+ip[1]}
#     try_ip=ip[0]
#     #print(try_ip)
#     try:
#         r=requests.get(test_url,headers=get_random_header(),proxies=proxies,timeout=time_out)
#         if r.status_code==200:
#             r.encoding='gbk'
#             result=re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',r.text)
#             result=result.group()
#             if result[:9]==try_ip[:9]:
#                 print(r.text)
#                 print('测试通过')
#                 return True
#             else:
#                 print('%s:%s 携带代理失败,使用了本地IP' %(ip[0],ip[1]))
#                 return False    
#         else:
#             print('%s:%s 请求码不是200' %(ip[0],ip[1]))
#             return False
#     except:
#         print('%s:%s 请求过程错误' %(ip[0],ip[1]))
#         return False


# if __name__=="__main__":
#     available_ip=scraw_proxies(3)

######################
# #-*-coding:utf-8 -*-
# import urllib.request as urllib2
# from urllib.request import ProxyHandler, build_opener
# from bs4 import BeautifulSoup 
# import codecs
 
# User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
# header = {}
# header['User-Agent'] = User_Agent
 
# url = 'http://www.xicidaili.com/nn/1'
# req = urllib2.Request(url,headers=header)
# res = urllib2.urlopen(req).read()
 
# soup = BeautifulSoup(res,features="lxml")
# ips = soup.findAll('tr')
# f = codecs.open("./proxy","w", 'utf-8')
 
# for x in range(1, len(ips)):
#     ip = ips[x]
#     tds = ip.findAll("td")
#     ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]+"\n"
#     f.write(ip_temp)
# f.close()
 
# import urllib
# import socket
# socket.setdefaulttimeout(3)
# f = open("./proxy")
# fd_proxy = codecs.open("./access.txt", "w", 'utf-8')
# lines = f.readlines()
# proxys = []
# for i in range(0, len(lines)):
#     ip = lines[i].strip("\n").split("\t")
#     proxy_host = "http://" + ip[0] + ":" + ip[1]
#     proxy_temp = {"http":proxy_host}
#     proxys.append(proxy_temp)
# url = "http://ip.chinaz.com/getip.aspx"
# for proxy in proxys:
#     try:
#         proxy_handler = ProxyHandler(proxy)
#         opener = build_opener(proxy_handler)
#         res = opener.open(url, timeout=30).read()
#         # res = urllib2.urlopen(url,proxies=proxy).read()

#         fd_proxy.write(proxy["http"]+"\n")
#         print (res)
#     except Exception as e:
#         print (proxy)
#         print (e)
#         continue
# f.close()
# fd_proxy.close()

##################################################
#     from urllib.request import ProxyHandler, build_opener

#     headers = {
#         'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
#         'Accept - Encoding': 'gzip, deflate',
#         'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
#         # 'Connection': 'Keep-Alive',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# 　　　}
#  　　proxies = { "socks5": "socks5://user:pwd@ip:port" }

#     url = 'https://www.baidu.com/'

#     proxy_handler = ProxyHandler(proxies)

#     opener = build_opener(proxy_handler)
#     opener.addheaders = [(k, v) for k, v in headers.items()]
#     resp = opener.open(url, timeout=30)

#     resp_html = resp.read()
#     print(resp_html.decode())


##################################################
import requests
import os
from bs4 import BeautifulSoup
import bs4
global header
import time

header = {'User-Agent': 'Mozilla/5.0'}

def get_ip_soup(url):
    try:
        r=requests.get(url,timeout=20,headers=header)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        soup=BeautifulSoup(r.text,"html.parser")
        #print(soup)
        return soup
    except:
        print("申请错误")

ips = []
def get_list_text(soup):
    trs=soup.find("tbody").children
    for tr in trs:
        if isinstance(tr, bs4.element.Tag):
            tds=tr("td")
            http=tds[3].string
            ip=tds[0].string
            port=tds[1].string
            true_ip=http+"://"+ip+":"+port
            ips.append(true_ip)
    return ips

def deal_with_url2(soup,url):
    index=soup.find("div",{"id":"listnav"})
    lis=index("li")
    page=lis[-2].string
    print(page)

def writeFile(dir_url,ips):
    #print(ips)
    if not os.path.exists(dir_url):
        os.mkdir(dir_url)
    path=dir_url+"\\ip_list.txt"

    with open(path,"w") as f:
        for item in ips:
            f.write(item)
            f.write("\n")

def add_page(url,num):
    url_=url+"inha/"+str(num)+"/"
    return url_

if __name__ == '__main__':
    urls=["http://www.goubanjia.com/","http://www.ip181.com/","https://www.kuaidaili.com/free/","http://www.xicidaili.com/"]
    dir_url="D:\\IP_LIST"
    # ip_soup=get_ip_soup(urls[2])
    # pages=deal_with_url2(ip_soup,urls[2])#所有页数，这里只提取前五十页
    for page in range(1,51):
        time.sleep(1)
        url_ =add_page(urls[2],page)
        print(url_)
        ip_soup = get_ip_soup(url_)
        ips=get_list_text(ip_soup)

    print("共%d个"%len(ips))
    writeFile(dir_url,ips)
