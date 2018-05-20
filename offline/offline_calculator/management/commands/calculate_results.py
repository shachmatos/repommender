from django.core.management import BaseCommand

import pandas as pd
import ast

from django.db import transaction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from offline_calculator.models import Recommendation, Repository, UserRepository, User
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):

        repos = Repository.objects.all()
        repositories_df = pd.DataFrame(list(repos.values()))
        repositories_df["topics"] = repositories_df["topics"].apply(ast.literal_eval)
        repositories_df["type"] = "repo"

        user_df = pd.DataFrame(list(User.objects.all().values()))
        user_repo_df = pd.DataFrame(list(UserRepository.objects.all().values()))

        intermediate_user_join = pd.merge(user_repo_df, repositories_df[["id", "topics"]], left_on="repo_id", right_on="id")
        user_vector_df = pd.DataFrame()
        user_vector_df[["id", "repo_id", "topics"]] = intermediate_user_join[["user_id", "repo_id", "topics"]]

        user_vector_df["repo_id"] = user_vector_df["repo_id"].apply(str)
        user_vector_df = user_vector_df.groupby('id', as_index=False).agg(
            {'topics': 'sum', 'repo_id': lambda x: ' '.join(x)})
        user_vector_df["type"] = "user"
        user_vector_df = pd.merge(user_vector_df, user_df[["id", "preferred_topics"]], on="id")

        user_vector_df["preferred_topics"] = user_vector_df["preferred_topics"].apply(lambda x: ast.literal_eval(x) if x is not None else [])
        user_vector_df["topics"] = user_vector_df["topics"] + user_vector_df["preferred_topics"]
        user_vector_df = user_vector_df.drop(columns=['preferred_topics', ])

        user_vector_df = user_vector_df.append({"id": "default", "topics": [], "repo_id": 0, "type": "user"},
                                               ignore_index=True)
        user_vector_df.at[user_vector_df.shape[0] - 1, "topics"] = user_vector_df["topics"].sum(axis=0)

        joined_vectors = pd.concat(
            [user_vector_df[["topics", "type", "id"]], repositories_df[["topics", "type", "id"]]], axis=0)
        joined_vectors["id"] = joined_vectors["type"] + joined_vectors["id"].apply(str)

        tf = TfidfVectorizer(
            analyzer='word',
            tokenizer=lambda x: x,
            preprocessor=lambda x: x,
            token_pattern=str(None))

        tfidf_matrix_repositories = tf.fit_transform(repositories_df['topics'])
        tfidf_matrix_joined_vectors = tf.fit_transform(joined_vectors['topics'])

        cosine_similarities_repo_repo = cosine_similarity(tfidf_matrix_repositories, tfidf_matrix_repositories)
        repo_results = {}
        for idx, row in tqdm(repositories_df.iterrows(), "Repo Results calculator"):
            similar_indices = cosine_similarities_repo_repo[idx].argsort()[:-12:-1]
            similar_items = [(cosine_similarities_repo_repo[idx][i], repositories_df['id'][i]) for i in similar_indices]
            repo_results[row['id']] = similar_items[1:]

        cosine_similarities_all_repo = cosine_similarity(tfidf_matrix_joined_vectors, tfidf_matrix_repositories)
        user_results = {}

        for idx, row in tqdm(joined_vectors.iterrows(), "User Results calculator"):
            similar_indices = cosine_similarities_all_repo[idx].argsort()[::-1]
            similar_items = [(cosine_similarities_all_repo[idx][i], repositories_df['id'][i]) for i in similar_indices]
            user_results[row['id']] = similar_items[:]

        user_results_with_int_keys = {}

        for k, v in list(user_results.items()):
            if "repo" in k:
                continue
            elif "default" in k:
                user_results_with_int_keys["default"] = user_results[k]
            else:
                user_results_with_int_keys[int(k.replace("user", ""))] = user_results[k]

        with transaction.atomic():
            r = []

            for user_repo in tqdm(UserRepository.objects.all()):  # type:UserRepository
                for repo_for_user in repo_results[user_repo.repo_id]:
                    score = repo_for_user[0]
                    for repo_score_by_user in user_results_with_int_keys[user_repo.user_id]:
                        if repo_for_user[1] == repo_score_by_user[1]:
                            score = repo_score_by_user[0]
                    r.append(
                        Recommendation(
                            user_id=user_repo.user_id,
                            source=user_repo.repo_id,
                            target_id=repo_for_user[1],
                            score=score,
                            channel_type='r'))

            for user_id, result_picks_for_you in user_results_with_int_keys.items():
                pick_for_you_count = 30
                for pick in result_picks_for_you:
                    if pick_for_you_count < 1:
                        break
                    pick_for_you_count -= 1

                    user_id_int = user_id
                    if user_id_int == "default":
                        user_id_int = 0
                        User.objects.update_or_create(id=0, login="default", avatar_url="")

                    r.append(
                        Recommendation(
                            user_id=user_id_int,
                            source=user_id_int,
                            target_id=pick[1],
                            score=pick[0],
                            channel_type='u'))

            cursor = connection.cursor()
            cursor.execute("TRUNCATE TABLE " + Recommendation._meta.db_table)

            Recommendation.objects.bulk_create(r)
