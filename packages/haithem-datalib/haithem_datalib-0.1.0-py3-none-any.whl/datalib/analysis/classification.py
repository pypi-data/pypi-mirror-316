from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils.validation import check_X_y

def knn_classifier(x_train, y_train, n_neighbors=3):
    """
    Create and train a k-Nearest Neighbors (k-NN) classifier.
    
    Parameters:
        x_train (array-like): Feature matrix for training data.
        y_train (array-like): Target labels for training data.
        n_neighbors (int, optional): Number of neighbors to consider. Default is 3.
    
    Returns:
        KNeighborsClassifier: Trained k-NN classifier.
    
    Example:
        >>> model = knn_classifier(x_train, y_train, n_neighbors=5)
        >>> predictions = model.predict(x_test)
    """
    x_train, y_train = check_X_y(x_train, y_train)
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(x_train, y_train)
    return model

def decision_tree_classifier(x_train, y_train, max_depth=None, min_samples_split=2):
    """
    Create and train a Decision Tree classifier.
    
    Parameters:
        x_train (array-like): Feature matrix for training data.
        y_train (array-like): Target labels for training data.
        max_depth (int, optional): Maximum depth of the tree. Default is None (unlimited depth).
        min_samples_split (int, optional): Minimum number of samples required to split an internal node. Default is 2.
    
    Returns:
        DecisionTreeClassifier: Trained Decision Tree classifier.
    
    Example:
        >>> model = decision_tree_classifier(x_train, y_train, max_depth=5, min_samples_split=4)
        >>> predictions = model.predict(x_test)
    """
    x_train, y_train = check_X_y(x_train, y_train)
    model = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split)
    model.fit(x_train, y_train)
    return model
