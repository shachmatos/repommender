from django.http import HttpResponse
import json


def fetch_recommendation_channels(request, user_id):
    channels = {
        "user": user_id,
        "channels": [
            {
                'title': 'Some source',
                'repositories': [
                    {
                        "name": "chinese-independent-developer",
                        "url": "https://github.com/1c7/chinese-independent-developer",
                        "tags": ["indie", "indie-developer", "china"],
                    },
                    {
                        "name": "chinese-independent-developer 2",
                        "url": "https://github.com/1c7/chinese-independent-developer",
                        "tags": ["indie", "indie-developer", "china"],
                    },
                    {
                        "name": "chinese-independent-developer 3",
                        "url": "https://github.com/1c7/chinese-independent-developer",
                        "tags": ["indie", "indie-developer", "china"],
                    }
                ],
            },
            {
                'title': 'Some other source',
                'repositories': [
                    {
                        "name": "driver.js",
                        "url": "https://github.com/kamranahmedse/driver.js",
                        "tags": ["tour", "walk-through", "user-onboarding"],
                    }
                ],
            },
        ],
    }
    return HttpResponse(str(json.dumps(channels)))
