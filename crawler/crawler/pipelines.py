import pymongo
from decouple import config


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline:
    collection_name = config("MONGODB_COLLECTION")
    client = None
    db = None

    _mongodb_uri = config("MONGODB_URI")
    _mongodb_db = config("MONGODB_DB")

    def open_spider(self, spider):
        spider.logger.info("action=MongoPipeline, message=conecting to mongodb")
        self.client = pymongo.MongoClient(self._mongodb_uri)
        self.db = self.client[self._mongodb_db]

    def close_spider(self, spider):
        spider.logger.info("action=MongoPipeline, message=closing the mongodb connection")
        self.client.close()

    def process_item(self, item, spider):
        spider.logger.info(f"action=MongoPipeline, message=store item {item}")
        if self.db[self.collection_name].count_documents({"link": item["link"]}) > 0:
            spider.logger.info("action=MongoPipeline, message=the item already exists")
            return item

        self.db[self.collection_name].insert_one(item)
        item["_id"] = str(item["_id"])
        spider.logger.info(f"action=MongoPipeline, message=stored {item['_id']} item")
        return item
