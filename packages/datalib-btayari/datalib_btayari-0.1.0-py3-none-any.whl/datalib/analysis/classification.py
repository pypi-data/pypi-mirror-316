from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

def knn_classifier(x_train, y_train, n_neighbors=3):
    """Créer un classificateur k-NN."""
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(x_train, y_train)
    return model

def decision_tree_classifier(x_train, y_train):
    """Créer un arbre de décision."""
    model = DecisionTreeClassifier()
    model.fit(x_train, y_train)
    return model
