这个项目是scrapy框架结合selenium爬取JavaScript动态渲染后的页面内容，
主要通过对DownloadMiddlewares中间件的配置添加实现；
    def process_request(self, request, spider):
        spider.browser.get(request.url)
        return HtmlResponse(body=spider.browser.page_source, url=spider.browser.current_url,encoding='utf-8',request=request)

在setting中注意中间件和pipeline的优先级。
