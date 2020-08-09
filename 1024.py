# -*- coding: UTF-8 -*-
import requests
import re
import random
import onetimepass as otp
from time import sleep
from urllib import parse
class Autoreply:
    result=None
    loginurl = 'http://t66y.com/login.php'
    url='http://t66y.com/thread0806.php?fid=7&search=today'
    posturl='http://t66y.com/post.php?'
    indexurl='http://t66y.com/index.php'
    black_list=['htm_data/2007/7/4032088.html','htm_data/2003/7/3832698.html','htm_data/1602/7/37458.html','htm_data/1502/7/1331010.html','htm_data/2005/7/2520305.html','htm_data/2005/7/2404767.html']
    s=requests.Session()
    headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4209.2 Safari/537.36'
    }
    headers1={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/login.php',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4209.2 Safari/537.36'
    }
    headers2={
        'Host': 't66y.com',
        'Origin': 'null',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4209.2 Safari/537.36'
    }
    def __init__(self,user,password,secret):
        self.user= user
        self.password= password
        self.secret =secret


    def login1(self):
        sleep(2)
        flag=False
        Err=None
        data={
                'pwuser': self.user,
                'pwpwd':  self.password,
                'hideid': '0',
                'cktime': '86400',
                'forward': 'http://t66y.com/post.php?',
                'jumpurl': 'http://t66y.com/post.php?',
                'step': '2'
        }
        login=self.s.post(self.loginurl,headers=self.headers,data=data)
        login=login.text.encode('iso-8859-1').decode('gbk')
        #print(login)
        #print('login1')
        if login.find('登录尝试次数过多')!=-1:
            Err='登录尝试次数过多,需输入验证码'
            return Err
        elif login.find('賬號已開啟兩步驗證')!=-1:
            Err='賬號已開啟兩步驗證'
            return Err


    def login2(self):
        sleep(2)
        my_token = otp.get_totp(self.secret)
        data={
        'step': '2',
        'cktime': '0',
        'oneCode': str(my_token)
        }
        login=self.s.post(self.loginurl,headers=self.headers,data=data)
        login=login.text.encode('iso-8859-1').decode('gbk')
        #print('login2')
        if login.find('您已經順利登錄')!=-1:
            res='已經順利登錄'
            return res

    def getverwebq(self):
        code=random.uniform(0,1)
        code=round(code,16)
        vercodeurl='http://t66y.com/require/codeimg.php?'+str(code)
        image=self.s.get(vercodeurl,headers=self.headers1)
        f=open('image.webq','wb')
        f.write(image.content)
        f.close()

    def inputvercode(self):
        sleep(2)
        vercode=input('请输入验证码:')
        data={
            'validate': vercode
        }
        login=self.s.post(self.loginurl,data=data,headers=self.headers1)
        login=login.text.encode('iso-8859-1').decode('gbk')
        #print(login)
        if login.find('驗證碼不正確')!=-1:
            Err='验证码不正确，请重新输入'
            return Err

    def gettodaylist(self):
        con=self.s.get(self.url,headers=self.headers)
        con = con.text.encode('iso-8859-1').decode('gbk')
        pat=('htm_data/\w+/\w+/\w+.html')
        match=re.findall(pat,con)
        try:
            for data in self.black_list:
                match.remove(data)
            self.match=match
        except:
            print('移除失败，不知道因为啥。。。')
            pass
        #print(match)

    def getonelink(self):
        geturl=''
        m=random.randint(0,len(self.match)-1)
        geturl='http://t66y.com/'+self.match[m]
        self.geturl=geturl
        #将今日回复过的加入黑名单
        self.black_list.append(geturl)
        tid=self.match[m][16:len(self.match[m])-5]
        self.tid=tid
        print('请求链接是: '+geturl)
    
    #不知道啥用，留着吧
    def getmatch(self):
        get=self.s.get(self.geturl,headers=self.headers)
        get=get.text.encode('iso-8859-1').decode('gbk')
        pat='<h4>.*</h4>'
        res=re.search(pat,get)
        res=res.group(0).replace('<h4>','').replace('</h4>','')
        res='Re:'+res
        self.res=res
        #print(res)

    def getreply(self):
        #自定义回复内容，记得修改随机数
        reply=['1024','感谢分享']
        reply_m=random.randint(0,1)
        reply_news=reply[reply_m]
        self.reply_news=reply_news.encode('gb2312')
        print("本次回复内容是:"+reply_news)

    #暂时没用，看以后了
    # def encodepost(self):
    #     res=self.res.encode('gbk')
    #     res=parse.quote(res)
    #     self.encoderesult=res
    #     print(self.encoderesult)
    #     reply_news=self.reply_news.encode('gbk')
    #     reply_news=parse.quote(reply_news)
    #     self.encoderesult=res
    #     self.encodereply=reply_news
    #     #print(self.encodereply)


    def postreply(self):
        data={
            'atc_usesign':'1',
            'atc_convert':'1',
            'atc_autourl': '1',
            #'atc_title':self.encoderesult,
            #'atc_content': self.encodereply ,
            'atc_title':self.res,
            'atc_content': self.reply_news ,
            'step': '2',
            'action': 'reply',
            'fid': '7',
            'tid': self.tid ,
            'atc_attachment': 'none',
            'pid':'',
            'article':'',
            'touid':'',
            'verify':'verify'
        }
        #print(data)
        post=self.s.post(self.posturl,data=data,headers=self.headers2)
        post = post.text.encode('iso-8859-1').decode('gbk')
        if post.find('發貼完畢點擊')!=-1:
            status='回复成功'
            #print('回复成功')
            return status
        if post.find('所屬的用戶組')!=-1:
            status='今日已达上限'
            return status
        #print(post)

    def getnumber(self):
        index=self.s.get(self.indexurl,headers=self.headers)
        index = index.text.encode('iso-8859-1').decode('gbk')
        pat='共發表帖子: \d{1,5}'
        num=re.search(pat,index).group(0)
        num=num.replace('共發表帖子: ','')
        #print(num)
        return num

if __name__ == "__main__":
    success=None
    suc=False
    n=0
    #设置参数
    user= 'XXXXXXXX'
    password= 'XXXXXXXX'
    secret ='XXXXXXXXXXXXXXXX'
    auto=Autoreply(user,password,secret)
    #登录
    while success is None:
        while auto.login1()=='登录尝试次数过多,需输入验证码':
            print('登录尝试次数过多,需输入验证码')
            auto.getverwebq()
            while auto.inputvercode()=='验证码不正确，请重新输入':
                auto.getverwebq()
                print('验证码不正确，请重新输入')
            if auto.login1()=='賬號已開啟兩步驗證':
                if auto.login2()=='已經順利登錄':
                    print('登录成功')
                    success = True
        else:
            if auto.login1()=='賬號已開啟兩步驗證':
                while auto.login2()=='已經順利登錄':
                    print('登录成功')
                    success = True
    m=auto.getnumber()
    auto.gettodaylist()
    #回复
    while n<10 and suc is False:
        auto.getonelink()
        auto.getreply()
        auto.getmatch()
        sleeptime=random.randint(1030,2048)
        au=auto.postreply()
        if au=='今日已达上限':
            print('回复成功')
            print('休眠'+str(sleeptime)+'s...')
            sleep(sleeptime)
        elif au=='今日已达上限':
            print('今日次数已达10次')
            suc=True
        else:
            print('失败！！！')
    n=auto.getnumber()
    print('开始时发表帖子:'+m)
    print('结束时发表帖子:'+n)
    print('回复'+str(int(m)-int(n))+'次')