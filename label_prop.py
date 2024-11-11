import matplotlib.pyplot as plt
import networkx as nx
import random
import pandas as pd
from collections import Counter
import json

def label_propagation(G, max_iter=50):
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


def visualize_communities(G, labels, plotname):
    # Saving community info
    with open(f"label_prop_outputs/{plotname}.json", "w") as file:
        json.dump(labels, file, indent=4)

    # Set up colors for each community
    unique_labels = set(labels.values())
    color_map = plt.get_cmap("tab10")  # Choose a color map with enough distinct colors
    colors = {label: color_map(i) for i, label in enumerate(unique_labels)}

    # Apply colors based on community labels
    node_colors = [colors[labels[node]] for node in G.nodes()]

    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G, seed=42)  # Use spring layout for visualization

    # Draw nodes with community colors
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=100, alpha=0.8)
    nx.draw_networkx_edges(G, pos, alpha=0.5)

    # Draw node labels (node IDs)
    # nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")

    plt.title("Community Detection using Label Propagation")
    plt.savefig(f"label_prop_outputs/{plotname}.png")


# Week 1
G = nx.read_gexf("graphs/week_1.gexf")
print("G1 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week1")

# Week 2
G = nx.read_gexf("graphs/week_2.gexf")
print("G2 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week2")

# Week 3
G = nx.read_gexf("graphs/week_3.gexf")
print("G3 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week3")

# Week 4
G = nx.read_gexf("graphs/week_4.gexf")
print("G4 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week4")

# Week 5
G = nx.read_gexf("graphs/week_5.gexf")
print("G5 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week5")

# Week 6
G = nx.read_gexf("graphs/week_6.gexf")
print("G6 Nodes: ", len(G.nodes()))
labels = label_propagation(G)
visualize_communities(G, labels, "week6")

