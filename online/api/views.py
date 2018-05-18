import requests, json
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from github import Github

from computation_service.models import Topic, Language
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
        # TODO save user if needed

    return HttpResponse(res)


def get_topics(request):
    topics = Topic.objects.all()
    return HttpResponse(str(serializers.serialize('json', topics)))


def get_languages(request):
    langs = Language.objects.all()
    return HttpResponse(str(serializers.serialize('json', langs)))