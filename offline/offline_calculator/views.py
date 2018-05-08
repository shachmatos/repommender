import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.db import transaction

from offline_calculator.models import Topic


@transaction.atomic
def test(request):
    f = open('/Users/yl/Downloads/topics.csv', 'r')
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
        topic = Topic.objects.get_or_create(name=row[0], display_name=row[1], short_description=row[2])
        if topic[1]:
            print('created: ', topic[0].name, topic[0].display_name, topic[0].short_description)

    return HttpResponse(1)