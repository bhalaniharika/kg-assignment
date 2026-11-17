# Energy-Storage Research Knowledge Graph (Neo4j Aura)

A knowledge graph built from the 35 documents in [corpus/](corpus/), loaded into a Neo4j Aura Free
instance and queried with Cypher to answer the 10 questions in [queries.txt](queries.txt).

**Deliverable:** [results.csv](results.csv) has the columns `Question`, `Cypher Query`, `Answer`, `Execution Time`.

## Project layout

| Path | Purpose |
|---|---|
| `corpus/` | Source documents (organizations, projects, people, papers, sites, patent, technologies) |
| `kg/graph_data.py` | Entities and relationships extracted from the corpus; every fact has a `source` file reference |
| `kg/load_graph.py` | Creates constraints and MERGEs the graph into Neo4j (idempotent, `--reset` to rebuild) |
| `kg/run_queries.py` | Runs each `cypher/qNN_*.cypher`, times it, writes `results.csv` and `results.json` |
| `kg/db.py` | Connection helper (reads `.env`) |
| `cypher/` | One Cypher query per question, in the order of `queries.txt` |
| `results.csv` | Final answers |
| `results.json` | Raw query records and per-run timings |

## Graph model

Nodes: `Organization` (with a second label `University`, `ResearchInstitute`, `Company`, `Utility` or
`FundingAgency`), `Country`, `Person`, `Project`, `Publication`, `Site`, `Patent`, `Technology`, `Event`.
Totals: 50 nodes and 155 relationships.

Main relationships:

```
(FundingAgency)-[:FUNDS {amount, currency, start_year, end_year}]->(Project)
(Organization)-[:PARTICIPATES_IN {role, contribution}]->(Project)
(Person)-[:AFFILIATED_WITH {type: employment|study|visiting, position, start_year, end_year, current}]->(Organization)
(Person)-[:SUPERVISED {degree, year, status}]->(Person)
(Person)-[:AUTHORED {position}]->(Publication)-[:RESULT_OF]->(Project)
(Publication)-[:CITES]->(Publication)
(Publication)-[:ABOUT]->(Technology)
(Organization)-[:HOLDS]->(Patent)-[:COVERS]->(Technology)<-[:USES_TECHNOLOGY]-(Site)
(Person)-[:INVENTED]->(Patent)
(Organization)-[:OPERATES]->(Site)<-[:ESTABLISHED]-(Project)
(Organization)-[:LOCATED_IN]->(Country)
```

The full list is in the docstring of [kg/graph_data.py](kg/graph_data.py).

## Setup and run

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
copy .env.example .env          # then fill in NEO4J_URI / NEO4J_PASSWORD from the Aura credentials file

python -m kg.load_graph         # build or update the graph (add --reset to wipe first)
python -m kg.run_queries        # write results.csv and results.json
```

TLS is verified against the operating-system certificate store (via `truststore`), so the connection
also works behind corporate proxies that re-sign HTTPS traffic.

## Modelling decisions

- **Consortium roles (Q1):** `PARTICIPATES_IN.role` uses the vocabulary from the question:
  coordinator, materials, manufacturing, pilot operation (plus modelling, software integration,
  research partner and industrial partner for the other projects).
- **Affiliations in Q2:** an author's affiliation is the organization they belonged to in the
  publication year, using the start and end years on `AFFILIATED_WITH`.
- **Mobility (Q4):** only `employment` and `study` affiliations count, as the question specifies.
  Priya Raghunathan's 2019 sabbatical at Maple Ridge is stored as `visiting`, so it is not counted as a move.
- **International reach (Q6):** a person's country is the country of their current affiliation.
- **Collaboration horizon (Q8):** one hop is Organization → shared Project → Organization.
  Each organization is reported at its minimum hop count.
- **Collaborator recommendation (Q10):** "same technology area" means both researchers have authored
  publications `ABOUT` the same `Technology` node.
- **Execution Time:** the median client-side wall-clock time over 5 runs, measured after one untimed
  warm-up run. It runs from sending the query to fetching every record, so it includes the network
  round trip to Aura, which accounts for most of the time.
