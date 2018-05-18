import csv
import errno
import time
from math import floor

from django.utils import dateparse
from github import Github
from github.Repository import Repository as githubRepository
from tqdm import tqdm, trange
from django.core.management import BaseCommand

from offline.settings import GITHUB_CONFIG, BASE_DIR
import os
from offline_calculator.models import Topic, Repository
from datetime import datetime, timedelta


def read_scanned_ids(path):
    f = open(path, 'r')
    result = set()
    reader = csv.reader(f)
    for row in reader:
        result.add(int(row))
    f.close()
    return result


def update_topics():
    g = Github(client_id=GITHUB_CONFIG['client_id'], client_secret=GITHUB_CONFIG['client_secret'])


def get_repositories(threshold, do_not_resume=False):
    g = Github(client_id=GITHUB_CONFIG['client_id'], client_secret=GITHUB_CONFIG['client_secret'])

    # repo_ids = set()
    # writer = None
    # topics_writer = None
    # repos_writer = None
    storage_path = BASE_DIR + '/storage/'
    scan_file_path = storage_path + 'scan.csv'
    topics_scanned_file = storage_path + 'topics.csv'
    repos_scanned_file = storage_path + 'repos.csv'
    starttime = time.time()
    # resumed = False
    complete = False
    result_name = storage_path + str(floor(starttime)) + '_repositories.csv'
    last_topic = ''

    if os.path.exists(scan_file_path):
        print('Scan already running')
        return

    # if os.path.exists(storage_path + 'scan_incomplete.csv'):
    if os.path.exists(storage_path + 'incomplete'):
        if do_not_resume:
            os.remove(storage_path + 'incomplete')
            # os.remove(storage_path + 'scan_incomplete.csv')
            # repo_file = open(scan_file_path, 'w')
            # topics_file = open(topics_scanned_file, 'w')
            # repo_ids_file = open(repos_scanned_file, 'w')
        else:
            with open(storage_path + 'incomplete', 'r') as resume:
                last_topic = resume.read()
                # print(last_topic)
                # exit(1)
            # resumed = True
            # repo_ids = read_scanned_ids(repos_scanned_file)
            # os.rename(storage_path + 'scan_incomplete.csv', scan_file_path)
            # repo_file = open(scan_file_path, 'a')
            # topics_file = open(topics_scanned_file, 'a')
            # repo_ids_file = open(repos_scanned_file, 'a')
    else:
        pass
        # repo_file = open(scan_file_path, 'w')
        # topics_file = open(topics_scanned_file, 'w')
        # repo_ids_file = open(repos_scanned_file, 'w')
    # print(1)
    # exit(1)

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
                    print('Wating for rate reset time...')
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
                        'forks_count':repo.forks_count,
                        'open_issues':repo.open_issues,
                        'subscribers_count':repo.subscribers_count,
                        'pushed_at': dateparse.parse_datetime(str(repo.pushed_at)),
                        'updated_at': dateparse.parse_datetime(str(repo.updated_at)),
                        'image': repo.owner.avatar_url,
                        "description": repo.description
                    },
                    id=repo.id
                    # size=repo.size,
                    # name=repo.name,
                    # url=repo.html_url,
                    # topics=repo.get_topics(),
                    # languages=repo.get_languages(),
                    # watchers_count=repo.watchers_count,
                    # forks_count=repo.forks_count,
                    # open_issues=repo.open_issues,
                    # subscribers_count=repo.subscribers_count,
                    # pushed_at=dateparse.parse_datetime(str(repo.pushed_at)),
                    # updated_at=dateparse.parse_datetime(str(repo.updated_at))
                )
                t.update()
                # time.sleep(3)
                # repo_dict = {
                #     "id": repo.id,
                #     "topics": repo.get_topics(),
                #     "url": repo.html_url,
                #     "name": repo.name,
                #     "updated_at": repo.updated_at,
                #     "pushed_at": repo.pushed_at,
                #     "size": repo.size,
                #     "watchers_count": repo.watchers_count,
                #     "forks_count": repo.forks_count,
                #     "open_issues": repo.open_issues,
                #     "subscribers_count": repo.subscribers_count,
                #     "languages": repo.get_languages()
                # }
                # if writer is None:
                #     fields = list(repo_dict.keys())
                #     writer = csv.DictWriter(repo_file, fields)
                #     if not resumed:
                #         writer.writeheader()
                #
                # if repos_writer is None:
                #     repos_writer = csv.writer(repo_ids_file)
                #
                # if topics_writer is None:
                #     topics_writer = csv.writer(topics_file)

                # if repo.id not in repo_ids:
                    # writer.writerow(repo_dict)
                    # repo_ids.add(repo.id)
                    # repos_writer.writerow([repo.id])
                    # time.sleep(3)
            # topics_writer.writerow(topic)
        complete = True
    finally:
        endtime = time.time()
        print("Runtime: " + str(endtime - starttime) + 's')
        # repo_file.close()
        # topics_file.close()
        # repo_ids_file.close()
        if complete:
            if os.path.exists(storage_path + 'incomplete'):
                os.remove(storage_path + 'incomplete')
            # os.remove(topics_scanned_file)
            # os.remove(repos_scanned_file)
        else:
            f = open(storage_path + 'incomplete', 'w')
            f.writelines(last_topic)
            f.close()
            result_name = storage_path + 'scan_incomplete.csv'
        # os.rename(scan_file_path, result_name)


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
        # if os.path.exists(BASE_DIR + '/storage/scan_incomplete.csv'):
        #     while resume not in ['y', 'Y', 'n', 'N']:
        #         resume = input('Previous scan detected. Resume? (y/n)')
        #         if resume == 'y' or resume == 'Y':
        #             do_not_resume = False
        #         else:
        #             do_not_resume = True
        if os.path.exists(BASE_DIR + '/storage/incomplete'):
            while resume not in ['y', 'Y', 'n', 'N']:
                resume = input('Previous scan detected. Resume? (y/n)')
                if resume == 'y' or resume == 'Y':
                    do_not_resume = False
                else:
                    do_not_resume = True
        get_repositories(threshold, do_not_resume)
