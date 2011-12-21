# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class FoospiderItem(Item):
    # define the fields for your item here like:
    # name = Field()
	url = Field()
	title = Field()
	price_url = Field()
	detail = Field()

class FooImageItem(Item):
	product_url = Field()
	product_image = Field()
	product_title = Field()
	product_price = Field()
	price_url = Field()
	product_detail = Field()
	image_urls = Field()
	images = Field()
