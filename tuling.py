import itchat
import requests
import re
import os
import random
from rename import rename
from picHandle import picHandle
#coding=utf8
apiUrl='http://www.tuling123.com/openapi/api'
key='6ba78da2a3b34dfd82b350f895b97bae'
selfInfo={}
myName=''
totalPicNumber=0
path='f:\\wxPic\\'
dic={}#userid username dic
lis=[]#filesize lis
tempSize=1
resend=0

def getResponse(info):
    data1={
        'key':key,
        'info':info,
        'userid':'wechat-robot',
        }
    try:
        r=requests.post(apiUrl,data=data1).json()
    except Exception:
        print ('error!')
        return
    if r.get('code')==100000:#text
        print(r.get('text'))#robot reply text
        return r.get('text')
    elif r.get('code')==200000:#pic
        print(r.get('url'))#robot reply url
        return r.get('url')
    elif r.get('code')==302000:#news
        print(r.get('list'))#robot reply lsit
        return r.get('list')
    elif r.get('code')==308000:#dish
        print(r.get('list'))#robot reply lsit
        return r.get('list')
    else:
        return '我不和你玩了，我要睡觉了!'


@itchat.msg_register(itchat.content.TEXT)#文字
def text_reply(msg):
    global dic
    try:
        textFromName=dic[msg['FromUserName']]
    except:
        textFromName=itchat.search_friends(userName=msg['FromUserName'])['NickName']
        dic[msg['FromUserName']]=textFromName
    try:
        textToName=dic[msg['ToUserName']]
    except:
        textToName=itchat.search_friends(userName=msg['ToUserName'])['NickName']
        dic[msg['ToUserName']]=textToName
    try:
        print('%s--->%s:%s'%(textFromName,textToName,msg['Text']))# friend/me : xxx
    except:
        print('text encode error!')
    if textFromName!=myName:
        #return getResponse(msg['Text'])['text']
        print('%s(Robot)--->%s:'%(myName,textFromName),end='')# me(Robot)---> friend:
        return getResponse(msg['Text'])
    else:
        return

    
def picdeal(msg):
    global lis
    global totalPicNumber
    global tempSize
    global resend
    try:
        msg['Text'](path+msg['FileName']) #save pic first !!!!!!
    except:
        print('pic save failed!')
        return
    fileFullPath=os.path.join(path,msg['FileName'])
    fileSize=os.path.getsize(fileFullPath)
    if fileSize==tempSize:
        resend=1
        os.remove(fileFullPath)
        try:
            itchat.send_image('f:/wxPic/'+str(totalPicNumber)+'.gif',toUserName=msg['FromUserName'])
        except:
            print('send repeated emoji error!')
            return
        #print('%s(Robot)--->%s:%s'%(myName,picFromName,str(tatalPicNumber)+'.gif'))
        return
    else:
        resend=0
    tempSize=fileSize#save this time's pic size
    fileType=os.path.splitext(msg['FileName'])[1]
    if (fileSize in lis) or fileSize==0 or fileSize/1024>500 or fileType!='.gif':
        try:
            os.remove(fileFullPath)
        except:
            print('emoji delete failed!')
    else:
        totalPicNumber=totalPicNumber+1
        lis.append(fileSize)
        newName=os.path.join(path,str(totalPicNumber)+'.gif')
        try:
            os.rename(fileFullPath,newName)
        except:
            print('emoji rename failed!')
        print('get new emoji ^_^')

         
@itchat.msg_register(itchat.content.PICTURE)#图片、表情
def picture_reply(msg):
    i=0
    global dic
    global totalPicNumber
    global resend
    try:
        picFromName=dic[msg['FromUserName']]
    except:
        picFromName=itchat.search_friends(userName=msg['FromUserName'])['NickName']
        dic[msg['FromUserName']]=picFromName
    try:
        picToName=dic[msg['ToUserName']]
    except:
        picToName=itchat.search_friends(userName=msg['ToUserName'])['NickName']
        dic[msg['ToUserName']]=picToName
    print('%s--->%s:<Pic>%s'%(picFromName,picToName,msg['FileName']))# friend/me : xxx.Pic
    if picFromName!=myName:
        try:
            picdeal(msg)  #only when others sending pic to me!
            if resend==0:
                i=random.randint(1,totalPicNumber)
                try:
                    itchat.send_image('f:/wxPic/'+str(i)+'.gif',toUserName=msg['FromUserName'])
                    print('%s(Robot)--->%s:%s'%(myName,picFromName,str(i)+'.gif'))
                except:
                    print('pic sending error!')               
            else:
                return
        except Exception:
            print ('pic collect or send error!')

    
@itchat.msg_register(itchat.content.RECORDING)#语音
def recording_reply(msg):
    try:
        recFromName=dic[msg['FromUserName']]
    except:
        recFromName=itchat.search_friends(userName=msg['FromUserName'])['NickName']
        dic[msg['FromUserName']]=recFromName
    try:
        recToName=dic[msg['ToUserName']]
    except:
        recToName=itchat.search_friends(userName=msg['ToUserName'])['NickName']
        dic[msg['ToUserName']]=recToName
    print('%s--->%s:<Rec>%s'%(recFromName,recToName,msg['MsgId']))# friend/me : xxxPic
    if recFromName!=myName:
        itchat.send('发你妹的语音，打字，我听不见！',toUserName=msg['FromUserName'])


@itchat.msg_register(itchat.content.SHARING)#分享
def shar_reply(msg):
    try:
        shaFromName=dic[msg['FromUserName']]
    except:
        shaFromName=itchat.search_friends(userName=msg['FromUserName'])['NickName']
        dic[msg['FromUserName']]=shaFromName
    try:
        shaToName=dic[msg['ToUserName']]
    except:
        shaToName=itchat.search_friends(userName=msg['ToUserName'])['NickName']
        dic[msg['ToUserName']]=shaToName
    print('%s--->%s:<Sha>%s'%(shaFromName,shaToName,msg['Text']))
    if shaFromName!=myName:
        print('%s(Robot)--->%s:'%(myName,shaFromName),end='')# me(Robot)---> friend:
        return msg['Text']+','+getResponse(msg['Text'])


@itchat.msg_register(itchat.content.MAP)#位置信息
def map_reply(msg):
    try:
        mapFromName=dic[msg['FromUserName']]
    except:
        mapFromName=itchat.search_friends(userName=msg['FromUserName'])['NickName']
        dic[msg['FromUserName']]=mapFromName
    try:
        mapToName=dic[msg['ToUserName']]
    except:
        mapToName=itchat.search_friends(userName=msg['ToUserName'])['NickName']
        dic[msg['ToUserName']]=mapToName
    print('%s--->%s:<Map>%s'%(mapFromName,mapToName,msg['Text']))
    msg_content=None
    x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
    #msg_content = r"" + location
    msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
    if mapFromName!=myName:
        itchat.send(msg_content,toUserName=msg['FromUserName'])
        print('%s--->%s:%s'%(myName,mapFromName,msg_content))


itchat.auto_login()
selfInfo=itchat.search_friends()#get self info
myName=selfInfo['NickName']
rename()
picHandle()
for pics in os.listdir(path):
    filename=os.path.join(path,pics)
    fileSize=os.path.getsize(filename)
    lis.append(fileSize)
    totalPicNumber=totalPicNumber+1
print('Emoji folder info loading successfully!')
print('Total emoji number was:%d'%totalPicNumber)
itchat.run()



