# Discoverires in to database partitioning

This project is created to test and benchmark database query performance on time series data with and without partitioning. Data is fetched from stackexchange and stored in a PostgreSQL database. The project includes scripts for loading data, creating partitions, and benchmarking query performance.

We're using CloudSQL for Postgres and it supports partitioning. The only downside is that it's single-node which is not the same as horizontal distribution. For that we'll need to migrate to AlloyDB instead, so this discovery is just to see if partitioning is enough to solve our performance problems.

## To run the project

### Activate and download lib
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install psycopg2-binary
```

### Download SE data
From https://archive.org/details/stackexchange

Download some of the 7Z files and extract them.


### Convert to csv
```
python3 parse_xml_csv.py ./askubuntu.com 
```

### Load to database
```
python3 load.py ./askubuntu.com
```

Sometimes load fails because of missing column, then just create a migration and run it:
```
psql -d samples -f migrations/001_add_badges_class.sql
```

Then run load again.