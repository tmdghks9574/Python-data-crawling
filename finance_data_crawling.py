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

base_url = 'https://www.bigdata-finance.kr/dataset/datasetList.do'

delay = 3
#browser = webdriver.Chrome('C:/Users/김영준/Desktop/chromedriver_win32/chromedriver.exe')
browser = webdriver.Chrome('C:/Users/seunghwan/Downloads/chromedriver_win32/chromedriver.exe')
browser.implicitly_wait(delay)

browser.get(base_url)
# browser.maximize_window()


body = browser.find_element_by_tag_name('body')#스크롤하기 위해 소스 추출

#갯수 맞춰서 알아서 수정하고
# num_of_pagedowns = 300 # EBS Learning
num_of_pagedowns = 2 # EBS Learning


#Crawling 시작 시간 (build time check)
# start = time.time()

# #스크롤 하기
# while num_of_pagedowns:
#     body.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)
#     num_of_pagedowns -= 1
html0 = browser.page_source
html = BeautifulSoup(html0,'html.parser')
# video_ls = html.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'})
#b = html.find('div',{'id':'items','class':'style-scope ytd-grid-renderer'})

#각 데이터를 담을 list 목록
l_url = [] # url list
platform_ls = [] # 플랫폼


url_ls = []
title_ls = []
category_ls = []
company_ls = []
postdate_ls = []
update_term_ls = []
data_usage_period_ls = []
last_modified_ls = []
downloadable_period_ls = []
#table_ls = html.find_all('a',{'class':'table table-bordered table striped v-middle'})
# table_ls = html.find_all('div',{'id':'list-results-wrap'})
# print(table_ls)
#//*[@id="frmList"]/div/div[3]/div[2]/div/ul/li[2]/a
#//*[@id="frmList"]/div/div[3]/div[2]/div/ul/li[19]/a
#//*[@id="frmList"]/div/div[3]/div[2]/div/ul/li[1]/a
dataset = pd.DataFrame({'url': [],
                        '제목' : [],
                        '카테고리' : [],
                        '제공기관' : [],
                        '등록일' : [],
                        '업데이트 주기' : [],
                        '데이터 사용기간' : [],
                        '최종 수정일' : [],
                        '다운로드 가능기간' : []})

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

for i in range(1,2):
    url = browser.find_element_by_xpath('//*[@id="frm"]/div[2]/div/div[2]/div/div[1]/div[2]/a[' + str(i) + ']')
    url = url.get_attribute('href')
    browser.find_element_by_xpath('//*[@id="frm"]/div[2]/div/div[2]/div/div[1]/div[2]/a[1]').click()
    url_ls.append(url)

    title = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[1]/dl/dd/strong').text
    title_ls.append(title)

    category = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]').text
    category_ls.append(category)

    company = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[2]/td[1]').text
    company_ls.append(company)

    postdate = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[3]/td[1]').text
    postdate_ls.append(postdate)

    update_term = browser.find_element_by_xpath('//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[4]/td[1]').text
    update_term_ls.append(update_term)

    data_usage_period = browser.find_element_by_xpath(
        '//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[5]/td[1]').text
    data_usage_period_ls.append(data_usage_period)

    last_modified = browser.find_element_by_xpath(
        '//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[3]/td[2]').text
    last_modified_ls.append(last_modified)

    downloadable = browser.find_element_by_xpath(
        '//*[@id="contain"]/div[2]/div/div[2]/table/tbody/tr[4]/td[2]').text
    downloadable_period_ls.append(downloadable)

    browser.implicitly_wait(1)
        #print(url)
    #button = browser.find_element_by_xpath('//*[@id="frmList"]/div/div[4]/div/span/a[' + str(k+1) + ']').click()
for i in range(0, len(url_ls)):
    insert_data = pd.DataFrame({'url' : [url_ls[i]],
                                '제목' : [title_ls[i]],
                                '카테고리' : [category_ls[i]],
                                '제공기관' : [company_ls[i]],
                                '등록일' : [postdate_ls[i]],
                                '업데이트 주기' : [update_term_ls[i]],
                                '데이터 사용기간' : [data_usage_period_ls[i]],
                                '최종 수정일' : [last_modified_ls[i]],
                                '다운로드 가능기간' : [downloadable_period_ls]})

    dataset = dataset.append(insert_data)

df = pd.DataFrame.from_records(dataset)
df.to_excel('test.xlsx')
exit()
#sample = html.find('a',{'class':'btn btn-sm btm-outline-primary landing-page-btn'})['href']


#url, title, run time Crawling
# for i in range(len(video_ls)):
#     url = base_url+video_ls[i].find('a',{'id':'thumbnail'})['href']
#     l_url.append(url)
#     run_time = video_ls[i].find('span',{'class':'style-scope ytd-thumbnail-overlay-time-status-renderer'})
#     minute = 60
#     tim = 1
#     try:
#         tmp = run_time.text
#         for k in range(len(tmp)):
#             if len(tmp) >= 18:
#                 if tmp[k] == ':':
#                     tmp2 = tmp[0:k]
#                     tim = int(tmp2)*3600
#                     tmp2 = tmp[k+1:k+3]
#                     tim = tim + int(tmp2) * minute
#                     tmp2 = tmp[k+4:k+6]
#                     tim = tim + int(tmp2)
#                     break
#             elif tmp[k] == ':':
#                 tmp2 = tmp[0:k]
#                 tim = int(tmp2) * minute
#                 tim = tim + int(tmp[k+1:])
#         #시간에 따른 분류 코드 (0~2분:0, 2~5분:1, 5~20분:2, 20~60분:3, 60분 이상:4)
#         if tim < 120:
#             time_categorization_ls.append('0')
#         elif tim < 300:
#             time_categorization_ls.append('1')
#         elif tim < 1200:
#             time_categorization_ls.append('2')
#         elif tim < 3600:
#             time_categorization_ls.append('3')
#         else:
#             time_categorization_ls.append('4')
#
#
#
#
#         run_time_ls.append(tim)
#     except:
#         run_time_ls.append("not data")
#         time_categorization_ls.append('null')
#
#     title = video_ls[i].find('a',{'id':'video-title'})
#     title_ls.append(title.text)
#     view = video_ls[i].find('span',{'class' : 'style-scope ytd-grid-video-renderer'})
#
#     #조회수
#     try:
#         str1 = view.text
#         str1 = str1[4:]
#         #print(str1)
#         for j in range(len(str1)):
#             if str1[j] == '.':
#                 if str1[j+2] == '만':
#                     str2 = str1[0:j] + str1[j+1] + "000"
#                     #print(str2)
#                     break
#             if str1[j] == '.':
#                 if str1[j+2] == '천':
#                     str2 = str1[0:j] + str1[j+1] + "00"
#                     #print(str2)
#                     break
#             elif str1[j] == '.':
#                 if str1[j+2] == '억':
#                     str2 = str1[0:j] + str1[j+1] + "0000000"
#                     break
#             elif str1[j] == '만':
#                 str2 = str1[0:j] + "0000"
#                 #print(str2)
#                 break
#                 #print(str2)
#             elif str1[j] == '억':
#                 str2 = str1[0:j] + "0000000"
#                 break
#             elif str1[j] >= '0' and str1[j] <= '9' and str1[j+1] == '회':
#                 str2 = str1[0:len(str1)-1]
#
#     except:
#         str2 = "not data"
#
#     view_ls.append(str2)
#
# #게시일, 조회수 가져오기
# for i in range(0, len(title_ls)):
#     soup0 = browser.page_source
#     soup = BeautifulSoup(soup0,'html.parser')
#     info1 = soup.find('div',{'id':'info-contents'})
#     # browser.get(l_url[i])
#     # time.sleep(1)
#     #게시일 가져오기
#     try:
#         browser.get(l_url[i])
#         time.sleep(2)
#
#         post = browser.find_element_by_xpath('//*[@id="date"]/yt-formatted-string').text
#         # print(post)
#         postdate_ls.append(post)
#
#     except:
#         postdate_ls.append("not data")
#
#     # 조회수 가져오기
#     try:
#         view = browser.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]').text
#         view_count = view[4:int(len(view)) - 1]
#         # print(view_count)
#         view_ls.append(view_count)
#
#     except:
#         view_ls.append("not data")
#
#     # 좋아요
#     try:
#         like = info1.find('yt-formatted-string',{'id': 'text', 'class': 'style-scope ytd-toggle-button-renderer style-text'})['aria-label']
#         str1 = like
#         str1 = str1[4:len(str1)-1]
#         #print(str1)
#         like_ls.append(str1)
#
#     except:
#         like_ls.append(l_url[i])
#
#     # 싫어요
#     try:
#         dislike = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[1].text
#         str1 = dislike
#         for j in range(len(str1)):
#             if str1[j] == '.':
#                 if str1[j+2] == '만':
#                     str2 = str1[0:j] + str1[j+1] + "000"
#                     #print(str2)
#                     break
#             if str1[j] == '.':
#                 if str1[j+2] == '천':
#                     str2 = str1[0:j] + str1[j+1] + "00"
#                     #print(str2)
#                     break
#             elif str1[j] == '만':
#                 str2 = str1[0:j] + "0000"
#                 #print(str2)
#                 break
#                 #print(str2)
#             elif str1[j] == '천':
#                 str2 = str1[0:j] + "000"
#                 break
#             if str1[len(str1)-1] >= '0' and str1[len(str1)-1] <= '9':
#                 str2 = str1
#         dislike_ls.append(str2)
#     except:
#         dislike_ls.append(l_url[i])
#
#     try:
#         try:
#             tag = browser.find_element_by_xpath("//*[@id='container']/yt-formatted-string/a[1]").text
#         except:
#             tag += ""
#         try:
#             tag2 = browser.find_element_by_xpath("//*[@id='container']/yt-formatted-string/a[2]").text
#             tag = tag + " " + tag2
#         except:
#             tag += ""
#         try:
#             tag2 = browser.find_element_by_xpath("//*[@id='container']/yt-formatted-string/a[3]").text
#             tag = tag + " " + tag2
#         except:
#             tag += ""
#
#         tag_ls.append(tag)
#         #print(tag)
#         tag = ""
#         #print(tag_ls)
#     except:
#         tag_ls.append("not data")
#         #print("not data")
#
#
#
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
# #채널 명 추가하기
# for i in range(0, len(video_ls)):
#     channel_ls.append(channel)
#
# for i in range(0, len(video_ls)):
#
#     insert_data = pd.DataFrame({
#                                 'channel': [channel_ls[i]],
#                                 'title': [title_ls[i]],
#                                 'view': [view_ls[i]],
#                                 'like': [like_ls[i]],
#                                 'dislike': [dislike_ls[i]],
#                                 # 'comment': [comment],
#                                 'time_categorization': [time_categorization_ls[i]],
#                                 'run_time(초)': [run_time_ls[i]],
#                                 'post_date(게시일)': [postdate_ls[i]],
#                                 'tag' : [tag_ls[i]],
#                                 'url': [l_url[i]]})
#
#     video_info = video_info.append(insert_data)
#
# df = pd.DataFrame.from_records(video_info)
# df.to_excel('test.xlsx')