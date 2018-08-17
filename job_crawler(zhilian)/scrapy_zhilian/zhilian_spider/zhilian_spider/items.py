# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Item(scrapy.Item):

    url=scrapy.Field()
    url_md5sum=scrapy.Field()

    sub_url= scrapy.Field()

    title= scrapy.Field()
    company_name=scrapy.Field()
    company_url=scrapy.Field()
    company_url_md5sum=scrapy.Field()

    time= scrapy.Field()
    hangye=scrapy.Field()
    city=scrapy.Field()
    salary=scrapy.Field()
    experience=scrapy.Field()
    xueli=scrapy.Field()

    source=scrapy.Field()


class Company_Item(scrapy.Item):
    company_url=scrapy.Field()
    company_url_md5sum=scrapy.Field()
    company_name=scrapy.Field()
    company_size=scrapy.Field()
    content=scrapy.Field()

    company_logo=scrapy.Field()

    source=scrapy.Field()
    sub_url=scrapy.Field()
