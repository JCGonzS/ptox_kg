import networkx as nx
from src.transform import add_all_nodes_and_edges


def build_graph_from_db(session):
    # Initialize directed graph
    G = nx.DiGraph()

    # Add nodes and edges sequentially
    G = add_all_nodes_and_edges(G, session)

    # Check graph
    print(G.number_of_nodes())
    print(G.number_of_edges())
    # for node, attrs in G.nodes(data=True):
    #     print(node, attrs)
    
    return G
