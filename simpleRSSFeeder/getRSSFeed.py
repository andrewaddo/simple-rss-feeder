from datetime import datetime, timedelta
from json import dumps
import os
from .simpleRSSParser import SimpleRSSParser

# Parse RSS feed, publish to Hangouts chat's webhook


def getRSSFeed(event, context):
    SEARCHITEM = "GCP Updates"
    RSSURL = os.environ.get(
        'rssURL', 'rssURL environment variable is not set.')
    WEBHOOKURL = os.environ.get(
        'webhook', 'webhook environment variable is not set.')
    simpleRSSParser = SimpleRSSParser(RSSURL, WEBHOOKURL)
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    simpleRSSParser.getAndPublishFeeds("GCP", yesterday, SEARCHITEM)
