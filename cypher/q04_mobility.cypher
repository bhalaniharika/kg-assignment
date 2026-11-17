// Q4 Mobility: researchers affiliated (employment or study) with more than one organization,
// and the direction of each move (sector and country, earlier -> later)
MATCH (p:Person)-[a:AFFILIATED_WITH]->(o:Organization)-[:LOCATED_IN]->(c:Country)
WHERE a.type IN ['employment', 'study']
WITH p, a, o, c
ORDER BY a.current, coalesce(a.start_year, a.end_year)
WITH p, collect({org: o.name, type: a.type, position: a.position, start: a.start_year, end: a.end_year,
                 country: c.name,
                 sector: CASE WHEN o:Company THEN 'industry' WHEN o:Utility THEN 'utility' ELSE 'academia' END}) AS hist
WHERE size(hist) > 1
UNWIND range(0, size(hist) - 2) AS i
WITH p, hist[i] AS f, hist[i + 1] AS t
RETURN p.name AS researcher,
       f.org + ' (' + f.type + ', ' + f.position + ')' AS moved_from,
       t.org + ' (' + t.type + ', ' + t.position + ')' AS moved_to,
       coalesce(t.start, f.end) AS year_of_move,
       f.sector + ' -> ' + t.sector AS sector_direction,
       f.country + ' -> ' + t.country AS geographic_direction
ORDER BY year_of_move, researcher
