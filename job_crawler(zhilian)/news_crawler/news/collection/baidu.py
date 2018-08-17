#coding:utf-8
import datetime
import hashlib
import sys
import time

import feedparser
import socket
import MySQLdb

from mysql.mysqlPal import mysqlPal
from newspaper import Article


class news:

    def __init__(self, log):
        # 连接mysql数据库
        try:
            self.mp = mysqlPal()
        except Exception, e:
            s=sys.exc_info()
            log.write_log("[baidu.py line:%d] Connect to the mysql database failed."%(s[2].tb_lineno))
            sys.exit()

        self.log = log

    def content(self, newsUrl):
        article = Article(newsUrl, language='zh')
        article.download()
        article.parse()
        return article.text

    def baiduRss(self, keyword, page=0):
        socket.setdefaulttimeout(5) #Rss 采集超时判断
        try:
            rss = feedparser.parse('http://news.baidu.com/ns?word=%s&tn=newsrss&sr=0&cl=2&rn=50&ct=0&pn=%d'%(keyword, page))
        except Exception, e:
            self.baiduRss(keyword, page)
            return False

        keycriteria = {"where": "name = '%s' or short_name = '%s'" % (keyword, keyword)}
        keywordInfo = self.mp.findOne('news_keyword', keycriteria)
        #  公司 ID 赋值。
        try:
            keywordInfo['company_id'] = int(keywordInfo['company_id'])
        except:
            keywordInfo['company_id'] = str(0)
   # 遍历解析到的数据数据   
        for newsInfo in rss.entries:
            #print json.dumps(newsInfo);
            md5 = hashlib.md5()
            md5.update(newsInfo.link)
            uniqueKey = md5.hexdigest()
            criteria = {"where": "unique_key = '%s'" % (uniqueKey)}
            newsData = self.mp.findOne('ent_news_primary', criteria)
# 如果不存在则插入，   
            if not newsData:
	
                isInsert = self.insert(newsInfo, uniqueKey, keyword, int(keywordInfo['company_id']))
	
                if isInsert == False:
                    return False
            else:
                return False
        # 判断是否还需要分页采集
        if len(rss.entries) == 50:
            self.baiduRss(keyword, page+1)
        else:
            return False

    def insert(self, newsInfo, uniqueKey, keyword, company_id):
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S'
        TIME = newsInfo.published
        publishTime = datetime.datetime.strptime(TIME, GMT_FORMAT).strftime("%Y-%m-%d %H:%M:%S")
        publishYear = int(time.mktime(time.strptime(publishTime, '%Y-%m-%d %H:%M:%S')))
        if publishYear < 1451577600:
             return False
	
	desc = newsInfo.summary;
        # 处理index中的特殊字符 
        try:
            index = desc.index("<br />")
            sub_desc=desc[index+6:len(desc)]
        except:
            sub_desc=desc
        
            
        data = dict(unique_key=uniqueKey, title=newsInfo.title, company_name=keyword, description=MySQLdb.escape_string(sub_desc), url=newsInfo.link,
                    publish_time=publishTime, source=newsInfo.author, insert_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        if company_id > 0:
            data['company_id'] = company_id
        self.mp.save('ent_news_primary',data)

        newsInfo = self.content(newsInfo.link)

        info = dict(unique_key=uniqueKey, content=MySQLdb.escape_string(newsInfo))
        self.mp.save('ent_news_detail', info)
        self.log.write_log("[%s] insert news '%s' success \n"%(time.strftime("%Y-%m-%d %H:%M:%S"), uniqueKey),'info')
        return True


    def start(self, queueName, keyword):
        # 获取关键词并开始采集
        if keyword:
            self.log.write_log("[%s] %s - start collection '%s' keyword \n" % (time.strftime("%Y-%m-%d %H:%M:%S"), queueName, keyword),
                               'info')
            return self.baiduRss(keyword)
        else:
            return False