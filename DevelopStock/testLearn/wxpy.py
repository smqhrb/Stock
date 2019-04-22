# #coding=utf8
# import itchat
# itchat.auto_login(hotReload=True) #热启动你的微信

# a =itchat.send("Hello World!")
# b =itchat.send("@fil@%s" % './hello.png')
# itchat.run()
# #itchat.run()
# # rooms=itchat.get_chatrooms(update=True)
# # for i in range(len(rooms)):
# #     print(rooms[i]) #查看你多有的群
 
# # room = itchat.search_friends(name=r'山山山') #这里输入你好友的名字或备注。
# # print(room)
# # userName = room[0]['NickName']
# # f="hello.png" #图片地址
# # try:
# #     itchat.send_image(f,toUserName=userName) #如果是其他文件可以直接send_file
# #     print("success")
# # except:
# #     print("fail")

# 给文件传输助手发一条消息 ok
# import itchat
# # itchat.auto_login(enableCmdQR=True)  # 这里需要你人工手机扫码登录
# itchat.auto_login(hotReload=True) #热启动你的微信
# itchat.send('Hello, 文件助手', toUserName='filehelper')
# itchat.send("@fil@%s" % './hello.png', toUserName='filehelper')
################
#用另外的微信号发消息ok
################
# import itchat
# @itchat.msg_register(itchat.content.TEXT)
# def text_replay(msg):
#     return msg.text  # 人家说啥你回复啥。。。
# itchat.auto_login()
# itchat.run()
################
#群发助手 not ok
#
####################
# import itchat
# import time

# # itchat.auto_login(hotReload=True, enableCmdQR=True)
# itchat.auto_login(hotReload=True)
# SINCERE_WISH = u"祝%s感恩节快乐！"

# friend_list = itchat.get_friends(update=True)  # 第一个是自己
# friend_list = friend_list[1:]

# for friend in friend_list:
#     # 如果是演示，把send改成print就行
#     # itchat.send(SINCERE_WISH % (friend['DisplayName'] or friend['NickName']), friend['UserName'])
#     print(SINCERE_WISH % (friend['DisplayName'] or friend['NickName']))
#     time.sleep(3)

# # 好友删除检测 not good

# """有时候我们会想知道某个好友有没有删除自己或者把自己拉入黑名单。

# 这一操作使用itchat也会变的非常简单。

# 原理的话，在于将好友拉入群聊时，非好友和黑名单好友不会被拉入群聊。

# 所以群聊的返回值中就有了好友与你关系的数据。

# 另外，群聊在第一次产生普通消息时才会被除创建者以外的人发现的（系统消息不算普通消息）。

# 这样，就可以隐蔽的完成好友检测
# """


# #coding=utf8
# import itchat

# CHATROOM_NAME = 'friend'
# CHATROOM = None
# HELP_MSG = u'''\
# 好友状态监测
# * 发送名片将会返回好友状态
# * 请确有名为%s的未使用的群聊
# * 并将该群聊保存到通讯录
# * 调用频率存在一定限制\
# ''' % CHATROOM_NAME
# CHATROOM_MSG = u'''\
# 无法自动创建群聊，请手动创建
# 确保群聊名称为%s
# 请不要使用已经使用过的群聊
# 创建后请将群聊保存到通讯录\
# ''' % CHATROOM_NAME


# def get_chatroom():
#     global CHATROOM
#     if CHATROOM is None:
#         itchat.get_chatrooms(update=True)
#         chatrooms = itchat.search_chatrooms(CHATROOM_NAME)
#         if chatrooms:
#             return chatrooms[0]
#         else:
#             r = itchat.create_chatroom(itchat.get_friends()[1:4], topic=CHATROOM_NAME)
#             if r['BaseResponse']['ErrMsg'] == '':
#                 CHATROOM = {'UserName': r['ChatRoomName']}
#                 return CHATROOM
#     else:
#         return CHATROOM
# def get_friend_status(friend):
#     ownAccount = itchat.get_friends(update=True)[0]
#     if friend['UserName'] == ownAccount['UserName']:
#         return u'检测到本人账号。'
#     elif itchat.search_friends(userName=friend['UserName']) is None:
#         return u'该用户不在你的好友列表中。'
#     else:
#         chatroom = CHATROOM or get_chatroom()
#         if chatroom is None: return CHATROOM_MSG
#         r = itchat.add_member_into_chatroom(chatroom['UserName'], [friend])
#         if r['BaseResponse']['ErrMsg'] == '':
#             status = r['MemberList'][0]['MemberStatus']
#             itchat.delete_member_from_chatroom(chatroom['UserName'], [friend])
#             return { 3: u'该好友已经将你加入黑名单。',
#                 4: u'该好友已经将你删除。', }.get(status,
#                 u'该好友仍旧与你是好友关系。')
#         else:
#             return u'无法获取好友状态，预计已经达到接口调用限制。'

# @itchat.msg_register(itchat.content.CARD)
# def get_friend(msg):
#     if msg['ToUserName'] != 'filehelper': 
#         return

#     friendStatus = get_friend_status(msg['RecommendInfo'])
#     itchat.send(friendStatus, 'filehelper')

# itchat.auto_login(hotReload=True)
# itchat.send(HELP_MSG, 'filehelper')
# itchat.run()

## 最简单的与图灵机器人的交互 not ok
# import requests
# import itchat

# KEY = '8edce3ce905adbb965e6b35c3834d'


# def get_response(msg):
#     # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
#     # 构造了要发送给服务器的数据
#     apiUrl = 'http://www.tuling123.com/openapi/api'
#     data = {
#         'key': KEY,
#         'info': msg,
#         'userid': 'wechat-robot',
#     }
#     try:
#         r = requests.post(apiUrl, data=data).json()
#         # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
#         return r.get('text')
#     # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
#     # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
#     except:
#         # 将会返回一个None
#         return


# # 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
# @itchat.msg_register(itchat.content.TEXT)
# def tuling_reply(msg):
#     # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
#     defaultReply = 'I received: ' + msg['Text']
#     # 如果图灵Key出现问题，那么reply将会是None
#     reply = get_response(msg['Text'])
#     # a or b的意思是，如果a有内容，那么返回a，否则返回b
#     # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
#     return reply or defaultReply


# # 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
# itchat.auto_login(hotReload=True)
# itchat.run()


# # 微信播放音乐
# # coding=utf-8

# """
# 这是一个通过微信控制电脑播放音乐的小项目，那么主要就是三个功能： 输入“帮助”，显示帮助 输入“关闭”，关闭音乐播放 * 输入具体歌名，进入歌曲的选择
# """
# import os

# import itchat
# from NetEaseMusicApi import interact_select_song

# HELP_MSG = """\
# 欢迎使用微信网易云音乐
# 帮助：显示帮助
# 关闭：关闭歌曲
# 歌名：按照引导播放音乐
# """

# with open('stop.mp3', 'w') as f:
#     pass


# def close_music():
#     os.startfile('stop.mp3')


# @itchat.msg_register(itchat.content.TEXT)
# def music_player(msg):
#     if msg['ToUserName'] != 'filehelper':
#         return
#     if msg['Text'] == u'关闭':
#         close_music()
#         itchat.send(u'音乐已关闭', 'filehelper')
#     if msg['Text'] == u'帮助':
#         itchat.send(HELP_MSG, 'filehelper')
#     else:
#         itchat.send(interact_select_song(msg['Text']), 'filehelper')


# itchat.auto_login(True)
# itchat.send(HELP_MSG, 'filehelper')
# itchat.run()

# ###############
# 获取微信好友的基本信息
import itchat
 
# hotReload(热加载),短时间内不需要再次扫码登陆
itchat.auto_login(hotReload=True)
 
# 获取微信好友的信息,返回的是json格式的信息
friends = itchat.get_friends(update=True)[0:]
# print(friends)
# 初始化性别的变量
male = female = others = 0
# 循环得到的全部好友
# 在好友的信息中有Sex标签,发现规律是当其值为1是表示男生,2表示女生,0表示没有填写的
for i in friends[1:]:
    sex = i['Sex']
    if(sex == 1):
        male += 1
    elif(sex == 2):
        female += 1
    else:
        others += 1
 
total = len(friends[2:])
# print(total)
print("男生好友比例 : %.2f%%" % (float(male) / total * 100) + "\n"
      "女生好友比例 : %.2f%%" % (float(female) / total * 100) + "\n"
      "不明性别好友 : %.2f%%" % (float(others) / total * 100))

######################
# import itchat
# import re
# import jieba
# import matplotlib.pyplot as plt
# import numpy as np
# import PIL.Image as Image
# from wordcloud import WordCloud, ImageColorGenerator
 
# # 模拟登陆微信
# # 参数hotReload(热加载)短时间内不需要重复扫描二维码登录
# itchat.auto_login(hotReload=True)
# # itchat.send(u'这是一条测试消息', 'filehelper')
# friends = itchat.get_friends(update=True)[0:]
# # print(friends)
# siglist = []
# male = female = others = 0
# for i in friends[2:]:
#     sex = i['Sex']
#     if(sex == 1):
#         male += 1
#     elif(sex == 2):
#         female += 1
#     else:
#         others += 1
#     # print(i['Signature'])
#     # 有的好友签名中带有其他的表情什么的,先全部清掉
#     signature = i['Signature'].strip().replace(
#         "span", "").replace("class", "").replace("emoji", "")
#     rep = re.compile("1f\d+\w*|[<>/=]")
#     signature = rep.sub("", signature)
#     siglist.append(signature)
 
# # 将处理好的签名加到text中
# text = "".join(siglist)
 
# total = len(friends[2:])
# # print(total)
# print("男生好友比例 : %.2f%%" % (float(male) / total * 100) + "\n"
#       "女生好友比例 : %.2f%%" % (float(female) / total * 100) + "\n"
#       "不明性别好友 : %.2f%%" % (float(others) / total * 100))
 
# # 采用jieba分词,对生成的text进行分词
# wordlist = jieba.cut(text, cut_all=True)
# # 分词完成后在没个词之间加上空格
# word_space_split = " ".join(wordlist)
# cover = np.array(Image.open("F:\\Python_UP\\WordCloud\\image\\love.jpg"))
# my_wordcloud = WordCloud(background_color="white",
#                          max_words=2000,
#                          mask=cover,
#                          max_font_size=60,
#                          random_state=42,
#                          scale=2,
#                          font_path="C:\\Windows\\Fonts\\STXINGKA.TTF").generate(word_space_split)
# image_color = ImageColorGenerator(cover)
# plt.imshow(my_wordcloud.recolor(color_func=image_color))
# plt.imshow(my_wordcloud)
# plt.axis("off")
# plt.show()

