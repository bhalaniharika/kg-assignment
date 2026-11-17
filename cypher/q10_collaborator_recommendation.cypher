// Q10 Collaborator recommendation: researcher pairs who never co-authored, share >= 1 common
// co-author, and have published on the same technology area
MATCH (a:Person)-[:AUTHORED]->(:Publication)<-[:AUTHORED]-(common:Person)
      -[:AUTHORED]->(:Publication)<-[:AUTHORED]-(b:Person)
WHERE a.name < b.name
  AND NOT EXISTS { (a)-[:AUTHORED]->(:Publication)<-[:AUTHORED]-(b) }
WITH a, b, collect(DISTINCT common.name) AS common_coauthors
MATCH (a)-[:AUTHORED]->(:Publication)-[:ABOUT]->(t:Technology)<-[:ABOUT]-(:Publication)<-[:AUTHORED]-(b)
WITH a, b, common_coauthors, collect(DISTINCT t.name) AS shared_technology
RETURN a.name AS researcher_1,
       b.name AS researcher_2,
       common_coauthors,
       shared_technology,
       size(common_coauthors) + size(shared_technology) AS score
ORDER BY score DESC, researcher_1, researcher_2
