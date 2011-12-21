from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
#from fooSpider.pipelines import FooPipeline
from fooSpider.items import FoospiderItem, FooImageItem
from scrapy.conf import settings
from scrapy import log
import re
#settings.overrides['ITEM_PIPELINES'] = ['fooSpider.pipelines.FooImagePipeline']
settings.overrides['ITEM_PIPELINES']=['fooSpider.pipelines.FooImagePipeline']

class FooSpider(BaseSpider):
	name = "foo"
	domain_name = "360buy.com"
	base_url = "http://www.360buy.com/products/"
	start_urls = ["http://www.360buy.com/products/670-671-672.html"]
	
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		links = hxs.select('//div[@id="plist"]/ul[@class="list-h"]/li/div[@class="p-img"]/a/@href').extract()
		#print links
		for link in links:
			#print link
			request = Request(link, callback=self.parse_post)
			yield request
		
		link = hxs.select('//a[@class="next"]/@href').extract()[0]
		url = self.base_url+link
		#print "next url:"+url
		request = Request(url, callback=self.parse)
		yield request
		
	def parse_post(self, response):
		item = FooImageItem()
		hxs = HtmlXPathSelector(response)
		item['product_title'] = hxs.select('//div[@id="name"]/h1/text()').extract()[0].split('<')[0].strip()
		item['product_url'] = response.url
		item['product_image'] = hxs.select('//div[@id="spec-n1"]/img/@src').extract()[0]
		product_detail = hxs.select('//ul[@id="i-detail"]').extract()[0]
		#log.msg("product detail: %s" % product_detail, level=log.DEBUG)
		item['product_detail'] = self.striphtml(product_detail)
		log.msg("product detail: %s" % item['product_detail'], level=log.DEBUG)
		item['price_url'] = hxs.select('//strong[@class="price"]/img/@src').extract()[0]
		item['image_urls'] = hxs.select('//strong[@class="price"]/img/@src').extract()
		yield item
		
	def parse_response(self, response):
		item = FooImageItem()
		hxs = HtmlXPathSelector(response)
		item['product_title'] = hxs.select('//title/text()').extract()[0]
		item['product_url'] = response.url
		item['product_image'] = hxs.select('//div[@id="spec-n1"]/img/@src')[0]
		product_detail = hxs.select('//ul[@id="i-detail"]').extract()[0]
		item['product_detail'] = self.striphtml(product_detail)
		item['price_url'] = hxs.select('//strong[@class="price"]/img/@src').extract()[0]
		item['image_urls'] = hxs.select('//strong[@class="price"]/img/@src').extract()
		yield item
	
	def striphtml(self, data):
		p = re.compile(r'<.*?>')
		return p.sub('', data)