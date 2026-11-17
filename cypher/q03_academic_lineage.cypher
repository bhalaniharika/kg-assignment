// Q3 Academic lineage: full supervision chain for every doctoral researcher
MATCH path = (root:Person)-[:SUPERVISED*1..]->(student:Person)
WHERE NOT ()-[:SUPERVISED]->(root)
WITH student, path, nodes(path) AS chain, last(relationships(path)) AS sup
RETURN student.name AS doctoral_researcher,
       sup.status AS doctorate_status,
       sup.year AS completed_year,
       chain[-2].name AS supervisor,
       CASE WHEN size(chain) >= 3 THEN chain[-3].name END AS academic_grandparent,
       reduce(s = head(chain).name, n IN tail(chain) | s + ' -> ' + n.name) AS supervision_chain,
       length(path) AS generations_from_root
ORDER BY generations_from_root DESC, doctoral_researcher
