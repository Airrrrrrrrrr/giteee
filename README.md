首先你需要确保已安装scrapy和selenium

可以使用pip命令进行安装

```
pip install scrapy selenium
```

如果速度过慢，可以使用国内的镜像源。

## 国内镜像源：

清华：https://pypi.tuna.tsinghua.edu.cn/simple

阿里云：http://mirrors.aliyun.com/pypi/simple/

中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

华中理工大学：http://pypi.hustunique.com/

山东理工大学：http://pypi.sdutlinux.org/

豆瓣：http://pypi.douban.com/simple/

我这里使用的是清华的镜像源。

```
pip install scrapy selenium -i https://pypi.tuna.tsinghua.edu.cn/simple
```



本文旨在快速上手scrapy + selenium 。

如果不会scrapy的话，可以看我的scrapy单独实例。[Airrrrrrrrrr/ssr1: scrapy爬取崔庆才练习网站1的实例 (github.com)](https://github.com/Airrrrrrrrrr/ssr1)



**step1：添加init函数，这个函数在爬虫开始执行时会自动触发。**

这里仅实例化了一个chrome浏览器，未进行参数添加。

可按需求进行添加参数

```
def __init__(self):
    self.browser = webdriver.Chrome()
    super().__init__()
```

**step2：修改process_request()函数**

原函数返回的是None，这里需要注意，返回None是正确的，如果返回的是request，则会陷入死循环。

```
def process_request(self, request, spider):
    spider.browser.get(request.url)
    return HtmlResponse(body=spider.browser.page_source, url=spider.browser.current_url,encoding='utf-8',request=request)
```

**step3：添加spider_closed()函数**

因为selenium在爬虫运行完后不会自动进行关闭，所以需要添加相应的函数和操作

```
def spider_closed(self, spider):
    spider.browser.quit()
```

**step4：将中间件的优先级调高**

```
DOWNLOADER_MIDDLEWARES = {
   "gitee.middlewares.GiteeDownloaderMiddleware": 299,
}
```

```
ITEM_PIPELINES = {
   "gitee.pipelines.GiteePipeline": 300,
}
```
