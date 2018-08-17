# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ParkBaseItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    level = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    industry = scrapy.Field()
    image = scrapy.Field()
    detail = scrapy.Field()
    plan = scrapy.Field()
    preferential = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field()
    created = scrapy.Field()
    sub_url=scrapy.Field()
    pass
class ParkCompanyItem(scrapy.Item):
    company_name=scrapy.Field()
    park_md5=scrapy.Field()
    pass
