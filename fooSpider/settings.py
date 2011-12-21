# Scrapy settings for fooSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'fooSpider'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['fooSpider.spiders']
NEWSPIDER_MODULE = 'fooSpider.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
IMAGES_STORE = '/Users/roger/imgs'