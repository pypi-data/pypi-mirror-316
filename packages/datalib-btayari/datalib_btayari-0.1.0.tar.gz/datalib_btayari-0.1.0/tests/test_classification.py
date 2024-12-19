import numpy as np
from src.datalib.analysis.classification import knn_classifier, decision_tree_classifier

def test_knn_classifier():
    x_train = np.array([[1], [2], [3]])
    y_train = np.array([0, 0, 1])
    model = knn_classifier(x_train, y_train, n_neighbors=1)
    assert model.predict([[2]])[0] == 0, "knn_classifier ne fonctionne pas."

def test_decision_tree_classifier():
    x_train = np.array([[1], [2], [3]])
    y_train = np.array([0, 0, 1])
    model = decision_tree_classifier(x_train, y_train)
    assert model.predict([[3]])[0] == 1, "decision_tree_classifier ne fonctionne pas."
