// Q5 Funding overview: per agency, funded projects, amount, currency, and participating companies/utilities
MATCH (agency:FundingAgency)-[f:FUNDS]->(p:Project)
OPTIONAL MATCH (o:Organization)-[r:PARTICIPATES_IN]->(p)
  WHERE o:Company OR o:Utility
WITH agency, f, p, o, r ORDER BY o.name
WITH agency, f, p,
     [x IN collect(CASE WHEN o:Company THEN o.name + ' (' + r.role + ')' END) WHERE x IS NOT NULL] AS companies,
     [x IN collect(CASE WHEN o:Utility THEN o.name + ' (' + r.role + ')' END) WHERE x IS NOT NULL] AS utilities
RETURN agency.name AS funding_agency,
       p.name AS project,
       f.amount AS amount,
       f.currency AS currency,
       toString(f.start_year) + '-' + toString(f.end_year) AS period,
       companies,
       utilities
ORDER BY funding_agency, project
