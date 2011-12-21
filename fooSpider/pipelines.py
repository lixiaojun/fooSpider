# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet.threads import deferToThread
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from cStringIO import StringIO
from fooSpider.pytesser import *
from fooSpider.settings import *
from scrapy.conf import settings
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi

import time
import MySQLdb.cursors
import hashlib
import json

class FooItemPipeline(object):
	def __init__(self):
		dispatcher.connect(self.spider_opened, signals.spider_opened)
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		#self.file = open("item.jl", "wb")
		
	def process_item(self, item, spider):
		line = json.dumps(dict(item))+"\n"
		self.file.write(line)
		return item
	
	def spider_opened(self, spider):
		self.file = open("items.jl", "wb")
    
	def spider_closed(self, spider):
		self.file.close()

class FooImagePipeline(ImagesPipeline):
	def __init__(self, store_uri, download_func=None):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',
					  db='cye_db',
					  user='root',
					  passwd='',
					  cursorclass=MySQLdb.cursors.DictCursor,
					  charset='utf8',
					  use_unicode=True
					  )
		super(FooImagePipeline, self).__init__(store_uri, download_func=download_func)
        
	def image_key(self, url):		
		filename = url.split('/')[-1]		
		return 'price\\%s' % (filename)
		
	def convert_images(self, image, size=None):
		buf = StringIO()
		try:
			image.save(buf, 'PNG')
		except Exception, ex:
			raise ImageException("Cannot process image. Error: %s" % ex)
		return image, buf
		
	def get_media_request(self, item, info):
		for image_url in item['image_urls']:
			yield Request(image_url, errback=handle_error)
			
	def item_completed(self, results, item, info):
		image_paths = [x['path'] for ok, x in results if ok]
		for image_path in image_paths:
			full_path = IMAGES_STORE+'/'+image_path
			im = Image.open(full_path)
			text = image_to_string(im)
			item['product_price'] = text[2:].strip()			
			query = self.dbpool.runInteraction(self._conditional_insert, item)
			query.addErrback(self.handle_error)
		return item

	def _conditional_insert(self, tx, item):
		# create record if doesn't exist. 
		# all this block run on it's own thread
		tx.execute("select * from cye_tb where url = %s", (item['product_url']))
		result = tx.fetchone()
		if result:
			log.msg("Item already stored in db: %s" (item['url']), level=log.DEBUG)
		else:
			tx.execute(\
						"insert into cye_tb (url, title, price, product_img_url, price_img_url, detail) "
						"values (%s, %s, %s, %s, %s, %s)",
						(item['product_url'],
						item['product_title'],
						item['product_price'],
						item['product_image'],
						item['price_url'],
						item['product_detail']
						)
			)
			log.msg("Item stored in db: %s" % item, level=log.DEBUG)

	def handle_error(self, e):
		log.err(e)