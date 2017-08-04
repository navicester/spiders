from selenium import webdriver
import time
import os
#from bs4 import BeautifulSoup
''' 

''' 


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def webdriver_env_setup():
    #chrome path error solution (II)
    os.environ["webdriver.chrome.driver"] = "E:\Tools\Python\seleniumDriver\chromedriver.exe"
    #OR
    driver = webdriver.Chrome(r"E:\Tools\Python\seleniumDriver\chromedriver.exe")

def login(browser,loginurl):
    browser.get(loginurl)  
    time.sleep(1)

    username = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='id_username']")))
    username.send_keys("bhe001")   
    print "name sent"    
    time.sleep(1)
    password = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='id_password']")))
    password.send_keys("Navice18@")    
    print "password sent"    
    sign = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='submit-id-sign_in']")))
    sign.click()
    print "sign sent"    
    time.sleep(1)
    
def wait_until_web_loaded(browser):
    cell_id = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ui-grid-cell-id"))) 
    if cell_id:
        return True
    return False
'''
    OPEN Chrome
'''
browser = webdriver.Chrome()
loginurl = 'http://asb-rp.wroclaw.nsn-rdnet.net/login/?next=/reports/test-runs/%3Fca%3D%2522DevSH3%2522%26result%3D%2522not%2520analyzed%2522%26fs%3D4g/'  
#targeturl = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/%3Fca%3D%2522DevSH3%2522%26result%3D%2522not%2520analyzed%2522%26fs%3D4g/'  
#targeturl = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?result=%2522not%2520analyzed%2522&end_db=25&ca=%2522DevSH3%2522&limit=25&res_tester=huihz'  
targeturl = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?result=%22not%20analyzed%22&end_db=10&ca=%22DevSH3%22&limit=25&res_tester=huihz'  
#targeturl = 'http://asb-rp.wroclaw.nsn-rdnet.net/reports/test-runs/?result=%22not%20analyzed%22&end_db=30&ca=%22DevSH3%22&limit=25'  

login(browser,loginurl)
browser.get(targeturl) 
"""
    Wait until loaded
"""
if False == wait_until_web_loaded(browser):
    #browser.refresh()
    browser.get(targeturl) 
    #time.sleep(60)    

"""
    Get Header
"""

file = open('output\output %s.csv' % (time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))), 'w')

# find_element_by_class_name WebElement
headers = browser.find_elements_by_class_name('ui-grid-header-cell-label')
list_elems_of_header = []
for elem_of_header,count in zip(headers,range(0,len(headers))):
    list_elems_of_header.append(elem_of_header.get_attribute('innerHTML'))    

print list_elems_of_header
#os._exit(0)

"""
    Get Body cells
"""    
list_elems_in_first_page = browser.find_elements_by_class_name('ui-grid-cell')
list_elems_in_first_page = list_elems_in_first_page[25:] #workaround, 0~24 are header with class ui-grid-cell-contents

    
#list_list_elems_per_row = [[]]*(len(list_elems_in_first_page)/len(headers))
list_list_elems_per_row = [[]]
inner_index = 0  #index in one page
last_index = 0   #index in total

for loop_elem,count in zip(list_elems_in_first_page,range(0,len(list_elems_in_first_page))):
    inner_index = count/len(headers)
    list_list_elems_per_row[last_index + inner_index].append(loop_elem.text)
    if last_index + inner_index >= len(list_list_elems_per_row)-1:
        list_list_elems_per_row.append([])

last_index = last_index + inner_index + 1

#cur_page = browser.find_element_by_class_name('ui-grid-pager-control-input').text
#total_page = browser.find_element_by_class_name('ui-grid-pager-max-pages-number').text
is_not_last = browser.find_element_by_class_name('ui-grid-pager-last').is_enabled()

while browser.find_element_by_class_name('ui-grid-pager-last').is_enabled(): #cur_page < total_page:
    next = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='ui-grid-pager-next']")))
        #EC.presence_of_element_located((By.XPATH, "//button[@class=''ui-grid-pager-last']")))
    next.click()
    cell_id = WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ui-grid-cell-id")))    
    #cur_page = browser.find_element_by_class_name('ui-grid-pager-control-input')    

    list_elems_in_next_page = []
    list_elems_in_next_page = browser.find_elements_by_class_name('ui-grid-cell')
    list_elems_in_next_page = list_elems_in_next_page[25:] #workaround, 0~24 are header with class ui-grid-cell-contents
    
    if browser.find_element_by_class_name('ui-grid-pager-last').is_enabled() == False:
        pass
        '''
        print browser.find_element_by_class_name('ui-grid-pager-last').is_enabled()
        #browser.refresh()
        a = browser.find_elements_by_class_name('ui-grid-icon-ok')
        b = browser.find_elements_by_class_name('ui-grid-selection-row-header-buttons')
        container = browser.find_element_by_class_name('ui-grid-render-container-body')
        print len(a), len(b)
        
        i=0
        container_body = container.find_elements_by_xpath("//div[@role='rowgroup']")[1]
        #bodies2 = container_body.find_elements_by_class_name('ui-grid-cell')
        bodies2 = browser.find_elements_by_xpath("//*[contains(@class, 'ui-grid-cell ng-scope ui-grid-coluiGrid')]")

        print len(bodies2)
        for body in bodies2:
            print str(i) + " - " +body.get_attribute('innerHTML')
            i = i + 1
        '''
    
    for loop_elem,count in zip(list_elems_in_next_page,range(0,len(list_elems_in_next_page))):
        inner_index = count/len(headers)
        #print last_index, inner_index, len(list_list_elems_per_row)
        try:
            list_list_elems_per_row[last_index + inner_index].append(loop_elem.text)
            #print "list_elems_per_row_loop[%d][%d] = %s" % (last_index + inner_index + 1, count % (len(headers)), loop_elem.text)            
        except:
            print "raised exception" # for the last page
            #print loop_elem.is_displayed()            
            #print list_list_elems_per_row[last_index + inner_index]
            #print list_elems_in_next_page
            print last_index
            print inner_index
            print len(list_list_elems_per_row)
            print len(list_elems_in_next_page)
            print count
            #print loop_elem.get_attribute('innerHTML')
            break
        if last_index + inner_index >= len(list_list_elems_per_row)-1:
            list_list_elems_per_row.append([])

    last_index = last_index +  inner_index + 1
    list_list_elems_per_row.append([])

idx_Responsible_Tester  = list_elems_of_header.index('Responsible Tester')  
idx_exe_time = list_elems_of_header.index('End')
list_header_extended = list(list_elems_of_header)
list_header_extended.insert(idx_exe_time+1,"Exe Time") ###############????????

'''
{ date : { tester : number}
'''
dict_not_analysis_per_date = {}
'''
{ tester : { date : number}
'''
dict_not_analysis_per_tester = {}

for elem_head in list_header_extended:
    file.write( elem_head + "$")
file.write('\n')

for list_elems_per_row_loop in list_list_elems_per_row:    
    try:
        tester_name = list_elems_per_row_loop[idx_Responsible_Tester]
        exe_time = list_elems_per_row_loop[idx_exe_time][0:10] 
        
        dict_not_analysis_per_tester.update({tester_name:{exe_time:0}})     
               
        if dict_not_analysis_per_date.has_key(exe_time):
            dic_not_analy_per_day = dict_not_analysis_per_date.get(exe_time)
            if dic_not_analy_per_day.has_key(tester_name):
                dic_not_analy_per_day[tester_name] = dic_not_analy_per_day[tester_name] + 1
            else:
                dic_not_analy_per_day.update({tester_name:1})
        else:
            dict_not_analysis_per_date.update({exe_time:{tester_name:1}})
            
        list_elems_per_row_loop.insert(idx_exe_time+1, exe_time )
    except:
        print len(list_elems_per_row_loop)
        if 0 == len(list_elems_per_row_loop):
            continue
            
    for elem_loop_in_row in list_elems_per_row_loop:
        file.write("".join(elem_loop_in_row.split()) + "$")
    file.write('\n')


for key_date,value in dict_not_analysis_per_date.items():
    for key_tester,value0 in value.items():
        if dict_not_analysis_per_tester.has_key(key_tester):
            dict_not_analysis_per_tester[key_tester].update({key_date : value0})
        else:
            dict_not_analysis_per_tester.update({key_tester : {key_date : 0} })

print dict_not_analysis_per_tester
print dict_not_analysis_per_date

html_file = open('export\export %s.html' % (time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))), 'w')
head = ""
output_bodies = ""
date_keys = list(dict_not_analysis_per_date.keys())
date_keys.sort()

for key in date_keys:
    head = head + "<th>" + str(key) + "</th>"
for key_tester, value in dict_not_analysis_per_tester.items():
    output_bodies = output_bodies+ "<tr>"
    output_bodies = output_bodies + "<td>" + key_tester + "</td>"
    for key in date_keys:
        if value.has_key(key):
            output_bodies = output_bodies + "<td class='highlight'>" +  str(value.get(key,0)) + "</td>"
        else:
            output_bodies = output_bodies + "<td>" +  str(0) + "</td>"
    output_bodies = output_bodies+ "</tr>"        
    
html = """\
<style type="text/css">
<!--
table.t1 {
border-width: 1px 0 0 1px;
border-style: solid;
border-color: #666;
}
table.t1 td{
border-width: 0 1px 1px 0;
border-style: solid;
border-color: #666;
font:Arial;
text-align:center;

td.highlight{
font-color:red;
background-color:yellow;
}
}
-->
</style>

<html>
  <head></head>
  <body>
    <p>Hi All!<br>
      Not Analysis Test Cases to be completed, please take actions!!
        <table border="1" class="t1">
          <tr>
            <th>Name</th> """ + head + """
          </tr>""" + output_bodies + """
        </table>
    </p>
  </body>
</html>
"""

html_file.write(html)
html_file.close()
            
file.close()
#browser.close()
    
'''
driver=webdriver.PhantomJS()
driver.get(targeturl)
result = BeautifulSoup(driver.page_source,'lxml').find_all('div',class_='ui-grid-contents-wrapper')
print len(result)
'''
    
    
'''
username = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
username.clear()
username.send_keys("bhe001")
nextButton = browser.find_element_by_id('username')
nextButton.click()
time.sleep(3)

browser.execute_script("document.getElementById('password').setAttribute('class', 'form-control')")
password = WebDriverWait(browser, 50).until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
password.clear()
password.send_keys("Navice18@")
browser.execute_script("document.getElementById('password').disabled=false")
signinButton = browser.find_element_by_id('idSIButton9')
signinButton.send_keys(u"login")
signinButton.click()
time.sleep(5)
browser.close()
'''

'''
driver.get("http://somedomain/url_that_delays_loading")
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
finally:
    driver.quit()
'''    