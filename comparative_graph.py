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

# Сравнительный граф: допустим, есть два словаря — question_words и comment_words
question_words = {"accent", "sound", "american", "sentence", "correct", "practice", "say", "mean", "words"}
comment_words = {"accent", "native", "speaker", "say", "means", "like", "correct", "sentence", "books"}

all_words = question_words | comment_words
compare_graph = nx.Graph()

compare_graph.add_node("Questions", type="meta")
compare_graph.add_node("Comments", type="meta")

for word in all_words:
    if word in question_words:
        compare_graph.add_node(word, type="question")
        compare_graph.add_edge("Questions", word)
    if word in comment_words:
        compare_graph.add_node(word, type="comment")
        compare_graph.add_edge("Comments", word)

pos_compare = nx.spring_layout(compare_graph, seed=7)

edge_x_c = []
edge_y_c = []
for edge in compare_graph.edges():
    x0, y0 = pos_compare[edge[0]]
    x1, y1 = pos_compare[edge[1]]
    edge_x_c += [x0, x1, None]
    edge_y_c += [y0, y1, None]

edge_trace_c = go.Scatter(
    x=edge_x_c, y=edge_y_c,
    line=dict(width=0.5, color='#aaa'),
    hoverinfo='none',
    mode='lines'
)

node_x_c = []
node_y_c = []
labels_c = []
colors_c = []

for node in compare_graph.nodes():
    x, y = pos_compare[node]
    node_x_c.append(x)
    node_y_c.append(y)
    labels_c.append(node)
    if node == "Questions":
        colors_c.append("lightblue")
    elif node == "Comments":
        colors_c.append("lightgreen")
    elif node in question_words and node in comment_words:
        colors_c.append("violet")  # В обеих
    elif node in question_words:
        colors_c.append("red")
    else:
        colors_c.append("blue")

node_trace_c = go.Scatter(
    x=node_x_c, y=node_y_c,
    mode='markers+text',
    text=labels_c,
    textposition="top center",
    hoverinfo='text',
    marker=dict(
        showscale=False,
        color=colors_c,
        size=20,
        line_width=2
    )
)

fig_compare = go.Figure(data=[edge_trace_c, node_trace_c],
                        layout=go.Layout(
                            title=dict(text='Сравнительный граф: вопросы vs комментарии', font=dict(size=16)),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=5,r=5,t=40),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False)))
fig_compare.write_html("compare_graph.html")
print("Сравнительный граф сохранён как compare_graph.html")
