import scrapy
from selenium import webdriver
from gitee.items import GiteeItem


class ExploreSpider(scrapy.Spider):
    name = "explore"
    allowed_domains = ["gitee.com"]
    start_urls = ["https://gitee.com/explore/all"]

    def __init__(self):
        self.browser = webdriver.Chrome()
        super().__init__()



    def parse(self, response):
        item = GiteeItem()
        for i in range(1, 16):
            item["name"] = response.xpath('//*[@id="explores-show"]/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div['+ str(i) +']/div/div[1]/div[1]/h3/a/text()').extract_first()
            item["href"] = response.xpath('//*[@id="explores-show"]/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div['+ str(i) +']/div/div[1]/div[1]/h3/a/@href').extract_first()
            item["href"] = "https://gitee.com/" + item["href"]
            item["title"] = response.xpath('//*[@id="explores-show"]/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div['+ str(i) +']/div/div[2]/text()').extract_first()
            item["stars"] = response.xpath('//*[@id="explores-show"]/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div['+ str(i) +']/div/div[1]/div[2]/a/div/text()').extract_first()
            print(item)
            yield item
            if response.xpath('//*[@id="git-discover-page"]/a[last()]/@href').extract_first() is not None:
                next_url = response.urljoin(response.xpath('//*[@id="git-discover-page"]/a[last()]/@href').extract_first())
                yield scrapy.Request(next_url, callback=self.parse)





if __name__ == "__main__":
    from scrapy import cmdline
    cmdline.execute("scrapy crawl explore --nolog".split())
