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




#Get a date object
today = datetime.date.today()
date_string=today.strftime("%y%m%d")


class SQLStorePipeline(object):
    def __init__(self):
        #self.MYSQL_SERVER='180.76.189.148'
        #self.MYSQL_DB='jobs'
        #self.MYSQL_USERNAME='luodezhao'
        #self.MYSQL_PASSWORD='luodezhao@PS2017'
        self.MYSQL_SERVER='180.76.189.148'
        self.MYSQL_DB='jobs'
        self.MYSQL_USERNAME='yangchaoming'
        self.MYSQL_PASSWORD='ycm@2017'
        

        try:
            ##用户名和密码
            self.dbpool = adbapi.ConnectionPool('MySQLdb', host=self.MYSQL_SERVER,db=self.MYSQL_DB,user=self.MYSQL_USERNAME, passwd=self.MYSQL_PASSWORD, 
                                                
                                                cursorclass=MySQLdb.cursors.DictCursor,charset='utf8', use_unicode=True)
        except Exception as e:
            print "ERROR(SQLStorePipeline): %s"%(str(e),)

    def process_item(self, item, spider):
        #run db query in thread pool
        try:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        except Exception as e:
            self.dbpool = adbapi.ConnectionPool('MySQLdb', host=self.MYSQL_SERVER,db=self.MYSQL_DB,user=self.MYSQL_USERNAME, passwd=self.MYSQL_PASSWORD, cursorclass=MySQLdb.cursors.DictCursor,charset='utf8', use_unicode=True)
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):

        if "salary" in item:
            tx.execute(\
                "insert into job_info_test (url_md5sum,url,title,company_name,experience,company_url,company_url_md5sum,time,hangye,city,salary,xueli,source,sub_url,created)"
                "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update title=%s,company_name=%s,experience=%s,company_url=%s,\
                company_url_md5sum=%s,time=%s,hangye=%s,city=%s,salary=%s,xueli=%s,sub_url=%s ,created=%s",
                (
                  item["url_md5sum"],
                  item["url"],
                  item["title"],
                  item["company_name"],
                  item["experience"],
                  item["company_url"],
                  item["company_url_md5sum"],
                  item["time"],
                  item["hangye"],
                  item["city"],
                  item["salary"],
                  item["xueli"],
                  item["source"],
                  item["sub_url"],
                  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                  

                  item["title"],
                  item["company_name"],
                  item["experience"],
                  item["company_url"],
                  item["company_url_md5sum"],
                  item["time"],
                  item["hangye"],
                  item["city"],
                  item["salary"],
                  item["xueli"],
                  item["sub_url"],
                  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

		)
            )
        elif "company_size" in item:
            tx.execute(\
              "insert into job_company_test (company_name,company_url,company_url_md5sum,company_size,content,source,sub_url,company_logo)"
              "values(%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update company_name=%s,company_size=%s,content=%s,source=%s,sub_url=%s,company_logo=%s",
              (
                item["company_name"],
                item["company_url"],
                item["company_url_md5sum"],
                item["company_size"],
                item["content"],
                item["source"],
                item["sub_url"],
                item["company_logo"],
                item["company_name"],
                item["company_size"],
                item["content"],
                item["source"],
                item["sub_url"],
                item["company_logo"]
                )
            )
        print 'insert one'

        
        

        
    def handle_error(self, e):
        print str(e)
        pass

class JsonPipeline(object):
    def __init__(self):
        self.f = open("zhilianzhaopin.json", "w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii = False) + ",\n"
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()


