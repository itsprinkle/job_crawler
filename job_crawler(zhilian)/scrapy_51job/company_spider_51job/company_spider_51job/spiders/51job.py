
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
import threading

from xml.dom import minidom,Node

from company_spider_51job.items import *

from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from company_spider_51job.xmlparser import get_xml_data
from time import sleep
from _csv import field_size_limit

try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
    from scrapy.utils.response import get_base_url
    from scrapy.utils.url import urljoin_rfc
    from scrapy.spiders import CrawlSpider, Rule
    from scrapy.linkextractors.sgml import SgmlLinkExtractor as sle



import  threading
import  time

from company_spider_51job.settings import *
import logging


reload(sys)
sys.setdefaultencoding('utf8')


logger = logging.getLogger("aa");  

#./hangye.dict ./city.dict ./salary.dict ./company_type.dict ./years.dict ./xueli.dict ./zhiweileixing.dict ./fabushijian.dict
class CRAWLERSPIDER(scrapy.spiders.Spider):
#爬虫名称
    name = "51job"
    #起始url
    #start_urls=["http://search.51job.com/list/131000,000000,0000,00,9,99,java,2,1.html?lang=c&degreefrom=99&stype=&workyear=99&cotype=99&jobterm=99&companysize=99&radius=-1&address=&lonlat=&postchannel=&list_type=&ord_field=&curr_page=&dibiaoid=0&landmark=&welfare="]
    #start_urls=["http://search.51job.com/list/120300,000000,0000,00,9,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="]
    #青岛,北京,上海,广州
    start_urls=["http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=030200&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9"]
    #该url的下一页
    nextpage_xpath='//a[text()="下一页"]/@href'.decode("utf8")
    list_xpath='//div[@id="resultList"]/div[@class="el"]'.decode("utf8")
    #job信息的属性和解析方式（直接从列表页可以解析到的信息）
    list_field_xpath = {u'salary': u'span[@class="t4"]/text()',
                         u'title': u'p/span/a/@title',
                          u'url': u'p/span/a/@href',
                         u'company_url': u'span[@class="t2"]/a/@href',
                         u'company_name': u'span[@class="t2"]/a/text()', 
                         u'city': u'span[@class="t3"]/text()',
                          u'time': u'span[@class="t5"]/text()'}
    #从详情页才能解析到的数据
    detail_filed_xpath = {u'hangye':u'//p[@class="msg ltype"]/text()',
                          u'experience':u'//div[@class="jtag inbox"]/div[1]/span/em[@class="i1"]/../text()',
                          u'xueli':u'//div[@class="jtag inbox"]/div[1]/span/em[@class="i2"]/../text()'
                          }
    #详情的地址
    item_xpath = '//div[@id="resultList"]/div[@class="el"]/span[@class="t2"]/a/@href'.decode("utf8")
    #详情解析方式
    company_field_xpath={
                         u'content': u'//div[@class="con_msg"]/div[@class="in"]/descendant::text()',
                           u'company_logo': u'//img[@class="cimg"]/@src',
                               u'company_size': u'//p[@class="ltype"]/descendant::text()'}
                        

  

    #filetag=0

    #def __init__(self,filetag):

        #self.filetag=filetag
        #log设置
        #error_handler = logging.FileHandler("d:/error_."+str(filetag)+".txt");  
        #error_handler.setLevel(logging.ERROR);  
        #info_handler = logging.FileHandler("d:/info_."+str(filetag)+".txt");  
        #info_handler.setLevel(logging.INFO);  

        #logger.addHandler(error_handler);  
        #logger.addHandler(info_handler);  
        #读取文件中的链接
        #file=open("company_spider_51job/conf/sub.list_"+str(filetag),"r")
        #for line in file.readlines():
         #   url=line
          #  self.start_urls.append(url)

    def parse(self,response):

        print "current link"+response.url
        logger.info("current link："+response.url)
        response_selector = HtmlXPathSelector(response)
        #获取下一页的链接，进行继续爬取
        #print self.nextpage
        #print response_selector.select(self.nextpage).extract()
        for next_link  in response_selector.select(self.nextpage_xpath).extract():
                  base_url = get_base_url(response)
                  relative_url = next_link
                  next_link= urljoin_rfc(base_url,relative_url)
                  print "next_link" +next_link
                  yield scrapy.Request(url=next_link,callback=self.parse,headers=DEFAULT_REQUEST_HEADERS)
	
           #解析列表中可以获取的信息         
             #一页数据
        job_page = response_selector.select(self.list_xpath)
        job_list = []
        for line_sel in job_page:
               field_value = {"sub_url":response.url}
               #解析每一条数据
               for next_field_item_name in self.list_field_xpath:
                   if len(line_sel.select(self.list_field_xpath[next_field_item_name]).extract())>0:
                        field_value[next_field_item_name]=line_sel.select(self.list_field_xpath[next_field_item_name]).extract()[0]
                   else:
                       field_value[next_field_item_name]=""
               job_list.append(field_value)

         #解析一页的数据，（列表）
        for index in range(0,len(job_list)):
            field_value = job_list[index]
            
            detail_link = field_value["url"]
            company_link = field_value["company_url"]
            yield scrapy.Request(url=detail_link,callback=self.parse_detail,meta = field_value,headers=DEFAULT_REQUEST_HEADERS)
            yield Request(url=company_link,callback=self.parse_company,meta=field_value,headers=DEFAULT_REQUEST_HEADERS)
        
          

        #解析详情
    def parse_detail(self,response):

        #sleep(100)
        url = response.url
        response_selector = HtmlXPathSelector(response)
        field_value = response.meta 
        item = Item()
        #将第一页解析到的数据。组装到item
        for file_name in self.list_field_xpath:
            item[file_name] = field_value[file_name]
#解析详情界面中才能获取的字段
        for file_name in self.detail_filed_xpath:

            if len(response_selector.select(self.detail_filed_xpath[file_name]).extract())>0:
                item[file_name]=response_selector.select(self.detail_filed_xpath[file_name]).extract()[0]
            else:
                item[file_name]=""
                #组装固定内容
        item["source"]= "51job"
        item["sub_url"]=response.meta["sub_url"]
        m2 = hashlib.md5()
        m2.update(item["url"])
        item["url_md5sum"]=m2.hexdigest()
        m2 = hashlib.md5()
        m2.update(item["company_url"])
        item["company_url_md5sum"]=m2.hexdigest()
        item['created']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
               #处理发布时间，如果月份比今天大，那么就是2016年的数据
        publish_at = '2017-'+item['time']
               
        t = time.strptime(publish_at,"%Y-%m-%d")
        pub_time=time.mktime(t)
        now_time=time.mktime(time.localtime(time.time()))
                        #说明月份比当前大，为去年的信息
        if(float(pub_time) >= float(now_time)):
                publish_at = '2016-'+item['time']
        item['time']=publish_at
        str_arr =  item['hangye'].split("|")
        hangye = str_arr[len(str_arr)-1].strip()
        item['hangye']=hangye
        
        yield item
        #解析公司
    def parse_company(self, response):
        item =Company_Item()
        #组装公司信息
        sub_url=response.meta['sub_url']	

        item["sub_url"]=sub_url

        item["source"]="51job"
        
        item["company_url"]=response.url
        
        item["company_name"]=response.meta["company_name"]
        
        response_selector = HtmlXPathSelector(response)
      #解析公司信息
        for node_name in self.company_field_xpath:
            item[node_name]=""
            #大于0则代表有数据
            if len(response_selector.select(self.company_field_xpath[node_name]).extract())>0:
               item[node_name]=("".join(response_selector.select(self.company_field_xpath[node_name]).extract())).replace("\n","").strip()
               

               if node_name=="company_size":
                  if len(item[node_name].split("|"))>=2:
                     item[node_name]=item[node_name].split("|")[1].replace("\t","").replace(" ","")
                  else:
                     item[node_name]=item[node_name].split("|")[0].replace("\t","").replace(" ","")


#生产公司url的MD5

        m2 = hashlib.md5()
        m2.update(item["company_url"])
        item["company_url_md5sum"]=m2.hexdigest()
        yield item 
    @staticmethod        
    def close(spider, reason):
        #输出到文件
        currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        logger.error(currentTime+":close in :"+spider.filetag)
        

        
