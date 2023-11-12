from utils.Context import context
from utils.job_utils import schedule
import asyncio
# from aiologger import Logger
import logging
import aiojobs
from PageTopicsRetrieval import PageTopicsRetrieval
from datetime import datetime
logging.basicConfig(level=context.log_level)


class AccountsManager:
    def __init__(self):
        self.context = context
        self.loop = asyncio.get_event_loop()
        self.pages_config = []

    async def __load_page_configs(self):
        # retrieve pages config from database
        # for testing, we have these 3 URLs hardcoded
        self.pages_config = [
            {
                "page_url": "http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/",
                "active": True,
                "page_backoff_value": 1,
                "page_cycle_increment": 0
            },
            {
                "page_url": "http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/",
                "active": True,
                "page_backoff_value": 1,
                "page_cycle_increment": 0
            }
        ]

    async def initialize(self):
        # load Necessary Configs(pages for example) info from database connection created from Context file
        await self.__load_page_configs()
        logging.debug(msg="{datetime}:{classname}:{message}".format(datetime=datetime.utcnow().isoformat(),
                                                                    classname=self.__class__.__name__,
                                                                    message="Re-Initialized All Configs"
                                                                    ))

    async def start(self):
        await self.context.send_notification("Starting PagesManager Module (%s)" % datetime.utcnow().isoformat())
        # Schedule auto reinitalizing of the configs from the respective dbs
        schedule(self.initialize, interval=1 * 60 * 60, loop=self.loop)
        # Starting infinite loop that fetches the data for new pages added to database
        # 1. Get pages which are not retrieved
        # 2. Parse pages and save the topics to a different database

        while True:

            await self.fetch_pages_data()
            logging.info(msg="{datetime}:{classname}:{message}".format(datetime=datetime.utcnow().isoformat(),
                                                                        classname=self.__class__.__name__,
                                                                        message="Sleeping for %s minutes" % ((3 * 60)-datetime.utcnow().minute)))
            await asyncio.sleep(1 * 60 * (60 - datetime.utcnow().minute))

    async def fetch_pages_data(self):
        scheduler = await aiojobs.create_scheduler(limit=self.context.pages_concurrency)

        for each_page_obj in self.pages_config:
            page_obj = PageTopicsRetrieval(each_page_obj, priority_page=True)
            await scheduler.spawn(page_obj())

        while True:
            if scheduler.active_count == 0:
                await scheduler.close()
                break
            else:
                await asyncio.sleep(10)


async def main():
    accounts_manager = AccountsManager()
    await accounts_manager.initialize()
    await accounts_manager.start()
    while True:
        await asyncio.sleep(10)


loop = asyncio.get_event_loop()
comments = loop.run_until_complete(main())


