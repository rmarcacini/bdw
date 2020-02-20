import random
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report


def get_train_test(G, labeled_nodes, test_size=0.7):
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
