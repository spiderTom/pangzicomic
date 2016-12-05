#coding:utf-8
import requests
import re
import os
from bs4 import BeautifulSoup
import string
from lxml import etree



temp = str(12345.678)

index = temp.find('.')
print temp[:index]
print temp[:-1]


