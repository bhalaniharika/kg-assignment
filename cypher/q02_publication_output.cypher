// Q2 Publication output: per project, publications with authors and their affiliation
// (affiliation = the organization the author belonged to in the publication year)
MATCH (proj:Project)<-[:RESULT_OF]-(pub:Publication)<-[a:AUTHORED]-(per:Person)
OPTIONAL MATCH (per)-[aff:AFFILIATED_WITH]->(org:Organization)
  WHERE aff.type IN ['employment', 'study']
    AND coalesce(aff.start_year, 0) <= pub.year
    AND coalesce(aff.end_year, 9999) >= pub.year
WITH proj, pub, a.position AS pos, per, collect(org.name) AS orgs
ORDER BY proj.name, pub.year, pub.title, pos
WITH proj, pub,
     collect(per.name + ' (' + reduce(s = '', o IN orgs | s + CASE WHEN s = '' THEN '' ELSE ', ' END + o) + ')') AS authors
RETURN proj.name AS project,
       pub.title AS publication,
       pub.year AS year,
       pub.venue AS venue,
       authors AS authors_with_affiliation
ORDER BY project, year, publication
