import requests # 웹 페이지 소스를 얻기 위한 패키지(기본 내장 패키지이다.)
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from datetime import datetime
import pandas as pd # 데이터를 처리하기 위한 가장 기본적인 패키지
import time # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


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

    base_url = 'https://console.cloud.google.com/marketplace/browse?filter=solution-type:dataset&hl=ko'

    delay = 3

    # browser = webdriver.Chrome('C:/Users/김영준/Desktop/chromedriver_win32/chromedriver.exe')
    browser = webdriver.Chrome('C:/Users/seunghwan/Downloads/chromedriver_win32/chromedriver.exe')
    browser.implicitly_wait(delay)
    browser.get(base_url)

    # browser.maximize_window()
    time.sleep(4)

    for i in range(0,4):
        try:
            browser.find_element_by_xpath(
                '/html/body/pan-shell/pcc-shell/cfc-panel-container/div/div/cfc-panel[1]/div[1]/div/div[3]/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-container/div/div/cfc-panel[1]/div/div/cfc-panel-container/div/div/cfc-panel[2]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/ng1-router-root-loader/xap-deferred-loader-outlet/ng1-router-root-wrapper/ng1-router-root/div/ng-view/mp-solution-browse/div/div[2]/div[2]/div/section/div/mp-shelf/div/div/div/mp-pagination/div/button[2]/md-icon').send_keys(
                Keys.ENTER)
        except:
            browser.find_element_by_xpath(
                '/html/body/pan-shell/pcc-shell/cfc-panel-container/div/div/cfc-panel[1]/div[1]/div/div[3]/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-container/div/div/cfc-panel[1]/div/div/cfc-panel-container/div/div/cfc-panel[2]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/ng1-router-root-loader/xap-deferred-loader-outlet/ng1-router-root-wrapper/ng1-router-root/div/ng-view/mp-solution-browse/div/div[2]/div[2]/div/section/div/mp-shelf/div/div/div/mp-pagination/div/button[2]/md-icon').click()
        time.sleep(3)

    #base_url 에서 긁어와야할 카테고리 xpath
    # browser.find_element_by_xpath('//*[@id="categoryGroups"]/li[5]/button').click()
    # time.sleep(1.5)

    # 중도 터지는걸 방지하고자 끊어 받기위한 코드
    # for i in range(0, 27):
    #     browser.find_element_by_xpath('//*[@id="datasetVO"]/div[2]/div/section/div[2]/div/div/button[13]').send_keys(Keys.ENTER)
    #     time.sleep(2)
    tmp_ls = []


    t = -1
    for k in range(0, 1):
        for j in range(0, 1):
            if t >= 32:
                break
            print("j = ", j)
            for i in range(1,34):
                login_url = browser.find_element_by_xpath('/html/body/pan-shell/pcc-shell/cfc-panel-container/div/div/cfc-panel[1]/div[1]/div/div[3]/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-container/div/div/cfc-panel[1]/div/div/cfc-panel-container/div/div/cfc-panel[2]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/ng1-router-root-loader/xap-deferred-loader-outlet/ng1-router-root-wrapper/ng1-router-root/div/ng-view/mp-solution-browse/div/div[2]/div[2]/div/section/div/mp-shelf/div/div/pan-shelf/div/div[2]/div[' + str(i) + ']/pan-result-card/a')
                tmp = login_url.get_attribute('href')
                #목롯 갯수에 따른 url xpath
                tmp_ls.append(tmp)
                company = browser.find_element_by_xpath('/html/body/pan-shell/pcc-shell/cfc-panel-container/div/div/cfc-panel[1]/div[1]/div/div[3]/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-container/div/div/cfc-panel[1]/div/div/cfc-panel-container/div/div/cfc-panel[2]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/ng1-router-root-loader/xap-deferred-loader-outlet/ng1-router-root-wrapper/ng1-router-root/div/ng-view/mp-solution-browse/div/div[2]/div[2]/div/section/div/mp-shelf/div/div/pan-shelf/div/div[2]/div[' + str(i) + ']/pan-result-card/a/div/h4').text
                company_ls.append(company)
                print(company)

            for i in range(len(tmp_ls)):
                t += 1
                print("t = ", t)
                if t == 33:
                    break
                browser.get(tmp_ls[i])
                time.sleep(3)

                try:
                    title = browser.find_element_by_xpath('//*[@id="main"]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/mp-details-page/mp-details-component/cfc-single-panel-layout/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-body/cfc-virtual-viewport/div[1]/div/mp-product-details-banner/section/div/cfc-product-header/div/div/h1').text
                    title_ls.append(title)
                except:
                    title_ls.append("not data")

                try:
                    script = browser.find_element_by_xpath('//*[@id="main"]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/mp-details-page/mp-details-component/cfc-single-panel-layout/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-body/cfc-virtual-viewport/div[1]/div/mp-product-details-banner/section/div/cfc-product-header/div/div/p[2]').text
                    script_ls.append(script)
                except:
                    script_ls.append("not data")

                # try:
                #     postdate = browser.find_element_by_xpath('//*[@id="frm"]/div[3]/div[2]/table/tbody/tr[1]/td[1]/span').text
                #     postdate_ls.append(postdate)
                # except:
                #     postdate_ls.append("not data")

                try:
                    last_modified = browser.find_element_by_xpath('//*[@id="main"]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/mp-details-page/mp-details-component/cfc-single-panel-layout/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-body/cfc-virtual-viewport/div[1]/div/div/mp-product-details-overview/div/div[2]/mp-product-details-metadata/ul/li[2]/mp-product-details-metadata-entry/span[2]').text
                    last_modified_ls.append(last_modified)
                except:
                    last_modified_ls.append("not data")

                try:
                    category = browser.find_element_by_xpath('//*[@id="main"]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/mp-details-page/mp-details-component/cfc-single-panel-layout/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-body/cfc-virtual-viewport/div[1]/div/div/mp-product-details-overview/div/div[2]/mp-product-details-metadata/ul/li[3]/mp-product-details-metadata-entry').text
                    category = category[5:len(category)]
                    category_ls.append(category)
                    print(category)
                except:
                    category_ls.append("not data")
                # try:
                #     price = browser.find_element_by_xpath('//*[@id="detail-free"]').text
                #     price_ls.append(price)
                # except:
                #     price_ls.append("not data")

                # try:
                #     reload = browser.find_element_by_xpath('//*[@id="detail-update-frequence"]').text
                #     reload_ls.append(reload)
                # except:
                #     reload_ls.append("not data")
                # try:
                #     company = browser.find_element_by_xpath('/html/body/pan-shell/pcc-shell/cfc-panel-container/div/div/cfc-panel[1]/div[1]/div/div[3]/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-container/div/div/cfc-panel[1]/div/div/cfc-panel-container/div/div/cfc-panel[2]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/mp-details-page/mp-details-component/cfc-single-panel-layout/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-body/cfc-virtual-viewport/div[1]/div/mp-product-details-banner/section/div/cfc-product-header/div/div/p[1]').text
                #     company_ls.append(company)
                #     print(company)
                # except:
                #     company_ls.append("not data")

                url = browser.current_url
                try:
                    url_ls.append(url)
                except:
                    url_ls.append("not data")

                time.sleep(2)

                # browser.back()
                # time.sleep(5)

            # if j == 12:
            #     break
            # 다음 페이지 xpath (ex: " > " 버튼)
            # try:
            #     browser.find_element_by_xpath('/html/body/pan-shell/pcc-shell/cfc-panel-container/div/div/cfc-panel[1]/div[1]/div/div[3]/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-container/div/div/cfc-panel[1]/div/div/cfc-panel-container/div/div/cfc-panel[2]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/ng1-router-root-loader/xap-deferred-loader-outlet/ng1-router-root-wrapper/ng1-router-root/div/ng-view/mp-solution-browse/div/div[2]/div[2]/div/section/div/mp-shelf/div/div/div/mp-pagination/div/button[2]/md-icon').send_keys(Keys.ENTER)
            # except:
            #     browser.find_element_by_xpath('/html/body/pan-shell/pcc-shell/cfc-panel-container/div/div/cfc-panel[1]/div[1]/div/div[3]/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-container/div/div/cfc-panel[1]/div/div/cfc-panel-container/div/div/cfc-panel[2]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/ng2-router-root/div/ng1-router-root-loader/xap-deferred-loader-outlet/ng1-router-root-wrapper/ng1-router-root/div/ng-view/mp-solution-browse/div/div[2]/div[2]/div/section/div/mp-shelf/div/div/div/mp-pagination/div/button[2]/md-icon').click()
            # time.sleep(2)


        if t >= 32:
            break
        # browser.find_element_by_xpath('//*[@id="datasetVO"]/div[2]/div/section/div[2]/div/div/button[13]').send_keys(Keys.ENTER)

    dataset = pd.DataFrame({'제목' : [],
                            '내용' : [],
                            # '등록일' : [],
                            '최종 수정일' : [],
                            # '가격' : [],
                            '카테고리' : [],
                            # '업데이트 주기' : [],
                            '제공기관' : [],
                            'url': []})


    for i in range(len(url_ls)):
        insert_data = pd.DataFrame({
                                    '제목' : [title_ls[i]],
                                    '내용' : [script_ls[i]],
                                    # '등록일' : [postdate_ls[i]],
                                    '최종 수정일' : [last_modified_ls[i]],
                                    # # '가격' : [price_ls[i]],
                                    '카테고리' : [category_ls[i]],
                                    # # '업데이트 주기' : [reload_ls[i]],
                                    '제공기관' : [company_ls[i]],
                                    'url' : [url_ls[i]]})

        dataset = dataset.append(insert_data)

    df = pd.DataFrame.from_records(dataset)
    return df
    # df.to_excel(category_ls[num_list] + '.xlsx')
    # df.to_csv(category_ls[num_list] + '.csv', encoding='utf-8')


if __name__ == '__main__':

    df = crawling()
    df.to_excel('google.xlsx')
    exit()
