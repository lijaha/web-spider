#coding:utf-8
import urllib
import urllib2
import re
class Tool:
    RemoveImg=re.compile('<img.*?>| {7}|')   #默认先删除匹配左边img，如左边没有，再匹配右边7个空格
    RemoveAddr=re.compile('<a.*?>|</a>')     #删除链接标签
    ReplaceLine=re.compile('<tr>|<div>|</div></p>') #把换行的标签替换为\n
    ReplaceTD=re.compile('<td>')   #把制表替换为\t
    ReplacePara=re.compile('<p.*?>')  #把段落开头替换为\n并在开头加两个空格
    ReplaceBR=re.compile('<br><br>|<br>')  #把换行和双换行替换为\n
    RemoveTag=re.compile('<.*?>')     #把其余的标签去除
    def replace(self,x):
        x=re.sub(self.RemoveImg,"",x)
        x=re.sub(self.RemoveAddr,"",x)
        x=re.sub(self.ReplaceLine,"\n",x)
        x=re.sub(self.ReplaceTD,"\t",x)
        x=re.sub(self.ReplacePara,"\n  ",x)
        x=re.sub(self.ReplaceBR,"\n",x)
        x=re.sub(self.RemoveTag,"",x)
        return x.strip()             #删除空格


class BDTB:
    def __init__(self,baseurl,num,floorTag):
        self.url=baseurl
        self.Seelz="?see_lz="+str(num)
        self.tool=Tool()         #初始化Tool的对象tool
        self.file=None           #初始化file为全局变量，file为文件操作的对象
        self.floor=1             #标记楼层
        self.floorTag=floorTag  #是否写入楼层分隔符标记
        self.defaultTitle=u"百度贴吧"


    def getHtml(self,pageNum): #获取帖子的页面代码
        Url=self.url+self.Seelz+"&pn="+str(pageNum)
        request=urllib2.Request(Url)
        response=urllib2.urlopen(request)
        return response.read().decode('utf-8')

    def getTitle(self,page):    #获取帖子的标题
        pattern=re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result=re.search(pattern,page)
        if result:
            return result.group(1).strip()  #获得匹配分组的第二部分，并通过strip去除空格部分
        else:
            return None

    def getHtmlNum(self,page):  #获取帖子的页数
        pattern=re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        num=re.search(pattern,page)
        if num:
            return num.group(1).strip()
        else:
            return None

    def getContent(self,page):              #获取帖子的内容
        pattern=re.compile('div id="post_content_.*?>(.*?)</div>',re.S)
        items=re.findall(pattern,page)
        contents=[]
        for item in items:
            content="\n"+self.tool.replace(item)+"\n"
            contents.append(content.encode('utf-8'))
        return contents

    def fileTitle(self,title):   #创建文件名
        if title is not None:
            self.file=open(title+".txt","w+")
        else:
            self.file=open(self.defaultTitle+".txt","w+")

    def WriteFlie(self,contents):      #向每一楼写入文件
        for item in contents:
            if self.floorTag ==1:
                floorLine="\n" + str(self.floor) + u"----------------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexpage=self.getHtml(1)
        pagenum=self.getHtmlNum(indexpage)
        title=self.getTitle(indexpage)
        self.fileTitle(title)
        if pagenum == None:
            print u"获取页数出错！！！"
            return

        try:
            print "本次读取的帖子的页数为"+str(pagenum)+"页:"
            for i in range(1,int(pagenum)+1):
                print "正在读取第"+str(i)+"页数据..."
                page=self.getHtml(i)
                contents=self.getContent(page)
                self.WriteFlie(contents)

        except IOError,e:
            print "错误的原因为："+e.message
        finally:
            print "读写任务完成！"






print "请输入贴吧帖子编号："
baseurl="http://tieba.baidu.com/p/"+str(raw_input("http://tieba.baidu.com/p/"))
num=1
floorTag=1
bdtb=BDTB(baseurl,num,floorTag)
bdtb.start()





