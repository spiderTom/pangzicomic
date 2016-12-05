#coding:utf-8
import requests
import re
import os
from bs4 import BeautifulSoup
import string
from lxml import etree


isProxyNeeded = False

def getsource(url):
    if isProxyNeeded:
        result = session.get(url, headers=setting.myHeaders, proxies=setting.proxy)
    else:
        result = session.get(url, headers=setting.myHeaders)
    return result


def downloadImageFile(imgUrl, filename, path):
    extendname = imgUrl.split('.')[-1]
    filename = str(filename)
    filename += '.' + extendname
    path = str(path)
    path = "D:/test/" + path + "/"
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
    filename = path + filename
    print "Download Image File=", filename
    #r = getsource(imgUrl)
    r = requests.get(imgUrl, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()
    return filename


def handletopic(topic, topicid, page):
    isNeedDownload = False
    picturesurl = []
    picturesurl.append(topicid)

    index = topicid.find(".")
    topicid = topicid[:index]
    page = str(page)
    folderid = topicid
    index = folderid.rfind("/")
    folderid = folderid[index:]
    page = page + "/" + folderid
    topicid = topicid + "_"

    topicresult = getsource(topic)
    #get topic sourc, try to check if it has more than one picture
    #if yes, download them, otherwise ignore it
    firstsoup = BeautifulSoup(topicresult.content)

    for url in firstsoup.find_all('a'):
        if url.has_attr("href") and url.get("href").find(topicid) != -1 and url.get("href") not in picturesurl:
            picturesurl.append(url.get("href"))
            isNeedDownload = True

    if not isNeedDownload:
        return

    for pictures in picturesurl:
        index = pictures.find(".")
        picturename = pictures[:index]
        index = picturename.rfind("/")
        picturename = picturename[index:]
        pictureurl = setting.prefixUrl + pictures
        pictureresult = getsource(pictureurl)
        picturesoup = BeautifulSoup(pictureresult.content)
        for picture in picturesoup.find_all('img'):
            if picture.has_attr("alt"):
                print "@@@@@@@@@@@"
                print picture.get("src")
                finaltarget = picture.get("src")
                downloadImageFile(finaltarget, picturename, page)
                print "@@@@@@@@@@@"

def handlepage(page):
    if page == 1:
        target_url = setting.searchUrl
    else:
        target_url = setting.searchUrl + "index_" + str(page) + ".html"
    print target_url
    #get page resource
    result = getsource(target_url)

    soup = BeautifulSoup(result.content)
    #get topics in current page
    for link in soup.find_all('a'):
        #for each topic, get the source
        if link.has_attr("title") and link.has_attr("href") and link.get("href").find("selie") != -1:
            topicid = link.get("href")
            topicurl = setting.prefixUrl + link.get("href")
            handletopic(topicurl, topicid, page)


class NetWorkSetting:
    def __init__(self):
        self.proxy = {
            "http": 'http://10.158.100.8:8080',
            "https": 'https://10.158.100.8:8080'}
        #self.searchUrl = 'http://m.xemh520.com/selie/'
        self.searchUrl = 'http://m.xemh520.com/selie/'
        self.prefixUrl = 'http://m.xemh520.com'
        self.myHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://m.xemh520.com/selie/'
}


#1. get result for key word search
print "1, open home page to get all url for comics"
setting = NetWorkSetting()
session = requests.Session()
target_url = setting.searchUrl


page = 21
while page <= 68:
    handlepage(page)
    page += 1

