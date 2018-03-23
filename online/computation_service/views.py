from django.http import HttpResponse
import json


def fetch_recommendation_channels(request, user_id):
    channels = {
        "user": user_id,
        "best": [
            {
                "name": "chinese-independent-developer",
                "url": "https://github.com/1c7/chinese-independent-developer",
                "tags": ["indie", "indie-developer", "china"],
            },
        ],
        "worst": [
            {
                "name": "driver.js",
                "url": "https://github.com/kamranahmedse/driver.js",
                "tags": ["tour", "walk-through", "user-onboarding"],
            },
        ],
    }
    return HttpResponse(str(json.dumps(channels)))
