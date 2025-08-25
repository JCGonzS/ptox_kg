from py2neo import Graph, Node, Relationship
import networkx as nx

def connect_to_neo4j_db(address="localhost:7687", user="neo4j", passw=""):
    graph_db = Graph(f"bolt://{address}", auth=(f"{user}", f"{passw}"))
    return graph_db


def upload_to_neo4j_db(G, graph_db):
    graph_db.delete_all()  # Careful: clears the DB

    # Create nodes
    for node_id, attrs in G.nodes(data=True):
        label = attrs.get("type", "Entity")
        attrs = {k: v for k, v in attrs.items() if k != "id"}
        node = Node(label, id=node_id, **attrs)
        graph_db.create(node)

    # Create relationships
    for source, target, attrs in G.edges(data=True):
        rel_type = attrs.get("relation", "RELATED_TO")
        # Match existing nodes
        query = """
        MATCH (a {id: $source_id}), (b {id: $target_id})
        CREATE (a)-[r:%s $props]->(b)
        """ % rel_type.upper()
        graph_db.run(query, source_id=source, target_id=target, props=attrs)

    print("✅ Upload complete.")
