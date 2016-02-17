import urllib
import urllib2
import re

from django.http import HttpResponse

def home(request):
    # request = urllib2.Request("http://www.baidu.com")
    # response = urllib2.urlopen(request)
    # return HttpResponse(response.read())

    values = {}
    values['email'] = "hebinn@hotmail.com"
    values['password'] = "steer101214"
    data = urllib.urlencode(values) 
    url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
    request = urllib2.Request(url,data)
    try:
        response = urllib2.urlopen(request)
        return HttpResponse(response.read())
    except urllib2.HTTPError, e:
        print e.code
        print e.reason
        return HttpResponse(e.code) 

def home2(request):
    html = getImg("http://www.healforce.com/cn/index.php?ac=article&at=read&did=471")
    return HttpResponse(html) 

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    reg = r'src=".+\.jpg" style'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    # x = 0
    # for imgurl in imglist:
    #     urllib.urlretrieve(imgurl,'%s.jpg' % x)
    #     x+=1    
    return imglist      
