import scrapy
from scrapy_movie.items import ScrapyMovieItem

class DySpider(scrapy.Spider):
    name = 'dy'
    allowed_domains = ['www.ygdy8.net']
    start_urls = ['https://www.ygdy8.net/html/gndy/oumei/index.html']

    def parse(self, response):
        mv_list = response.xpath('//div[@class="co_content8"]//td[2]//a[2]')
        for mv in mv_list:
            name = mv.xpath('./text()').extract_first()
            href = mv.xpath('./@href').extract_first()
            #第二页地址是
            url = 'https://www.ygdy8.net'+href
            yield scrapy.Request(url,callback=self.parse_second,meta={'name':name})

    def parse_second(self, response):
        src = response.xpath('//div[@id="Zoom"]//img/@src').extract_first()
        name = response.meta['name']
        move = ScrapyMovieItem(name=name,src=src)
        yield move
