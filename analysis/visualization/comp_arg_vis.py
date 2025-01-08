import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import heapq

file_path = '../../code/results/aggregated/clean_final_annotations.csv'
df = pd.read_csv(file_path)

G = nx.DiGraph()

criteria = ['Clarity of Review', 'Justification of Scores', 'Depth of Analysis',
            'Fairness and Objectivity', 'Constructiveness of Feedback',
            'Engagement with Related Work', 'Accuracy in Understanding',
            'Consistency of Evaluation', 'Identification of Novelty',
            'Ethical Considerations and Responsibility']

for i, row in df.iterrows():
    review_id = row['Index']
    
    for crit in criteria:
        G.add_node(f"{review_id}_{crit}", score=row[crit])

relations = {
    'Justification of Scores': ['Clarity of Review', 'Accuracy in Understanding', 'Consistency of Evaluation'],
    'Depth of Analysis': ['Constructiveness of Feedback', 'Fairness and Objectivity', 'Engagement with Related Work'],
    'Clarity of Review': ['Constructiveness of Feedback', 'Fairness and Objectivity'],
    'Constructiveness of Feedback': ['Fairness and Objectivity', 'Justification of Scores'],
    'Identification of Novelty': ['Engagement with Related Work', 'Justification of Scores'],
    'Ethical Considerations and Responsibility': ['Fairness and Objectivity', 'Constructiveness of Feedback'],
    'Engagement with Related Work': ['Justification of Scores', 'Accuracy in Understanding', 'Clarity of Review'],
    'Fairness and Objectivity': ['Accuracy in Understanding', 'Depth of Analysis', 'Clarity of Review'],
    'Consistency of Evaluation': ['Accuracy in Understanding', 'Justification of Scores'],
    'Accuracy in Understanding': ['Constructiveness of Feedback', 'Engagement with Related Work']
}

for i, row in df.iterrows():
    review_id = row['Index']
    count = 0
    for crit, supports in relations.items():
        if count == 5:
            break
        inner_count = 0
        for support in supports:
            if inner_count == 5:
                break
            if row[crit] == 1: 
                G.add_edge(f"{review_id}_{crit}", f"{review_id}_{support}", weight=1)
            elif row[crit] == -1: 
                G.add_edge(f"{review_id}_{crit}", f"{review_id}_{support}", weight=-1)
            inner_count += 1
        count += 1
    nx.draw(G, with_labels=True)
    break

def get_top_n_items(dictionary):
    n = 10
    items = [(value, key) for key, value in dictionary.items()]
    heapq.nlargest(n, items)
    return items[:n]

centrality = nx.degree_centrality(G)
print("Degree Centrality:", get_top_n_items(centrality))

shortest_paths = dict(nx.all_pairs_shortest_path_length(G))
print("Shortest Paths:", get_top_n_items(shortest_paths))

components = list(nx.strongly_connected_components(G))
print("Strongly Connected Components:", get_top_n_items(components))

filtered_nodes = [node for node in G.nodes if 'Clarity of Review' in node or 'Justification of Scores' in node]
subgraph = G.subgraph(filtered_nodes)
plt.figure(figsize=(8, 8))
pos = nx.spring_layout(subgraph)
nx.draw(subgraph, pos, with_labels=True, node_size=500, node_color='lightblue')
nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=nx.get_edge_attributes(subgraph, 'weight'))
plt.title('Filtered Argumentation Graph')
plt.show()

centrality = nx.degree_centrality(G)
sorted_nodes = sorted(centrality, key=centrality.get, reverse=True)[:20]
subgraph = G.subgraph(sorted_nodes)
plt.figure(figsize=(8, 8))
pos = nx.spring_layout(subgraph)
nx.draw(subgraph, pos, with_labels=True, node_size=500, node_color='lightblue')
nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=nx.get_edge_attributes(subgraph, 'weight'))
plt.title('Top 20 Central Nodes Argumentation Graph')
plt.show()
