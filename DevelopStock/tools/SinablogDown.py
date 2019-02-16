# coding=utf-8 
import urllib2
import sys, os
import re
import string
from BeautifulSoup import BeautifulSoup
def encode(s):
    return s.decode('utf-8').encode(sys.stdout.encoding, 'ignore')
def getHTML(url):
    #proxy_handler = urllib2.ProxyHandler({'http':'http://211.138.124.211:80'})
    #opener = urllib2.build_opener(proxy_handler)
    #urllib2.install_opener(opener)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req, timeout=15)
    return BeautifulSoup(response, convertEntities=BeautifulSoup.HTML_ENTITIES)
def visible(element):
    '''抓取可见的文本元素'''
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    elif element == u'\xa0':
        return False
    return True
def delReturn(element):
    '''删除元素内的换行'''
    return re.sub('(?<!^)\n+(?!$)', ' ', str(element)).decode('utf-8')
def validFilename(filename):
    # windows
    return re.sub('[\/:*?<>"|\xa0]', '', filename)
def writeToFile(text, filename, dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print encode('保存到目录'), dirname
    filename = validFilename(filename)
    print encode('保存文章'), filename
    path = os.path.join(dirname, filename)
    if not os.path.exists(path):
        f = open(path, 'w')
        f.write(text)
        f.close()
    else:
        print filename, encode('已经存在')
def formatContent(url, title=''):
    '''格式化文章内容'''
    page = getHTML(url)
    content = page.find('div', {'class':'articalContent'})
    art_id = re.search('blog_(\w+)\.html', url).group(1)
    blog_name = page.find('span', id='blognamespan').string
    if title == '':
        title = page.find('h2', id=re.compile('^t_')).string
    temp_data = filter(visible, content.findAll(text=True)) # 去掉不可见元素
    temp_data = ''.join(map(delReturn, temp_data)) # 删除元素内的换行符
    temp_data = temp_data.strip() # 删除文章首尾的空行
    temp_data = re.sub('\n{2,}', '\n\n', temp_data) # 删除文章内过多的空行
    # 输出到文件
    # 编码问题
    temp_data = '本文地址:'.decode('utf-8') + url + '\n\n' + temp_data
    op_text = temp_data.encode('utf-8')
    op_file = title + '_' + art_id +'.txt'
    writeToFile(op_text, op_file, blog_name)
def articlelist(url):
    articles = {}
    page = getHTML(url)
    pages = page.find('ul', {'class':'SG_pages'}).span.string
    page_num = int(re.search('(\d+)', pages).group(1))
    for i in range(1, page_num+1):
        print encode('生成第%d页文章索引'%i)
        if i != 1:
            url = re.sub('(_)\d+(\.html)$', '\g<1>'+str(i)+'\g<2>', url)
            page = getHTML(url)
            article = page.findAll('span', {'class':'atc_title'})
            for art in article:
                art_title = art.a['title']
                art_href = art.a['href']
                articles[art_title] = art_href
    return articles
def blog_dld(articles):
    if not isinstance(articles, dict):
        return False
    print encode('开始下载文章')
    for art_title, art_href in articles.items():
        formatContent(art_href, art_title)
if __name__ == '__main__':
    sel = raw_input(encode('你要下载的是(1)全部文章还是(2)单篇文章，输入1或者2: '))
    if sel == '1':
        #articlelist_url = 'http://blog.sina.com.cn/s/articlelist_1303481411_0_1.html'
        articlelist_url = raw_input(encode('请输入博客文章目录链接: '))
        articles = articlelist(articlelist_url)
        blog_dld(articles)
    else:
        #article_url = 'http://blog.sina.com.cn/s/blog_4db18c430100gxc5.html'
        article_url = raw_input(encode('请输入博客文章链接: '))
        formatContent(article_url)
