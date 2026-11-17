// Q9 Intellectual property to field: sites using technology covered by a Lumen patent,
// with the connected projects, operators and inventors
MATCH (lumen:Organization {name: 'Lumen Storage Systems'})-[:HOLDS]->(pat:Patent)
      -[:COVERS]->(tech:Technology)<-[:USES_TECHNOLOGY]-(site:Site)
RETURN site.name AS site,
       pat.id + ' - ' + pat.title AS patent,
       tech.name AS technology,
       EXISTS { (site)-[:IMPLEMENTS]->(pat) } AS built_to_patent_design,
       COLLECT { MATCH (proj:Project)-[:ESTABLISHED]->(site) RETURN proj.name } AS site_projects,
       COLLECT { MATCH (pat)-[:LICENSED_IN]->(lp:Project) RETURN lp.name } AS patent_licensed_in,
       COLLECT { MATCH (op:Organization)-[:OPERATES]->(site) RETURN op.name ORDER BY op.name } AS operators,
       COLLECT { MATCH (m:Person)-[:MANAGES]->(site) RETURN m.name } AS site_managers,
       COLLECT { MATCH (sup:Organization)-[:SUPPLIED_CELLS_TO]->(site) RETURN sup.name } AS cell_supplier,
       COLLECT { MATCH (inv:Person)-[:INVENTED]->(pat) RETURN inv.name ORDER BY inv.name } AS inventors
ORDER BY site
