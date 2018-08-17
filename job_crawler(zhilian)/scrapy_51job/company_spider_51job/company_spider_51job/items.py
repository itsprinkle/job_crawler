# -*- coding: utf-8 -*-

import scrapy
class Item(scrapy.Item):
    sub_url= scrapy.Field()
    title=scrapy.Field()
    url=scrapy.Field()
    url_md5sum=scrapy.Field()
    hangye=scrapy.Field()
    city=scrapy.Field()

    experience=scrapy.Field()
    xueli=scrapy.Field()

    company_name=scrapy.Field()
    company_location=scrapy.Field()
    company_url=scrapy.Field()
    company_url_md5sum=scrapy.Field()
    salary=scrapy.Field()
    time=scrapy.Field()
    created = scrapy.Field()

    source=scrapy.Field()

class Company_Item(scrapy.Item):
    company_size=scrapy.Field()
    content=scrapy.Field()
    company_name=scrapy.Field()
    sub_url= scrapy.Field()
    company_url=scrapy.Field()
    company_url_md5sum=scrapy.Field()

    company_logo=scrapy.Field()

    source=scrapy.Field()
