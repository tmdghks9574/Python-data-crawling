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

#Crawling 할 웹 페이지 주소로 바꿔줘야함

#start_url = 'https://www.youtube.com/c/BigHitLabels/videos' # 빅히트 url
base_url = 'https://youtube.com/'
#start_url = 'https://www.youtube.com/user/BANGTANTV/videos?view=0&flow=grid' # 방탄tv url
# start_url = 'https://www.youtube.com/c/SOURCEMUSIC/videos' # 소스뮤직 url
# start_url = 'https://www.youtube.com/c/pledisartist/videos' # 플레디스 url
# start_url = 'https://www.youtube.com/c/%EA%B8%B1%EB%B8%94Geekble/videos' # 긱블 url
start_url = 'https://www.youtube.com/c/motorgraph/videos' # 모터그래프 url
#start_url = 'https://www.youtube.com/c/EBSLearning/videos' #EBS Learning url
#start_url = 'https://www.youtube.com/channel/UCGDjzLOfSakCGHuu7uPw1hg/videos' # 미디어오늘 url
# start_url = 'https://www.youtube.com/c/VIDEOBROCCOLIYOUTOO/videos?view=0&flow=grid' #브로콜리너마저
#start_url = 'https://www.youtube.com/c/GlanceTV/videos' # 글랜스 TV

#채널 명
# channel = 'SOURCE MUSIC' #소스뮤직
# channel = 'PLEDIS ENTERTAINMENT' #플레디스
# channel = '긱블 Geekble' #긱블
channel = 'Motorgraph 모터그래프' #모터그래프
#channel = 'EBS Learning' #EBS Learning
#channel = '미디어오늘' #미디어오늘
#channel = 'GlanceTV / 글랜스TV' #글랜스TV
# channel = '브로콜리너마저' #브로콜리너마저

delay = 3
#browser = webdriver.Chrome('C:/Users/김영준/Desktop/chromedriver_win32/chromedriver.exe')
browser = webdriver.Chrome('C:/Users/seunghwan/Downloads/chromedriver_win32/chromedriver.exe')
browser.implicitly_wait(delay)

browser.get(start_url)
#browser.maximize_window()


body = browser.find_element_by_tag_name('body')#스크롤하기 위해 소스 추출

#갯수 맞춰서 알아서 수정하고
#num_of_pagedowns = 300 # EBS Learning
#num_of_pagedowns = 120 # 방탄 TV
num_of_pagedowns = 150 # 모터그래프
#num_of_pagedowns = 40 # bit hit labels
# num_of_pagedowns = 1 # test
# num_of_pagedowns = 8 # 쏘스뮤직
#num_of_pagedowns = 25 # 플레디스
# num_of_pagedowns = 20 # 긱블
# num_of_pagedowns = 20 # 브로콜리너마저

#Crawling 시작 시간 (build time check)
start = time.time()

#스크롤 하기
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    num_of_pagedowns -= 1
html0 = browser.page_source
html = BeautifulSoup(html0,'html.parser')
video_ls = html.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'})
b = html.find('div',{'id':'items','class':'style-scope ytd-grid-renderer'})

#각 데이터를 담을 list 목록
l_url = [] # url list
run_time_ls = [] # run time list
title_ls = [] # title list
view_ls = [] # view(조회수) list
time_categorization_ls = [] # 시간에 따른 분류 list
channel_ls = [] # 채널 명 list
postdate_ls = [] # 게시일 list
like_ls = [] # 좋아요 개수 list
dislike_ls = [] # 싫어요 개수 list

#전체 영상 개수
print((len(video_ls)))

#url, title, run time Crawling
for i in range(len(video_ls)):
    url = base_url+video_ls[i].find('a',{'id':'thumbnail'})['href']
    l_url.append(url)
    run_time = video_ls[i].find('span',{'class':'style-scope ytd-thumbnail-overlay-time-status-renderer'})
    minute = 60
    tim = 1
    try:
        tmp = run_time.text
        for k in range(len(tmp)):
            if len(tmp) >= 18:
                if tmp[k] == ':':
                    tmp2 = tmp[0:k]
                    tim = int(tmp2)*3600
                    tmp2 = tmp[k+1:k+3]
                    tim = tim + int(tmp2) * minute
                    tmp2 = tmp[k+4:k+6]
                    tim = tim + int(tmp2)
                    break
            elif tmp[k] == ':':
                tmp2 = tmp[0:k]
                tim = int(tmp2) * minute
                tim = tim + int(tmp[k+1:])
        #시간에 따른 분류 코드 (0~2분:0, 2~5분:1, 5~20분:2, 20~60분:3, 60분 이상:4)
        if tim < 120:
            time_categorization_ls.append('0')
        elif tim < 300:
            time_categorization_ls.append('1')
        elif tim < 1200:
            time_categorization_ls.append('2')
        elif tim < 3600:
            time_categorization_ls.append('3')
        else:
            time_categorization_ls.append('4')

        run_time_ls.append(tim)
    except:
        run_time_ls.append("not data")
        time_categorization_ls.append('9')

    title = video_ls[i].find('a',{'id':'video-title'})
    title_ls.append(title.text)
    # view = video_ls[i].find('span',{'class' : 'style-scope ytd-grid-video-renderer'})

    #조회수
    # try:
    #     str1 = view.text
    #     str1 = str1[4:]
    #     #print(str1)
    #     for j in range(len(str1)):
    #         if str1[j] == '.':
    #             if str1[j+2] == '만':
    #                 str2 = str1[0:j] + str1[j+1] + "000"
    #                 #print(str2)
    #                 break
    #         if str1[j] == '.':
    #             if str1[j+2] == '천':
    #                 str2 = str1[0:j] + str1[j+1] + "00"
    #                 #print(str2)
    #                 break
    #         elif str1[j] == '.':
    #             if str1[j+2] == '억':
    #                 str2 = str1[0:j] + str1[j+1] + "0000000"
    #                 break
    #         elif str1[j] == '만':
    #             str2 = str1[0:j] + "0000"
    #             #print(str2)
    #             break
    #             #print(str2)
    #         elif str1[j] == '억':
    #             str2 = str1[0:j] + "0000000"
    #             break
    #         elif str1[j] >= '0' and str1[j] <= '9' and str1[j+1] == '회':
    #             str2 = str1[0:len(str1)-1]
    #
    # except:
    #     str2 = "not data"
    #
    # view_ls.append(str2)

#게시일, 조회수 가져오기
for i in range(0, len(title_ls)):
    soup0 = browser.page_source
    soup = BeautifulSoup(soup0,'html.parser')
    info1 = soup.find('div',{'id':'info-contents'})
    #게시일 가져오기
    try:
        browser.get(l_url[i])
        time.sleep(2)

        post = browser.find_element_by_xpath('//*[@id="date"]/yt-formatted-string').text
        # print(post)
        postdate_ls.append(post)

    except:
        postdate_ls.append("not data")

    # 조회수 가져오기
    try:
        view = browser.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]').text
        view_count = view[4:int(len(view)) - 1]
        # print(view_count)
        view_ls.append(view_count)

    except:
        view_ls.append("not data")

    # 좋아요
    try:
        like = info1.find('yt-formatted-string',{'id': 'text', 'class': 'style-scope ytd-toggle-button-renderer style-text'})['aria-label']
        str1 = like
        str1 = str1[4:len(str1)-1]
        #print(str1)
        like_ls.append(str1)

    except:
        like_ls.append(l_url[i])

    # 싫어요
    try:
        dislike = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[1].text
        str1 = dislike
        for j in range(len(str1)):
            if str1[j] == '.':
                if str1[j+2] == '만':
                    str2 = str1[0:j] + str1[j+1] + "000"
                    #print(str2)
                    break
            if str1[j] == '.':
                if str1[j+2] == '천':
                    str2 = str1[0:j] + str1[j+1] + "00"
                    #print(str2)
                    break
            elif str1[j] == '만':
                str2 = str1[0:j] + "0000"
                #print(str2)
                break
                #print(str2)
            elif str1[j] == '천':
                str2 = str1[0:j] + "000"
                break
            if str1[len(str1)-1] >= '0' and str1[len(str1)-1] <= '9':
                str2 = str1
        dislike_ls.append(str2)
    except:
        dislike_ls.append(l_url[i])



video_info = pd.DataFrame({
                           'channel':[],
                           'title':[],
                           'view':[],
                           'like':[],
                           'dislike':[],
                           #'comment':[],
                           'time_categorization':[],
                           'run_time(초)':[],
                           'post_date(게시일)':[],
                           'url':[]})

#채널 명 추가하기
for i in range(0, len(video_ls)):
    channel_ls.append(channel)

for i in range(0, len(video_ls)):

    insert_data = pd.DataFrame({
                                'channel': [channel_ls[i]],
                                'title': [title_ls[i]],
                                'view': [view_ls[i]],
                                'like': [like_ls[i]],
                                'dislike': [dislike_ls[i]],
                                # 'comment': [comment],
                                'time_categorization': [time_categorization_ls[i]],
                                'run_time(초)': [run_time_ls[i]],
                                'post_date(게시일)': [postdate_ls[i]],
                                'url': [l_url[i]]})

    video_info = video_info.append(insert_data)

df = pd.DataFrame.from_records(video_info)
df.to_excel('test.xlsx')

#print(time.time()-start)
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