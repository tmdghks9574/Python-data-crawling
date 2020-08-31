import requests # 웹 페이지 소스를 얻기 위한 패키지(기본 내장 패키지이다.)
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from datetime import datetime                                # (!pip install beautifulsoup4 으로 다운받을 수 있다.)
import pandas as pd # 데이터를 처리하기 위한 가장 기본적인 패키지
import time # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
from selenium.webdriver import Chrome
from selenium import webdriver
import numpy as np

base_url = 'https://bdp.kt.co.kr/invoke/SOKBP2602/'

delay = 3
browser = webdriver.Chrome('C:/Users/seunghwan/Downloads/chromedriver_win32/chromedriver.exe')
browser.implicitly_wait(delay)

browser.get(base_url)

browser.find_element_by_xpath('//*[@id="pageSize_nm"]').click()
browser.find_element_by_xpath('/html/body/main/section/header/div[2]/div/div/menu/li[4]/span[1]').click()
time.sleep(2)
browser.find_element_by_xpath('//*[@id="div_paging"]/a[3]').click()

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
tag_ls = []
tmp_ls = []
time.sleep(2)
for i in range(1,33):
    url = browser.find_element_by_xpath('//*[@id="goodsList"]/dl[' + str(i) + ']/dt/p/a')
    url = url.get_attribute('onclick')
    url2 = url

    # url을 뽑기 위해서 스트링 처리
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

    try:
        tag = browser.find_element_by_xpath('//*[@id="tag_li"]').text
        print(tag)
    except:
        print("not data")
    exit()

    time.sleep(0.5)

dataset = pd.DataFrame({'제목' : [],
                        '내용' : [],
                        '등록일' : [],
                        '최종 수정일' : [],
                        '가격' : [],
                        '카테고리' : [],
                        '업데이트 주기' : [],
                        '제공기관' : [],
                        '태그' : [],
                        'url': []})

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
                                '태그' : [tag_ls[i]],
                                'url' : [url_ls[i]]})

    dataset = dataset.append(insert_data)

df = pd.DataFrame.from_records(dataset)
df.to_excel('test.xlsx')
exit()