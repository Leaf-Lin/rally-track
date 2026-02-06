# ESRally Track: RRF Benchmark

This track allows benchmarking Elasticsearch rrf query with randomized query inputs from a CSV file.
It uses custom param-source to select random query strings. The input contains two columns, text and vector which will be parsed into separate part of the rrf query.

## File Structure

```
.rally/benchmarks/tracks/search_template/
├── track.json            # Track definition
├── track.py              # ParamSource: RandomParamSource
├── queries.csv           # CSV file with one query per line
├── get_vector.sh         # Bash script to generate some random string and vector based on the index data. User should generate the queries.csv based on real search rather than this. It merely used for testing performance.
├── vector.json           # Raw Elasticsearch output from get_vector.sh. It can be useful as a starting point.
└── README.md             # This file
```
 - track.json: Defines the track, operations, and challenges.
 - track.py: Custom Python param source to supply randomized query strings.
 - queries.csv: Input dataset for random queries. Each row should contain a realistic query string, which can include multiple terms and a vector. Providing realistic queries helps simulate actual search workloads and produces more accurate benchmarking results.


## Requirements
-	Elasticsearch Rally￼installed on a load driver. This machine needs to have sufficient CPU to generate the load for large number of clients. 
-	The load driver needs to have access to the target Elasticsearch cluster and the monitoring cluster.


## Explanation of Options
-	`--track-path`: Path to the track folder
-	`--pipeline=benchmark-only`: Only runs the track operations, no system setup
-   `--target-hosts`: Elasticsearch hosts contains the target index and search template
-	`--client-options`: Connection options, including api_key and use_ssl
-	`--telemetry`: Collect node-level telemetry, defined in `.rally/rally.ini`
-	`--kill-running-processes`: Stop any previous Rally processes
-	`--user-tags`: Add custom tags to the run
-	`--track-params`: Override runtime parameters (`index` and `search_template`)
-	`--challenge`: Specify challenge schedule (e.g., `dryrun` or `real`)

## Running the Track

Example Command:
```
esrally race \
  --track-path=<path_to>/.rally/benchmarks/tracks/hybrid_query \
  --pipeline=benchmark-only \
  --target-hosts=<preprod_es_cluster_endpoint>:443 \
  --client-options="basic_auth_user:$user,basic_auth_password:$password,use_ssl:True" \
  --telemetry="node-stats" \
  --kill-running-processes \
  --user-tags="model:changeme" \
  --track-params="index:my_index" \
  --challenge="dryrun"
```

## Example queries.csv
```
text,vector
"apple banana orange","[0.040384497,0.0189368,...]"
```
