from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import sys
from lxml import etree
import re
import requests
import time
import random

head = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
urls = []

def fofa(driver, page, count):
    driver.get("https://fofa.so/")
    input('请输入任意字符继续...')
    num = 0
    pageNum = 0
    while True:
        #=============处理数据=================
        m = processSource(driver.page_source)
        num+=m if m!=None else 0
        pageNum+=1
        #====================================
        if(count!=None):
            if(num>=count):
                exit()
        if(page!=None):
            if(pageNum>=page):
                exit()
        try:
            nextElement = driver.find_element(By.CLASS_NAME,'next_page')
            nextElement.click()
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME,'next_page')))
            time.sleep(int(random.random()*10)+3)
        except:
            exit()

def google(driver, key, save, engine):
    url = "http://google.com/search?source=hp&q=" + key + "&num=100&filter=0"
    xpath = '//*[@id="rso"]/div/div/div/a/@href'
    driver.get(url)
    flag = input("是否遇到人机检测？若是则在处理完成之后输入任意字符继续...")
    while True:
        if("pnnext" in str(driver.page_source)):
            setResult(driver.page_source, save, engine, xpath)
            html = etree.HTML(driver.page_source)
            nextElementText = html.xpath('//*[@id="pnnext"]')[0].xpath("./@href")[0]
            nextUrl = "http://google.com" + nextElementText
            pnnextElement = driver.find_element(By.ID,'pnnext')
            try:
                pnnextElement.click()
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'fsl')))
            except:
                flag = str(input("是否遇到人机检测？若是则在处理完成之后输入1，若退出输入其他:"))
                if(flag == '1'):
                    driver.get(nextUrl)
                    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'fsl')))
                    continue
                else:
                    saveToFile(urls)
                    exit()
        else:
            setResult(driver.page_source, save, engine, xpath)
            saveToFile(urls)
            exit()

def baidu(driver, key, save,engine):
    xpath = '/html/body/div/div/div/div/div/h3/a/@href'
    pn = 0
    url = "https://www.baidu.com/s?ie=utf-8&f=8&wd=" + key + "&rn=50&pn=" + str(pn)
    driver.get(url)
    num = 0
    while True:
        if(len(driver.find_elements(By.CLASS_NAME,'n'))>=2 or num == 0):
            setResult(driver.page_source, save, engine, xpath)
            try:
                pn+=50
                url = "https://www.baidu.com/s?ie=utf-8&f=8&wd=" + key + "&rn=50&pn=" + str(pn)
                driver.get(url)
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'help')))
                if (num == 0):
                    num += 1
            except:
                flag = str(input("是否遇到人机检测？若是则在处理完成之后输入1，若退出输入其他:"))
                if (flag == '1'):
                    url = "https://www.baidu.com/s?ie=utf-8&f=8&wd=" + key + "&rn=50&pn=" + str(pn)
                    driver.get(url)
                    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'help')))
                    continue
                else:
                    saveToFile(urls)
                    exit()
        else:
            setResult(driver.page_source, save, engine, xpath)
            saveToFile(urls)
            exit()

def bing(driver, key, save, engine):
    xpath = '//*[@id="b_results"]/li/h2/a/@href'
    if(engine=='bingCN'):
        url = 'https://cn.bing.com/search?q=' + key + '&amp;first=50&FORM=BESBTB&first='
    else:
        url = 'https://cn.bing.com/search?q=' + key + '&amp;first=50&ensearch=1&FORM=BESBTB&first='
    pn = 0
    driver.get(url + str(pn))
    while True:
        if(pn<501):
            setResult(driver.page_source, save, engine, xpath)
            try:
                pn+=10
                driver.get(url + str(pn))
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'sw_next')))
            except:
                flag = str(input("是否遇到人机检测？若是则在处理完成之后输入1，若退出输入其他:"))
                if (flag == '1'):
                    driver.get(url + str(pn))
                    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'sw_next')))
                    continue
                else:
                    saveToFile(urls)
                    exit()
        else:
            setResult(driver.page_source, save, engine, xpath)
            saveToFile(urls)
            exit()

def setResult(source, save, engine, xpath):
    html = etree.HTML(source)
    elementList = html.xpath(xpath)
    if (save == "site"):
        reStr = r'(http|https)://([a-z.]*)/'
        index = 0
    elif (save == "domain"):
        reStr = r'(http|https)://([a-z.]*)/'
        index = 2
    else:
        reStr = r'.*'
        index = 0
    for furl in elementList:
        try:
            href = furl
            if(engine == 'baidu'):
                res = requests.get(furl, headers=head, timeout=15)
                href = res.history[len(res.history) - 1].headers['location']
            url = re.match(reStr, href).group(index)
            if url not in urls:
                urls.append(url)
                print(url)
        except:
            continue

def processSource(source):
    xpath = '//*[@id="ajax_content"]/div/div[1]/div[1]/a/@href'
    html = etree.HTML(source)
    elementList = html.xpath(xpath)
    c = len(elementList)
    f = open('fofa.txt', 'a+', encoding='utf-8')
    for href in elementList:
        if(href!='#'):
            f.write(href+'/\n')
            print(href)
    f.close()
    return c

def setOpinions(os, engine, key, save, page, count):
    driverPath = ""
    if(os == "windows"):
        driverPath = "chromedriver.exe"
    elif(os == "linux"):
        driverPath = "chromedriverLinux"
    elif(os == "mac"):
        driverPath = "chromedriverMac"
    else:
        print("Please enter the correct os!")
        exit()
    driver = webdriver.Chrome(executable_path=driverPath)
    if(engine == "google"):
        google(driver, key, save, engine)
    elif(engine == "baidu"):
        baidu(driver, key, save, engine)
    elif(engine == "bing"):
        bing(driver, key, save, engine)
    elif(engine ==  "fofa"):
        fofa(driver, page, count)
    else:
        print('Please input right engine!')

def saveToFile(urls):
    f = open('result.txt', 'a+', encoding='utf-8')
    for url in urls:
        f.write(url+"\n")
    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = '多搜索引擎Url半自动化采集器'
    parser.add_argument('-os', help="Your os type [linux/windows/mac]", type=str, dest='os', default="windows")
    parser.add_argument('-e', help="Choose the search engine you want to use.[baidu/google/bingCN(国内版)/bingEN(国际版)/fofa(需自行登录和搜索)]", type=str, dest='engine', default="baidu")
    parser.add_argument('-key', help="input the key to search for", type=str, dest='key')
    parser.add_argument('-save', help="What type do you want to save.\ndoamin[www.baidu.com]\nsite[https://www.baidu.com/]\nurl[https://www.aidu.com/news.php?id=xxx]", type=str, dest='save', default="site")
    parser.add_argument('-page', help='setting max number pages.', type=int, dest='page', default=10)
    parser.add_argument('-count', help='Set the count of results', type=int, dest='count', default=100)
    args = parser.parse_args()
    print("-" * 80)
    print("\t多搜索引擎Url半自动化采集器")
    print("\t主要为了采集google，使用selenium方便过人机验证\n")
    print("注意：\t若使用google搜索引擎，在第一页的时候需要确认是否遇到人机检测\n\t若遇到则需要在确定人机检测完毕之后输入任意键继续...\n\tBing末页判断比较麻烦，所以只采集到500\n\t只为满足自己需求的小脚本，不喜勿喷")
    print('\n新增：\t新增fofa抓取，需等待浏览器打开之后进行常规的登录搜索操作')
    print('\t搜索结果出来之后，等待页面加载完毕在命令行输入任意键继续...\n')
    print("-" * 80)

    if args.key==None and args.engine!='fofa':
        print('useage : python ' +str(sys.argv[0]) + ' -h')
    else:
        setOpinions(args.os, args.engine, args.key, args.save, args.page, args.count)
