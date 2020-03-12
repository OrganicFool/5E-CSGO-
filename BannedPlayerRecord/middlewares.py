# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
import time
import math

# geckodriver所在的目录，也就是你的火狐浏览器所在的目录
GECKODRIVER_ADDRESS = r"C:\Program Files\Mozilla Firefox\geckodriver.exe"


class BannedplayerrecordSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BannedplayerrecordDownloaderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 判断请求类型
        if request.url == spider.start_urls[0]:

            # 创建geckodriver对象
            driver = webdriver.Firefox(executable_path = GECKODRIVER_ADDRESS)
            driver.get(request.url)
            time.sleep(1)

            # 根据需要爬取的数据量动态加载页面（每摁一次“显示更多”，页面会自动加载200条数据）
            button = driver.find_elements_by_xpath('//*[@id="loadData"]')[0]
            times = math.ceil(spider.player_number/200)
            for i in  range(times):
                button.click()
                time.sleep(1)

            # 创建response对象并返回
            html = driver.page_source
            driver.quit()
            return HtmlResponse(url=request.url, body=html, request=request,encoding='utf-8')
        else:
            return None


    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
