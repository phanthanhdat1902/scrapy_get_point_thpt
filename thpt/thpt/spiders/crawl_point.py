import scrapy
from thpt.items import ThptItem


class CrawlerSpider(scrapy.Spider):
    name = "crawl_point"
    MaVung="02"
    start_urls = [
        'https://vietnamnet.vn/vn/giao-duc/tra-cuu-diem-thi-thpt'
    ]

    def parse(self, response):
        SBD='02000000'
        for i in range(1,74719):
            SBD=SBD[:len(SBD)-len(str(i))]+str(i)
            print(i)
            yield scrapy.Request("https://vietnamnet.vn/vn/giao-duc/tra-cuu-diem-thi-thpt/?y=2020&sbd="+SBD, callback=self.crawlLyric)

    def crawlLyric(self, response):
        item = ThptItem()
        item['SBD']=response.xpath('//p[@class="SoBD m-t-10"]/span/text()')[0].extract() 
        item['MaVung']=item['SBD'][0:2]
        #set default NgoaiNgu
        item['N1'] = -1
        item['N2'] = -1
        item['N3'] = -1
        item['N4'] = -1
        item['N5'] = -1
        item['N6'] = -1
        arrTr = response.xpath(
            '//table[@class="table thpt-mobile hidden-md hidden-sm hidden-lg"]/tr')
        if len(arrTr[2].xpath('td/text()').extract()) == 2:
            type = arrTr[2].xpath('td/text()').extract()[1].split(':')[0]
            point = arrTr[2].xpath('td/text()').extract()[1].split(':')[1]
            item[type] = point
        for i in range(9):
            arr = arrTr[i].xpath('td/text()').extract()
            arr[0] = arr[0].replace(' ', '')
            if len(arr) == 2:
                item[arr[0]] = arr[1]
            else:
                item[arr[0]] = -1
        yield item
        # print(response.xpath('//table[@class="table thpt-mobile hidden-md hidden-sm hidden-lg"]/tr')[0].xpath('td/text()').extract())
