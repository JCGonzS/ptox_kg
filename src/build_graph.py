import networkx as nx
import pickle
from src.transform import add_all_nodes_and_edges


def clean_none_attributes(graph):
    for _, attrs in graph.nodes(data=True):
        for key in list(attrs):
            if attrs[key] is None:
                print(attrs)
                del attrs[key]

    for _, _, attrs in graph.edges(data=True):
        for key in list(attrs):
            if attrs[key] is None:
                del attrs[key]
                print(attrs)


def build_graph_from_db(session, out_file_name="my_graph"):
    # Initialize directed graph
    G = nx.DiGraph()

    # Add nodes and edges sequentially
    G = add_all_nodes_and_edges(G, session)

    # Check graph
    print(G.number_of_nodes())
    print(G.number_of_edges())
    # for node, attrs in G.nodes(data=True):
    #     print(node, attrs)

    # Export graph
    clean_none_attributes(G)
    nx.write_graphml(G, f"{out_file_name}.graphml") # .graphml, for visual tools
    pickle.dump(G, open(f"{out_file_name}.pkl", "wb"))  # .pkl, for faster reloads

    return G
