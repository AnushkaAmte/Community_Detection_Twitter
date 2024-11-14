import matplotlib.pyplot as plt
import networkx as nx
import random
import pandas as pd
from collections import Counter
import json

def label_propagation(G, max_iter=10):
    # Initialize each node with a unique integer label
    labels = {node: i for i, node in enumerate(G.nodes())}
    
    for _ in range(max_iter):
        # print("Iteration: ", _)
        # print("Initial Labels: ", labels)
        nodes = list(G.nodes())
        random.shuffle(nodes)  # Randomize order of nodes

        for node in nodes:
            # Get the labels of the neighbors
            neighbor_labels = [labels[neighbor] for neighbor in G.neighbors(node)]
            if not neighbor_labels:
                continue

            # Find the most common label among neighbors
            most_common_label = Counter(neighbor_labels).most_common(1)[0][0]
            
            # Update the label if it's different from the current label
            labels[node] = most_common_label


    # Convert the labels to integer community ids
    unique_labels = sorted(set(labels.values()))
    print("Unique Labels (Num. of Communities): ", len(unique_labels))
    label_map = {old_label: new_id for new_id, old_label in enumerate(unique_labels)}
    
    # Map the current labels to the new community ids
    int_labels = {node: label_map[label] for node, label in labels.items()}

    return int_labels


def visualize_communities(g, community_map, plotname):
    # Saving community info
    with open(f"label_prop_outputs/{plotname}.json", "w") as file:
        json.dump(labels, file, indent=4)

    for node in g.nodes():
        if node in community_map:
            g.nodes[node]['community'] = community_map[node]
        else:
            g.nodes[node]['community'] = None  # Or a default value if needed

    community_counts = Counter(community_map.values())

    # Step 3: Assign community size as a node attribute
    for node in g.nodes():
        community_id = g.nodes[node].get('community')
        if community_id is not None:
            g.nodes[node]['community_size'] = community_counts[community_id]
        else:
            g.nodes[node]['community_size'] = 0  # Or a default value

    community_dict = {}

    for node, community_id in community_map.items():
        if community_id not in community_dict:
            community_dict[community_id] = []
        community_dict[community_id].append(node)

    # Step 3: Remove edges between nodes that belong to different communities
    edges_to_remove = []

    for u, v in g.edges():
        if community_map.get(u) != community_map.get(v):  # If nodes belong to different communities
            edges_to_remove.append((u, v))

    # Remove the cross-community edges
    g.remove_edges_from(edges_to_remove)

    # # Set up colors for each community
    # unique_labels = set(labels.values())
    # color_map = plt.get_cmap("tab10")  # Choose a color map with enough distinct colors
    # colors = {label: color_map(i) for i, label in enumerate(unique_labels)}

    # # Apply colors based on community labels
    # node_colors = [colors[labels[node]] for node in G.nodes()]

    # plt.figure(figsize=(10, 10))
    # pos = nx.spring_layout(G, seed=42)  # Use spring layout for visualization

    # # Draw nodes with community colors
    # nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=100, alpha=0.8)
    # nx.draw_networkx_edges(G, pos, alpha=0.5)

    # # Draw node labels (node IDs)
    # # nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")

    # plt.title("Community Detection using Label Propagation")
    # plt.savefig(f"label_prop_outputs/{plotname}.png")


# Week 1
G = nx.read_gexf("graphs/week_1.gexf")
print("G1 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week1")
nx.write_gexf(G, "graphs/week_1_communities_forests_label_prop.gexf")

# Week 2
G = nx.read_gexf("graphs/week_2.gexf")
print("G2 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week2")
nx.write_gexf(G, "graphs/week_2_communities_forests_label_prop.gexf")

# Week 3
G = nx.read_gexf("graphs/week_3.gexf")
print("G3 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week3")
nx.write_gexf(G, "graphs/week_3_communities_forests_label_prop.gexf")

# Week 4
G = nx.read_gexf("graphs/week_4.gexf")
print("G4 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week4")
nx.write_gexf(G, "graphs/week_4_communities_forests_label_prop.gexf")

# Week 5
G = nx.read_gexf("graphs/week_5.gexf")
print("G5 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week5")
nx.write_gexf(G, "graphs/week_5_communities_forests_label_prop.gexf")

# Week 6
G = nx.read_gexf("graphs/week_6.gexf")
print("G6 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week6")
nx.write_gexf(G, "graphs/week_6_communities_forests_label_prop.gexf")

