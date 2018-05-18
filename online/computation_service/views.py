import ast

from django.core import serializers
from django.db.models import QuerySet
from django.http import HttpResponse
# from github import Github
# from github.Repository import Repository
# from online.settings import GITHUB_CONFIG
import json

from github import Github

from computation_service.models import Recommendation, Repository, Topic


def get_channels(user_id: int, access_token: str):

    repo_ids = [
        989886,
        592533,
        1561299,
        1643158,
        45393000,
        132267704
    ]

    channels = []

    for repo_id in repo_ids:
        source_repo = Repository.objects.get(id=repo_id)
        source_repo_d = source_repo.__dict__
        source_repo_d.pop('_state')
        source_repo_d['pushed_at'] = str(source_repo_d['pushed_at'])
        source_repo_d['updated_at'] = str(source_repo_d['updated_at'])
        source_repo_d['topics'] = ast.literal_eval(source_repo_d['topics'])
        recommended = Recommendation.objects.filter(source=source_repo).all().prefetch_related('target')

        # serializers.serialize('json', source_repo.recommended.all())
        # similar_repos = []
        # for similar_id in similar_ids:
        #     # repo = g.get_repo(similar_id.target)
        #     repo = similar_id.target;
        #     similar_repos.append(repo)
        if recommended.count() > 0:
            channel_recs = []
            for rec in recommended:
                target = rec.target.__dict__;
                target.pop('_state')
                target['pushed_at'] = str(target['pushed_at'])
                target['updated_at'] = str(target['updated_at'])
                target['topics'] = ast.literal_eval(target['topics'])
                target['score'] = rec.score
                channel_recs.append(target)

            channels.append({
                'title': 'Because you\'re contributing to ' + source_repo.name,
                'source': source_repo_d,
                'repositories': channel_recs
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
