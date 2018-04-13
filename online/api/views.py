import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_access_token(request, code):
    post_data = {
        'code': code,
        'client_id': '9ab1a214485633eea22a',
        'client_secret': 'f4890d82d266677c43fbc2dc5aa26de9c2c31f67'
    }

    headers = {
        'Accept': 'application/json'
    }

    result = requests\
        .post('https://github.com/login/oauth/access_token',
              headers=headers
            ,data=post_data)
    return HttpResponse(result);