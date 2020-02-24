import io
import zipfile
import matplotlib.pyplot as plt
import networkx as nx
import urllib.request as urllib
from zipfile import ZipFile
import pandas as pd

def football():

  print('Loading football network...')
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

def blogcatalog3():
  
  print('Loading BlogCatalog network...')
  url = "http://websensors.net.br/projects/biased-deep-walk/BlogCatalog-dataset.zip"    

  zipfile = urllib.URLopener()
  zipfile.retrieve(url, 'BlogCatalog-dataset.zip')

  with ZipFile('BlogCatalog-dataset.zip', 'r') as zipObj:
     # Extract all the contents of zip file in different directory
     zipObj.extractall('BlogCatalog-dataset')

  df_edges = pd.read_csv('BlogCatalog-dataset/BlogCatalog-dataset/data/edges.csv',header=None)

  df_edges.columns = ['source', 'target']
  df_edges['source'] = df_edges['source'].astype(str)+':n'
  df_edges['target'] = df_edges['target'].astype(str)+':n'

  G = nx.Graph()
  G = nx.from_pandas_edgelist(df_edges, create_using=G)

  df_groups = pd.read_csv('BlogCatalog-dataset/BlogCatalog-dataset/data/group-edges.csv',header=None)
  for index,row in df_groups.iterrows():
      G.nodes[str(row[0])+':n']['label'] = row[1]
        
  num_classes = 39
  return G,num_classes


def ppi_homo_sapiens():
  
  print('Loading PPI-HomoSapiens-MonoLabel network...')
  url = "http://websensors.net.br/projects/biased-deep-walk/PPI-HomoSapiens-MonoLabel.zip"

  zipfile = urllib.URLopener()
  zipfile.retrieve(url, 'PPI-HomoSapiens-MonoLabel.zip')

  with ZipFile('PPI-HomoSapiens-MonoLabel.zip', 'r') as zipObj:
     # Extract all the contents of zip file in different directory
     zipObj.extractall('PPI-HomoSapiens-MonoLabel')

  df_edges = pd.read_csv('PPI-HomoSapiens-MonoLabel/edges.csv')
  df_edges['source'] = df_edges['source'].astype(str)+':n'
  df_edges['target'] = df_edges['target'].astype(str)+':n'

  G = nx.Graph()
  G = nx.from_pandas_edgelist(df_edges, create_using=G)

  df_groups = pd.read_csv('PPI-HomoSapiens-MonoLabel/groups.csv')
  for index,row in df_groups.iterrows():
      G.nodes[str(row[0])+':n']['label'] = row[1]
        
  num_classes = 50
  return G,num_classes

#G,num_classes = get_dataset_blogcatalog3()
#G,num_classes = get_dataset_footbal()
