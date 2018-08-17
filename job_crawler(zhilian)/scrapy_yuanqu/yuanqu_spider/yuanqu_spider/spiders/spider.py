#-*-coding:utf-8-*-
import hashlib
import time
import scrapy
from scrapy.selector.lxmlsel import HtmlXPathSelector
from yuanqu_spider.settings import *
from yuanqu_spider.items import *
from time import sleep
import sys
from pip._vendor.requests.models import Response
reload(sys)
sys.setdefaultencoding('utf8')

class CRAWLERSPIDER(scrapy.spiders.Spider):
    #�б������ʽ
    list_xpath=u'//div[@class="park_listL"]/div[@class="parkinfo_list"]/div[@class="fact_list"]'
    #԰����ҳ����
    home_xpath=u'div[@class="fact_incon2"]/div[@class="fact_date"]/text()'
    #԰����ҳ���ֶν���
    home_field_xpath = {u'name': u'//div[@class="btit"]/h1/a/text()',
                         u'level': u'//div[@class="stit"]/em/text()',
                          u'address': u'//strong[contains(text(),"\u9879\u76ee\u5730\u5740")]/../../div[@class="inf_right f_l f14"]/text()',
                          u'area': u'//strong[contains(text(),"\u56ed\u533a\u9762\u79ef")]/../../div[@class="inf_right f_l f14"]/text()',
                          u'industry': u'//strong[contains(text(),"\u4e3b\u5bfc\u4ea7\u4e1a")]/../../div[@class="inf_right f_l f14"]/span/text()',
                          u'image':u'//ul[@class="fimglist clearfix"]/li/a/@href'

    }
    #԰���������
    detail_xpath=u'//div[@class="parkinfo_L"]'
    #԰���滮
    plan_xpath=u'//div[@class="parkinfo_L"]'
    #԰���Ż����߽���
    yhzc_xpath=u'//div[@class="parkinfo_L"]'
    #ҳ���������õ�PageList(1,10,10,104,'gyyclass=0&keyword=&CY_id=0&city=0',8)���������ַ��������б���û����һҳ���ӣ�ֻ�ܽ�������ַ������жϵ�ǰҳ
    #下一页的数据
    nextpage_xpath=u'//div[@id="LoadPageList"]/script/text()'

    name = "spider"
    start_urls=[]

    def __init__(self):
        #���ļ��ж�ȡ����
        #D:/spider_workspace/scrapy_yuanqu/yuanqu_spider/yuanqu_spider/
        file=open(r"conf/sub.list","r")
        for line in file.readlines():
            url= ''.join(line).strip('\n')
            self.start_urls.append(url[0:-1])
    def parse(self,response):
        #print response.url
        response_selector = HtmlXPathSelector(response)
        list=response_selector.select(self.list_xpath)
        #���û��page�����ǵ�һ����ȡ��Ϊ��һҳ
        try:
            page=response.meta['page']
        except:
            page=1
#��������
        for sel in list:
            home=sel.select(self.home_xpath).extract()[0]
            home_link=home[4:]
            #print home_link
            yield scrapy.Request(url=home_link,callback=self.parse_home,meta={"sub_url":response.url},headers=DEFAULT_REQUEST_HEADERS)
        #������һҳ��Ϣ���ַ�������PageList(1,10,10,104,'gyyclass=0&keyword=&CY_id=0&city=0',8)
        nextMsg=response_selector.select(self.nextpage_xpath).extract()[0]
       # �����ַ������õ���ǰҳ��
        currentPage=nextMsg.split(",")[0].split("(")[1]
        #�����ǰҳ���meta�е�ҳ����ȣ���ȥ��ȡ��һҳ�����򣬾Ͳ�������һҳ���������pageΪ12ʱ�����û�е�12ҳ�����������currentPage��Ϊ11����˵����ǰ�Ѿ��������ҳ
        if cmp(str(page),str(currentPage))==0:
            if page==1:
                url=response.url+"?page="+str(page+1)
            else:
                url=response.url.split("=")[0]+"="+str(page+1)
           # ������һҳ
            yield scrapy.Request(url=url,callback=self.parse,meta={"page":page+1},headers=DEFAULT_REQUEST_HEADERS)

               
#����԰����base��Ϣ
    def parse_home(self,response):
        response_selector = HtmlXPathSelector(response)
        field_value={}
        field_value['url']=response.url
        field_value['sub_url']=response.meta["sub_url"]
        for field_name in self.home_field_xpath:
            field_value[field_name]=""
            if len(response_selector.select(self.home_field_xpath[field_name]).extract())>0:
                if field_name =="industry":
                    #���Ϊ��ҵ����Ҫ�÷���ƴ��������Ϊ�ַ���
                    industries=response_selector.select(self.home_field_xpath[field_name]).extract()
                    field_value[field_name]=",".join(industries)
                else:
                    field_value[field_name]=response_selector.select(self.home_field_xpath[field_name]).extract()[0]
                    #ƴ��ͼƬ��ַ
        field_value["image"]="http://"+response.url.split("/")[2]+field_value["image"]
        
        yield scrapy.Request(url=response.url+"detail/",callback=self.parse_detail,meta=field_value,headers=DEFAULT_REQUEST_HEADERS)
        #԰������
    def parse_detail(self,response):
        
        response_selector = HtmlXPathSelector(response)
        detailList= response_selector.select(self.detail_xpath).extract()
        detailStr="".join(detailList)
        baseUrl=response.meta['url']
        response.meta['detail']=detailStr.decode("utf-8")
        yield scrapy.Request(url=baseUrl+"plan/",callback=self.parse_plan,meta=response.meta,headers=DEFAULT_REQUEST_HEADERS)
    ###��ȡ�滮
    def parse_plan(self,response):
        response_selector = HtmlXPathSelector(response)
        planList=response_selector.select(self.plan_xpath).extract()
        planStr="".join(planList)
        baseUrl=response.meta['url']
        response.meta['plan']=planStr.decode("utf-8")
        yield scrapy.Request(url=baseUrl+"yhzc/",callback=self.parse_yhzc,meta=response.meta,headers=DEFAULT_REQUEST_HEADERS)

    ###��ȡ����
    def parse_yhzc(self,response):
         response_selector = HtmlXPathSelector(response)
         yhzcList=response_selector.select(self.yhzc_xpath).extract()
         yhzcStr="".join(yhzcList)

         message=response.meta
         #��װ԰����Ϣ
         item=ParkBaseItem()
         item['preferential']=yhzcStr.decode("utf-8")
         item['name']=message['name']
         item['level']=message['level']
         item['address']=message['address']
         item['area']=message['area']
         item['industry']=message['industry']
         item['image']=message['image']
         item['detail']=message['detail']
         item['plan']=message['plan']
         item['url']=message['url']
         item["sub_url"]=message["sub_url"]
         m2 = hashlib.md5()
         m2.update(item["url"])
         item["url_md5"]=m2.hexdigest()
        
         item['created']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


        # print item
         yield item
         yield scrapy.Request(url=item['url']+"company/",callback=self.parse_company,meta={"park_md5":item["url_md5"],"page":1},headers=DEFAULT_REQUEST_HEADERS)
    #��˾�б�
    companylist_xpath=u'//div[@class="companylist"]/ul/li'
    #g��˾����
    companyname_xpath=u'div[@class="comlist_con"]/a/text()'
    ###����company�б�
    def parse_company(self,response):
        response_selector = HtmlXPathSelector(response)
        list=response_selector.select(self.companylist_xpath)
        #print list
        for sel in list:
             item=ParkCompanyItem()
             company_name=sel.select(self.companyname_xpath).extract()[0]
             #print company_name
            # print response.meta["park_md5"]
             item['company_name']=company_name
             item["park_md5"]=response.meta["park_md5"]
             yield item
        #��һҳ
        page=response.meta['page']
#��һҳ��ԭ����԰��ҳ����ͬ
        if len(response_selector.select(self.nextpage_xpath).extract()) >0:
                nextMsg=response_selector.select(self.nextpage_xpath).extract()[0]
                currentPage=nextMsg.split(",")[0].split("(")[1]
                if cmp(str(page),str(currentPage))==0:

                    if page==1:
                        url=response.url+"?page="+str(page+1)
                    else:
                        url=response.url.split("=")[0]+"="+str(page+1)
                    print  url
                    yield scrapy.Request(url=url,callback=self.parse_company,meta={"park_md5":item["park_md5"],"page":page+1},headers=DEFAULT_REQUEST_HEADERS)



        
        


        
