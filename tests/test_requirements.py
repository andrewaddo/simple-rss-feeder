from json import dumps
import simpleRSSFeeder
from simpleRSSFeeder import webhookPublisher, getRSSFeed
import os

# DEV webhook for testing
# TODO is there throttling to prevent spam?
WEBHOOK = "https://chat.googleapis.com/v1/spaces/AAAAZjRiWtQ/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=iRwqG6II2ivcnSz6VV_CldAFVBXe2_x_CtVByTTZrag%3D"

def test_publisher_invalidURL():
    web = webhookPublisher.WebhookPublisher(WEBHOOK)
    content = {
        'text': 'Hello from a Python script!'}
    responseStatus = web.publish(dumps(content))
    print("response status code", responseStatus)
    assert responseStatus == 301


def test_getRSSFeed():
    os.environ['rssURL'] = 'https://cloudblog.withgoogle.com/rss/'
    os.environ['webhook'] = WEBHOOK
    getRSSFeed.getRSSFeed(event={}, context={})
    print("end")
