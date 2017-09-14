# -*- coding: utf-8 -*-
import os, errno
import re

class WuxiaPipeline(object):

	wuxia_name = ""
	path = ""

	def __init__(self):
		self.pattern = re.compile(r"Chapter ([\d]+)")

	def open_spider(self, spider):
		#check directory if it exists. If not, create directory
		self.wuxia_name = spider.wuxia_name
		self.path = spider.directory + self.wuxia_name
		try:
			os.makedirs(self.path)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise

	def processTitle(self,title):
		'''Captures the chapter number from the title and pads zeroes accordingly'''
		capture = self.pattern.search(title)
		chapterNumber =  capture.group(1).rjust(3,'0')
		return ("%s Chapter %s.txt" % (self.wuxia_name, chapterNumber)).encode('ascii')


	def process_item(self, item, spider):
		#save to file
		if len(item["chapterContent"]) > 2000: #spoiler filter
			title = self.processTitle(item['chapterTitle'])
			with open("%s/%s" % (self.path,title), "w+") as f:
				f.write(item["chapterContent"].encode('utf-8'))
				print '%s downloaded successfully' % title

		else:
			#mark last chapter for future updates
			with open("%s/lastchapter.txt" % self.path, "w+") as f:
				f.write(item["url"].encode('utf-8'))