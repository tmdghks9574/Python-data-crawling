import requests  # 웹 페이지 소스를 얻기 위한 패키지(기본 내장 패키지이다.)
from bs4 import BeautifulSoup  # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from datetime import datetime  # (!pip install beautifulsoup4 으로 다운받을 수 있다.)
import pandas as pd  # 데이터를 처리하기 위한 가장 기본적인 패키지
import time  # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
import urllib.request  #
from selenium.webdriver import Chrome
import json
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime as dt
from selenium import webdriver
import numpy as np

# base_url = 'https://www.bigdata-map.kr/search/theme?platformFilters=traffic'  # Big data platform 교통 11210
# base_url = 'https://www.bigdata-map.kr/search/theme?platformFilters=health' # Big data platform 헬스케어 126
# base_url = 'https://www.bigdata-map.kr/search/theme?platformFilters=finance' # Big data platform 금융 140
# base_url = 'https://www.bigdata-map.kr/search/theme?platformFilters=economy' # Big data platform 지역경제 324
base_url = 'https://www.bigdata-map.kr/search/theme?platformFilters=communication' # Big data platform 통신 140
# base_url = 'https://www.bigdata-map.kr/search/theme?platformFilters=small_business' # Big data platform 중소기업 240
# base_url = 'https://www.bigdata-map.kr/search/theme?platformFilters=environment' # Big data platform 환경 459
# base_url = 'https://www.bigdata-map.kr/search/theme?platformFilters=forest' # Big data platform 산림 463
# base_url = 'https://www.bigdata-map.kr/search/theme?platformFilters=culture' # Big data platform 문화 1548
# base_url = 'https://www.bigdata-map.kr/search/theme?platformFilters=distribution' # Big data platform 유통 3364


# platform name
# platform = '교통'
# platform = '헬스케어'
# platform = '금융'
# platform = '지역경제'
platform = '통신'
# platform = '중소기업'
# platform = '환경'
# platform = '산림'
# platform = '문화'
# platform = '유통'

delay = 3
browser = webdriver.Chrome('C:/Users/김영준/Desktop/chromedriver_win32/chromedriver.exe')
# browser = webdriver.Chrome('C:/Users/seunghwan/Downloads/chromedriver_win32/chromedriver.exe')
browser.implicitly_wait(delay)

start = time.time()

# 수집 데이터 list
platform_ls = []  # 플랫폼
title_ls = []  # 제목
type_ls = []  # 제공 타입
explain_ls = []  # 설명
createdate_ls = []  # 생성일
keyword_ls = []  # 키워드
link_ls = []  # 링크

browser.get(base_url)
time.sleep(1)

soup0 = browser.page_source
soup = BeautifulSoup(soup0, 'html.parser')

start = time.time()

for n in range(1, 25):
    try:
        for i in range(1, 20, 2):
            try:
                # title click
                browser.find_element_by_xpath("//*[@id='list-results-wrap']/div[" + str(i) + "]/div/div[1]/div[1]/a").click()
                time.sleep(1.5)

                a = browser.find_element_by_xpath('//*[@id="dataset-detail-modal"]/div/div/div[2]/table/tbody/tr[7]/td/a')
                link_ls.append(a.get_attribute('href'))
                # print(a.get_attribute('href'))
                # print(b.text)

                for j in range(2, 7):
                    try:
                        str2 = browser.find_element_by_xpath('//*[@id="dataset-detail-modal"]/div/div/div[2]/table/tbody/tr[' + str(j) + ']/td').text
                        if j == 2:
                            title_ls.append(str2)
                        elif j == 3:
                            type_ls.append(str2)
                        elif j == 4:
                            explain_ls.append(str2)
                        elif j == 5:
                            createdate_ls.append(str2)
                        else:
                            keyword_ls.append(str2)

                        str2 = ""

                    except:
                        title_ls.append("")
                        type_ls.append("")
                        explain_ls.append("")
                        createdate_ls.append("")
                        keyword_ls.append("")


                # X 버튼 click
                browser.find_element_by_xpath('//*[@id="dataset-detail-modal"]/div/div/div[1]/button/span').click()
                platform_ls.append(platform)

            except:
                print('Ooops~')

        # page 이동
        if n <= 8:
            browser.find_element_by_xpath('//*[@id="hbs-target-search-pagination"]/div/ul/li[' + str(n + 1) + ']/a').click()
            time.sleep(1.5)
        elif n >= 9 and n <= 23:
            browser.find_element_by_xpath('//*[@id="hbs-target-search-pagination"]/div/ul/li[9]/a').click()
            time.sleep(1.5)
        else:
            break

    except:
        break

traffic_info = pd.DataFrame({
    'platform': [],
    'title': [],
    'type': [],
    'explain': [],
    'create_date': [],
    'keyword': [],
    'link': []})

for i in range(0, len(platform_ls)):
    insert_data = pd.DataFrame({
        'platform': [platform_ls[i]],
        'title': [title_ls[i]],
        'type': [type_ls[i]],
        'explain': [explain_ls[i]],
        'create_date': [createdate_ls[i]],
        'keyword': [keyword_ls[i]],
        'link': [link_ls[i]]})

    traffic_info = traffic_info.append(insert_data)

df = pd.DataFrame.from_records(traffic_info)
df.to_excel('small.xlsx')

print(time.time() - start)