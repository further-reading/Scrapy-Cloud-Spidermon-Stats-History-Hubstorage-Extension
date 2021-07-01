# Scrapy Cloud Spidermon Stats History Hubstorage Extension

This is a spidermon extension to create a version of [stats history collector](https://spidermon.readthedocs.io/en/latest/howto/stats-collection.html) that works better with scrapy dash.

The _DotScrapy Persistence Add-on_ is not needed when using this. The _STATS_CLASS_ override step is still requred however the drawback mentioned will not occur when using this extension.

The spider will create a dash collection named {spider_name}\_stats\_history that contains the stats for the last SPIDERMON_MAX_STORED_STATS runs of your spider. There will be an additional job_url field added that will have the url to open the job in scrapy cloud.

To enable, install the requirements, place the dash_collection_stats.py file in your project and update settings.py as such:

```python
STATS_CLASS = (
    "path.to.dash_collection_stats.DashCollectionsStatsHistoryCollector"
)

# Stores the stats of the last 10 spider execution (default=100)
SPIDERMON_MAX_STORED_STATS = 10
```
Monitors can be enabled using the same example code from [stats history collector](https://spidermon.readthedocs.io/en/latest/howto/stats-collection.html).
