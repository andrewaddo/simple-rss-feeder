import feedparser
from datetime import datetime, timedelta
from json import dumps
from httplib2 import Http
import re
import os

# Parse RSS feed, publish to Hangouts chat's webhook

POST_HEADERS = {'Content-Type': 'application/json; charset=UTF-8'}
SEARCHITEM = "GCP Updates"
RSSURL = os.environ.get('rssURL', 'rssURL environment variable is not set.')
WEBHOOKURL = os.environ.get('webhook', 'webhook environment variable is not set.')


def getRSSFeed(event, context):
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    getFeedPerSearchItem("GCP", yesterday, SEARCHITEM, RSSURL)


def getFeedPerSearchItem(profileID, filterTime, searchItem, rssUrl):
    print("Parsing feed for", searchItem, "with rss", rssUrl, filterTime)
    # get the feed from url
    raw = feedparser.parse(rssUrl)
    feeds = raw.entries
    # print("Got feeds", feeds[0].published, datetime.strptime(feeds[0].published, '%a, %d %b %Y %H:%M:%S %z').isoformat(), "filter time", filterTime)
    # check each feed, filter by last check time e.g. "Tue, 31 Mar 2020 18:17:41 +0000",
    # AWS what's new has timestamp 'Fri, 15 May 2020 17:03:58 +0000' does not match format '%a, %d %b %Y %H:%M:%S %z'
    # Google News has timestamp 'Fri, 15 May 2020 17:03:58 UTC' does not match format '%a, %d %b %Y %H:%M:%S %Z'
    newPosts = []
    # print("feeds count", len(feeds))
    try:
        newPosts = {entry for entry in feeds if datetime.strptime(
            entry.published, '%a, %d %b %Y %H:%M:%S %z').isoformat() > filterTime}
    except:
        print("Error with %z")
        try:
            newPosts = {entry for entry in feeds if datetime.strptime(
                entry.published, '%a, %d %b %Y %H:%M:%S %Z').isoformat() > filterTime}
        except Exception as e:  # work on python 3.x
            print('Failed to filter feeds by date: ' + str(e))
    # print("Got filtered items", newPosts, len(newPosts))
    print("found feeds count", len(newPosts))
    # publish a header
    for post in newPosts:
        # print("Title publish date", post.title, " filter date", filterTime)
        publishFeed(profileID, searchItem, post)


def publishFeed(profileID, searchItem, post):
    webhookURL = WEBHOOKURL
    if 'hooks.slack' in webhookURL:  # slack webhook
        label = "text"
        additionalSlack = ", \"username\": \"NFH\", \"icon_emoji\": \":newspaper:\""
    else:
        label = "text"
        additionalSlack = ""
    payload = "{\"" + label + "\":\"" + searchItem + " - " + post.published + "\\n" \
        + post.title + "\\n" \
        + post.link + "\"" \
        + additionalSlack \
        + "}"
    printable = "\\n".join(payload.split("\n"))
    # print("post data", printable)
    publishToWebHook(printable, webhookURL)


def publishToWebHook(postData, webhookURL):
    http_obj = Http()

    response = http_obj.request(
        uri=webhookURL,
        method='POST',
        headers=POST_HEADERS,
        body=postData.encode('utf-8'), 
        #!IMPORTANT: default Latin-1 would fail on certain special characters
    )
    if response[0].status == 200:
        print("Published to webhook")
    else:
        print("Error publishing to webhook", response)
