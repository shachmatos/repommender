import csv
import errno
import time
from math import floor

from github import Github
from tqdm import tqdm
from django.core.management import BaseCommand

from offline.settings import GITHUB_CONFIG, BASE_DIR
import os
from offline_calculator.models import Topic


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
    topics = Topic.objects.all()
    repo_ids = set()
    writer = None
    topics_writer = None
    repos_writer = None
    storage_path = BASE_DIR + '/storage/'
    scan_file_path = storage_path + 'scan.csv'
    topics_scanned_file = storage_path + 'topics.csv'
    repos_scanned_file = storage_path + 'repos.csv'
    starttime = time.time()
    resumed = False
    complete = False
    result_name = storage_path + str(floor(starttime)) + '_repositories.csv'

    if os.path.exists(scan_file_path):
        print('Scan already running')
        return

    if os.path.exists(storage_path + 'scan_incomplete.csv'):
        if do_not_resume:
            os.remove(storage_path + 'scan_incomplete.csv')
            repo_file = open(scan_file_path, 'w')
            topics_file = open(topics_scanned_file, 'w')
            repo_ids_file = open(repos_scanned_file, 'w')
        else:
            resumed = True
            repo_ids = read_scanned_ids(repos_scanned_file)
            os.rename(storage_path + 'scan_incomplete.csv', scan_file_path)
            repo_file = open(scan_file_path, 'a')
            topics_file = open(topics_scanned_file, 'a')
            repo_ids_file = open(repos_scanned_file, 'a')
    else:
        repo_file = open(scan_file_path, 'w')
        topics_file = open(topics_scanned_file, 'w')
        repo_ids_file = open(repos_scanned_file, 'w')
    try:
        for topic in tqdm(topics, desc='topics'):
            repos = g.search_repositories('topic:' + topic.name)
            count = repos.totalCount * threshold

            top_n = list(repos[:count])

            for repo in tqdm(top_n, desc='repositories'):
                repo_dict = {
                    "id": repo.id,
                    "topics": repo.get_topics(),
                    "name": repo.name,
                    "updated_at": repo.updated_at,
                    "pushed_at": repo.pushed_at,
                    "size": repo.size,
                    "watchers_count": repo.watchers_count,
                    "forks_count": repo.forks_count,
                    "open_issues": repo.open_issues,
                    "subscribers_count": repo.subscribers_count,
                    "languages": repo.get_languages()
                }
                if writer is None:
                    fields = list(repo_dict.keys())
                    writer = csv.DictWriter(repo_file, fields)
                    if not resumed:
                        writer.writeheader()

                if repos_writer is None:
                    repos_writer = csv.writer(repo_ids_file)

                if topics_writer is None:
                    topics_writer = csv.writer(topics_file)

                if repo.id not in repo_ids:
                    writer.writerow(repo_dict)
                    repo_ids.add(repo.id)
                    repos_writer.writerow([repo.id])
                    time.sleep(3)
            topics_writer.writerow(topic)
        complete = True
    except Exception as e:
        print(e)
    finally:
        endtime = time.time()
        print("Runtime: " + str(endtime - starttime) + 's')
        repo_file.close()
        topics_file.close()
        repo_ids_file.close()
        if complete:
            os.remove(topics_scanned_file)
            os.remove(repos_scanned_file)
        else:
            result_name = storage_path + 'scan_incomplete.csv'
        os.rename(scan_file_path, result_name)


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
        if os.path.exists(BASE_DIR + '/storage/scan_incomplete.csv'):
            while resume not in ['y', 'Y', 'n', 'N']:
                resume = input('Previous scan detected. Resume? (y/n)')
                if resume == 'y' or resume == 'Y':
                    do_not_resume = False
                else:
                    do_not_resume = True
        get_repositories(threshold, do_not_resume)
