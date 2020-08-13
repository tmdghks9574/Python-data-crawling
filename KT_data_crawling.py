import requests # 웹 페이지 소스를 얻기 위한 패키지(기본 내장 패키지이다.)
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from datetime import datetime                                # (!pip install beautifulsoup4 으로 다운받을 수 있다.)
import pandas as pd # 데이터를 처리하기 위한 가장 기본적인 패키지
import time # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
import urllib.request #
from selenium.webdriver import Chrome
import json
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime as dt
from selenium import webdriver
import numpy as np
import mutable_strings
#Crawling 할 웹 페이지 주소로 바꿔줘야함
# str1 = mutable_strings.MutStr("asdasd")
# str1[3] = '0'
# print(str1)

base_url = 'https://bdp.kt.co.kr/invoke/SOKBP2602/'

delay = 3
#browser = webdriver.Chrome('C:/Users/김영준/Desktop/chromedriver_win32/chromedriver.exe')
browser = webdriver.Chrome('C:/Users/seunghwan/Downloads/chromedriver_win32/chromedriver.exe')
browser.implicitly_wait(delay)

browser.get(base_url)
# browser.maximize_window()

browser.find_element_by_xpath('//*[@id="pageSize_nm"]').click()
browser.find_element_by_xpath('/html/body/main/section/header/div[2]/div/div/menu/li[4]/span[1]').click()
time.sleep(2)
browser.find_element_by_xpath('//*[@id="div_paging"]/a[3]').click()
#//*[@id="div_paging"]/a[3]
#//*[@id="div_paging"]/a[3]
#//*[@id="div_paging"]/a[2]
browser.implicitly_wait(3)

url_ls = []
title_ls = []
script_ls = []
price_ls = []
reload_ls = []
category_ls = []
company_ls = []
postdate_ls = []
update_term_ls = []
data_usage_period_ls = []
last_modified_ls = []
downloadable_period_ls = []
tmp_ls = []
time.sleep(2)
for i in range(1,33):
    #//*[@id="goodsList"]/dl[1]/dt/p/a
    url = browser.find_element_by_xpath('//*[@id="goodsList"]/dl[' + str(i) + ']/dt/p/a')
    url = url.get_attribute('onclick')
    url2 = url
    for i in range(len(url2)):
        if url2[i] == "'":
            k = int(i)
            break
    for i in range(k+1,len(url2)):
        if url2[i] == "'":
            l = int(i)
            break
    url3 = url2[k+1:l]
    tmp_ls.append(url3)
    final_url = 'https://bdp.kt.co.kr/invoke/SOKBP2603/?goodsCode=' + url3
    url_ls.append(final_url)

for i in range(0,32):
    if i >= 1 and i < 21:
        browser.get(url_ls[i])
    elif i >= 21 and i < 30:
        browser.get('https://bdp.kt.co.kr/invoke/SOKBP2607/?goodsCode=' + tmp_ls[i])
    else:
        browser.get(url_ls[i])

    time.sleep(0.5)
    try:
        title = browser.find_element_by_xpath('//*[@id="gd_nm"]').text
        title_ls.append(title)
    except:
        title_ls.append("not data")

    try:
        script = browser.find_element_by_xpath('//*[@id="gd_dc"]').text
        script_ls.append(script)
    except:
        script_ls.append("not data")

    try:
        postdate = browser.find_element_by_xpath('//*[@id="pblicte_dt"]').text
        postdate_ls.append(postdate)
    except:
        postdate_ls.append("not data")

    try:
        last_modified = browser.find_element_by_xpath('//*[@id="change_dt"]').text
        last_modified_ls.append(last_modified)
    except:
        last_modified_ls.append("not data")

    try:
        price = browser.find_element_by_xpath('/html/body/main/section/article[1]/div/table/tbody/tr[5]/td[1]/span/span').text
        price_ls.append(price)
    except:
        price_ls.append("not data")
    #/html/body/main/section/article[1]/div/table/tbody/tr[3]/td[2]/span/span

    try:
        category = browser.find_element_by_xpath('//*[@id="dtck_lclas_cn"]').text
        category_ls.append(category)
    except:
        category_ls.append("not data")

    try:
        company = browser.find_element_by_xpath('//*[@id="wdtb_instt_nm"]').text
        company_ls.append(company)
    except:
        company_ls.append("not data")

    try:
        reload = browser.find_element_by_xpath('//*[@id="wdtb_cycle_nm"]').text
        reload_ls.append(reload)
    except:
        reload_ls.append("not data")

    time.sleep(0.5)



# browser.back()
# body = browser.find_element_by_tag_name('body')#스크롤하기 위해 소스 추출

#갯수 맞춰서 알아서 수정하고
# num_of_pagedowns = 300 # EBS Learning
# num_of_pagedowns = 2 # EBS Learning


#Crawling 시작 시간 (build time check)
# start = time.time()

# #스크롤 하기
# while num_of_pagedowns:
#     body.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)
#     num_of_pagedowns -= 1
# html0 = browser.page_source
# html = BeautifulSoup(html0,'html.parser')
# video_ls = html.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'})
#b = html.find('div',{'id':'items','class':'style-scope ytd-grid-renderer'})


#table_ls = html.find_all('a',{'class':'table table-bordered table striped v-middle'})
# table_ls = html.find_all('div',{'id':'list-results-wrap'})
# print(table_ls)

dataset = pd.DataFrame({'제목' : [],
                        '내용' : [],
                        '등록일' : [],
                        '최종 수정일' : [],
                        '가격' : [],
                        '카테고리' : [],
                        '업데이트 주기' : [],
                        '제공기관' : [],
                        'url': []})

#//*[@id="frm"]/div[2]/div/div[2]/div/div[1]/div[2]/a[1]
# url = browser.find_element_by_xpath('//*[@id="frm"]/div[2]/div/div[2]/div/div[1]/div[2]/a[1]')
# url = url.get_attribute('href')
# browser.find_element_by_xpath('//*[@id="frm"]/div[2]/div/div[2]/div/div[1]/div[2]/a[1]').click()
# url_ls.append(url)
# title = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[1]/dl/dd/strong').text
# category = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]').text
# company = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[2]/td[1]').text
# postdate = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[3]/td[1]').text
# update_term = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[4]/td[1]').text
# data_usage_period = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[5]/td[1]').text
# last_modified = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[3]/td[2]').text
# downloadable = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[4]/td[2]').text
# print(title)
# print(category)
# print(company)
# print(postdate + update_term + data_usage_period + last_modified + downloadable)
# print(url)
# exit()
k = 0
# for j in range(1,24):
#     k += 1

# url = browser.find_element_by_xpath('//*[@id="frm"]/div[2]/div/div[2]/div/div[1]/div[2]/a[' + str(i) + ']')
# url = url.get_attribute('href')
# browser.find_element_by_xpath('//*[@id="frm"]/div[2]/div/div[2]/div/div[1]/div[2]/a[1]').click()
# url_ls.append(url)


        #print(url)
    #button = browser.find_element_by_xpath('//*[@id="frmList"]/div/div[4]/div/span/a[' + str(k+1) + ']').click()
for i in range(0, 32):
    insert_data = pd.DataFrame({
                                '제목' : [title_ls[i]],
                                '내용' : [script_ls[i]],
                                '등록일' : [postdate_ls[i]],
                                '최종 수정일' : [last_modified_ls[i]],
                                '가격' : [price_ls[i]],
                                '카테고리' : [category_ls[i]],
                                '업데이트 주기' : [reload_ls[i]],
                                '제공기관' : [company_ls[i]],
                                'url' : [url_ls[i]]})

    dataset = dataset.append(insert_data)

df = pd.DataFrame.from_records(dataset)
df.to_excel('test.xlsx')
exit()
#sample = html.find('a',{'class':'btn btn-sm btm-outline-primary landing-page-btn'})['href']



# video_info = pd.DataFrame({
#                            'channel':[],
#                            'title':[],
#                            'view':[],
#                            'like':[],
#                            'dislike':[],
#                            #'comment':[],
#                            'time_categorization':[],
#                            'run_time(초)':[],
#                            'post_date(게시일)':[],
#                            'tag':[],
#                            'url':[]})
#
