import io
import zipfile
import matplotlib.pyplot as plt
import networkx as nx
import urllib.request as urllib

def get_dataset_footbal():

  print('Loading footbal network...')
  url = "http://websensors.net.br/projects/biased-deep-walk/football.zip"

  sock = urllib.urlopen(url)  # open URL
  s = io.BytesIO(sock.read())  # read into BytesIO "file"
  sock.close()

  zf = zipfile.ZipFile(s)  # zipfile object
  txt = zf.read('football.txt').decode()  # read info file
  gml = zf.read('football.gml').decode()  # read gml data
  # throw away bogus first line with # from mejn files
  gml = gml.split('\n')[1:]
  G = nx.parse_gml(gml)  # parse gml data


  for item in G.nodes(data=True):
      G.nodes[item[0]]['label'] = G.nodes[item[0]]['value']+0
      
  num_classes = 12

  print('Loading footbal network... OK!')

  return G,num_classes

def get_dataset_blogcatalog3():
  #!wget http://socialcomputing.asu.edu/uploads/1283153973/BlogCatalog-dataset.zip
  #!unzip BlogCatalog-dataset.zip
  df_edges = pd.read_csv('BlogCatalog-dataset/data/edges.csv',header=None)
  df_groups = pd.read_csv('BlogCatalog-dataset/data/group-edges.csv',header=None)
  G = nx.Graph()
  for index,row in df_edges.iterrows():
    G.add_edge(str(row[0])+':node',str(row[1])+':node')
  
  for index,row in df_groups.iterrows():
    node_id = str(row[0])+':node'
    G.nodes[node_id]['label'] = row[1]
  
  num_classes = 39
  return G,num_classes


#G,num_classes = get_dataset_blogcatalog3()
#G,num_classes = get_dataset_footbal()
