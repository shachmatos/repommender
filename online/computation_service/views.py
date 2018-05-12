from django.http import HttpResponse
# from github import Github
# from github.Repository import Repository
# from online.settings import GITHUB_CONFIG
import json

from github import Github

from computation_service.models import Recommendation


def get_channels(user_id: int, access_token: str):
    g = Github(login_or_token=access_token)

    # repos = g.get_repos()
    #
    # page = repos.get_page(0)
    # for repo in page: # type: Repository
    #     print(repo.get_topics())

    repo_ids = [
        277297,

    ]

    channels = []

    for id in repo_ids:
        source_repo = g.get_repo(id)
        similar_ids = Recommendation.objects.filter(source=id).all()
        similar_repos = []
        for similar_id in similar_ids:
            repo = g.get_repo(similar_id.target)
            similar_repos.append({
                'name': repo.name,
                'url': repo.html_url,
                'topics': repo.get_topics()
            })

        channels.append({
            'title': 'Because you\'re contributing to ' + source_repo.name,
            'repositories': similar_repos
        })


    return {
        "user": user_id,
        "channels": channels
    }


def fetch_recommendation_channels(request):
    # print(request.GET.get('access_token'))
    access_token = request.GET.get('access_token')
    user_id = request.GET.get('user_id')
    if user_id is None or access_token is None:
        return HttpResponse(None, status=400)

    channels = get_channels(user_id, access_token)
    return HttpResponse(str(json.dumps(channels)))
