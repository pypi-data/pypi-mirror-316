"""
Functions for supervised machine learning models.
"""
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def train_knn(X, y, n_neighbors=5, problem_type='classification'):
    """
    Train a K-Nearest Neighbors model.

    Args:
        X: Feature matrix
        y: Target variable
        n_neighbors: Number of neighbors (default=5)
        problem_type: Either 'classification' or 'regression' (default='classification')

    Returns:
        Trained KNN model
    """
    if problem_type == 'classification':
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
    else:  # regression
        model = KNeighborsRegressor(n_neighbors=n_neighbors)
    
    # Ensure y is 1D
    if hasattr(y, 'ravel'):
        y = y.ravel()
        
    model.fit(X, y)
    return model

def train_decision_tree(X, y, max_depth=None):
    """
    Train a Decision Tree classifier.

    Args:
        X: Feature matrix.
        y: Target vector.
        max_depth: Maximum depth of the tree.
    """
    model = DecisionTreeClassifier(max_depth=max_depth)
    model.fit(X, y)
    return model

def train_random_forest(X, y, n_estimators=100):
    """
    Train a Random Forest classifier.

    Args:
        X: Feature matrix.
        y: Target vector.
        n_estimators: Number of trees in the forest (default: 100).
    """
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X, y)
    return model