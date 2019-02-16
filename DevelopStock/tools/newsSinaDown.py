'''
code source link:
    https://www.cnblogs.com/zengbojia/p/7220190.html
'''
# 获取新闻的标题，内容，时间和评论数
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import pandas

def getNewsdetial(newsurl):
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    newsTitle = soup.select('.page-header h1')[0].text.strip()
    nt = datetime.strptime(soup.select('.time-source')[0].contents[0].strip(),'%Y年%m月%d日%H:%M')
    newsTime = datetime.strftime(nt,'%Y-%m-%d %H:%M')
    newsArticle = getnewsArticle(soup.select('.article p'))
    newsAuthor = newsArticle[-1]
    return newsTitle,newsTime,newsArticle,newsAuthor
def getnewsArticle(news):
    newsArticle = []
    for p in news:
         newsArticle.append(p.text.strip())
    return newsArticle

# 获取评论数量

def getCommentCount(newsurl):
    m = re.search('doc-i(.+).shtml',newsurl)
    newsid = m.group(1)
    commenturl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
    comment = requests.get(commenturl.format(newsid))   #将要修改的地方换成大括号，并用format将newsid放入大括号的位置
    jd = json.loads(comment.text.lstrip('var data='))
    return jd['result']['count']['total']


def getNewsLinkUrl():
#     得到异步载入的新闻地址（即获得所有分页新闻地址）
    urlFormat = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1501000415111'
    url = []
    for i in range(1,10):
        res = requests.get(urlFormat.format(i))
        jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
        url.extend(getUrl(jd))     #entend和append的区别
    return url

def getUrl(jd):
#     获取每一分页的新闻地址
    url = []
    for i in jd['result']['data']:
        url.append(i['url'])
    return url

# 取得新闻时间，编辑，内容，标题，评论数量并整合在total_2中
def getNewsDetial():
    title_all = []
    author_all = []
    commentCount_all = []
    article_all = []
    time_all = []
    url_all = getNewsLinkUrl()
    for url in url_all:
        title_all.append(getNewsdetial(url)[0])
        time_all.append(getNewsdetial(url)[1])
        article_all.append(getNewsdetial(url)[2])
        author_all.append(getNewsdetial(url)[3])
        commentCount_all.append(getCommentCount(url))
    total_2 = {'a_title':title_all,'b_article':article_all,'c_commentCount':commentCount_all,'d_time':time_all,'e_editor':author_all}
    return total_2

# ( 运行起始点 )用pandas模块处理数据并转化为excel文档

df = pandas.DataFrame(getNewsDetial())
df.to_excel('news2.xlsx')


################################
#encoding utf-8
import requests
import re
from datetime import datetime
import json
from bs4 import BeautifulSoup
new_urls = set() #存放未访问url set集合
#根据得到的url获取新闻信息
def get_soup(url):
    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    return soup

#添加新的url
def add_urls(arr):
    for link in arr:
        if(len(link.select('h2'))>0):
            h2 = link.select('h2')[0]
            a = h2.select('a')
            if (len(a) > 0):
                a = a[0]
                time = link.select('.time')
                if(len(time)>0):
                    #print(h2.text,time[0].text,a['href'])
                    new_urls.add(a['href'])

#从new_urls获取未访问的url
def get_url():
    if(new_urls is not None):
        return new_urls.pop()

#通过新闻页url获取id，并拼接返回存放评论数
def get_commentsJs(url):
    m = re.search('doc-i(.+).shtml',url)
    m.group(1)
    url = "http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}"
    comments = requests.get(url.format(m.group(1)))  #url.format(m.group(1))url拼接
    comments.encoding = 'utf-8'
    jd = json.loads(comments.text.strip('var data='))  # 移除改内容将其变为json数据
    return jd['result']['count']['total']

#获取新闻内容中所需内容
def get_information(soup,url):
    dict = {}
    title = soup.select_one('#artibodyTitle')
    dict['title'] = title.text
    time_source = soup.select_one('.time-source')
    time = time_source.contents[0].strip()  # str 格式
    dict['site'] = time_source.contents[1].text.strip('\n') #新闻来源
    dict['time'] = datetime.strptime(time, '%Y年%m月%d日%H:%M')  # 将字符串转化为时间类型
    content = ' '.join([p.text.strip() for p in soup.select('#artibody p')[0:-1]])  # 生成器写法
    # ' '.join(content)  #将其合并为字符串
    dict['content'] = content
    # 取出责任编辑
    editor = soup.select_one('.article-editor').text.lstrip('责任编辑：')  # 并从左边将责任编辑：移除
    dict['editor'] = editor
    dict['comments'] = get_commentsJs(url)
    return dict


#国内新闻页面所有新闻
root_url = "http://news.sina.com.cn/china/"
soup = get_soup(root_url)
items = soup.select('.news-item')
add_urls(items) #将新获取的url加入集合
content = []

while 1:
    if (new_urls is  None):
        break
    url = get_url() #从url集合中得到要访问的url
    soup = get_soup(url) #得到soup
    dict = get_information(soup,url)
    content.append(dict)
    print(dict)