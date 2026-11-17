"""
Build / update the knowledge graph in Neo4j from kg/graph_data.py.

All writes use MERGE, so the script is idempotent and can be re-run to update
the graph after the data file changes.

    python -m kg.load_graph            # create or update
    python -m kg.load_graph --reset    # wipe the database first, then load
"""
import argparse
from collections import defaultdict

from kg import graph_data as g
from kg.db import database, get_driver

NODE_SETS = {
    "Country": g.COUNTRIES,
    "Organization": g.ORGANIZATIONS,
    "Person": g.PEOPLE,
    "Project": g.PROJECTS,
    "Publication": g.PUBLICATIONS,
    "Site": g.SITES,
    "Patent": g.PATENTS,
    "Technology": g.TECHNOLOGIES,
    "Event": g.EVENTS,
}
ORG_KINDS = {"University", "ResearchInstitute", "Company", "Utility", "FundingAgency"}


def create_constraints(session):
    for label in NODE_SETS:
        session.run(
            f"CREATE CONSTRAINT {label.lower()}_id IF NOT EXISTS "
            f"FOR (n:{label}) REQUIRE n.id IS UNIQUE"
        ).consume()
    session.run(
        "CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name)"
    ).consume()


def load_nodes(session):
    for label, rows in NODE_SETS.items():
        if label == "Organization":
            by_kind = defaultdict(list)
            for r in rows:
                assert r["kind"] in ORG_KINDS, r
                by_kind[r["kind"]].append({k: v for k, v in r.items() if k != "country"})
            for kind, batch in by_kind.items():
                session.run(
                    f"UNWIND $rows AS row MERGE (n:Organization {{id: row.id}}) "
                    f"SET n += row, n:{kind}",
                    rows=batch,
                ).consume()
        else:
            batch = [{k: v for k, v in r.items() if v is not None} for r in rows]
            session.run(
                f"UNWIND $rows AS row MERGE (n:{label} {{id: row.id}}) SET n += row",
                rows=batch,
            ).consume()


def load_relationships(session):
    grouped = defaultdict(list)
    for fl, fid, rel, tl, tid, props in g.RELATIONSHIPS:
        grouped[(fl, rel, tl)].append({"from": fid, "to": tid, "props": props})
    for (fl, rel, tl), batch in grouped.items():
        summary = session.run(
            f"UNWIND $rows AS row "
            f"MATCH (a:{fl} {{id: row.from}}) MATCH (b:{tl} {{id: row.to}}) "
            f"MERGE (a)-[r:{rel}]->(b) SET r += row.props "
            f"RETURN count(r) AS n",
            rows=batch,
        ).single()
        if summary["n"] != len(batch):
            raise RuntimeError(f"{fl}-[{rel}]->{tl}: matched {summary['n']} of {len(batch)} rows")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reset", action="store_true", help="delete all nodes before loading")
    args = ap.parse_args()

    with get_driver() as driver, driver.session(database=database()) as session:
        if args.reset:
            session.run("MATCH (n) DETACH DELETE n").consume()
        create_constraints(session)
        load_nodes(session)
        load_relationships(session)

        print("Nodes by label:")
        for r in session.run(
            "MATCH (n) UNWIND labels(n) AS l RETURN l, count(*) AS c ORDER BY l"
        ):
            print(f"  {r['l']:<18}{r['c']}")
        print("Relationships by type:")
        for r in session.run(
            "MATCH ()-[r]->() RETURN type(r) AS t, count(*) AS c ORDER BY t"
        ):
            print(f"  {r['t']:<22}{r['c']}")


if __name__ == "__main__":
    main()
