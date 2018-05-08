from github.GithubException import GithubException
from github.Repository import Repository
import csv
import http.client
import requests
import json
import importlib
import github
import time

from github import Github
from github import AuthenticatedUser

g = Github(client_id="9ab1a214485633eea22a", client_secret="f4890d82d266677c43fbc2dc5aa26de9c2c31f67")

print(g.get_api_status())

# amount = 2
# cols = ["id", "name", "labels", "languages"]
#
#
# with open('data5.csv', 'w', newline='', encoding="utf-8") as f:
#     writer = None
#     for repo in g.get_repos():  # type: Repository
#         try:
#             row = repo.raw_data
#             if writer is None:
#                 writer = csv.DictWriter(f, row.keys())
#                 writer.writeheader()
#             # row = {"id": repo.id, "name": repo.name, "labels": [x.name for x in repo.get_labels()],
#             #        "languages": list(repo.get_languages())}
#             writer.writerow(row)
#         except GithubException:
#             continue
#
#         amount -= 1
#         if 0 == amount:
#             break

# for i, repo in enumerate(g.search_repositories("topic:wordplate")):  # type: Repository
#     print(repo.name)
#     # print(repo.raw_data)
#
#     print(repo.get_topics())
#     if i == 2:
#         break
#
#
# url = "https://api.github.com/search/topics"
#
# querystring = {"q": "is:curated"}
#
# headers = {
#     'client_id': "9ab1a214485633eea22a",
#     'client_secret': "f4890d82d266677c43fbc2dc5aa26de9c2c31f67",
#     'Accept': "application/vnd.github.mercy-preview+json",
#     'Cache-Control': "no-cache",
#     'Postman-Token': "6d709c8b-1770-42f1-aaf2-c32b11e25d76"
#     }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
# link = response.headers["Link"]
# # print(response.text)
# response_dict = json.loads(response.text)
# print(link)
# # print(response_dict)

threshold = 0.1
topics = []
repository_ids = set()
repo_dict = {}

with open('topics.csv', 'r', newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        topics.append(row["name"])

with open('repositories10.csv', 'w', newline='', encoding="utf-8") as repo_f:
    writer = None
    for topic in topics:
        repo_result = g.search_repositories("topic:" + topic)
        how_many = repo_result.totalCount * threshold
        for i, repo in enumerate(repo_result):
            repo_dict = {"id": repo.id, "topics": repo.get_topics()["names"], "name": repo.name,
                         "updated_at": repo.updated_at, "pushed_at": repo.pushed_at, "size": repo.size,
                         "watchers_count": repo.watchers_count, "forks_count": repo.forks_count,
                         "open_issues": repo.open_issues, "subscribers_count": repo.subscribers_count,
                         "languages": repo.get_languages()}
            if writer is None:
                fields = list(repo_dict.keys())
                writer = csv.DictWriter(repo_f, fields)
                writer.writeheader()
            if i >= how_many:
                break
            print("topic: ", topic, ", ", i, "/", how_many, " left", ", repo_name: ", repo.name)
            if repo.id not in repository_ids:
                repository_ids.add(repo.id)
                writer.writerow(repo_dict)
                time.sleep(10)
                # repo_f.close()
