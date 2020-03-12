#5E封禁记录生成工具
5E封禁记录生成命令行工具，基于scrapy框架和selenium库
可以查询到最近n个被封禁的用户

## 开发环境
火狐版本：66.0.1

[scrapy](https://github.com/scrapy/scrapy) 版本：2.0.0

```
conda install scrapy 
```
[geckodriver](https://github.com/mozilla/geckodriver/releases)版本:0.24.0 win64

pandas：0.25.1

## 使用方法
项目下使用如下命令生成记录数据，可以自己调整爬取数量
```
scrapy crawl BannedPlayer -a playernumber=1000
```