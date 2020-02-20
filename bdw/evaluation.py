import random
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report


def get_train_test(G, labeled_nodes, model):
  X_train = []
  y_train = []
  X_test = []
  y_test = []

  vocab = []
  for node in model.wv.vocab:
    vocab.append(node)

  random.shuffle(vocab)
  
  for node in model.wv.vocab:
    if node in labeled_nodes:
      X_train.append(model[node])
      y_train.append(G.nodes[node]['label'])
    else:
      X_test.append(model[node])
      y_test.append(G.nodes[node]['label'])

  return X_train, X_test, y_train, y_test

def linear_svc(X_train, X_test, y_train, y_test):
  clf = LinearSVC(random_state=0, tol=1e-5)
  clf.fit(X_train, y_train)
  y_preds = clf.predict(X_test)
  return y_preds

def metrics(y_test, y_preds):
  return classification_report(y_test, y_preds, output_dict=True)


from sklearn.model_selection import train_test_split


def sample_labeled_nodes(G,train_size=0.3):
  T = []
  t = []
  for node in G.nodes():
    T.append([node])
    t.append([G.nodes[node]['label']])

  T_train, T_test, t_train, t_test = train_test_split(T, t, test_size=1.0-train_size, random_state=42)

  labeled_nodes = []
  for s in T_train: labeled_nodes.append(s[0])

  return labeled_nodes
