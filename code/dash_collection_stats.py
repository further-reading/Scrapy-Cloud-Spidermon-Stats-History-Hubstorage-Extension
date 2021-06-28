import os
from collections import deque
import scrapinghub
from sh_scrapy.stats import HubStorageStatsCollector
import logging
logger = logging.getLogger(__name__)


class DashCollectionsStatsHistoryCollector(HubStorageStatsCollector):
    def _open_collection(self, spider):
        sh_client = scrapinghub.ScrapinghubClient()
        proj_id = os.environ.get('SCRAPY_PROJECT_ID')
        if proj_id is None:
            return

        project = sh_client.get_project(proj_id)
        collections = project.collections
        stats_location = f"{spider.name}_stats_history"
        store = collections.get_store(stats_location)
        return store

    def _get_stat_history(self):
        try:
            data = self.store.list()
            data = [d.get('value') for d in data]
        except scrapinghub.client.exceptions.NotFound:
            data = []
        return data

    def open_spider(self, spider):
        super().open_spider(spider)
        self.store = self._open_collection(spider)
        if self.store is None:
            spider.stats_history = []
            return
        max_stored_stats = spider.crawler.settings.getint(
            "SPIDERMON_MAX_STORED_STATS", default=100
        )

        try:
            data = self._get_stat_history()
            stats_history = deque(data, maxlen=max_stored_stats)
        except scrapinghub.client.exceptions.NotFound:
            stats_history = deque([], maxlen=max_stored_stats)

        spider.stats_history = stats_history

    def _persist_stats(self, stats, spider):
        if self.store is not None:
            stats_history = spider.stats_history
            stats_history.appendleft(self._stats)
            for index, data in enumerate(stats_history):
                self.store.set({'_key': str(index), 'value': data})