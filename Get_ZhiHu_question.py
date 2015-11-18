#coding:utf-8
import urllib2
import urllib
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

class ZHIHU:
    def __init__(self,url):
        self.url=url
        self.tool=Tool()
        self.file=None

    # 获取页面源码
    def gethtml(self):
        url=self.url
        request=urllib2.Request(url)
        respones=urllib2.urlopen(request)
        html=respones.read()
        return html

    # 获取知乎的标题
    def gettitle(self,html):
        pattern=re.compile('<h2 class="zm-item-title.*?>(.*?)</h2>',re.S)
        title=re.search(pattern,html)
        if title:
            return title.group(1).strip()
        else:
            return None

    # 获取知乎问题的问题描述
    def getdetail(self,html):
        pattern=re.compile('<div id="zh-question-detail.*?>.*?<div class="zm-editable.*?>(.*?)</div>.*?</div>',re.S)
        detail=re.search(pattern,html)
        if detail:
            return detail.group(1).strip()
        else:
            return None

    #获取知乎的回答
    def getque(self,html):
        pattern=re.compile('<div class="zm-item-rich-text.*?>.*?</div>.*?<div class="zm-editable-content.*?>(.*?)</div>',re.S)
        items=re.findall(pattern,html)
        contents=[]
        i=0
        for item in items:
            if(i<10):
                content="\n"+self.tool.replace(item)+"\n"
                contents.append(content)
                i+=1
        return contents

    def getvote(self,html):
        pattern=re.compile('<div class="zm-votebar.*?>.*?<button class="up.*?>.*?<span class="count.*?>(.*?)</span>',re.S)
        items=re.findall(pattern,html)
        votes=[]
        i=0
        for item in items:
            if (i<10):
                item="\n"+self.tool.replace(item)+"\n"
                votes.append(item)
                i+=1
        return votes


    #设置本次读取的文件名
    def filename(self,title):
        if title:
            self.file=open(title+".txt","w+")
        else:
            print "文件创建出错！"

    #向文件中写入数据
    def writefile(self,question,detail,votes):
        if detail:
            miaoshu="\n"+"本次的问题描述为："+"\n"+self.tool.replace(detail)+"\n"
            self.file.write(miaoshu)
        else:
            print "写入问题描述出错！"

        if question:
            i=1
            a=0
            for que in question:
                biaoji="\n"+"第"+str(i)+"个回答："+"\n"+"本回答的点赞数为："+str(votes[a])+"\n"
                self.file.write(biaoji)
                self.file.write(que)
                i+=1
                a+=1
        else:
            print "写入回答出错！"



    def start(self):
        html=self.gethtml()
        print "已获取知乎页面的源代码，正在获取问题："
        title=self.gettitle(html)
        print "本次获取的知乎问题为：",title
        detail=self.getdetail(html)
        question=self.getque(html)
        votes=self.getvote(html)
        print "正在创建知乎文件..."
        self.filename(title)
        print "本次所创建的文件为："+title+".txt"
        self.writefile(question,detail,votes)


print "欢迎使用知乎回答抓取，请输入知乎的帖子编号："
url='http://www.zhihu.com/question/'+raw_input("http://www.zhihu.com/question/")
zhihu=ZHIHU(url)
zhihu.start()
