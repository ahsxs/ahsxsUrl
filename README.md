# ahsxsUrl

#### Url采集器

采集速度不算快，主要是用来采集Google的，使用selenium也是为了方便过人机验证

仅仅为了满足自己需求，程序设计新手，欢迎大佬提意见

##### 新增fofa搜索抓取

花了300大洋买会员，可惜api只能获取前100条结果，不过翻页可以获取10000条ヾ(o◕∀◕)ﾉヾ

果断加了一个功能，fofa采集比较慢，因为不做强制休眠的话发包太快会被封号(这玩意儿真亲测)

所以让每页强制休眠3-13秒，2020.12.25下午测试爬取1k条稳定，1w条的大家自行测试

```
optional arguments:
  -h, --help    show this help message and exit
  -os OS        Your os type [linux/windows/mac]
  -e ENGINE     Choose the search engine you want to
                use.[baidu/google/bingCN(国内版)/bingEN(国际版)/fofa(需自行登录和搜索)]
  -key KEY      input the key to search for
  -save SAVE    What type do you want to save. doamin[www.baidu.com]
                site[https://www.baidu.com/]
                url[https://www.aidu.com/news.php?id=xxx]
  -page PAGE    setting max number pages.
  -count COUNT  Set the count of results
  
参数列表：
optional arguments:
  -h, --help    查看帮助信息
  -os OS        设置你的操作系统信息 [linux/windows/mac]
  -e ENGINE     选择你想要使用的搜索引擎.[baidu/google/bingCN(国内版)/bingEN(国际版)/fofa(需自行登录和搜索)]
  -key KEY      输入你要搜索的关键词（fofa不需要）
  -save SAVE    设置你想要的保存格式（fofa不支持设置）. 
  				域名[www.baidu.com]
                站点[https://www.baidu.com/]
                原始链接[https://www.aidu.com/news.php?id=xxx]
  -page PAGE    设置fofa的最大爬行页
  -count COUNT  设置fofa的最大抓取条数
  
除fofa以外其他搜索引擎结果都已经自动去重
```

  
