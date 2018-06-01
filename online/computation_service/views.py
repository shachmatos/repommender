import ast


from django.http import HttpResponse
import json

from computation_service.models import *


def get_channels(user_id: int):
    repo_ids = [1]

    # for recommendation in Recommendation.objects.filter(user_id=0):
    #     repo_ids.append(recommendation.target.id)

    channels = []

    for repo_id in repo_ids:
        # source_repo = Repository.objects.get(id=repo_id)
        # source_repo_d = source_repo.__dict__
        # source_repo_d.pop('_state')
        # source_repo_d['pushed_at'] = str(source_repo_d['pushed_at'])
        # source_repo_d['updated_at'] = str(source_repo_d['updated_at'])
        # source_repo_d['topics'] = ast.literal_eval(source_repo_d['topics'])
        recommended = Recommendation.objects.filter(user_id=0).all().prefetch_related('target')

        if recommended.count() > 0:
            channel_recs = []
            for rec in recommended:
                target = rec.target.__dict__
                # if target["id"] == 43278409:
                #     pass
                target.pop('_state')
                target['pushed_at'] = str(target['pushed_at'])
                target['updated_at'] = str(target['updated_at'])
                target['topics'] = ast.literal_eval(target['topics'])
                target['score'] = rec.score
                channel_recs.append(target)

            channels.append({
                'title': "Top picks for you",
                'source': "Top picks for you",
                'repositories': channel_recs
            })

    return {
        "user": user_id,
        "channels": channels
    }


def fetch_recommendation_channels(request):
    access_token = request.GET.get('access_token')
    user_id = request.GET.get('user_id')
    if user_id is None or access_token is None:
        return HttpResponse(None, status=400)

    channels = get_channels(user_id)
    return HttpResponse(str(json.dumps(channels)))
