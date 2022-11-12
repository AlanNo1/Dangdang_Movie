import scrapy
from scrapy_dangdang.items import ScrapyDangdangItem

class DangdangSpider(scrapy.Spider):
    name = 'dangdang'  # 爬取所有python电子书
    allowed_domains = ['category.dangdang.com']
    start_urls = ['http://category.dangdang.com/cp01.03.44.00.00.00.html']
    base_url = 'http://category.dangdang.com/pg'
    page = 1

    def parse(self, response):
        li_list = response.xpath('//ul[@id="component_59"]/li')
        for li in li_list:
            src = li.xpath('.//a/img/@data-original').extract_first()
            if src:
                src = src
            else:
                src = li.xpath('.//a/img/@src').extract_first()
            name = li.xpath('.//a/img/@alt').extract_first()
            price = li.xpath('.//p[@class="price"]/span[@class="search_now_price"]/text()').extract_first()
            print(src, name, price)
            book = ScrapyDangdangItem(
                src = src,
                name = name,
                price = price
            )
            #获取book提交给管道
            yield book
        if self.page < 100:
            self.page += 1
            url = self.base_url + str(self.page)+'-cp01.03.44.00.00.00.html'
            yield scrapy.Request(url,callback=self.parse)


