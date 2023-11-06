import logging
import re


class ContentLogFilter(logging.Filter):
    def filter(self, record):
        return bool(re.search(r"\[QuotesToScrape\]", record.msg)) or bool(
            "closed" in record.msg
        )
