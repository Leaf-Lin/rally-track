#!/bin/bash
### THIS IS AN EXAMPLE TO GENERATE SOME QUERY INPUT BASED ON INDEXED DATA
### GENERATE TWO COLUMNS: text and vector

curl -X GET -u $user -H "Content-Type: application/json" -d '{"size":2000,"_source":["face_embeddings","metadata.name"],"query":{"function_score":{"functions":[{"random_score":{}}],"query":{"match_all":{}}}}}' "https://$es_host/$index/_search" -o vector.json

echo 'text,vector' > queries.csv
cat vector.json | jq -rc '.hits.hits[] | [._source.metadata.name, (._source.face_embeddings | tojson )] | @csv' >> queries.csv

