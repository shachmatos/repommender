from django.http import HttpResponse
from django.utils.encoding import smart_text

import ast
import json

from computation_service.models import *


def get_channels(user_id: int):
    channel_picks_for_you = []
    channels = []
    repo_seed_ids = set()

    if not Recommendation.objects.filter(user_id=user_id).exists():
        return get_channels(0)

    for recommendation in Recommendation.objects.filter(user_id=user_id, channel_type='r'):
        repo_seed_ids.add(recommendation.source)

    for repo_id in repo_seed_ids:
        source_repo = Repository.objects.get(id=repo_id)
        source_repo_d = source_repo.__dict__
        source_repo_d.pop('_state')
        source_repo_d['pushed_at'] = str(source_repo_d['pushed_at'])
        source_repo_d['updated_at'] = str(source_repo_d['updated_at'])
        source_repo_d['topics'] = ast.literal_eval(source_repo_d['topics'])
        recommended = Recommendation.objects.filter(user_id=user_id, source=repo_id).all().prefetch_related('target')

        if recommended.count() > 0:
            channel_recs = []
            for recommendation in recommended:
                channel_recs.append(format_repo_to_json(recommendation.target.__dict__, recommendation.score))

            channels.append({
                'title': 'Because you\'re contributing to ' + source_repo.name,
                'source': source_repo_d,
                'repositories': channel_recs
            })

    picks_for_you = []
    for recommendation in Recommendation.objects.filter(user_id=user_id, channel_type='u'):
        picks_for_you.append(format_repo_to_json(recommendation.target.__dict__, recommendation.score))

    channel_picks_for_you.append({
        'repositories': picks_for_you
    })

    return {
        "user": user_id,
        "picks_for_you": channel_picks_for_you,
        "channels": channels
    }


def format_repo_to_json(repo, score):
    repo.pop('_state')
    repo['pushed_at'] = str(repo['pushed_at'])
    repo['updated_at'] = str(repo['updated_at'])
    repo['topics'] = ast.literal_eval(repo['topics'])
    repo['languages'] = ast.literal_eval(repo['languages'])
    repo['score'] = score
    repo['description'] = smart_text(repo['description'])
    return repo


def fetch_recommendation_channels(request):
    access_token = request.GET.get('access_token')
    user_id = request.GET.get('user_id')
    if user_id is None or access_token is None:
        return HttpResponse(None, status=400)

    channels = get_channels(user_id)
    return HttpResponse(str(json.dumps(channels)))
