import csv
import os
import json
import random


class QueryParamSource:
    def __init__(self, track, params, **kwargs):
        self._params = params
        self.infinite = True
        self.queries = []

        random.seed(4)  # predictable randomness

        cwd = os.path.dirname(__file__)
        csv_path = os.path.join(cwd, "queries.csv")

        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)   # <-- supports 2 columns
            for row in reader:
                text = row["text"]
                vector = json.loads(row["vector"])

                self.queries.append({
                    "text": text,
                    "vector": vector
                })

    def partition(self, partition_index, total_partitions):
        return self


class RandomParamSource(QueryParamSource):
    def params(self):
        q = random.choice(self.queries)

        text = q["text"]
        vec = q["vector"]

        result = {
            "index": self._params["index"],
            "body": {
                "size": 10,
                "retriever": {
                    "rrf": {
                        "retrievers": [
                            {
                                "standard": {
                                    "query": {
                                        "match": {
                                            "metadata.name": text
                                        }
                                    }
                                }
                            },
                            {
                                "knn": {
                                    "field": "face_embeddings",
                                    "query_vector": vec,
                                    "k": 10,
                                    "num_candidates": 100
                                }
                            }
                        ]
                    }
                }
            }
        }
        print("DEBUG:", json.dumps(result, indent=2))
        return result



def register(registry):
    registry.register_param_source("random_hybrid", RandomParamSource)
