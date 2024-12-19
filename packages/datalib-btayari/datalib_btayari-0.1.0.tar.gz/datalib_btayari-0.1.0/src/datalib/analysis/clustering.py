from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def k_means_clustering(data, n_clusters=3):
    """Effectuer un clustering k-means."""
    model = KMeans(n_clusters=n_clusters)
    model.fit(data)
    return model

def principal_component_analysis(data, n_components=2):
    """Effectuer une analyse en composantes principales (ACP)."""
    pca = PCA(n_components=n_components)
    return pca.fit_transform(data)
