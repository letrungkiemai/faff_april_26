votes table has 30M rows

### BEFORE PARTITIONING AND INDEXING

#### On query across 1 year span
```
explain analyze 
select * from votes ph
where ph.creation_date between '2020-01-01' and '2020-12-31'
```

```
QUERY PLAN                                                                                                                                                       |
-----------------------------------------------------------------------------------------------------------------------------------------------------------------+
Gather  (cost=1000.00..545048.18 rows=1311414 width=38) (actual time=0.333..260.589 rows=1354371.00 loops=1)                                                     |
  Workers Planned: 2                                                                                                                                             |
  Workers Launched: 2                                                                                                                                            |
  Buffers: shared hit=4733 read=218877                                                                                                                           |
  ->  Parallel Seq Scan on votes ph  (cost=0.00..412906.78 rows=546422 width=38) (actual time=0.155..246.558 rows=451457.00 loops=3)                             |
        Filter: ((creation_date >= '2020-01-01 00:00:00'::timestamp without time zone) AND (creation_date <= '2020-12-31 00:00:00'::timestamp without time zone))|
        Rows Removed by Filter: 9648543                                                                                                                          |
        Buffers: shared hit=4733 read=218877                                                                                                                     |
Planning Time: 0.096 ms                                                                                                                                          |
Execution Time: 286.246 ms                                                                                                                                       |

```

Execution time increases as the time span increase, to max of 1373.625 


### AFTER Indexing the creation_date column

It took ~5s to create the index
```
create index votes_idx on votes (creation_date)
```

After indexing, execution time on querying on the entire span of time in the dataset does not change much, still about 1300ms.

The same query
```
explain analyze 
select * from votes ph
where ph.creation_date between '2020-01-01' and '2020-12-31'
```
takes 327ms.

Although the shorter the timespan, the faster the query is. So between '2020-01-01' and '2020-01-03' it takes 23ms.


### AFTER Partitioning by creation_date (by year)

The biggest perf gain is from querying within the same year. So querying `where ph.creation_date between '2020-01-01' and '2020-12-31'` now takes only 12ms, instead of ~300ms like before.

On 2 years span there is still some performance gain. This seems to be the case within several year's span.

But on multiple years span it looks like there's no perf difference between partitioned and non-partitioned table.

Performance on the partitioned table is worse if performing scan on all partitions.

## Conclusion
1. For shorter timespan, indexing the creation_date column is enough for performance gain.

2. For longer timespan (within a couple of years), partitioning can give a slight performance gain.

3. For a timespan that covers the entire dataset, there is no difference in performance between indexing and not indexing. Perf on the partitioned dataset in this case is the worst.



