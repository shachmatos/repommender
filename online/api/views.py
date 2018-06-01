import ast

import requests, json
from django.core import serializers
from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from github import Github

from computation_service.models import Topic, Language, User
from online.settings import GITHUB_CONFIG


@csrf_exempt
def get_access_token(request, code):
    post_data = {
        'code': code,
        'client_id':  GITHUB_CONFIG['client_id'],
        'client_secret': GITHUB_CONFIG['client_secret']
    }

    headers = {
        'Accept': 'application/json'
    }

    res = requests\
        .post('https://github.com/login/oauth/access_token',
              headers=headers
            ,data=post_data)

    token = json.loads(res.content)

    if res.status_code == 200 and 'access_token' in token.keys():
        g = Github(token['access_token'])
        github_user = g.get_user()
        User.objects.update_or_create(defaults={
            'id': github_user.id,
            'login': github_user.login,
            'avatar_url': github_user.avatar_url
        }, id=github_user.id)

    return HttpResponse(res)


def get_topics(request):
    topics = Topic.objects.all()
    return HttpResponse(str(serializers.serialize('json', topics)))


def get_languages(request):
    langs = Language.objects.all()
    return HttpResponse(str(serializers.serialize('json', langs)))


def get_user_preferences(request, user_id):
    user = User.objects.get(id=user_id)
    user_topics = ast.literal_eval(user.preferred_topics)
    result = {
        'topics': user_topics,
    }
    return HttpResponse(str(json.dumps(result)))


@csrf_exempt
def save_user_preferences(request, user_id):
    data = json.loads(request.body)
    user = User.objects.get(id=user_id)
    user.preferred_topics = data['topics']
    print(user.preferred_topics)
    user.save()

    return HttpResponse()

