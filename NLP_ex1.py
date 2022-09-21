#coding=utf-8
from numpy import nested_iters
import requests
import sys
from bs4 import BeautifulSoup
import os
from math import log
import sys

class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'w')
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass

def get_text(url):
    try:
        news=''
        r=requests.get(url)
        r.encoding=r.apparent_encoding
        soup = BeautifulSoup(r.text,'html.parser')
        title=soup.title.text.strip()
        title+="!!!!"
        news+=title
        for x in soup.find_all('div',{'id':['detail']}):
            for y in x.find_all('p'):
                text=y.text.strip()
                news+=text
        return news
    except:
        print("fail for crawler_1")
        
def getHTMLText(url):
    try:
        r=requests.get(url)
        r.encoding=r.apparent_encoding
        return r.text
    except:
        print("fail for crawler_2")
        
def get_all_url(url):
    try:
        news_list=[]
        r=requests.get(url)
        r.encoding=r.apparent_encoding
        soup=BeautifulSoup(r.text,'html.parser')
        tags=soup.find_all('a')
        for tag in tags:
            news_list.append(str(tag.get('href')).strip())
        return news_list
    except:
        print("fail for crawler_3")
    
def get_xinhua_news(home_url):
    path='data_en_test4.text'
    news_list=[]
    url_list=get_all_url(home_url)
    url_list=list(set(url_list))
    for url in url_list:
        news=get_text(url)
        if news==None:
            continue
        if news=='javascript:void(0)':
            continue
        news_list.append(news)
        write_text(news_list,path)
 
def write_text(news_list,path):
    jg=open(path,'a')
    jg.write(str(news_list))
    jg.close()
    
def data_clean(path1,path2):
    kk=open(path2,'a')
    jg=open(path1,encoding = "utf-8")
    temp = jg.read()
    X,Y = ['\u0061','\u007a']
    #X,Y = ['\u4e00','\u9fa5']
    for x in temp:
        if X <= x <= Y:
            kk.write(x)
    kk.close
    jg.close
      
def split(filename):
    jg=open(filename,encoding = "utf-8")
    size = 1000000
    sub = 1
    while size <= 6000000:
        buf = jg.read(size)
        sub = mkfile(filename,sub,buf)
        size = size + 1000000
        
     
def mkfile(filename,sub,buf):
    [ex,la] = os.path.splitext(filename)
    temp = ex + '_' + str(sub) + la
    with open(temp,'a') as fout:
        fout.write(buf)
        return sub+1
    
def calculate(filename,size):
    wd=[]
    num=[]
    probability = []
    jg=open(filename,encoding = "utf-8")
    buf=jg.read()
    for x in buf:
        if(myfind(wd,x)):
            tem = myfind(wd,x)-1
            num[tem] = num[tem] + 1
        else:
            wd.append(x)
            num.append(float(1))
    probability = [i/size for i in num]
    shang = 0
    for x in probability:
        shang = shang + (-1*x*log(x,2))
    print("正在输出字符表...")
    print(wd)
    print("正在输出字符对应概率表...")
    #print(num)
    print(probability)
    print("文本规模=",size)
    print("熵=",shang)
           
def myfind(lst,ele):   
    for kk in lst:
        if(kk == ele):
            return lst.index(kk)+1
    return False   
    
    

if __name__=='__main__':
    sys.stdout = Logger('en_result.txt', sys.stdout)
    sys.stderr = Logger('a.log_file', sys.stderr)
    #url='https://english.news.cn/home.htm'
    #url='http://www.news.cn/2022-09/14/c_1129000047.htm'
    #url='/Users/deng/Desktop/刷题/data_en_test4.text'
    #url1='/Users/deng/Desktop/刷题/data_en_all.text'
    url = 'data_en_all.text'#choose from data_all_1-4/data_en_all
    size = os.path.getsize(url)
    #size = 4000000
    #print(get_text(url))
    # the(get_all_url(url))
    #get_xinhua_news(url)
    #data_clean(url,url1)
    #split(url)
    calculate(url,size)