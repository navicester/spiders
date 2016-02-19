#coding: utf-8
import urllib
import urllib2
import re
import settings
import os
import time
from django.shortcuts import render

from django.http import HttpResponse

src = ["http://www.healforce.com/cn/index.php?ac=article&at=read&did=444",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=387",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=383",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=445",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=446",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=447",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=388",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=389",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=458",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=457",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=456",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=455",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=454",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=394",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=398",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=397",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=459",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=399",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=401",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=461",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=460",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=464",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=463",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=462",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=466",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=465",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=469",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=468",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=467",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=468",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=470",
       "http://www.healforce.com/cn/index.php?ac=article&at=read&did=471"]
src_home = "http://www.healforce.com/cn/"



def home2(request):
    imgs = []
    for inst in src:
        html = getHtml(inst)
        img = getImg(html)
        imgs.append(img)
    #return HttpResponse(imgs) 
    context = {'imgs':imgs} 
    return render(request, "home.html", context)

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    # <dt><h1>VP100鍛煎惛鏈�</h1></dt>
    req = r'\<dt\>\<h1\>(.+?)\<\/h1\>\<\/dt\>'
    title = re.compile(req)
    titlelist = re.findall(title,html)
    #filename = titlelist[0]+'-%s.jpg' % x
    dir = os.path.join(settings.MEDIA_ROOT,titlelist[0])
    dir_unicode = unicode(dir,'utf8')
    if not os.path.exists(dir_unicode):
        os.mkdir(dir_unicode)    

    # src="http://www.healforce.com/cn/datacache/pic/360_300_6e7cdb990419190a1a7e7c962cc9488b.jpg" style="display: block;">
    reg = r'src="(.+?\.jpg)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)

    x = 0
    for imgurl in imglist:
        #upfile\\2015\\12\\04\\20151204124020_996.jpg
        #upfile/2015/12/04/20151204124020_996.jpg
        list = []
        reg = r'^(upfile.+?\.jpg)'
        filename2 = re.compile(reg)
        titlelist2 = re.findall(filename2,imgurl)
        if len(titlelist2):
            imgurl = src_home + imgurl
        list = imgurl.split('/') 
        #filename = '%s.jpg' % (x)
        filename = list[len(list)-1]
        path = os.path.join(dir, filename)
        path = unicode(path,'utf8')
        if os.path.exists(path):
            '''
            y = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
            filename = '%s.%s.jpg' % (x,y)
            path = os.path.join(dir, filename)
            path = unicode(path,'utf8')
            '''
        else:
            try:
                urllib.urlretrieve(imgurl,path)
            except:
                pass
        x+=1    
  
    return imglist      

def home(request):
    # request = urllib2.Request("http://www.baidu.com")
    # response = urllib2.urlopen(request)
    # return HttpResponse(response.read())

    values = {}
    values['email'] = "hebinn@hotmail.com"
    values['password'] = "steer101214"
    data = urllib.urlencode(values) 
    url = src
    request = urllib2.Request(url,data)
    try:
        response = urllib2.urlopen(request)
        return HttpResponse(response.read())
    except urllib2.HTTPError, e:
        print e.code
        print e.reason
        return HttpResponse(e.code) 