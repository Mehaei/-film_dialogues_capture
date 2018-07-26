import scrapy
from urllib import request
class VideoSpider(scrapy.Spider):
    name = 'video'
    start_urls = ['http://www.dian-ying.org/']

    def parse(self, response):
        # 大分类url
        classUrlList = response.xpath('.//ul[@class="nav navbar-nav hidden-sm"]/li/a/@href').extract()[1:]
        url = 'http://www.dian-ying.org/'
        # 循环请求分类
        for classUrl in classUrlList:
            base_url = request.urljoin(url,classUrl)
            yield scrapy.Request(base_url,callback=self.classInfo)
    # 小分类列表
    def classInfo(self,response):
        # title = response.xpath('//h6[@class="media-heading"]/a/@title').extract()
        detailHrefList = response.xpath('//h6[@class="media-heading"]/a/@href').extract()
        for detailHref in detailHrefList:
            detailUrl = request.urljoin(response.url,detailHref)
            yield scrapy.Request(detailUrl,callback=self.getVideoInfo)

        # 下一页
        totalPage = response.xpath('//div[@class="c mt1 list_page"]/a[last()]/text()').extract_first().split('/')[-1]
        pageHz = 'index_%d.html'
        for i in range(1,int(totalPage)+1):
            if i == 1:
                pageUrl = response.url
            else:
                pageUrl = request.urljoin(response.url,pageHz%i)
            yield scrapy.Request(pageUrl,callback=self.classInfo)
    # 获取对话 和 电影名
    def getVideoInfo(self,response):
        videoTitle = response.xpath('//h2[@class="page-header"]/text()').extract_first()
        videoCon = response.xpath('//div[@class="info-content"]//p/text()').extract()
        print(response.url,videoCon)

