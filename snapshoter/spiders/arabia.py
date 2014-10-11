# -*- coding: utf-8 -*-
import string
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Compose, Join
from urlparse import urljoin

from snapshoter.items import ArabiaPostItem, ArabiaCommentItem, ArabiaCommunityItem


class ArabiaSpider(CrawlSpider):
    name = 'arabia'
    allowed_domains = ['arabia.io']

    rules = (
        Rule(LinkExtractor(allow=r'/[a-zA-Z0-9_-]+$', deny=r'/u/.+?$'), callback='parse_community', follow=True),
        #Rule(LinkExtractor(allow=r'/[a-zA-Z0-9_-]+/\d+-.*?'), callback='parse_post', follow=True)
    )
    
    def start_requests(self):
        yield Request('https://arabia.io/communities')
        yield Request('https://arabia.io/sitemap-1.xml', callback=self.parse_sitemap)
    
    def parse_sitemap(self, response):
        selector = Selector(text=response.body)
        for url in selector.xpath('//loc/text()').extract():
            # adding meta date will result memory leak, avoid it !
            yield Request(url, callback=self.parse_post)
        
    def parse_post(self, response):
        post = ItemLoader(item=ArabiaPostItem(), response=response)
        post.default_output_processor = TakeFirst()
        #post.add_xpath('id', '//*[@class="post_content replace_urls"]/@id', MapCompose(int), re=r'(\d+)')
        post.add_xpath('id', '//*[@class="short_url inputtext"]/@value', MapCompose(int), re=r'(\d+)')
        post.add_xpath('title', '//*[@id="nav_title"]/a/text()')
        post.add_xpath('up_votes', '//*[@class="s_upvotes"]/text()', MapCompose(int), re=r'(\d+)')
        post.add_xpath('down_votes', '//*[@class="s_downvotes"]/text()', MapCompose(int), re=r'(\d+)')
        post.add_xpath('points', '//*[@class="post_points ltr"]/text()', MapCompose(int))
        post.add_xpath('author_username', '//*[@class="block username"]/text()')
        post.add_xpath('author_fullname', '//*[@class="block full_name"]/text()', MapCompose(lambda value: value.replace(u'\xa0', u'')))
        post.add_xpath('date', '//*[@class="icon-time"]/../text()')
        post.add_xpath('community', '//*[@class="icon-reorder"]/../a[1]/text()')
        post.add_xpath('topics', '//*[@class="topic"]/text()', MapCompose(string.strip))
        post.add_xpath('url', '//*[@class="short_url inputtext"]/@value')
        post.add_value('type', 'link' if post.get_xpath('//*[@id="nav_title"]/a/@rel', TakeFirst()) == 'nofollow' else 'text')
        if post.get_output_value('type') == 'link':
            post.add_xpath('link', '//*[@id="nav_title"]/a/@href')
            post.add_xpath('domain', '//*[@class="post_domain"]/text()', re=r'\((.+?)\)')
        post.add_xpath('content', '//*[@class="post_content replace_urls"]/*', Join('\n'))
        post.add_value('item', 'post')
        yield post.load_item()

        comments = []
        for row in response.selector.xpath('//*[contains(@class, "post_comment")]'):
            comment = ItemLoader(item=ArabiaCommentItem(), selector=row, response=response)
            comment.default_output_processor = TakeFirst()
            comment.add_xpath('id', './@id', re=r'(\d+)')
            comment.add_xpath('index', './@class', MapCompose(int), re=r'index(\d+)')
            comment.add_value('post_id', post.get_output_value('id'))
            #comment.add_value('parent_id', '')
            comment.add_xpath('author_username', './/*[@class="comment_user"]/a/text()')
            comment.add_xpath('date', './/*[@class="comment_date"]/text()')
            comment.add_xpath('points', './/*[@class="comment_points ltr"]/text()')
            comment.add_xpath('content', './/*[@class="post_content comment_content replace_urls"]/*', Join('\n'))
            #comment.add_xpath('url', './/*[@class="comment_short_url"]/a/@href')
            comment.add_value('url', 'https://arabia.io/go/{0}/{1}'.format(post.get_output_value('id'), comment.get_output_value('id')))
            comment.add_value('item', 'comment')
            comments.append(comment)
        
        for (index, comment) in enumerate(comments):
            if comment.get_output_value('index') == 0:
                comment.add_value('parent_id', 0)
                continue
            for comment_cursor in comments[:index][::-1]:
                if comment_cursor.get_output_value('index') == comment.get_output_value('index') - 1:
                    comment.add_value('parent_id', comment_cursor.get_output_value('id'))
                    break
        
        for comment in comments:
            yield comment.load_item()


    def parse_community(self, response):
        community = ItemLoader(item=ArabiaCommunityItem(), response=response)
        community.default_output_processor = TakeFirst()
        community.add_xpath('id', '//*[@id="nav_title"]/a/@href', re=r'/([a-zA-Z0-9-_]+)$')
        community.add_xpath('logo', '//*[@class="category_logo"]/@src', MapCompose(lambda relative_url: urljoin(response.url, relative_url)))
        community.add_xpath('title', '//*[@id="nav_title"]/a/text()')
        community.add_xpath('description', '//*[@class="category_description"]/text()')
        community.add_xpath('followers', '//*[@id="category_follow"]/h3/text()', MapCompose(int), re=r'(\d+)')
        community.add_value('url', response.url)
        community.add_value('item', 'community')
        yield community.load_item()




