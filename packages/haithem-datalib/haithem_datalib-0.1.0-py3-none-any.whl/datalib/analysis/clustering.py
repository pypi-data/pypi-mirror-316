from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.utils.validation import check_array

def k_means_clustering(data, n_clusters=3, init='k-means++', max_iter=300, random_state=None):
    """
    Perform k-means clustering on the given data.

    Parameters:
        data (array-like): Input data for clustering. Must be numeric and of shape (n_samples, n_features).
        n_clusters (int, optional): The number of clusters to form. Default is 3.
        init (str, optional): Method for initialization ('k-means++', 'random'). Default is 'k-means++'.
        max_iter (int, optional): Maximum number of iterations of the k-means algorithm. Default is 300.
        random_state (int, optional): Determines random number generation for centroid initialization. Default is None.

    Returns:
        KMeans: Fitted KMeans object.
        array: Cluster labels for each point.

    Example:
        >>> model, labels = k_means_clustering(data, n_clusters=5)
        >>> print(labels)
    """
    data = check_array(data)
    model = KMeans(n_clusters=n_clusters, init=init, max_iter=max_iter, random_state=random_state)
    model.fit(data)
    return model, model.labels_

def principal_component_analysis(data, n_components=2, svd_solver='auto'):
    """
    Perform Principal Component Analysis (PCA) on the given data.

    Parameters:
        data (array-like): Input data to transform. Must be numeric and of shape (n_samples, n_features).
        n_components (int, optional): Number of components to keep. Default is 2.
        svd_solver (str, optional): Solver to use ('auto', 'full', 'arpack', 'randomized'). Default is 'auto'.

    Returns:
        array: Transformed data of shape (n_samples, n_components).
        PCA: Fitted PCA object.

    Example:
        >>> transformed_data, pca = principal_component_analysis(data, n_components=3)
        >>> print(transformed_data.shape)
    """
    data = check_array(data)
    pca = PCA(n_components=n_components, svd_solver=svd_solver)
    transformed_data = pca.fit_transform(data)
    return transformed_data, pca
