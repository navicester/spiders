
import urllib  
import urllib2  

print "hello"

url = 'http://wlsweb.cn.alcatel-lucent.com/heros/login.php'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
values = {'cs1' : 'bhe001',  'password' : 'Navice11@' }  
headers = { 'User-Agent' : user_agent }  
data = urllib.urlencode(values)  
request = urllib2.Request(url, data, headers)  
response = urllib2.urlopen(request)  
page = response.read()
print page





