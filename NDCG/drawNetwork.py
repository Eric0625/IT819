import networkx as nx
import matplotlib.pyplot as plt
import h5py

# 创建DAG
G = nx.DiGraph()

# 顶点列表
vertex_list = ['v'+str(i) for i in range(1, 27)]
# 添加顶点
G.add_nodes_from(vertex_list)

# 边列表
edge_list = []
for i in range(1, 5):
    for j in range(5, 15):
        edge_list.append((f'v{i}', f'v{j}'))
for i in range(5, 15):
    for j in range(15, 20):
        edge_list.append((f'v{i}', f'v{j}'))
for i in range(15, 20):
    for j in range(20, 22):
        edge_list.append((f'v{i}', f'v{j}'))
for i in range(20, 22):
    for j in range(22, 27):
        edge_list.append((f'v{i}', f'v{j}'))
# 通过列表形式来添加边
G.add_edges_from(edge_list)

pos = {
        'v1':(-2,3),
        'v2':(-2,1),
        'v3':(-2,-1),
        'v4':(-2,-3),
        'v5':(-1,4.5),
        'v6':(-1,3.5),
        'v7':(-1,2.5),
        'v8':(-1,1.5),
        'v9':(-1,0.5),
        'v10':(-1,-0.5),
        'v11':(-1,-1.5),
        'v12':(-1,-2.5),
        'v13':(-1,-3.5),
        'v14':(-1,-4.5),
        'v15':(0,3),
        'v16':(0,1.5),
        'v17':(0,0),
        'v18':(0,-1.5),
        'v19':(0,-3),
        'v20':(1,1),
        'v21':(1,-1),
        'v22':(2,3),
        'v23':(2,1.5),
        'v24':(2,0),
        'v25':(2,-1.5),
        'v26':(2,-3),
       }
# 绘制DAG图
#plt.title('DNN for NDCG Testing')    #图片标题
plt.xlim(-2.2, 2.2)                     #设置X轴坐标范围
plt.ylim(-5.5, 5.5)                     #设置Y轴坐标范围
# nx.draw(
#         G,
#         pos = pos,                      
#         node_color = 'white',             
#         edge_color = 'black',
#         node_size = 400,                  
#        )
color_map = []
for node in G:
    name = int(node[1:])
    if name < 5:
        color_map.append('#355AB5')
    elif name < 22:
        color_map.append('#C25821')
    else: 
        color_map.append('#5D9E37')   
nx.draw_networkx_edges(G, pos=pos, edge_color='black')
nx.draw_networkx_nodes(G, pos=pos, node_size=450, node_color=color_map, edgecolors='white')
labels={}

values = [10.0, 2.0, 0.0, 1.0, 0.0, 0, 5.370, 0, 337.8, 0, 0, 0, 0, 0.5427, 0, 0, 2351, 0, 245.1, 3.543, 0, 1.352, 0.417, -0.346, -2.729, -3.248]
i = 0
for name in list(G.nodes):
    labels[name] = values[i]
    i += 1
nx.draw_networkx_labels(G,pos,labels,font_size=6, font_color='#ffffff')
plt.show()
#plt.savefig('DNN.png')
print('done')
