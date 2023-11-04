import os
import subprocess
from celery import shared_task

CRAWLER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'crawler')

@shared_task
def run_spider():
    spider_name = 'quotes'
    file_name = 'quotes.json'
    subprocess.check_output(['scrapy', 'crawl', spider_name, '-o', file_name], cwd=CRAWLER_PATH)