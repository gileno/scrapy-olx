# -*- coding: utf-8 -*-
import scrapy


class OlxSpider(scrapy.Spider):
    name = "olx"
    allowed_domains = ["pe.olx.com.br"]
    start_urls = (
        'http://pe.olx.com.br/imoveis/aluguel',
    )

    def parse(self, response):
        items =  response.xpath(
            '//div[contains(@class,"section_OLXad-list")]//li[contains'
            '(@class,"item")]'
        )
        for item in items:
            url = item.xpath(
                ".//a[contains(@class,'OLXad-list-link')]/@href"
            ).extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            '//li[contains(@class,"item next")]//a/@href'
        ).extract_first()
        if next_page:
            self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        self.log(u'Imóvel URL: {0}'.format(response.url))
        item = {}
        item['photos'] = response.xpath(
            '//div[contains(@class,"photos")]//a/@href'
        ).extract()
        item['url'] = response.url
        item['address'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-location")]'
            '//.)'
        ).extract_first()
        item['title'] = response.xpath(
            'normalize-space(//h1[contains(@id,"ad_title")]//.)'
        ).extract_first()
        item['price'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-price")]'
            '//span[contains(@class,"actual-price")]//.)'
        ).extract_first()
        item['details'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-description")]'
            '//.)'
        ).extract_first()
        item['source_id'] = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-id")]//strong//.)'
        ).extract_first()
        date = response.xpath(
            'normalize-space(//div[contains(@class,"OLXad-date")]//.)'
        ).re("Inserido em: (.*).")
        item['date'] = (date and date[0]) or ''
        yield item
