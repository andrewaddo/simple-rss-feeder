from httplib2 import Http

POST_HEADERS = {'Content-Type': 'application/json; charset=UTF-8'}


class WebhookPublisher:

    def __init__(self, webhookURL):
        self.webhookURL = webhookURL
        print("")

    def setWebhookURL(self, webhookURL):
        self.webhookURL = webhookURL

    def publish(self, content):
        http_obj = Http()

        response = http_obj.request(
            uri=self.webhookURL,
            method='POST',
            headers=POST_HEADERS,
            body=content.encode('utf-8'),
            #!IMPORTANT: default Latin-1 would fail on certain special characters
        )
        if response[0].status == 200:
            print("Published to webhook")
        else:
            print("Error publishing to webhook", response)
        return response[0].status
