import os
import yaml
import pickle
from sql.utils import connect_to_psql_database
from src.build_graph import build_graph_from_db
from src.neo4j.utils import connect_to_neo4j_db, upload_to_neo4j_db
import matplotlib.pyplot as plt
import networkx as nx
from random import choice


def graph_simple_plot(G, out_file="graph.png"):
    node_types = set(nx.get_node_attributes(G, "type").values())
    type_color_map = {
        "Chemical": "lightcoral",
        "Protein": "skyblue",
        "Disease": "orchid",
        "Organism": "lightgreen",
        "Biosystem": "gold",
        "Exposure": "orange",
        "Pathway": "lightgray",
        "Dose": "plum",
        "Timepoint": "tan"
    }

    plt.figure(figsize=(10, 9))
    pos = nx.spring_layout(G, seed=30, k=0.5)  # positions for all nodes

    # Draw each type separately with color and shape
    for node_type in node_types:
        nodelist = [n for n, d in G.nodes(data=True) if d.get("type") == node_type]
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=nodelist,
            node_size=600,
            node_color=type_color_map.get(node_type, "gray"),
            label=node_type
        )

    # Draw edges and labels
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    edge_labels = nx.get_edge_attributes(G, "relation")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5)
    node_labels = {n: G.nodes[n].get("label", n) for n in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=6)

    plt.legend(scatterpoints=1)
    plt.axis("off")
    # plt.title("Knowledge Graph by Node Type")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()
    return

# Load database connection parameters from .yaml file
HERE_PATH = os.path.dirname(os.path.abspath(__file__))
with open(f"{HERE_PATH}/config.yml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

graph_name = "ptox_kg"
graphml_file = f"{graph_name}.graphml"
pkl_file = f"{graph_name}.pkl"

# Setup Ptox DB session
session = connect_to_psql_database(config)

# Build graph if it does not exist
if os.path.isfile(pkl_file):
    G = pickle.load(open(pkl_file, "rb"))
else:
    G = build_graph_from_db(session, graph_name)

print(G.number_of_nodes())
print(G.number_of_edges())

# Plot graph (use only on small graph subset)
# graph_simple_plot(G, out_file="graph.png")

# Connect to Neo4j
graph_db = connect_to_neo4j_db(
    config["neo4j_address"],
    config["neo4j_user"],
    config["neo4j_pass"]
)
# Upload graph to Neo4J
upload_to_neo4j_db(G, graph_db)
