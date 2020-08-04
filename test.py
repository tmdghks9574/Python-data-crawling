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

#start_url = 'https://www.youtube.com/c/BigHitLabels/videos' # 빅히트 url
play_url = 'https://youtube.com/'
start_url = 'https://www.youtube.com/user/BANGTANTV/videos?view=0&flow=grid' # 방탄tv url
#start_url = 'https://www.youtube.com/c/SOURCEMUSIC/videos' # 소스뮤직 url
#start_url = 'https://www.youtube.com/c/pledisartist/videos' # 플레디스 url
delay = 3
browser = webdriver.Chrome('C:/Users/seunghwan/Downloads/chromedriver_win32/chromedriver.exe')
browser.implicitly_wait(delay)

browser.get(start_url)
#browser.maximize_window()


body = browser.find_element_by_tag_name('body')#스크롤하기 위해 소스 추출
num_of_pagedowns = 150 # 방탄 TV
#num_of_pagedowns = 40 # bit hit labels
#num_of_pagedowns = 1 # test
#num_of_pagedowns = 8 # 쏘스뮤직
#num_of_pagedowns = 25 # 플레디스

#10번 밑으로 내리는 것
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    num_of_pagedowns -= 1
html0 = browser.page_source
html = BeautifulSoup(html0,'html.parser')
video_ls = html.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'})
b = html.find('div',{'id':'items','class':'style-scope ytd-grid-renderer'})
#print(len(b.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'})))

big_hit_url = []
run_time_ls = []
title_ls = []
view_ls = []


for i in range(len(video_ls)):
    url = play_url+video_ls[i].find('a',{'id':'thumbnail'})['href']
    big_hit_url.append(url)
    run_time = video_ls[i].find('span',{'class':'style-scope ytd-thumbnail-overlay-time-status-renderer'})
    #print(url)
    #//*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span
    # print(run_time.text)
    minute = 60
    tim = 1
    try:
        tmp = run_time.text
        for k in range(len(tmp)):
            if tmp[k] == ':':
                tmp2 = tmp[0:k]
                tim = int(tmp2) * minute
                tim = tim + int(tmp[k+1:])
        run_time_ls.append(tim)
    except:
        run_time_ls.append("not data")

    title = video_ls[i].find('a',{'id':'video-title'})
    title_ls.append(title.text)
    view = video_ls[i].find('span',{'class' : 'style-scope ytd-grid-video-renderer'})
    #print(view.text)
    try:
        str1 = view.text
        str1 = str1[4:]
        for j in range(len(str1)):
            if str1[j] == '.':
                if str1[j+2] == '만':
                    str2 = str1[0:j] + str1[j+1] + "000"
                    #print(str2)
                    break
            elif str1[j] == '.':
                if str1[j+2] == '천':
                    str2 = str1[0:j] + str1[j+1] + "00"
                    #print(str2)
                    break
            elif str1[j] == '.':
                if str1[j+2] == '억':
                    str2 = str1[0:j] + str1[j+1] + "0000000"
                    break
            elif str1[j] == '만':
                str2 = str1[0:j] + "0000"
                #print(str2)
                break
                #print(str2)
            elif str1[j] == '억':
                str2 = str1[0:j] + "0000000"
                break

    except:
        str2 = "not data"

    #print(str1)
    view_ls.append(str2)
    #print(title.text)
    ##video-title

video_info = pd.DataFrame({'title':[],
                           'view':[],
                           #'like':[],
                           #'unlike':[],
                           #'comment':[],
                           'run_time':[],
                           'url':[]})

for i in range(0, len(video_ls)):
    #browser.get(big_hit_url[i])
    #time.sleep(0.5)

    #body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출

    #num_of_pagedowns = 2
    # 10번 밑으로 내리는 것
    # while num_of_pagedowns:
    #     body.send_keys(Keys.PAGE_DOWN)
    #     time.sleep(2)
    #     num_of_pagedowns -= 1

    #time.sleep(0.5)

    # soup0 = browser.page_source
    # time.sleep(0.5)
    # soup = BeautifulSoup(soup0, 'html.parser')
    #
    # info1 = soup.find('div', {'id': 'info-contents'})
    # run_time = browser.find_element_by_xpath('//*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span')
    # print(run_time)
    # try:
    #     comment = soup.find('yt-formatted-string',
    #                         {'class': 'count-text style-scope ytd-comments-header-renderer'}).text
    # except:
    #     comment = '댓글x'
    # title = info1.find('h1', {'class': 'title style-scope ytd-video-primary-info-renderer'}).text
    # view = \
    # info1.find('yt-view-count-renderer', {'class': 'style-scope ytd-video-primary-info-renderer'}).find_all('span')[
    #     0].text
    # like = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[0].text
    # unlike = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[1].text
    # date = soup.find('span', {'class': 'date style-scope ytd-video-secondary-info-renderer'}).text
    # print(title + "\n" + view + " " + date)

    insert_data = pd.DataFrame({'title': [title_ls[i]],
                                'view': [view_ls[i]],
                                # 'like': [like],
                                # 'unlike': [unlike],
                                # 'comment': [comment],
                                'run_time' : [run_time_ls[i]],
                                'url': [big_hit_url[i]]})

    video_info = video_info.append(insert_data)

df = pd.DataFrame.from_records(video_info)
df.to_excel('test.xlsx')
#df.to_csv('test1.csv')


# browser.get(big_hit_url[2])
# body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출
#
# num_of_pagedowns = 2
# # 10번 밑으로 내리는 것
# while num_of_pagedowns:
#     body.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)
#     num_of_pagedowns -= 1
#
# time.sleep(2)
#
# soup0 = browser.page_source
# soup = BeautifulSoup(soup0,'html.parser')
# info1 = soup.find('div',{'id':'info-contents'})
# #comment = soup.find('yt-formatted-string',{'class':'count-text style-scope ytd-comments-header-renderer'}).text
# title = info1.find('h1',{'class':'title style-scope ytd-video-primary-info-renderer'}).text
# view =info1.find('yt-view-count-renderer',{'class':'style-scope ytd-video-primary-info-renderer'}).find_all('span')[0].text
# #like = info1.find('div',{'id':'top-level-buttons'}).find_all('yt-formatted-string')[0].text
# #unlike = info1.find('div',{'id':'top-level-buttons'}).find_all('yt-formatted-string')[1].text
# #date = soup.find('span',{'class':'date style-scope ytd-video-secondary-info-renderer'}).text
# url = play_url+video_ls[i].find('a',{'id':'thumbnail'})['href']
#
# video_info = pd.DataFrame({'title':[],
#                            'view':[],
#                            #'like':[],
#                            #'unlike':[],
#                            #'comment':[],
#                            'run_time':[],
#                            'url':[]})

# for i in range(0, len(big_hit_url)):
#     browser.get(big_hit_url[i])
#     time.sleep(0.5)
#
#     body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출
#
#     num_of_pagedowns = 2
#     # 10번 밑으로 내리는 것
#     # while num_of_pagedowns:
#     #     body.send_keys(Keys.PAGE_DOWN)
#     #     time.sleep(2)
#     #     num_of_pagedowns -= 1
#
#     time.sleep(0.5)
#
#     soup0 = browser.page_source
#     time.sleep(0.5)
#     soup = BeautifulSoup(soup0, 'html.parser')
#
#     info1 = soup.find('div', {'id': 'info-contents'})
#     # run_time = browser.find_element_by_xpath('//*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span')
#     # print(run_time)
#     # try:
#     #     comment = soup.find('yt-formatted-string',
#     #                         {'class': 'count-text style-scope ytd-comments-header-renderer'}).text
#     # except:
#     #     comment = '댓글x'
#     title = info1.find('h1', {'class': 'title style-scope ytd-video-primary-info-renderer'}).text
#     view = \
#     info1.find('yt-view-count-renderer', {'class': 'style-scope ytd-video-primary-info-renderer'}).find_all('span')[
#         0].text
#     # like = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[0].text
#     # unlike = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[1].text
#     date = soup.find('span', {'class': 'date style-scope ytd-video-secondary-info-renderer'}).text
#     # print(title + "\n" + view + " " + date)
#
#     insert_data = pd.DataFrame({'title': [title],
#                                 'view': [view],
#                                 # 'like': [like],
#                                 # 'unlike': [unlike],
#                                 # 'comment': [comment],
#                                 'run_time' : [run_time_ls[i]],
#                                 'url': [big_hit_url[i]]})
#
#     video_info = video_info.append(insert_data)
#
# df = pd.DataFrame.from_records(video_info)
# df.to_excel('test.xlsx')

#video_info.index = range(len(video_info))
#video_info.index = range(len(video_info))
#print(video_info)