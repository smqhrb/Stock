# test.py
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup, SoupStrainer
import traceback
import json
from lxml import etree
import re
import time

def getHtmlText(url):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        if r.encoding == 'ISO-8859-1':
            r.encoding = r.apparent_encoding
        return r.text
    except:
        traceback.print_exc()

def parseWithBeautifulSoup(html_text):
    soup = BeautifulSoup(html_text, 'html.parser') # 后改为 'lxml'
    content = []
    for mulu in soup.find_all(class_='mulu'):
        h2 = mulu.find('h2')
        if h2 != None:
            h2_title = h2.string # 获取标题
            lst = []
            for a in mulu.select('div.box a'):
                href = a.get('href')
                box_title = a.get('title')
                pattern = re.compile(r'\s*\[(.*)\]\s+(.*)') # (re) 匹配括号内的表达式，也表示一个组
                match = pattern.search(box_title)
                if match != None:
                    date = match.group(1)
                    real_title = match.group(2)
                    lst.append({'href':href,'title':real_title,'date':date})
            content.append({'title':h2_title,'content':lst})
    with open('dmbj_bs.json', 'w') as fp:
        json.dump(content, fp=fp, indent=4)

def parseWithXpath(html_text):
    html = etree.HTML(html_text)
    div_mulus = html.xpath('.//*[@class="mulu"]') # 先找到所有的 div class=mulu 标记
    content = []
    for div_mulu in div_mulus:
        # 找到所有的 div_h2 标记
        div_h2 = div_mulu.xpath('./div[@class="mulu-title"]/center/h2/text()')

        if len(div_h2) > 0:
            h2_title = div_h2[0]
            a_s = div_mulu.xpath('./div[@class="box"]/ul/li/a')
            lst = []
            for a in a_s:
                # 找到 href 属性
                href = a.xpath('./@href')[0]
                # 找到 title 属性
                box_title = a.xpath('./@title')[0]
                pattern = re.compile(r'\s*\[(.*)\]\s+(.*)') # (re) 匹配括号内的表达式，也表示一个组
                match = pattern.search(box_title)
                if match != None:
                    date = match.group(1)
                    real_title = match.group(2)
                    lst.append({'href':href,'title':real_title,'date':date})
            content.append({'title':h2_title,'content':lst})
    with open('dmbj_xp.json', 'w') as fp:
        json.dump(content, fp=fp, indent=4)

def main():
    html_text = getHtmlText('http://www.seputu.com')
    print(len(html_text))
    start = time.clock()
    parseWithBeautifulSoup(html_text)
    print('BSoup cost:', time.clock()-start)
    start = time.clock()
    parseWithXpath(html_text)
    print('Xpath cost:', time.clock()-start)

if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    headers={'User-Agent': user_agent}
    main()
