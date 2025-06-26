import json
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Загрузка данных
with open("keywords.json", "r", encoding="utf-8") as f:
    categories = json.load(f)

# Построение графа
G = nx.Graph()
word_to_categories = {}

for cat, words in categories.items():
    G.add_node(cat, type="category")
    for word in words:
        G.add_node(word, type="keyword")
        G.add_edge(cat, word)
        word_to_categories.setdefault(word, set()).add(cat)

# Построение интерактивного графа с plotly
pos = nx.spring_layout(G, seed=42)

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines'
)

node_x = []
node_y = []
labels = []
colors = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    labels.append(node)
    colors.append('lightblue' if G.nodes[node]['type'] == 'category' else 'lightgreen')

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=labels,
    textposition="top center",
    hoverinfo='text',
    marker=dict(
        showscale=False,
        color=colors,
        size=20,
        line_width=2
    )
)

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title=dict(text='Интерактивный граф категорий и ключевых слов', font=dict(size=16)),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False)))
fig.write_html("interactive_keywords_graph.html")
print("Интерактивный граф сохранён как interactive_keywords_graph.html")

# Построение тепловой карты перекрытий слов
cats = list(categories.keys())
heatmap_data = pd.DataFrame(0, index=cats, columns=cats)

for word, cat_set in word_to_categories.items():
    cat_list = list(cat_set)
    for i in range(len(cat_list)):
        for j in range(i, len(cat_list)):
            heatmap_data.loc[cat_list[i], cat_list[j]] += 1
            if i != j:
                heatmap_data.loc[cat_list[j], cat_list[i]] += 1

plt.figure(figsize=(8, 6))
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Blues')
plt.title("Тепловая карта перекрытий слов между категориями")
plt.tight_layout()
plt.savefig("keyword_overlap_heatmap.png")
plt.show()
print("Тепловая карта сохранена как keyword_overlap_heatmap.png")
