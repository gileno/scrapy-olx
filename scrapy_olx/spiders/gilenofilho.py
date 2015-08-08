# -*- coding: utf-8 -*-

import scrapy


class GilenoFilhoSpider(scrapy.Spider):

    name = "gilenofilho"
    allowed_domains = ["gilenofilho.com.br"]
    start_urls = (
        'http://www.gilenofilho.com.br/',
    )

    def parse(self, response):
        self.log('Hello World: {0}'.format(response.url))
