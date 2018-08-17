
#-*-coding:utf-8-*-
import hashlib
import time
import scrapy
from pprint import pprint
import re
import json
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
import os, os.path
import sys
import datetime
from xml.dom import minidom,Node

from zhilian_spider.items import *

from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from zhilian_spider.xmlparser import get_xml_data
from time import sleep

try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
    from scrapy.utils.response import get_base_url
    from scrapy.utils.url import urljoin_rfc
    from scrapy.spiders import CrawlSpider, Rule
    from scrapy.linkextractors.sgml import SgmlLinkExtractor as sle



import  time
import logging
from zhilian_spider.settings import *


reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger("aa");  

#./hangye.dict ./city.dict ./salary.dict ./company_type.dict ./years.dict ./xueli.dict ./zhiweileixing.dict ./fabushijian.dict
class CRAWLERSPIDER(scrapy.spiders.Spider):

    name = "zhilian"
    #start_urls=["http://sou.zhaopin.com/jobs/searchresult.ashx?in=121000%3B129900%3B121100%3B121200%3B210600%3B120700%3B121300%3B121500%3B300000&jl=晋中&sf=2001&st=4000&ct=9&&el=5&pd=30"]
    #start_urls=["http://sou.zhaopin.com/jobs/searchresult.ashx"]
    start_urls=["http://sou.zhaopin.com/jobs/searchresult.ashx?in=210500%3B121000%3B129900%3B121100%3B121200%3B210600%3B120700%3B121300%3B121500%3B300000&jl=%E6%99%8B%E4%B8%AD&p=1&isadv=0"]
  
    #下一页链接的解析
    next_page_xpath=u'//li[@class="pagesDown-pos"]/a[text()="下一页"]/@href'
    #列表页的列表解析
    list_xpath=u'//div[@class="newlist_list_content"]/table'
    #详情链接的解析
    detail_xpath=u'tr/td[1]/div/a/@href'
    #详情字段解析
    detail_xpath_dict={
                       u'hangye':u'//span[contains(text(),"\u804c\u4f4d\u7c7b\u522b")]/../strong/a/text()',
                       u'city':u'//span[contains(text(),"\u5de5\u4f5c\u5730\u70b9")]/../strong/a/text()',
                       u'salary':u'//span[contains(text(),"\u804c\u4f4d\u6708\u85aa")]/../strong/text()',
                       u'time':u'//span[contains(text(),"\u53d1\u5e03\u65e5\u671f")]/../strong/span/text()',
                       u'experience':u'//span[contains(text(),"\u5de5\u4f5c\u7ecf\u9a8c")]/../strong/text()',
                       u'xueli':u'//span[contains(text(),"\u6700\u4f4e\u5b66\u5386")]/../strong/text()',
                       u'title':u'//div[@class="inner-left fl"]/h1/text()',
                       u'company_name':u'//div[@class="inner-left fl"]/h2/a/text()',
                       u'company_url':u'//div[@class="inner-left fl"]/h2/a/@href'
                       }
    #公司字段解析
    company_xpath_dict={
                       u'content': u'//div[@class="company-content"]/descendant::text()',
                       u'company_logo':u'//img[@class="companyLogo"]/@src',
                       u'company_size': u'//span[contains(text(),"\u516c\u53f8\u89c4\u6a21\uff1a")]/../following-sibling::td/descendant::text()'
                       }
    
    #allowed_domains = ["http://www.pingwest.com/category/news/"]
    #def __init__(self,filetag):
        #log初始化
    #    error_handler = logging.FileHandler("d:/error_."+str(filetag)+".txt");  
    #    error_handler.setLevel(logging.ERROR);  
    #    info_handler = logging.FileHandler("d:/info_."+str(filetag)+".txt");  
    #    info_handler.setLevel(logging.INFO);  

    #    logger.addHandler(error_handler);  
    #    logger.addHandler(info_handler); 
        #从文件中读取url
     #   file=open("zhilian_spider/conf/sub.list_"+str(filetag),"r")
        #for line in file.readlines():
         #   url=line.replace("%0A","")
      
         #   self.start_urls.append(url)

    def parse(self,response):
        
        print 'current:'+response.url
        logger.info("current link："+response.url)

        response_selector = HtmlXPathSelector(response)
        #print response.body;
        #获取下一页的链接，进行继续爬取
        next_links=response_selector.select(self.next_page_xpath).extract()
        for next_link in next_links:

                  #print "next_link is :"+next_link
                  base_url = get_base_url(response)
                  relative_url = next_link
                  next_link= urljoin_rfc(base_url,relative_url)

                  yield Request(url=next_link,callback=self.parse,headers=DEFAULT_REQUEST_HEADERS)
	

  

        ###详情页面进行调度 
	   ##获取页面上面才能获取的field
        job_page= response_selector.select(self.list_xpath)
        job_list=[]
        for line_sel in job_page:
            if(job_page.index(line_sel)==0):
                continue
            if(len(line_sel.select(self.detail_xpath).extract())>0):
                detail_link = line_sel.select(self.detail_xpath).extract()[0]
                yield Request(url=detail_link,callback=self.parse_detail,meta={"sub_url":response.url},headers=DETAIL_REQUEST_HEADERS)
           
                #解析详情
    def parse_detail(self,response):
        item=Item()
        item["url"]=response.url
        m2 = hashlib.md5()
        m2.update(item["url"])
        item["url_md5sum"]=m2.hexdigest()
        item["source"]="智联招聘"
        item["sub_url"]=response.meta["sub_url"] 
        response_selector = HtmlXPathSelector(response)
#组装item
        for file_name in self.detail_xpath_dict:
            item[file_name]= ""
            if(len(response_selector.select(self.detail_xpath_dict[file_name]).extract())>0):
                item[file_name]= response_selector.select(self.detail_xpath_dict[file_name]).extract()[0]
        
        #公司url的MD5
        
        m2 = hashlib.md5()
        m2.update(item["company_url"])
        item["company_url_md5sum"]=m2.hexdigest()
        #时间处理
        pub_at=item['time']
        today = datetime.date.today()
        if pub_at=='15天前':
            item['time']=(today-datetime.timedelta(days=15)).strftime('%Y-%m-%d')
            print 'a'
        elif pub_at=="前天":
            item['time']=(today-datetime.timedelta(days=2)).strftime('%Y-%m-%d')
            print 'b'
        elif pub_at.find('刚')!=-1 or pub_at.find("小时")!=-1:
            print 'c'
            item['time']=today.strftime('%Y-%m-%d')
        elif pub_at=='昨天':
            item['time']=(today-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            print 'd'

            
            #组装完成，返回发送到pipline
            
        yield item



        company_url = item['company_url']
        #如果没有公司链接
        if len(company_url) == 0:

            return
        if company_url.split("/")[2]=="special.zhaopin.com":
            yield Request(url=company_url,callback=self.parse_company,meta={"sub_url":response.url,"company_name":item["company_name"]},headers=SPECIAL_REQUEST_HEADERS,dont_filter=False)
        elif company_url.split("/")[2]=="company.zhaopin.com":
            yield Request(url=company_url,callback=self.parse_company,meta={"sub_url":response.url,"company_name":item["company_name"]},headers=COMPANY_REQUEST_HEADERS,dont_filter=False)



                #解析公司信息          
    def parse_company(self, response):
        item =Company_Item()
        sub_url=response.meta["sub_url"]	
        company_name=response.meta['company_name']


    
        response_selector = HtmlXPathSelector(response)

        item["company_url"]=response.url
        item["sub_url"]=sub_url
        item["company_name"]=company_name
        item["source"]="智联招聘"

    
        ##填充item的值
        for node_name in self.company_xpath_dict:
            item[node_name]=""
            if len(response_selector.select(self.company_xpath_dict[node_name]).extract())>0:
                   item[node_name]=("".join(response_selector.select(self.company_xpath_dict[node_name]).extract())).replace("\n","").strip()

            
        #公司链接的MD5
        m2 = hashlib.md5()
        m2.update(item["company_url"])
        item["company_url_md5sum"]=m2.hexdigest()
        #print item
        yield item 
    @staticmethod        
    def close(spider, reason):
        currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        logger.error(currentTime+":close in :")
