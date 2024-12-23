"""
Functions for unsupervised learning algorithms.
"""
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture

def perform_kmeans(X, n_clusters, random_state=42):
    """
    Perform k-means clustering.

    Args:
        X: Feature matrix.
        n_clusters: Number of clusters.
        random_state: Random seed.
    """
    model = KMeans(n_clusters=n_clusters, random_state=random_state)
    model.fit(X)
    return model

def perform_pca(X, n_components):
    """
    Perform Principal Component Analysis (PCA).

    Args:
        X: Feature matrix.
        n_components: Number of components to retain.
    """
    pca = PCA(n_components=n_components)
    X_reduced = pca.fit_transform(X)
    explained_variance = pca.explained_variance_ratio_
    return X_reduced, explained_variance, pca

def perform_gaussian_mixture(X, n_components):
    """
    Perform Gaussian Mixture Modeling.

    Args:
        X: Feature matrix.
        n_components: Number of mixture components.
    """
    model = GaussianMixture(n_components=n_components)
    model.fit(X)
    return model