import asyncio
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config.yaml'


class __Context:
    def __init__(self, path):
        self.log_level = 10 # 10 for DEBUG, 20 for INFO
        self.pages_concurrency = 1
        # load other configs here like Database Connections, Notification Service, Analytics Service(Grafana, Prometheus)

    async def send_notification(self, message):
        pass
        # Notification service either to Slack/Logs/Grafana


async def __create_context():
    return context

context = __Context(config_path)

loop = asyncio.get_event_loop()
loop.run_until_complete(__create_context())