import networkx as nx


# Create graph
G = nx.DiGraph()

# Populate graph
nodes = []
G.add_nodes_from(nodes)

edges = []
G.add_edges_from(edges)

# Check graph
G.number_of_nodes()
list(G.nodes)
G.number_of_edges()
list(G.edges)