# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class SpiderDispatcherPipeline(object):
    spider_name = None 
    
    def open_spider(self, spider):
        if spider.name == self.spider_name:
            self.open(spider)
            
    def process_item(self, item, spider):
        if spider.name == self.spider_name:
            return self.process(item, spider)
        else:
            return item
        
    def close_spider(self, spider):
        if spider.name == self.spider_name:
            self.close(spider)
            
    def open(self, spider):
        raise NotImplementedError('subclasses must override open()') 
         
    def process(self, item, spider):
        raise NotImplementedError('subclasses must override process()')
    
    def close(self, spider):
        raise NotImplementedError('subclasses must override close()')

class ArabiaPipeline(SpiderDispatcherPipeline):
    spider_name = 'arabia'
    
    def open(self, spider):
        self.ids = []
        
    def process(self, item, spider):
        # drop invalid scraped community items
        if item.get('item') == 'community' and not item.get('followers'):
            raise DropItem('Invalid community item')
        # convert HTML content to Markdown
        if item.get('content'):
            import html2text
            h2t = html2text.HTML2Text()
            h2t.ignore_links = True
            item['content'] = h2t.handle(item.get('content'))
        # check duplicate
        if item.get('id') in self.ids:
            raise DropItem('Duplicated item')
        
        self.ids.append(item.get('id'))
        return item

    def close(self, spider):
        del self.ids