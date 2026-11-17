// Q1 Consortium roles: organizations in ALPINE, their role, and the funding agency
MATCH (p:Project {name: 'ALPINE'})<-[r:PARTICIPATES_IN]-(o:Organization)
OPTIONAL MATCH (agency:FundingAgency)-[f:FUNDS]->(p)
RETURN o.name AS organization,
       [l IN labels(o) WHERE l <> 'Organization'][0] AS org_type,
       r.role AS role,
       r.contribution AS contribution,
       agency.name AS funded_by,
       f.amount AS grant_amount,
       f.currency AS currency
ORDER BY CASE r.role WHEN 'coordinator' THEN 0 WHEN 'materials' THEN 1
                     WHEN 'manufacturing' THEN 2 WHEN 'pilot operation' THEN 3 ELSE 4 END
