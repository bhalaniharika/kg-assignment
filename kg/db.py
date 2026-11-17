"""Neo4j connection helper. Reads credentials from .env (see .env.example)."""
import os
import ssl
import sys
from pathlib import Path

import truststore
from dotenv import load_dotenv
from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def get_driver():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    if not uri or not password:
        sys.exit("Missing NEO4J_URI / NEO4J_PASSWORD. Copy .env.example to .env and fill it in.")

    # Verify TLS against the operating-system certificate store instead of
    # Python's bundled CAs. This keeps full certificate verification while
    # working behind corporate proxies that re-sign TLS with an internal root CA.
    # The driver only accepts a custom ssl_context with the plain scheme, so
    # neo4j+s:// becomes neo4j:// + context (still encrypted and verified).
    kwargs = {}
    for secure, plain in (("neo4j+s://", "neo4j://"), ("bolt+s://", "bolt://")):
        if uri.startswith(secure):
            uri = plain + uri[len(secure):]
            kwargs["ssl_context"] = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    driver = GraphDatabase.driver(uri, auth=(user, password), **kwargs)
    driver.verify_connectivity()
    return driver


def database():
    return os.getenv("NEO4J_DATABASE") or None
