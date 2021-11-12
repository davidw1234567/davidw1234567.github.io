#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename: run.py

import re
import os, sys
from crawler import Crawler, CrawlerCache

if __name__ == "__main__": 
    # Using SQLite as a cache to avoid pulling twice
    crawler = Crawler(CrawlerCache('OGOPI_data.db'))
    root_re = re.compile('^/$').match
    #make a loop
file = open("urls.txt", "r") 
for line in file: 
	crawler.crawl(line, no_cache=root_re)
		
    #crawler.crawl('http://techcrunch.com/', no_cache=root_re)
    #crawler.crawl('http://www.engadget.com/', no_cache=root_re)
    #crawler.crawl('http://gizmodo.com/', no_cache=root_re)
    #crawler.crawl('http://www.zdnet.com/', no_cache=root_re)
    #crawler.crawl('http://www.wired.com/', no_cache=root_re)