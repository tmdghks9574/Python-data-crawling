import requests # 웹 페이지 소스를 얻기 위한 패키지(기본 내장 패키지이다.)
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from datetime import datetime
import pandas as pd # 데이터를 처리하기 위한 가장 기본적인 패키지
import time # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
import urllib.request #
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import threading
import numpy as np

#Crawling 할 웹 페이지 주소로 바꿔줘야함

#크롤링할 웹 페이지 주소
# base_url = 'https://www.datastore.or.kr/file/list'
#
# delay = 3
# #browser = webdriver.Chrome('C:/Users/김영준/Desktop/chromedriver_win32/chromedriver.exe')
# browser = webdriver.Chrome('C:/Users/seunghwan/Downloads/chromedriver_win32/chromedriver.exe')
# browser.implicitly_wait(delay)

# 카테고리 리스트
category_ls = ["유통/물류", "문화/관광/체육", "교육/취업", "사회/경제", "보건의료/건강", "IT/과학기술", "공공행정", "안전/복지", "국토/교통",
               "환경/에너지", "농축수산", "통계", "지도/지리"]

# xpath 리스트
xpath_ls = ['//*[@id="5c2lqk70xd"]/div/div[1]/a/span[2]', '//*[@id="mn01"]/div/div[1]/a/span[2]', '//*[@id="mn02"]/div/div[1]/a/span[2]',
            '//*[@id="mn03"]/div/div[1]/a/span[2]', '//*[@id="mn04"]/div/div[1]/a/span[2]', '//*[@id="mn05"]/div/div[1]/a/span[2]',
            '//*[@id="mn06"]/div/div[1]/a/span[2]', '//*[@id="mn07"]/div/div[1]/a/span[2]', '//*[@id="mn08"]/div/div[1]/a/span[2]',
            '//*[@id="mn09"]/div/div[1]/a/span[2]', '//*[@id="mn10"]/div/div[1]/a/span[2]', '//*[@id="mn11"]/div/div[1]/a/span[2]',
            '//*[@id="mn12"]/div/div[1]/a/span[2]']


def crawling(num_list):
    url_ls = []
    title_ls = []
    script_ls = []
    price_ls = []
    reload_ls = []
    category_ls = []
    company_ls = []
    postdate_ls = []
    last_modified_ls = []
    base_url = 'https://www.datastore.or.kr/file/list'

    delay = 3
    # browser = webdriver.Chrome('C:/Users/김영준/Desktop/chromedriver_win32/chromedriver.exe')
    browser = webdriver.Chrome('C:/Users/seunghwan/Downloads/chromedriver_win32/chromedriver.exe')
    browser.implicitly_wait(delay)
    browser.get(base_url)
    # browser.maximize_window()
    time.sleep(4)


    #base_url 에서 긁어와야할 카테고리 xpath
    browser.find_element_by_xpath(xpath_ls[num_list]).click()
    time.sleep(2)

    # 중도 터지는걸 방지하고자 끊어 받기위한 코드
    # for i in range(0,12):
    #     browser.find_element_by_xpath('//*[@id="paging"]/li[9]/a').send_keys(Keys.ENTER)
    #     time.sleep(2)

    number_of_list = browser.find_element_by_xpath('//*[@id="totalArea"]').text
    for i in range(0, len(number_of_list)):
        if number_of_list[i] == '/':
            number_of_list = number_of_list[i+2:len(number_of_list)-2]
            break

    # 끊어서 받기 때문에 중도 break 걸기위한 변수
    t = -1
    for k in range(0, 20):
        for j in range(4, 9):
            if t >= int(number_of_list)-1:
                break
            print("j = ", j)
            for i in range(1,11):
                t += 1
                print("t = ", t)
                if t == int(number_of_list):
                    break

                # 목롯 갯수에 따른 url xpath
                try:
                    browser.find_element_by_xpath('//*[@id="data-list"]/li[' + str(i) + ']/div/div[2]/div[1]/span[2]/a').send_keys(Keys.ENTER)
                except:
                    browser.find_element_by_xpath('//*[@id="data-list"]/li[' + str(i) + ']/div/div[2]/div[1]/span[2]/a').click()
                time.sleep(4)

                try:
                    title = browser.find_element_by_xpath('//*[@id="detail-title"]').text
                    title_ls.append(title)
                except:
                    title_ls.append("not data")

                try:
                    script = browser.find_element_by_xpath('//*[@id="detail-content"]/p[1]').text
                    script_ls.append(script)
                except:
                    script_ls.append("not data")

                try:
                    postdate = browser.find_element_by_xpath('//*[@id="detail-date"]').text
                    postdate_ls.append(postdate)
                except:
                    postdate_ls.append("not data")

                try:
                    last_modified = browser.find_element_by_xpath('//*[@id="update-modify-date"]').text
                    last_modified_ls.append(last_modified)
                except:
                    last_modified_ls.append("not data")

                try:
                    price = browser.find_element_by_xpath('//*[@id="detail-free"]').text
                    price_ls.append(price)
                except:
                    price_ls.append("not data")

                try:
                    reload = browser.find_element_by_xpath('//*[@id="detail-update-frequence"]').text
                    reload_ls.append(reload)
                except:
                    reload_ls.append("not data")

                try:
                    company = browser.find_element_by_xpath('//*[@id="provider-box"]/div[2]/span').text
                    company_ls.append(company)
                except:
                    company_ls.append("not data")

                url = browser.current_url
                try:
                    url_ls.append(url)
                except:
                    url_ls.append("not data")

                time.sleep(1)

                # 목록으로 가기 버튼 xpath
                browser.find_element_by_xpath('/html/body/div[1]/main/div[1]/div[2]/div/div/div[9]/div/div/a').send_keys(Keys.ENTER)
                time.sleep(1)

            if j == 8:
                break

            # 다음 페이지 xpath (ex: " > " 버튼)
            try:
                browser.find_element_by_xpath('//*[@id="paging"]/li[' + str(j+1) + ']/a').send_keys(Keys.ENTER)
            except:
                browser.find_element_by_xpath('//*[@id="paging"]/li[' + str(j+1) + ']/a').click()
            time.sleep(3)

        if t >= int(number_of_list)-1:
            break
        browser.find_element_by_xpath('//*[@id="paging"]/li[9]/a').send_keys(Keys.ENTER)

    dataset = pd.DataFrame({'제목' : [],
                            '내용' : [],
                            '등록일' : [],
                            '최종 수정일' : [],
                            '가격' : [],
                            '카테고리' : [],
                            '업데이트 주기' : [],
                            '제공기관' : [],
                            'url': []})


    for i in range(len(title_ls)):
        insert_data = pd.DataFrame({
                                    '제목' : [title_ls[i]],
                                    '내용' : [script_ls[i]],
                                    '등록일' : [postdate_ls[i]],
                                    '최종 수정일' : [last_modified_ls[i]],
                                    '가격' : [price_ls[i]],
                                    '카테고리' : [category_ls[num_list]],
                                    '업데이트 주기' : [reload_ls[i]],
                                    '제공기관' : [company_ls[i]],
                                    'url' : [url_ls[i]]})

        dataset = dataset.append(insert_data)

    df = pd.DataFrame.from_records(dataset)
    df.to_excel(category_ls[num_list] + '.xlsx')
    df.to_csv(category_ls[num_list] + '.csv', encoding='utf-8')


if __name__ == '__main__':
    for i in range(6, 8):
        my_thread = threading.Thread(target=crawling, args=(i,))
        my_thread.start()
        time.sleep(10)