#-*-coding:utf-8-*-

from twisted.enterprise import adbapi
import MySQLdb.cursors
from scrapy import signals
import json
from scrapy import log
import time
import MySQLdb
from items import *
import sys
from time import sleep

reload(sys)
sys.setdefaultencoding('utf8')

class SQLStorePipeline(object):
    def open_spider(self,spider):
        self.MYSQL_SERVER='192.168.1.207'
        self.MYSQL_DB='park'
        self.MYSQL_USERNAME='luodezhao'
        self.MYSQL_PASSWORD='luodezhao'
        self.connectToDB()
        #self.MYSQL_SERVER='127.0.0.1'
        #self.MYSQL_DB='park'
        #self.MYSQL_USERNAME='root'
        #self.MYSQL_PASSWORD='mysql'
        #self.connectToDB()
        pass

       
    def connectToDB(self):
        try:
        
            ##用户名和密码

            self.dbpool = adbapi.ConnectionPool('MySQLdb', host=self.MYSQL_SERVER,db=self.MYSQL_DB,user=self.MYSQL_USERNAME, passwd=self.MYSQL_PASSWORD,
                                                 cursorclass=MySQLdb.cursors.DictCursor,charset='utf8', use_unicode=True)

            print "connect success `````````````````````````````````"
        except Exception as e:

            log.msg(("connect error,(SQLStorePipeline)",str(e)), log.ERROR)
    
    def process_item(self, item, spider):
        #run db query in thread pool
        try:

            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        except Exception as e:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            log.msg(("connect error,(SQLStorePipeline): %s",str(e)), log.ERROR)

        return item

    def _conditional_insert(self, tx, item):

        if isinstance(item,ParkBaseItem):
            sql = "insert into park_base(name,level,address,area,industry,image,detail,plan,preferential,url,url_md5,created,sub_url)\
             values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update created=%s,industry=%s"
          
            detail=MySQLdb.escape_string(str(item['detail']));
            plan=MySQLdb.escape_string(str(item['plan']));
            preferential=MySQLdb.escape_string(str(item['preferential']));
            params = (item['name'],item['level'],item['address'],item['area'],item['industry'],item['image'],detail,plan,
                      preferential,item['url'],item['url_md5'],item['created'],item['sub_url'],item['created'],item['industry'])



            #tx.execute(sql,params)
                   
            print 'insert one:'+item["url"]


        if isinstance(item,ParkCompanyItem):
            sql = "insert into park_company(company_name,park_md5) values(%s,%s)"
            params = (item['company_name'],item['park_md5'])
            #tx.execute(sql,params)
                   
            print 'insert one:'+item["company_name"]
                   


            

    def close_spider(self,spider):
        #self.db.close()
        log.msg("closing \n", log.ERROR)
        sleep(1000)
       pass
        
    def handle_error(self, e):
        #log.msg("error handle ``````````````````````\n", log.ERROR)
        #log.msg(("connect error,(SQLStorePipeline):",str(e)), log.ERROR)
        pass

      #  sleep(1000)

