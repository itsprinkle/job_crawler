# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import datetime
import MySQLdb.cursors
from scrapy import signals
import json
import codecs
import re
from scrapy import log
import time
import MySQLdb

import datetime
from items import *
from attr.validators import instance_of
from time import sleep




#Get a date object
today = datetime.date.today()
date_string=today.strftime("%y%m%d")


class SQLStorePipeline(object):
    def open_spider(self,spider):
        self.MYSQL_SERVER='180.76.189.148'
        self.MYSQL_DB='jobs'
        self.MYSQL_USERNAME='yangchaoming'
        self.MYSQL_PASSWORD='ycm@2017'
        self.connectToDB()
        pass

       
    def connectToDB(self):
        try:
        
            ##用户名和密码
            self.dbpool = adbapi.ConnectionPool('MySQLdb', host=self.MYSQL_SERVER,db=self.MYSQL_DB,user=self.MYSQL_USERNAME, passwd=self.MYSQL_PASSWORD,
                                                 cursorclass=MySQLdb.cursors.DictCursor,charset='utf8', use_unicode=True)

            print "connect success `````````````````````````````````"
        except Exception as e:

            log.msg(("connect error,(SQLStorePipeline): %s",str(e)), log.ERROR)
    
    def process_item(self, item, spider):
        #run db query in thread pool
        try:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        except Exception as e:
            self.connectToDB()
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            log.msg(("connect error"+str(e)), log.ERROR)

        return item

    def _conditional_insert(self, tx, item):
#如果是job职位item
        if isinstance(item,Item):
            sql = "insert into job_info_test(url_md5sum,url,title,company_name,experience,company_url,company_url_md5sum,time,hangye,city,salary,xueli,source,sub_url,\
            created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update sub_url=%s, time=%s , created=%s"
            params = (item['url_md5sum'],item['url'],item['title'],item['company_name'],item['experience'],item['company_url'],item['company_url_md5sum'],item['time'],
                      item['hangye'],item['city'],item['salary'],item['xueli'],item['source'],item['sub_url'],item['created'],item['sub_url'],item['time'],item['created'])
            tx.execute(sql,params)
                   
            print 'insert one:'+item["url_md5sum"]
#如果是company公司item

        if isinstance(item,Company_Item):
            sql = "insert into job_company_test(company_name,company_size,content,company_url,company_url_md5sum,company_logo,sub_url,source)\
             values(%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update company_name=%s , sub_url=%s"
            params = (item['company_name'],item['company_size'],item['content'],item['company_url'],item['company_url_md5sum'],item['company_logo'],item['sub_url'],item['source'],item['company_name'],item['sub_url'])
            tx.execute(sql,params)
                   
            print 'insert one:'+item["company_url_md5sum"]
                   


                        

  
        
    def handle_error(self, e):
        log.msg("error handle ``````````````````````\n", log.ERROR)
        log.msg(("connect error"+str(e)), log.ERROR)



