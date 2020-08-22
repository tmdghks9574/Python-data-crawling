import requests # 웹 페이지 소스를 얻기 위한 패키지(기본 내장 패키지이다.)
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from datetime import datetime
import pandas as pd # 데이터를 처리하기 위한 가장 기본적인 패키지
import time # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import threading
#
#


def crawling():
    url_ls = []
    title_ls = []
    script_ls = []
    price_ls = []
    reload_ls = []
    company_ls = []
    postdate_ls = []
    last_modified_ls = []
    category_ls = []

    base_url = 'https://www.findatamall.or.kr/fsec/dataProd/generalDataProd.do?cmnx=44&sCharge=charge&sFree=free&sNego=nego'

    delay = 3

    # browser = webdriver.Chrome('C:/Users/김영준/Desktop/chromedriver_win32/chromedriver.exe')
    browser = webdriver.Chrome('C:/Users/seunghwan/Downloads/chromedriver_win32/chromedriver.exe')
    browser.implicitly_wait(delay)
    browser.get(base_url)
    time.sleep(2)

    browser.find_element_by_xpath('//*[@id="menu-container"]/ul[2]/li[2]/a').click()
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="mid"]').click()
    browser.find_element_by_xpath('//*[@id="mid"]').send_keys('tmdghks9574@gmail.com')
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="mpwd"]').click()
    browser.find_element_by_xpath('//*[@id="mpwd"]').send_keys('Woals1201!')
    browser.find_element_by_xpath('//*[@id="submitBtn"]').send_keys(Keys.ENTER)
    time.sleep(2)

    browser.get(base_url)
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="fn_searchFrm"]/div[2]/label').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="search"]').click()
    time.sleep(1)


    # browser.maximize_window()

    #base_url 에서 긁어와야할 카테고리 xpath

    for i in range(0,30):
        try:
            browser.find_element_by_xpath('//*[@id="paging"]/ul/li[13]/a').send_keys(Keys.ENTER)
        except:
            browser.find_element_by_xpath('//*[@id="paging"]/ul/li[13]/a').click()
        time.sleep(3)

    t = -1
    for j in range(0, 44):
        if t >= 84:
            break
        print("j = ", j)
        for i in range(1,11):
            t += 1
            print("t = ", t)
            if t == 85:
                break

            # 목롯 갯수에 따른 url xpath
            try:
                browser.find_element_by_xpath('//*[@id="contents"]/div/div/div[3]/ul/li[' + str(i) + ']/a/div[2]').send_keys(Keys.ENTER)
            except:
                browser.find_element_by_xpath('//*[@id="contents"]/div/div/div[3]/ul/li[' + str(i) + ']/a/div[2]').click()
            time.sleep(3)

            try:
                title = browser.find_element_by_xpath('//*[@id="contents"]/div/div[1]/div[1]/div[2]/strong').text
                title_ls.append(title)
            except:
                title_ls.append("not data")

            try:
                script = browser.find_element_by_xpath('//*[@id="contents"]/div/div[1]/div[4]/dl/dd').text
                script_ls.append(script)
            except:
                script_ls.append("not data")

            try:
                postdate = browser.find_element_by_xpath('//*[@id="move1"]/dl/dd/table/tbody/tr[1]/td[1]/span').text
                postdate_ls.append(postdate)
            except:
                postdate_ls.append("not data")

            try:
                last_modified = browser.find_element_by_xpath('//*[@id="move1"]/dl/dd/table/tbody/tr[2]/td[1]/span').text
                last_modified_ls.append(last_modified)
            except:
                last_modified_ls.append("not data")

            try:
                price = browser.find_element_by_xpath('//*[@id="move1"]/dl/dd/table/tbody/tr[3]/td[2]/span').text
                price_ls.append(price)
            except:
                price_ls.append("not data")

            # try:
            #     reload = browser.find_element_by_xpath('//*[@id="contents"]/div/div[1]/div[5]/dl/dd').text
            #     reload_ls.append(reload)
            # except:
            #     reload_ls.append("not data")

            try:
                company = browser.find_element_by_xpath('//*[@id="contents"]/div/div[1]/div[1]/div[2]/div/dl[2]/dd').text
                company_ls.append(company)
            except:
                company_ls.append("not data")

            url = browser.current_url
            try:
                url_ls.append(url)
            except:
                url_ls.append("not data")

            try:
                category = browser.find_element_by_xpath('//*[@id="contents"]/div/div[1]/div[1]/div[2]/div/dl[1]/dd').text
                category_ls.append(category)
            except:
                category_ls.append("not data")

            time.sleep(1)

            # 목록으로 가기 버튼 xpath
            browser.back()
            time.sleep(1.5)


        # 다음 페이지 xpath (ex: " > " 버튼)
        try:
            browser.find_element_by_xpath('//*[@id="paging"]/ul/li[13]/a').send_keys(Keys.ENTER)
        except:
            browser.find_element_by_xpath('//*[@id="paging"]/ul/li[13]/a').click()
        time.sleep(3)




    dataset = pd.DataFrame({'제목' : [],
                            '내용' : [],
                            '등록일' : [],
                            '최종 수정일' : [],
                            '가격' : [],
                            '카테고리' : [],
                            # '업데이트 주기' : [],
                            '제공기관' : [],
                            'url': []})


    for i in range(len(title_ls)):
        insert_data = pd.DataFrame({
                                    '제목' : [title_ls[i]],
                                    '내용' : [script_ls[i]],
                                    '등록일' : [postdate_ls[i]],
                                    '최종 수정일' : [last_modified_ls[i]],
                                    '가격' : [price_ls[i]],
                                    '카테고리' : [category_ls[i]],
                                    # '업데이트 주기' : [reload_ls[i]],
                                    '제공기관' : [company_ls[i]],
                                    'url' : [url_ls[i]]})

        dataset = dataset.append(insert_data)

    df = pd.DataFrame.from_records(dataset)
    return df
    # df.to_excel(category_ls[num_list] + '.xlsx')
    # df.to_csv(category_ls[num_list] + '.csv', encoding='utf-8')


if __name__ == '__main__':

    df = crawling()
    df.to_excel('finance.xlsx')
