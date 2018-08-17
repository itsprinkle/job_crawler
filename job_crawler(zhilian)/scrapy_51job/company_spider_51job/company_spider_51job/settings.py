 # -*- coding: utf-8 -*-

# Scrapy settings for company_spider_51job project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import os
from scrapy import log
#import logging




BOT_NAME = 'company_spider_51job'
SPIDER_MODULES = ['company_spider_51job.spiders']
NEWSPIDER_MODULE = 'company_spider_51job.spiders'


#Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'company_spider_51job (+http://www.yourdomain.com)'

#Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=50

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=50
#CONCURRENT_REQUESTS_PER_IP=50
DOWNLOAD_TIMEOUT = 360

#CONCURRENT_REQUESTS_PER_SPIDER=50

#DEPTH_LIMIT=100000000

#SCHEDULER_ORDER ='BFO'

#DNSCACHE_ENABLED = True

#LOG_LEVEL=DEBUG


#Disable cookies (enabled by default)
COOKIES_ENABLED=False
#log配置
#LOG_FILE="d:/51jobErr.txt"
#LOG_ENABLED=True
#LOG_LEVEL=log.ERROR

#Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

#DUPEFILTER_DEBUG=True
#DUPEFILTER_CLASS ="company_spider_51job.dupefilters.SeenURLFilter"


#Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#"Accept-Encoding":"gzip, deflate, sdch",
#"Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
#"Cache-Control":"max-age=0",
#"Connection":"keep-alive",
#"Cookie":"D_SID=218.189.127.12:0ubuPCN+kLdO7bLJUrALR7AcKCSTuk9znBjshY92X4I; cX_S=ipnjhjd7ntxvuy4z; _ga=GA1.3.1846374206.1466397796; SEARCH_PER_PAGE=50; __utmt=1; __utmt_guru=1; PHPSESSID2=5nios33sptdd6bn8aese3sdjb2; PG_U=huzhongster%40gmail.com; PG_T=TQcMafvmMy7YjsHX3At6AcGRZrZHfPCk; PGID1=439402; PGID2=huzhongster%40gmail.com; PGURU_VISITOR=a0016026-4df0-452a-8fd7-f02b894c2225; cX_P=ipnjhjd94ghk7ito; D_PID=63A8B3E5-F76A-3166-9955-BE0C85641993; D_IID=D73AEDD1-4E2E-338F-A5D7-AD2CD2E258A4; D_UID=F01F6374-3751-3D56-A804-99236AFFA8F0; D_HID=owaC6qwzR0PFvMsSxFKZ7xm70s14yoEjuk00KTntvzE; __utma=165735807.1846374206.1466397796.1466406383.1466410059.4; __utmb=165735807.236.8.1466414973059; __utmc=165735807; __utmz=165735807.1466397963.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
#"Host":"www.commercialguru.com.sg",
#"Referer":"http://www.commercialguru.com.sg/singapore-property-listing/property-for-sale/2?distance=1",
#"Upgrade-Insecure-Requests":"1",
#"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
#}
#
#数据管道配置
ITEM_PIPELINES = {

   # 'company_spider_51job.pipelines.JsonPipeline': 300,
    'company_spider_51job.pipelines.SQLStorePipeline': 310,

}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'company_spider_51job.middlewares.MyCustomSpiderMiddleware': 543,
#}



#Enable or disable downloader middlewares
#See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
  #   'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
  #   'company_spider_51job.proxymiddlewares.ProxyMiddleware': 100,
  #   'company_spider_51job.rotate_useragent.RotateUserAgentMiddleware':90,
}


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html

#EXTENSIONS={'scrapy.resolver.CachingThreadedResolver': 0,}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'company_spider_51job.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

#Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}
