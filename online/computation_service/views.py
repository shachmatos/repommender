from django.http import HttpResponse
# from github import Github
# from github.Repository import Repository
# from online.settings import GITHUB_CONFIG
import json


def get_channels(user_id: int):
    # g = Github()
    # repos = g.get_repos()
    #
    # page = repos.get_page(0)
    # for repo in page: # type: Repository
    #     print(repo.get_topics())

    # TODO: get from DB


    return {
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


def fetch_recommendation_channels(request):
    # print(request.GET.get('access_token'))
    access_token = request.GET.get('access_token')
    user_id = request.GET.get('user_id')
    if user_id is None or access_token is None:
        return HttpResponse(None, status=400)

    channels = get_channels(user_id)
    return HttpResponse(str(json.dumps(channels)))
