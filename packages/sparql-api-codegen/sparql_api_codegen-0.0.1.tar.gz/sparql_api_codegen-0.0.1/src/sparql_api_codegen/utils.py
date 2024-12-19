from typing import Any, Optional

import requests


def query_sparql(query: str, endpoint_url: str, post: bool = False, timeout: Optional[int] = None) -> Any:
    """Execute a SPARQL query on a SPARQL endpoint using requests"""
    if post:
        resp = requests.post(
            endpoint_url,
            headers={
                "Accept": "application/sparql-results+json",
            },
            data={"query": query},
            timeout=timeout,
        )
    else:
        resp = requests.get(
            endpoint_url,
            headers={
                "Accept": "application/sparql-results+json",
                # "User-agent": "sparqlwrapper 2.0.1a0 (rdflib.github.io/sparqlwrapper)"
            },
            params={"query": query},
            timeout=timeout,
        )
    resp.raise_for_status()
    return resp.json()


# @dataclass
# class Entity:
#     iri: str
#     type: str = "http://www.w3.org/2000/01/rdf-schema#Resource"
#     sparql_endpoint: str = "https://www.bgee.org/sparql/"

#     def __post_init__(self):
#         exists = query_sparql(f"ASK WHERE {{ <{self.iri}> a <{self.type}> . }}", self.sparql_endpoint)
#         if not exists.get("boolean"):
#             raise ValueError(f"No resource found with IRI {self.iri} and type {self.type} in endpoint {self.sparql_endpoint}")


#     def get_predicate_value(self, predicate: str) -> str:
#         try:
#             res = query_sparql(f"SELECT ?value WHERE {{ <{self.iri}> <{predicate}> ?value }}", self.sparql_endpoint)
#             return res["results"]["bindings"][0]["value"]["value"]
#         except Exception as err:
#             raise ValueError(f"No value found for predicate {predicate} for entity IRI {self.iri} in endpoint {self.sparql_endpoint}") from err
