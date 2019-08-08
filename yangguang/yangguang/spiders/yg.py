# -*- coding: utf-8 -*-
import scrapy
from yangguang.items import YangguangItem


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://d.wz.sun0769.com/index.php/question/huiyin']

    def parse(self, response):
        tr_list = response.xpath(".//div[@class='newsHead clearfix']/table[2]//tr")
        for tr in tr_list:
            item = YangguangItem()
            item["title"] = tr.xpath("./td[@class='txt18']/a[1]/text()").extract_first()
            item["href"] = tr.xpath("./td[@class='txt18']/a[1]/@href").extract_first()
            item["publish_data"] = tr.xpath("./td[@class='txt16_2'][2]/text()").extract_first()
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item": item}
            )

        # 翻页
        next_url = response.xpath("//div[@class='disz']//a[text()='>']").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["content_img"] = response.xpath(".//div[@class='wzy1']/table[2]//div[@class='textpic']/img/@src").extract()
        item["content_img"] = ["http://wz.sun0769.com" + i for i in item["content_img"]]
        item["content"] = response.xpath(".//div[@class='wzy1']/table[2]//div[@class='contentext']/text()").extract()
        yield item