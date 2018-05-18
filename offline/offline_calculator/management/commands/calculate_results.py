from django.core.management import BaseCommand

import pandas as pd
import numpy as np
import ast

from django.db import transaction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from offline_calculator.models import Recommendation, Repository
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        repos = Repository.objects.all()
        repositories_df = pd.DataFrame(list(repos.values()))

        repositories_df["topics"] = repositories_df["topics"].apply(ast.literal_eval)
        tf = TfidfVectorizer(
            analyzer='word',
            tokenizer=lambda x: x,
            preprocessor=lambda x: x,
            token_pattern=str(None))

        tfidf_matrix = tf.fit_transform(repositories_df['topics'])
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
        results = {}
        for idx, row in tqdm(repositories_df.iterrows(), "Results calculator"):
            similar_indices = cosine_similarities[idx].argsort()[:-12:-1]

            similar_items = [(cosine_similarities[idx][i], repositories_df['id'][i]) for i in similar_indices]
            results[row['id']] = similar_items[1:]

        with transaction.atomic():
            r = []

            for source_id in tqdm(results.keys(), "Source"):
                for target_id in tqdm(results[source_id], "Target"):
                    r.append(Recommendation(source_id=int(source_id), target_id=int(target_id[1]), score=target_id[0]))
            cursor = connection.cursor()
            cursor.execute("TRUNCATE TABLE " + Recommendation._meta.db_table)

            Recommendation.objects.bulk_create(r)
