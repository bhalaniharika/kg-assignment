// Q7 Citation influence: publications citing the 2022 cathode stability paper, directly or transitively
MATCH (target:Publication {year: 2022})
WHERE toLower(target.title) CONTAINS 'cathode stability'
MATCH path = (citing:Publication)-[:CITES*1..]->(target)
WITH citing, path ORDER BY length(path)
WITH citing, collect(path)[0] AS shortest
RETURN citing.title AS citing_publication,
       citing.year AS year,
       length(shortest) AS citation_depth,
       CASE length(shortest) WHEN 1 THEN 'direct' ELSE 'indirect' END AS citation_type,
       reduce(s = head(nodes(shortest)).title, n IN tail(nodes(shortest)) | s + ' -> ' + n.title) AS citation_chain
ORDER BY citation_depth, year, citing_publication
