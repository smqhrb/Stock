from pymongo import MongoClient
from requests_html import HTMLSession
import time
import random
from threading import Thread


session = HTMLSession()
headers = [{'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding':'gzip, deflate, sdch',
           'Accept-Language':'zh-CN,zh;q=0.8',
           'Connection':'keep-alive',
           'Host':'vip.stock.finance.sina.com.cn',
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           },
            {'user-agent' : "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",},
           {'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",},
           {'user-agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',},
           {'user-agent':'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',},
           ]
stypes = {'300':'sz','600':'sh','601':'sh','603':'sh',
              '900':'sh','000':'sz','200':'sz','002':'sz'}
#stypes  根据股票代码前三位判断上市交易所代码
wztypes = {'AllNewsStock':'个股资讯','stockIndustryNews':'行业资讯','FinManDiv':'理财师解读',
           'gzbc':'更正或补充','gszc':'公司章程','gqfzgg':'股权分置改革说明书','hfbg':'回访报告',
           'lsgg':'临时公告','ndbg':'年度报告','ndbgzy':'年度报告（摘要）','pgsms':'配股说明书',
           'qzssgg':'权证上市公告书','qzsms':'权证说明书','sjdbg':'三季度报告','sjdbgzy':'三季度报告（摘要）',
           'ssggs':'上市公告书','yjdbg':'一季度报告','yjdbgzy':'一季度报告（摘要）','zgsmssbg':'招股说明书（申报稿）',
           'zgsmsyxs':'招股说明书/意向书','zqbg':'中期报告','zqbgzy':'中期报告（摘要）'
           }
def create_db():
    #创建mongo数据库，并建立集合
    client = MongoClient('localhost',27017)
    db = client.sina_finance
    col_basic = db.basic
    col_detail = db.detail
    return col_basic,col_detail

def get_basic_data(html,scode):
    #获取基本信息表的内容
    sname = html.find('div.hq_title',first = True).find('h1',first = True).text[:-11]
    col_basic.save({'_id':scode,'sname':sname})

def exist_next_page(html):
    #判断当前页面是否存在下一页
    p = html.find("div[style = 'margin-top:10px;float:right;margin-right:100px;']",first = True)
    if p is None :
        return False
    else:
        if '下一页' in p.text:
            return True
        else:
            return False

def get_wztype(url):
    #获取文章的类型（个股资讯、行业资讯、公司公告、理财师解读等等）
    for i in wztypes.keys():
        if i in url:
            wztype = wztypes[i]
            return wztype

def get_news_data(url,scode):
    #获取 个股资讯和行业资讯 的内容
    wztype = get_wztype(url)
    i= 1
    html = session.get(url,headers = random.choice(headers)).html
    while 1:
    #在while内 按页面遍历 当前板块的所有内容
        datelist = html.find('div.datelist',first = True)
        if datelist is None: break
        #判断当前页面是否有文章列表
        else:
            print('正在获取 %s【%s】第%s页信息...'%(scode,wztype,i))
            datelist = datelist.find('a')         
            for item in datelist:
            #遍历当前页面所有文章
                title = item.text
                zx_url = item.attrs['href']
                zx_html = session.get(zx_url).html
#                time.sleep(random.uniform(0,1))
                contents = zx_html.find("div[id = 'artibody']",first =True)
                if contents is not None:
                    contents = contents.find('p')
                    content =''
                    for c in contents:
                        content += c.text
                else:
                #如果当前文章内容为空，则直接进行下一次遍历。经过多次检验，如果文章内容为空，
                #很大概率是‘当前页面失效’。在‘sina_log.txt’文件中记录该网页链接。
                    with open('d://sina_broken_link.txt','a') as f:
                        f.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+':'+zx_url)
                    continue
                source = zx_html.find("meta[name = 'mediaid']",first = True)
                if source is not None:
                    source = source.attrs['content']
                else:
                    source = ''
                date = zx_html.find("meta[name = 'weibo: article:create_at']",first = True)
                if date is not None:
                    date = date.attrs['content']
                elif zx_html.find("span[id = 'pub_date']",first = True) is not None:
                    date = zx_html.find("span[id = 'pub_date']",first = True).text.replace(' ','')
                else : date = ''
                keywords = zx_html.find("meta[name ='keywords']",first = True)
                if keywords is not None:
                    keywords = keywords.attrs['content'].replace(title,'').split(',')
                else:
                    keywords = ''
#                print(zx_url)
                col_detail.save({'_id':zx_url,'scode':scode,'wztype':wztype,'title':title,'date':date,'source':source,'keywords':keywords,'content':content,'grabtime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))})
#                print('aaaaaaaaaaaaaaaaa')
            if exist_next_page(html):
                url = html.find("div[style = 'margin-top:10px;float:right;margin-right:100px;']",first = True).find('a')[-1].attrs['href']
                html = session.get(url,headers = random.choice(headers)).html
                i+=1
            else:break

def get_fmd_data(url,scode):
    #获取 理财师解读 板块的内容
    wztype = get_wztype(url)
    i =1
    html = session.get(url,headers = random.choice(headers)).html
    while 1:
        if html.find('div.datelist',first = True) is  None: break
        else:
            print('正在获取 %s【%s】第%s页信息...'%(scode,wztype,i))
            datelist= html.find('div.datelist',first = True).find('a')[1::2]
            for item in datelist:
                title = item.text
                fmd_url = item.attrs['href']
                fmd_html = session.get(fmd_url).html
#                time.sleep(random.uniform(0,1))
                contents = fmd_html.find("div.p_article",first = True)
                if contents is not None:
                    content =''
                    if fmd_html.find('div.p_quote',first = True) is None:
                        quote = ''
                    else:
                        quote = fmd_html.find('div.p_quote',first = True).text
                    contents = contents.find('p')
                    for c in contents:
                        content += c.text.replace('\u200d','').replace('\xa0','')
                    content = quote+ ' '+content
                else:
                    with open('d:\\sina_broken_link.txt','a') as f:
                        f.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+':'+fmd_url)
                    continue
                source = fmd_html.find("span.p_info_package",first = True)
                if source is not None:
                    source = source.text[3:].split('、')
                else:
                    source = ''
                date = fmd_html.find("time.p_info_time",first = True)
                if date is not None:
                    date = date.text
                else:
                    date = ''
                keywords = fmd_html.find("meta[name ='keywords']",first = True)
                if keywords is not None:
                    keywords = keywords.attrs['content'].split(',')
                else:
                    keywords = ''
                tag = fmd_html.find('span.p_info_tag',first = True)
                if tag is not None:
                    tag = tag.text[3:]
                else:
                    tag = ''
#                print('bbbbbbbbbbbbb')
                col_detail.save({'_id':fmd_url,'scode':scode,'wztype':wztype,'title':title,'date':date,'source':source,'keywords':keywords,'content':content,'grabtime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'tag':tag})
            if exist_next_page(html):
                url = html.find("div[style = 'margin-top:10px;float:right;margin-right:100px;']",first = True).find('a')[-1].attrs['href']
                html = session.get(url,headers = random.choice(headers)).html
                i+=1
            else:break

def get_bulletin_data(url,scode):
    #获取公司公告的所有内容
    time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    tp = [i for i in wztypes.keys()]
    tp.remove('AllNewsStock')
    tp.remove('stockIndustryNews')
    tp.remove('FinManDiv')
    urls = [url+'?ftype='+i for i in tp]
    #urls 所有公告类型的链接列表
    def get_gg_info(url,scode):
        #获取当前公告类型的所有内容
        wztype = get_wztype(url)
        i = 1
        html = session.get(url,headers = random.choice(headers)).html
        while 1:
            if html.find('div.datelist',first = True) is None:break
            else:
                print('正在获取 %s【%s】第%s页信息...'%(scode,wztype,i))
                datelist = html.find('div.datelist',first = True).find('a')
                for item in datelist:
                    gg_url = 'http://vip.stock.finance.sina.com.cn'+item.attrs['href']
                    title = item.text
                    gg_html = session.get(gg_url).html
#                    time.sleep(random.uniform(0,1))
                    content = gg_html.find("div[id = 'content']",first = True)
                    if content is None:
                        with open('d:\\sina_broken_link.txt','a') as f:
                            f.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+':'+gg_url)
                        continue
                    else:
                        content = content.text
                    keywords = gg_html.find("meta[name ='Keywords']",first = True)
                    if keywords is not None:
                        keywords = keywords.attrs['content'].split(',')
                    else:
                        keywords = ''
                    date = gg_html.find("td.graybgH2",first = True)
                    if date is not None: 
                        date = date.text[5:]
                    else:
                        date = ''
#                    print('cccccccccccccc')
                    col_detail.save({'_id':gg_url,'scode':scode,'wztype':wztype,'title':title,'date':date,'keywords':keywords,'content':content,'grabtime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))})
                if exist_next_page(html):
                    url = html.find("div[style = 'margin-top:10px;float:right;margin-right:100px;']",first = True).find('a')[-1].attrs['href']
                    html = session.get(url,headers = random.choice(headers)).html
                    i+=1
                else:break
    for url in urls :
        get_gg_info(url,scode)

def main(line):
    #根据url构建方式形成初始url，再调用相关方法获取所有板块的内容   
    links = []
    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/'+stypes[line[:3]]+line[:6]+'.phtml'
    html = session.get(url,headers = random.choice(headers)).html
    try:
        get_basic_data(html,line[:6])
        for url in html.find('ul.r-menu',first = True).find('a'):
            links.append(url.attrs['href'])
            #links 在初始url的页面中获取所有版块的链接列表
        try:
            for li in links:
                if 'AllNewsStock' in li or 'stockIndustryNews' in li:      
                    get_news_data(li,line[:6])
                if 'FinManDiv' in li :
                    get_fmd_data(li,line[:6])
                if 'AllBulletin' in li:
                    get_bulletin_data(li,line[:6])
        except Exception as e:
            print(e)
    except Exception as e1:
    #在初始的url中获取不到所有版块的链接，可能已退市。在'sina_scode.txt'文件中记录。
        print(e1)
        with open('d:\\sina_dead_code.txt','a') as f:
            f.writelines(line[:6]+',')

if __name__ == '__main__':
    col_basic,col_detail = create_db()  
    isalive = []
    complete = False
    temp = []
    for line in open('e:\\datasource.csv','r'):
        temp.append(line)
        
    while 1:
        try:
            for t in isalive:
                if not t.is_alive():
                    isalive.remove(t)
                    print('one complete')        
                else:pass
        except Exception:
            pass
        
        if len(isalive)<20:
            try:
                for i in range(20 - len(isalive)):
                    i = Thread(target = main,args = (temp.pop(),))
                    i.start()
    #                i.join()
                    isalive.append(i)
                    print('one start')
    #                print(threading.activeCount())
    #                print(threading.enumerate())
            except IndexError:
                complete = True
      
        if complete:break
        time.sleep(60)
    
#    while 1:
#        try :
#            line = temp.pop()
#            main(line)
#        except IndexError :
#            break