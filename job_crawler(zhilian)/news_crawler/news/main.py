# coding: utf-8
from logger.logger import logger
from mysql.mysqlPal import mysqlPal
from collection.baidu import news
from Queue import Queue
import threading
import traceback
import json
import time
import sys


class Producer(threading.Thread):
	def __init__(self, t_name, queue):
		threading.Thread.__init__(self, name=t_name)
		self.data = queue

	def run(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		while True:
			# 判断是否需要获取关键字
			log.write_log("[%d] Current number of keywords." % (self.data.qsize()), 'info')
			if self.data.qsize() == 0:
				# 连接mysql数据库
				try:
					self.mp = mysqlPal()
				except Exception, e:
					s = sys.exc_info()
					log.write_log("[baidu.py line:%d] Connect to the mysql database failed." % (s[2].tb_lineno))
					sys.exit()
				# 获取关键词
				criteria = {}
				keywordData = self.mp.find('news_keyword', criteria)
				for data in keywordData:
					if data['name']:
						self.data.put((data['name'].strip()))
					if data['short_name']:
						self.data.put((data['short_name'].strip()))
			else:
				time.sleep(10)


# Consumer thread
class Consumer(threading.Thread):
	def __init__(self, t_name, queue):
		threading.Thread.__init__(self, name=t_name)
		self.data = queue

	def run(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		rss = news(log)
		while True:
			try:
			    # 获取关键字，然后爬取
				data = self.data.get()
				status = rss.start(self.getName(), data.strip())
				if status:
					self.data.task_done()
			except Exception, e:
				log.write_log(traceback.print_exc(), 'error')


if __name__ == "__main__":
	#log = logger()  # 加载日志类
	queue = Queue()

	producer = Producer('Pro.', queue)
	producer.start()
	for i in range(10):
		consumer = Consumer('Con.' + str(i + 1), queue)
		consumer.start()
	producer.join()
	consumer.join()