# 1024-Autoreply

因为考研在即，加上1024的回复机制确实有点繁琐，所以打算用个python脚本做一个自动回帖 

通过设置

user= 'XXXXXXXX'                   		用户名

password= 'XXXXXXXX'			     密码

 secret ='XXXXXXXXXXXXXXXX'     谷歌身份验证器密钥

即可使用

其中可以通过`getreply()中的reply与reply_m(随机数)`设置回复内容，

​						`sleeptime设置为(1030,2048)之间`，可以根据需要修改

如果同一ip登录次数过多会触发验证码，生成的验证码保存为`image.webq`，如果有条件可以修改为打码平台

同样，可以修改为使用cookies登录，就不用这么繁琐了

**后继可能添加功能：**

1.修改为github Actions的形式

2.添加邮件通知功能

