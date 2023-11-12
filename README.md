# RSS Downloader

从RSS订阅中获取更新媒体信息，并下载到本地。

## 思路

根据html 页面元素爬虫有个痛点就是如果网站页面结构发生调整，爬虫程序会失效。
但是只要这个网站提供rss feed，对应的rss 符合rss或者atom 规范，rss feed的格式固定，从
rss feed 里爬取信息会更加稳定。


## Reference

https://feedparser.readthedocs.io/en/latest/atom-detail.html