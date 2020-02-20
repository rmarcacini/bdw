from node2vec import Node2Vec
from tqdm import trange
import random
import math
import numpy as np


def node2vec(G, dimensions=100, walk_length=10, num_walks=30, window=10, q=1, p=1):
  model = Node2Vec(G, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=1, q=q, p=p)
  model = model.fit(window=window, min_count=1, batch_words=4)
  return model

def deepwalk(G, dimensions=100, walk_length=10, num_walks=30, window=10):
  model = Node2Vec(G, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=1, q=1, p=1)
  model = model.fit(window=window, min_count=1, batch_words=4)
  return model

def bdw(G, labeled_nodes, num_classes, dimensions=100, walk_length=10, num_walks=30, window=10, gamma=1.0, max_iterations=15):

  nodes = []

  for node in G.nodes():
    G.nodes[node]['f'] = np.array([0.0]*num_classes)
    nodes.append(node)
  
  label_codes = {}
  counter = 0
  for node in labeled_nodes:
    if G.nodes[node]['label'] not in label_codes:
        label_codes[G.nodes[node]['label']] = counter
        counter += 1
    y = np.array([0.0]*num_classes)
    y[label_codes[G.nodes[node]['label']]]=1.0
    G.nodes[node]['y'] = y
    G.nodes[node]['f'] = y*1.0
  


  t = trange(max_iterations, desc='Learning Transition Function', leave=True)
  t.update(1)

  iteration = 0
  while(iteration < max_iterations):
    random.shuffle(nodes)
    energy = 0.0
    for node in nodes:
      f_new = np.array([0.0]*num_classes)
      f_old = np.array(G.nodes[node]['f'])*1.0
      
      sum_w = 0.0
      for neighbor in G.neighbors(node):
        
        w = 1.0
        if 'weight' in G[node][neighbor]: w = G[node][neighbor]['weight']

        w /= math.sqrt(G.degree[neighbor])

        f_new += w*G.nodes[neighbor]['f']

        sum_w += w
      f_new /= sum_w

      G.nodes[node]['f'] = f_new

      if 'y' in G.nodes[node]:
        G.nodes[node]['f'] = G.nodes[node]['f']*(1-gamma) + G.nodes[node]['y']*gamma
      
      energy += np.linalg.norm(f_new-f_old)
    
    iteration+=1
    
    message = 'Iteration '+str(iteration)+' | Energy = '+str(energy)+' | %i'
    t.set_description(message %iteration)
    t.refresh()
    t.update(1)

  for edge in G.edges(data=True):
    G[edge[0]][edge[1]]['weight'] = np.dot(G.nodes[edge[0]]['f'],G.nodes[edge[1]]['f']) + 0.000001
    #print(edge)

  model = Node2Vec(G, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=1, q=1, p=1)
  model = model.fit(window=window, min_count=1, batch_words=4)

  return model

