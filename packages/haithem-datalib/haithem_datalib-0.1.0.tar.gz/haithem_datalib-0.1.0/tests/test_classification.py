import numpy as np
from src.datalib.analysis.classification import knn_classifier, decision_tree_classifier

def test_knn_classifier():
    """Test KNN classifier on basic data."""
    x_train = np.array([[1], [2], [3]])
    y_train = np.array([0, 0, 1])
    
    # Train the model with k=1
    model = knn_classifier(x_train, y_train, n_neighbors=1)
    
    # Assert that the model predicts correctly for input [[2]]
    assert model.predict([[2]])[0] == 0, "knn_classifier ne fonctionne pas."
    
    # Test another sample
    assert model.predict([[3]])[0] == 1, "knn_classifier ne fonctionne pas pour l'échantillon [[3]]."
    
    # Test with a different k (k=2)
    model = knn_classifier(x_train, y_train, n_neighbors=2)
    assert model.predict([[2]])[0] == 0, "knn_classifier avec k=2 ne fonctionne pas."
    
def test_decision_tree_classifier():
    """Test Decision Tree classifier on basic data."""
    x_train = np.array([[1], [2], [3]])
    y_train = np.array([0, 0, 1])
    
    # Train the decision tree model
    model = decision_tree_classifier(x_train, y_train)
    
    # Assert correct prediction for [[3]]
    assert model.predict([[3]])[0] == 1, "decision_tree_classifier ne fonctionne pas pour l'échantillon [[3]]."
    
    # Test another sample (should be predicted as 0)
    assert model.predict([[1]])[0] == 0, "decision_tree_classifier ne fonctionne pas pour l'échantillon [[1]]."
    
    # Test with data that cannot be split well (should still work)
    x_train_small = np.array([[1], [2]])
    y_train_small = np.array([0, 1])
    model = decision_tree_classifier(x_train_small, y_train_small)
    assert model.predict([[1]])[0] == 0, "decision_tree_classifier ne fonctionne pas pour les petites données."
    
def test_knn_classifier_with_edge_cases():
    """Test KNN classifier with edge cases."""
    x_train = np.array([[1], [2], [3]])
    y_train = np.array([0, 1, 0])
    
    # Test with empty data (should raise an error)
    try:
        knn_classifier(np.array([]), np.array([]))
        assert False, "Le KNN n'a pas levé d'erreur pour les données vides."
    except ValueError:
        pass  # Expected behavior
    
    # Test with larger dataset
    x_train_large = np.random.rand(100, 1)  # 100 samples
    y_train_large = np.random.randint(0, 2, 100)  # 100 binary labels
    model = knn_classifier(x_train_large, y_train_large, n_neighbors=5)
    assert model is not None, "Le modèle KNN n'a pas été formé correctement avec un grand jeu de données."

def test_decision_tree_classifier_with_edge_cases():
    """Test Decision Tree classifier with edge cases."""
    x_train = np.array([[1], [2], [3]])
    y_train = np.array([0, 1, 0])
    
    # Test with empty data (should raise an error)
    try:
        decision_tree_classifier(np.array([]), np.array([]))
        assert False, "L'arbre de décision n'a pas levé d'erreur pour les données vides."
    except ValueError:
        pass  # Expected behavior
    
    # Test with a more complex dataset
    x_train_complex = np.random.rand(100, 3)  # 100 samples with 3 features
    y_train_complex = np.random.randint(0, 2, 100)  # 100 binary labels
    model = decision_tree_classifier(x_train_complex, y_train_complex)
    assert model is not None, "L'arbre de décision n'a pas été formé correctement avec un grand jeu de données."
