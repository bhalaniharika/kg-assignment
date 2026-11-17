// Q8 Collaboration horizon: organizations reachable from HIT within two project-collaboration hops
// (one hop = Organization -> shared Project -> Organization)
MATCH path = (start:Organization {name: 'Halvorsen Institute of Technology'})
             ((:Organization)-[:PARTICIPATES_IN]->(:Project)<-[:PARTICIPATES_IN]-(:Organization)){1,2}
             (target:Organization)
WITH start, target, path, nodes(path) AS ns
WHERE target <> start
  AND all(n IN ns WHERE size([m IN ns WHERE m = n]) = 1)
WITH target, length(path) / 2 AS hops,
     reduce(s = head(ns).name, n IN tail(ns) |
            s + CASE WHEN n:Project THEN ' -[' + n.name + ']-> ' ELSE n.name END) AS route
WITH target, min(hops) AS min_hops, collect({hops: hops, route: route}) AS routes
RETURN target.name AS organization,
       min_hops AS hops,
       [r IN routes WHERE r.hops = min_hops | r.route] AS via
ORDER BY hops, organization
