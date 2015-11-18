#coding:utf-8
import urllib
import urllib2
import re
class BDTB:
    def __init__(self,url,num):
        self.url=url
        self.seelz="?see_lz="+str(num)


    def gethtml(self,pagenum):
        url=self.url+self.seelz+"&pn="+str(pagenum)
        request=urllib2.Request(url)
        respones=urllib2.urlopen(request)
        html=respones.read()
        return html


    def getnum(self,html):
        pattern=re.compile('<li class="l_reply_num".*?</span>.*?<span class="red".*?>(.*?)</span>',re.S)
        num=re.search(pattern,html)
        if num:
            return num.group(1).strip()
        else:
            return None

    def getimg(self,html):
        print "进入函数"
        # pattern1=re.compile('ge"\ssrc="(.+?\.(?:jpg|png))"')         #该如何使用正则表达式取得图片的路径
        # pattern1=re.compile('^(<img class="BED_Image"){1}[.+?]\ssrc="(.+?\.(?:jpg|png))"')
        print "执行第一步"
        pattern1=re.compile('<img class="BDE_Image".*?src="(.*?)"[\s$]{1}')
        imglist=re.findall(pattern1,html)
        print "执行第二步"
        print "输出imglist的值：",imglist
        x = 0
        for Imgurl in imglist:
          imgurl=Imgurl.split(".")
          imgname=imgurl.pop()
          urllib.urlretrieve(Imgurl ,'%s.%s' %(x,imgname))
          x+=1

    def start(self):
        html=self.gethtml(1)
        num=self.getnum(html)
        for i in range(1,int(num)+1):
            print "正在读取第"+str(i)+"页的图片"
            html=self.gethtml(i)
            print "获取到页面了"
            self.getimg(html)
        print "本次读取结束，感谢您的使用！"




print "欢迎使用百度贴吧帖子抓取器，请输入贴子的代码："
url="http://tieba.baidu.com/p/"+raw_input("http://tieba.baidu.com/p/")
num=1
bdtb=BDTB(url,num)
bdtb.start()




