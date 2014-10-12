# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArabiaPostItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    up_votes = scrapy.Field()
    down_votes = scrapy.Field()
    points = scrapy.Field()
    author_username = scrapy.Field()
    author_fullname = scrapy.Field()
    date = scrapy.Field()
    community = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field() # text OR link
    content = scrapy.Field() # if type == text
    link = scrapy.Field() # if type == link
    domain = scrapy.Field() # if type == link
    item = scrapy.Field()

class ArabiaCommentItem(scrapy.Item):
    id = scrapy.Field()
    index = scrapy.Field()
    post_id = scrapy.Field()
    parent_id = scrapy.Field()
    author_username = scrapy.Field()
    date = scrapy.Field()
    points = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    item = scrapy.Field()

class ArabiaCommunityItem(scrapy.Item):
    id = scrapy.Field()
    logo = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    followers = scrapy.Field()
    url = scrapy.Field()
    item = scrapy.Field()
    
class ArabiaQuestionItem(scrapy.Item):
    id = scrapy.Field()
    asker_username = scrapy.Field()
    answerer_username = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    item = scrapy.Field()