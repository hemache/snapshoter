# -*- coding: utf-8 -*-

# Scrapy settings for snapshoter project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BOT_NAME = 'snapshoter'

SPIDER_MODULES = ['snapshoter.spiders']
NEWSPIDER_MODULE = 'snapshoter.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Web Snapshoter (+http://https://arabia.io/u/snapshoter/)'

ITEM_PIPELINES = {
    'snapshoter.pipelines.ArabiaPipeline': 300,
    #'scrapy_mongodb.MongoDBPipeline': 900
}

MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE')
MONGODB_UNIQUE_KEY = 'id'

CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = CONCURRENT_REQUESTS

