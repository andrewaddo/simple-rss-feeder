import feedparser
from datetime import datetime, timedelta
from .webhookPublisher import WebhookPublisher


class SimpleRSSParser:
    def __init__(self, RSSURL, webHookURL):
        self.RSSURL = RSSURL
        self.webhookURL = webHookURL
        self.webhookPublisher = WebhookPublisher(webHookURL)
        print("")

    def getAndPublishFeeds(self, profileID, filterTime, searchItem):
        print("Parsing feed for", searchItem, "with rss", self.RSSURL, filterTime)
        # get the feed from url
        raw = feedparser.parse(self.RSSURL)
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
            self.__publishFeed(profileID, searchItem, post)

    def __publishFeed(self, profileID, searchItem, post):
        if 'hooks.slack' in self.webhookURL:  # slack webhook
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
        return self.webhookPublisher.publish(printable)
