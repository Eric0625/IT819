from sklearn import datasets
import networkx as nx

# digits = datasets.load_digits()
# print(digits.images.shape)
# import matplotlib.pyplot as plt 
# plt.imshow(digits.images[-1], cmap=plt.cm.gray_r)
# plt.show()
G = nx.erdos_renyi_graph(20, 0.1)
color_map = []
for node in G:
    if node < 10:
        color_map.append('blue')
    else: 
        color_map.append('green')      
nx.draw(G, node_color=color_map, with_labels=True)
nx.draw_networkx_nodes(G, pos= edgecolors='b')
plt.show()