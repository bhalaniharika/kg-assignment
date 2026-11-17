// Q6 International reach: rank researchers by number of distinct co-author countries,
// excluding the researcher's own country (countries come from current affiliations)
MATCH (r:Person)-[:AUTHORED]->(:Publication)
WITH DISTINCT r
MATCH (r)-[:AFFILIATED_WITH {current: true}]->(:Organization)-[:LOCATED_IN]->(home:Country)
WITH r, collect(DISTINCT home) AS homes
OPTIONAL MATCH (r)-[:AUTHORED]->(:Publication)<-[:AUTHORED]-(co:Person)
               -[:AFFILIATED_WITH {current: true}]->(:Organization)-[:LOCATED_IN]->(c:Country)
WHERE NOT c IN homes
WITH r, homes, collect(DISTINCT c.name) AS foreign_countries
RETURN r.name AS researcher,
       [h IN homes | h.name] AS own_country,
       size(foreign_countries) AS distinct_foreign_coauthor_countries,
       foreign_countries
ORDER BY distinct_foreign_coauthor_countries DESC, researcher
