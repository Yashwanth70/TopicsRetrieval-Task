from utils.Context import context
import logging
from requests_html import AsyncHTMLSession
import html2text
logging.basicConfig(level=context.log_level, filename='PageScraper')


class PageScraper:
    def __init__(self, page_url: str):
        self.page_url = page_url
        self.asession = AsyncHTMLSession()
        # self.tags_to_process = ["title", "h1", "h2", "h3", "h4", "b", "strong", "em", "i", "a"]
        self.tags_to_process = ["title", "h1", "h2", "h3", "h4", "b", "strong", "em"]
        self.topics = []

    async def parse_html(self, html:str):
        for each_tag in self.tags_to_process:
            try:
                result = html.find(each_tag)
                for each_result in result:
                    self.topics.append(each_result.text)
            except Exception as e:
                print(e)

    async def fetch_page(self):
        result_html, page_content = "", ""
        try:
            result = await self.asession.get(self.page_url)
            if result.status_code == 200:
                result_html = result.html
                await self.parse_html(result_html)
                html_to_text = html2text.HTML2Text()
                html_to_text.ignore_links = True
                html_to_text.ignore_images = True
                html_to_text.wrap_links = False
                page_content = html_to_text.handle(result_html.html)
                del html_to_text
        except Exception as e:
            print(e)
        self.topics = list(set(self.topics))
        self.topics = list(filter(None, self.topics))
        return result_html, self.topics, page_content





