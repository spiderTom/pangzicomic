#coding:utf-8
import requests
import re
import os
from bs4 import BeautifulSoup
import string
from lxml import etree


isProxyNeeded = True


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
    r = requests.get(imgUrl, proxies=setting.proxy, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()
    return filename


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

testsample = 'http://m.xemh520.com/selie/30628.html'


#1. get result for key word search
print "1, open home page to get all url for comics"
setting = NetWorkSetting()
session = requests.Session()
target_url = setting.searchUrl

#tempname = u'测试'
#tempname = tempname.encode('gbk')
#downloadImageFile(target_url, tempname, '1')


picturename = 1
page = 12
while page <= 68:
    if page == 1:
        target_url = setting.searchUrl
    else:
        target_url = setting.searchUrl + "index_" + str(page) + ".html"
    print target_url

    if isProxyNeeded:
        result = session.get(target_url, headers=setting.myHeaders, proxies=setting.proxy)
    else:
        result = session.get(target_url, headers=setting.myHeaders)

    soup = BeautifulSoup(result.content)
    picturename = 1
    for link in soup.find_all('a'):
        if link.has_attr("title") and link.has_attr("href") and link.get("href").find("selie") != -1:
            pageurl = setting.prefixUrl + link.get("href")
            if isProxyNeeded:
                pageresult = session.get(pageurl, headers=setting.myHeaders, proxies=setting.proxy)
            else:
                pageresult = session.get(pageurl, headers=setting.myHeaders)
            pagesoup = BeautifulSoup(pageresult.content)
            for picture in pagesoup.find_all('img'):
                if picture.has_attr("alt"):
                    print "@@@@@@@@@@@"
                    print picture.get("src")
                    pictureul = picture.get("src")
                    downloadImageFile(pictureul, picturename, page)
                    picturename += 1
                    print "@@@@@@@@@@@"

    page += 1

