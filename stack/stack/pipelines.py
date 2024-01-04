# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class MongoDBPipeline:
    def __init__(self) -> None:
        self.conn = pymongo.MongoClient(
            host="localhost",
            port=27017
        )
        #connect to the database
        db = self.conn['stackoverflow']
        self.collection = db['questions']
        
    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
    
    def close_spider(self, spider):
        self.conn.close()