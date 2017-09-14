# -*- coding: utf-8 -*-

import scrapy
from w3lib.html import remove_tags
import re
from wuxia.items import Chapter

class wuxiaSpider(scrapy.Spider):
	'''Generic spider for downloading novels from WuxiaWorld.com
	   Subclass to scrape completely a novel by changing the start_urls
	   attribute to the first chapter of the novel you want.
	'''
	handle_httpstatus_list = [404]
	name = ""
	directory = "Wuxia/"
	url = ""

	def start_requests(self):
		if not self.url:
			with open("%s/lastchapter.txt" % (self.directory+self.wuxia_name)) as f:
				self.url = f.read()

		yield scrapy.Request(self.url,callback=self.parseChapter)
	

	def parseChapter(self, response):

		if response.status == 404:
			#mark last chapter for future updates
			with open("%s/lastchapter.txt" % (self.directory+self.wuxia_name), "w+") as f:
				f.write(response.url.encode('utf-8'))

		else:
			chapter = Chapter()
			main = response.xpath("//div[@itemprop='articleBody']")
			body = main.xpath("./p")[1:-1] #remove the previous/next chapter component

			#content extraction
			chapter['url'] = response.url
			chapter['chapterTitle'] = remove_tags(response.xpath("//title").extract_first())
			chapter['chapterContent'] = remove_tags('\n\n'.join(body.extract()))
			yield chapter

			#pagination
			nextPage = main.xpath("./p/span/a")[0]
			if nextPage:
				yield response.follow(nextPage,callback=self.parseChapter)
			

class ICDS_Spider(wuxiaSpider):
	name = "ICDS"
	url = 'http://www.wuxiaworld.com/icds-index/icds-chapter-0/'
	wuxia_name = name

class PTO_Spider(wuxiaSpider):
	name = "PTO"
	url = 'http://www.wuxiaworld.com/pto-index/pto-chapter-163/'
	wuxia_name = name