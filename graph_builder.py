import json
import networkx as nx
import matplotlib.pyplot as plt

# Загрузка данных
with open("keywords.json", "r", encoding="utf-8") as f:
    categories = json.load(f)

# Построение графа
G = nx.Graph()

# Добавляем узлы и связи
for cat, words in categories.items():
    G.add_node(cat, type="category")
    for word in words:
        G.add_node(word, type="keyword")
        G.add_edge(cat, word)

# Визуализация
pos = nx.spring_layout(G, seed=42)
node_colors = ['lightblue' if G.nodes[n]['type'] == 'category' else 'lightgreen' for n in G.nodes]

plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color=node_colors, font_size=9, node_size=800, edge_color="gray")
plt.title("Keyword Network by Category")
plt.tight_layout()
plt.savefig("keywords_graph.png")
plt.show()
