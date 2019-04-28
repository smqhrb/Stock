#coding=utf8
import requests
import itchat
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : '7e58ec4985b74bd9abb3b371b1bfc93a',    #这里自行输入key
        'info'   : msg,
        'userid' : '437062',     #这是我的账号
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return "呵呵"    #出问题就回复“呵呵”


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReply = 'I received: ' + msg['Text']  #一个默认回复
    reply = get_response(msg['Text'])  
    return reply or defaultReply

itchat.auto_login(hotReload=True)    #热启动，不需要多次扫码登录
itchat.run()
