from PageScraper import PageScraper
from PageTopicsClassifier import PageTopicsClassifier
from utils.Context import context
import logging
logging.basicConfig(level=context.log_level, filename='PageTopicsRetrieval')


class PageTopicsRetrieval:
    def __init__(self, page_obj: object, priority_page: bool = False):
        self.page_obj = page_obj
        self.page_url = page_obj["page_url"] if "page_url" in page_obj else ""
        self.priority_page = priority_page

    async def __call__(self):
        _ = PageScraper(self.page_url)
        page_html, page_topics, page_content = await _.fetch_page()

        _ = PageTopicsClassifier(self.page_url, page_html, page_topics, page_content)
        topics_classified = await _.classify_topics()
        print(topics_classified)



