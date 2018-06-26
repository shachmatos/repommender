from django.core.management import BaseCommand

import pandas as pd
import ast
import numpy as np

from django.db import transaction
from django.db.models import Avg, Count, Min, Sum
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from offline_calculator.models import Recommendation, Repository, UserRepository, User
from django.db import connection


def get_color_vec(color_vec, max_val, min_val):
    return [min(min_val + i / max_val, max_val) for i in color_vec]


class Command(BaseCommand):
    def handle(self, *args, **options):

        # if there are not users or repositories in the system then there is no need for recommendations
        if Repository.objects.all().count() == 0 or User.objects.all().count() == 0:
            return

        repos = Repository.objects.all()
        repositories_df = pd.DataFrame(list(repos.values()))
        repositories_df["topics"] = repositories_df["topics"].apply(ast.literal_eval)
        repositories_df["type"] = "repo"

        u = User.objects.annotate(repo_count=Count('userrepository'))
        user_df = pd.DataFrame(list(u.values()))
        user_repo_df = pd.DataFrame(list(UserRepository.objects.all().values()))

        # merging with repo_db to get all topics for each user-repo relation
        intermediate_user_join = pd.merge(user_repo_df, repositories_df[["id", "topics"]], left_on="repo_id",
                                          right_on="id")
        user_vector_df = pd.DataFrame()
        # extracting the relevant fields only
        user_vector_df[["id", "repo_id", "topics"]] = intermediate_user_join[["user_id", "repo_id", "topics"]]

        # turning it into string and the concatenating it - for debugging (enables to see the source of the topics)
        user_vector_df["repo_id"] = user_vector_df["repo_id"].apply(str)

        # grouping by user-id to combine all topics to a single row (user, bag_of_topics)
        user_vector_df = user_vector_df.groupby('id', as_index=False).agg(
            {'topics': 'sum', 'repo_id': lambda x: ' '.join(x)})

        # this is for differentiating the users from repos - they go into the same space
        user_vector_df["type"] = "user"
        user_vector_df = pd.merge(user_vector_df, user_df[["id", "preferred_topics", "repo_count"]], on="id")
        user_vector_df["preferred_topics_multiplier"] = user_vector_df["repo_count"].apply(lambda x: max(int(np.log2(x)), 1))

        # dealing with None values in preferred topics
        user_vector_df["preferred_topics"] = user_vector_df["preferred_topics"].apply(
            lambda x: ast.literal_eval(x) if x is not None else [])
        user_vector_df["topics"] = user_vector_df["topics"] + \
                                   (user_vector_df["preferred_topics"] * user_vector_df["preferred_topics_multiplier"])

        # removing the preferred_topics - after adding it into topics
        user_vector_df = user_vector_df.drop(columns=['preferred_topics', ])

        # adding a default user, this is an average of all other users (for cold start)
        user_vector_df = user_vector_df.append({"id": "default", "topics": [], "repo_id": 0, "type": "user"},
                                               ignore_index=True)
        user_vector_df.at[user_vector_df.shape[0] - 1, "topics"] = user_vector_df["topics"].sum(axis=0)

        # mixing users and repos into same vector space
        joined_vectors = pd.concat(
            [user_vector_df[["topics", "type", "id"]], repositories_df[["topics", "type", "id"]]], axis=0)
        joined_vectors["id"] = joined_vectors["type"] + joined_vectors["id"].apply(str)

        tf = TfidfVectorizer(
            analyzer='word',
            tokenizer=lambda x: x,
            preprocessor=lambda x: x,
            token_pattern=str(None))

        # one matrix for repositories_df
        tfidf_matrix_repositories = tf.fit_transform(repositories_df['topics'])
        # another matrix for mixed matrix
        tfidf_matrix_joined_vectors = tf.fit_transform(joined_vectors['topics'])

        # this batch calculates repo-repo tf-idf similarities
        cosine_similarities_repo_repo = cosine_similarity(tfidf_matrix_repositories, tfidf_matrix_repositories)
        repo_results = {}
        for idx, row in tqdm(repositories_df.iterrows(), "Repo Results calculator"):
            # get the best 10 score indexes (most similar)
            similar_indices = cosine_similarities_repo_repo[idx].argsort()[:-12:-1]
            # fet the items + score based on the indexes
            similar_items = [(cosine_similarities_repo_repo[idx][i], repositories_df['id'][i]) for i in similar_indices]
            repo_results[row['id']] = similar_items[1:]

        cosine_similarities_all_repo = cosine_similarity(tfidf_matrix_joined_vectors, tfidf_matrix_repositories)
        user_results = {}

        # this batch calculates mixed-repo tf-idf similarities
        for idx, row in tqdm(joined_vectors.iterrows(), "User Results calculator"):
            # normalizing similarities
            cosine_similarities_all_repo[idx] = get_color_vec(cosine_similarities_all_repo[idx], 1, 0.5)
            # similar calculation to the done in repo-repo
            similar_indices = cosine_similarities_all_repo[idx].argsort()[::-1]
            similar_items = [(cosine_similarities_all_repo[idx][i], repositories_df['id'][i]) for i in similar_indices]
            user_results[row['id']] = similar_items[:]

        user_results_with_int_keys = {}

        # removing all results which are non user-repo (they are repo-repo)
        for k, v in list(user_results.items()):
            if "repo" in k:
                continue
            elif "default" in k:
                user_results_with_int_keys[0] = user_results[k]
            else:
                user_results_with_int_keys[int(k.replace("user", ""))] = user_results[k]

        with transaction.atomic():
            result_picks_for_you = user_results_with_int_keys[0]
            User.objects.update_or_create(id=0, login="default", avatar_url="")
            # this part generates relation between the default user and each item of the top 30 picks
            pick_for_you_count = 30
            for pick in result_picks_for_you:
                if pick_for_you_count < 1:
                    break
                pick_for_you_count -= 1
                UserRepository.objects.update_or_create(user_id=0, repo_id=pick[1])

            r = []
            # for each user-repo relation create a recommendation for the repo recommendations
            # these are repo-repo recommendations with th user-repo score
            for user_repo in tqdm(UserRepository.objects.all()):  # type:UserRepository
                for repo_for_user in repo_results[user_repo.repo_id]:
                    # the default score is the one of the repo-repo
                    score = repo_for_user[0]
                    for repo_score_by_user in user_results_with_int_keys[user_repo.user_id]:
                        # take the score (similarity) of the user-repo
                        if repo_for_user[1] == repo_score_by_user[1]:
                            score = repo_score_by_user[0]
                    r.append(
                        Recommendation(
                            user_id=user_repo.user_id,
                            source=user_repo.repo_id,
                            target_id=repo_for_user[1],
                            score=score,
                            channel_type='r'))

            # for each user - get the top picks based on the user vector
            for user_id, result_picks_for_you in user_results_with_int_keys.items():
                # how many items to get in top picks for you
                pick_for_you_count = 30
                for pick in result_picks_for_you:
                    if pick_for_you_count < 1:
                        break
                    pick_for_you_count -= 1

                    r.append(
                        Recommendation(
                            user_id=user_id,
                            source=user_id,
                            target_id=pick[1],
                            score=pick[0],
                            channel_type='u'))

            cursor = connection.cursor()
            # clear recommendation DB to put new results
            cursor.execute("TRUNCATE TABLE " + Recommendation._meta.db_table)

            Recommendation.objects.bulk_create(r)
