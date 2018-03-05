# coding=utf-8
import urllib
import re
import codecs
import csv
import random
from urllib import request
from urllib import parse
from urllib.request import Request, urlopen
import requests
from html.parser import HTMLParser
from html.entities import name2codepoint
from bs4 import BeautifulSoup
from collections import defaultdict
import time


class Myparser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.infors = []
        self.next = ""

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "data-url":
                        self.infors.append(value)
        if tag == "link":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "rel" and value == "next":
                        for (variable, value) in attrs:
                            if variable == "href":
                                self.next = value


class Myparser_infor(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

        self.address = False
        self.cityState = False
        self.neighborhood = False
        self.price = False
        self.li_flag = False
        self.overiew = False
        self.descrip = False
        self.price_zip = False
        self.price_zip_count = 0

        self.value = defaultdict(lambda: "")
        self.data = []

    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname, attrvalue):
            for each in attrlist:
                if attrname == each[0] and attrvalue == each[1]:
                    return True
            return False
        if tag == 'div' and _attr(attrs, 'data-role', 'address'):
            self.address = True
        if tag == 'span' and _attr(attrs, 'data-role', 'cityState'):
            self.cityState = True
        if tag == 'span' and _attr(attrs, 'data-role', 'price'):
            self.price = True
        if tag == 'a' and _attr(attrs, 'class', 'linkLowlight linkUnderline'):
            self.neighborhood = True
        if tag == 'ul' and len(attrs) == 0:
            self.overiew = True
        if tag == 'li':
            self.li_flag = True
        if tag == 'p' and _attr(attrs, 'id', 'propertyDescription'):
            self.descrip = True
        if tag == 'div' and _attr(attrs, 'class', 'miniCol24 xsCol8 smlCol4 mdCol4 lrgCol4 pvmXxsVisible'):
            self.price_zip = True
            # if len(attrs) == 0:
            #     pass
            # else:
            #     for (variable, value) in attrs:
            #         if variable == "data-role" and value == "address":
            #             print("here")
            #             self.address = True

    def handle_endtag(self, tag):
        if tag == 'div':
            self.address = False
            self.price_zip = False
        if tag == 'span':
            self.cityState = False
            self.price = False
        if tag == 'a':
            self.neighborhood = False
        if tag == 'ul':
            self.overiew = False
        if tag == 'li':
            self.li_flag = False
        if tag == 'p':
            self.descrip = False

    def handle_data(self, data):
        if self.address:
            self.value['address'] = data.strip()

        elif self.cityState:
            self.value['cityState'] = data.strip()[:-5]
            self.value['zipcode'] = data.strip()[-5:]
        elif self.price:
            self.value['price'] = data.strip()
        elif self.neighborhood:
            self.value['neighborhood'] = data.strip()
        elif self.overiew and self.li_flag:
            data_ = data.strip()
            if 'Beds' in data_:
                self.value['beds'] = data_
            elif'Baths' in data_:
                self.value['baths'] = data_
            elif'Built' in data_:
                self.value['built'] = data_
            elif'house' in data_ or 'Family' in data_:
                self.value['type'] = data_
            elif'sqft lot size' in data_:
                self.value['lot_space'] = data_
            elif'/sqft' in data_:
                self.value['price_sqft'] = data_
            elif'sqft' in data_:
                self.value['space'] = data_
        elif self.descrip:
            self.value['description'] = data.strip()
        elif self.price_zip and self.price_zip_count == 0:
            self.value['Average_Listing_Price_for_zip'] = data.strip()
            self.price_zip_count += 1
        elif self.price_zip and self.price_zip_count == 1:
            self.value['Median_Sale_Price_for_zip'] = data.strip()
            self.price_zip_count += 1
        elif self.price_zip and self.price_zip_count == 2:
            self.value['Average_price_sqft_for_zip'] = data.strip()
            self.price_zip_count += 1

    # def handle_starttag(self, tag, attrs):
    #     if tag == 'div' and _attr(attrs, 'data-title'):
    #         movie = {}
    #         movie['actors'] = _attr(attrs, 'data-actors')
    #         movie['director'] = _attr(attrs, 'data-director')
    #         movie['duration'] = _attr(attrs, 'data-dutation')
    #         movie['title'] = _attr(attrs, 'data-title')
    #         movie['rate'] = _attr(attrs, 'data-rate')
    #         self.infors.append(movie)


def Get_suburl(url):
    headers = {}
    proxy_list = [  # 这是我当时用的代理IP，请更新能用的IP
        '12.221.240.25:8080',
        '35.196.26.166:3128',
        '216.177.233.181:8080',
        '47.206.51.67:8080',
        '58.30.233.200:8080',
        '115.182.92.87:8080',
        '210.75.240.62:3128',
        '211.71.20.246:3128',
        '115.182.83.38:8080',
        '121.69.8.234:8080',
    ]
    proxy = random.choice(proxy_list)
    # proxy = proxy_list[8]
    urlhandle = urllib.request.ProxyHandler({'http': proxy})
    opener = urllib.request.build_opener(urlhandle)
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    urllib.request.install_opener(opener)
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    # req = requests.get(url)
    # s = req.text
    # print(content)
    myparser = Myparser()
    myparser.feed(content)
    myparser.close()
    # print(myparser.infors)
    return myparser.infors, myparser.next


def Get_infor(url):

    headers = {}
    proxy_list = [  # 这是我当时用的代理IP，请更新能用的IP
        '12.221.240.25:8080',
        '35.196.26.166:3128',
        '216.177.233.181:8080',
        '47.206.51.67:8080',
        '58.30.233.200:8080',
        '115.182.92.87:8080',
        '210.75.240.62:3128',
        '211.71.20.246:3128',
        '115.182.83.38:8080',
        '121.69.8.234:8080',
    ]
    proxy = random.choice(proxy_list)
    # proxy = proxy_list[8]
    urlhandle = urllib.request.ProxyHandler({'http': proxy})
    opener = urllib.request.build_opener(urlhandle)
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    urllib.request.install_opener(opener)
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    # req = requests.get(url)
    # s = req.text
    # print(content)
    myparser = Myparser_infor()
    myparser.feed(content)
    myparser.close()

    # print(myparser.infors)
    return myparser.value


if __name__ == '__main__':
    # main()
    # url0 = 'https://www.trulia.com/CA/Los_Angeles'
    # urls, url_next = Get_suburl(url0)
    rows = []
    headers = ['zipcode', 'address', 'cityState', 'neighborhood', 'price', 'type','beds', 'baths','built','space','lot_space','price_sqft', 'Average_Listing_Price_for_zip','Median_Sale_Price_for_zip','Average_price_sqft_for_zip','description']
    with open('Infors.csv', 'w', newline='') as csvfile1:
        spamwriter1 = csv.writer(
            csvfile1, delimiter=" ", quoting=csv.QUOTE_MINIMAL)
        spamwriter1.writerow("################################")
        csvfile1.close()
    spamReader = csv.reader(open('urls.csv', newline=''),
                            delimiter=' ', quotechar='|')
    count = 0
    for row in spamReader:
        print("rows :", count)
        url = ''.join(row)
        print(url)
        url = "https://www.trulia.com" + url
        Infors = Get_infor(url)
        count += 1
        time.sleep(3)
        r = ""
        for x in Infors:
            r += Infors[x] + ','
        # print(r)
        # rows.append(r)
        with open('Infors.csv', 'a') as csvfile1:
            spamwriter1 = csv.DictWriter(csvfile1, headers)
            spamwriter1.writeheader()
            spamwriter1.writerow(Infors)
            csvfile1.close()
        # if count > 5:
        #     break

    # count = 0
    # for i in range(count + 5):
    #     if i < len(urls):
    #         url = "https://www.trulia.com" + urls[i]
    #         Infors = Get_infor(url)
    #         row = ""
    #         for x in Infors:
    #             if x == 'overiew':
    #                 if 'Beds' in Infors[x] and 'Baths' in Infors[x]:
    #                     row += Infors[x] + ','
    #                 elif'Beds' in Infors[x]:
    #                     p = Infors[x].find('Built')
    #                     row += Infors[x][:p-1] +',' + Infors[x][p-1:]
    #                 elif'Baths' in Infors[x]:
    #                     p = Infors[x].find('Baths')
    #                     row += Infors[x][:p-3] +',' + Infors[x][p-3:]
    #                 else:
    #                     p = Infors[x].find('Built')
    #                     row += Infors[x][:p-1] +',,' + Infors[x][p-1:]
    #             else:
    #                 row += Infors[x] + ','
    #         print(row)
    #         rows.append(row)
    #         with open('Infors.csv', 'a', newline='') as csvfile1:
    #             spamwriter1 = csv.writer(csvfile1, delimiter=" ", quoting=csv.QUOTE_MINIMAL)
    #             spamwriter1.writerows(rows)
    #             csvfile1.close()
    # count += 5
    # for x in Infors:

        # for url in urls:
        #     # print(url)
        #     url = url0 + url
        # print(url)

        # for each in infors:
        #     print('%(title)s|%(rate)s|%(actors)s|%(director)s|%(duration)s' % each)
