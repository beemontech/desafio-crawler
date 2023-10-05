import json

from datetime import datetime


class CrawlerPipeline(object):
    def open_spider(self, spider):
        file_name = datetime.now().strftime("%Y-%m-%d-%H-%M")
        self.file = open("IMDb_{}.json".format(file_name), "w")
        self.file.write("[")

    def close_spider(self, spider):
        self.file.write("{}]")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ","
        self.file.write(line)
        return item
