from github import Github
from github.Repository import Repository


# def hydrate(ids=None):
#     pass


g = Github(client_id="9ab1a214485633eea22a", client_secret="f4890d82d266677c43fbc2dc5aa26de9c2c31f67")


print(g.get_api_status())

for repo in g.get_repos():  # type: Repository

    # print(repo.name)
    # print(repo.get_languages())
    print(repo.raw_data)
    # print(list(repo.get_labels()))
