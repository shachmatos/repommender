import csv
import errno
import time

from django.utils import dateparse
from django.utils.encoding import smart_bytes
from github import Github
from github.Repository import Repository as githubRepository
from github.NamedUser import NamedUser as githubNamedUser
from tqdm import tqdm, trange
from django.core.management import BaseCommand

from offline.settings import GITHUB_CONFIG, BASE_DIR
import os
from offline_calculator.models import Topic, Repository, User, UserRepository
from datetime import datetime, timedelta


def read_scanned_ids(path):
    f = open(path, 'r')
    result = set()
    reader = csv.reader(f)
    for row in reader:
        result.add(int(row))
    f.close()
    return result


def get_repositories(threshold, do_not_resume=False):
    g = Github(client_id=GITHUB_CONFIG['client_id'], client_secret=GITHUB_CONFIG['client_secret'])

    storage_path = BASE_DIR + '/storage/'
    scan_file_path = storage_path + 'scan.csv'
    start_time = time.time()
    complete = False
    last_topic = ''

    user_count_sample = 400

    if os.path.exists(scan_file_path):
        print('Scan already running')
        return

    if os.path.exists(storage_path + 'incomplete'):
        if do_not_resume:
            os.remove(storage_path + 'incomplete')
        else:
            with open(storage_path + 'incomplete', 'r') as resume:
                last_topic = resume.read()

    topics = Topic.objects.filter(**{'name__gte': last_topic}).all()

    try:
        for topic in tqdm(topics, desc='topics search'):
            last_topic = topic.name
            search_limit = g.get_rate_limit().search_rate

            if search_limit.remaining < 1:
                time.sleep(60)

            days_last_updated = datetime.now() - timedelta(days=180)

            repos = g.search_repositories('topic:' + topic.name + " pushed:>" + days_last_updated.strftime("%Y-%m-%d"))
            count = repos.totalCount * threshold
            top_n = repos[:round(count)]
            t = trange(round(count))
            t.set_description("repos")
            for repo in top_n:  # type: githubRepository
                limit = g.get_rate_limit().rate.remaining
                t.set_postfix_str('limit: ' + str(limit))
                while limit < 10:
                    print('Waiting for rate reset time...')
                    time.sleep(g.rate_limiting_resettime - time.time() + 10)
                    limit = g.get_rate_limit().rate.remaining

                Repository.objects.update_or_create(
                    defaults={
                        'id': repo.id,
                        'size': repo.size,
                        'name': repo.name,
                        'url': repo.html_url,
                        'topics': repo.get_topics(),
                        'languages': repo.get_languages(),
                        'watchers_count': repo.watchers_count,
                        'forks_count': repo.forks_count,
                        'open_issues': repo.open_issues,
                        'subscribers_count': repo.subscribers_count,
                        'pushed_at': dateparse.parse_datetime(str(repo.pushed_at)),
                        'updated_at': dateparse.parse_datetime(str(repo.updated_at)),
                        'image': repo.owner.avatar_url,
                        "description": smart_bytes(repo.description)
                    },
                    id=repo.id
                )

                for contributor in repo.get_contributors():  # type: githubNamedUser
                    if user_count_sample > 0:
                        User.objects.update_or_create(id=contributor.id, login=contributor.login, avatar_url=contributor.avatar_url)
                        user_count_sample -= 1
                    if User.objects.filter(id=contributor.id).exists():
                        UserRepository.objects.update_or_create(user_id=contributor.id, repo_id=repo.id)
                t.update()

        complete = True
    finally:
        end_time = time.time()
        print("Runtime: " + str(end_time - start_time) + 's')
        if complete:
            if os.path.exists(storage_path + 'incomplete'):
                os.remove(storage_path + 'incomplete')
        else:
            f = open(storage_path + 'incomplete', 'w')
            f.writelines(last_topic)
            f.close()


class Command(BaseCommand):
    help = 'Runs the github crawler and stores results'

    def add_arguments(self, parser):
        parser.add_argument('--threshold', dest='threshold', type=float)

    def handle(self, *args, **options):
        threshold = 0.05
        if options['threshold'] and 0 <= options['threshold'] <= 1:
            threshold = options['threshold']

        try:
            os.makedirs(BASE_DIR + '/storage')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        do_not_resume = False
        resume = ''
        if os.path.exists(BASE_DIR + '/storage/incomplete'):
            while resume not in ['y', 'Y', 'n', 'N']:
                resume = input('Previous scan detected. Resume? (y/n)')
                if resume == 'y' or resume == 'Y':
                    do_not_resume = False
                else:
                    do_not_resume = True
        get_repositories(threshold, do_not_resume)
