import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from datasets import load_dataset

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)

def drawPCA():
  # Load data
  iris = sklearn.datasets.load_iris()
  X = iris.data
  y = iris.target
  target_names = iris.target_names

  # Reduce to 2D using PCA
  pca = PCA(n_components=2)
  X_r = pca.fit_transform(X)

  # Plot
  plt.figure(figsize=(8, 6))
  colors = ['navy', 'turquoise', 'darkorange']
  for color, i, target_name in zip(colors, [0, 1, 2], target_names):
    plt.scatter(X_r[y == i, 0], X_r[y == i, 1], alpha=0.7, label=target_name, color=color)

  plt.legend()
  plt.title('PCA of IRIS dataset')
  plt.xlabel('Principal Component 1')
  plt.ylabel('Principal Component 2')
  plt.grid(True)
  plt.show()


if __name__ == "__main__":
    # Set seed for reproducibility
    seed = 18
    set_seed(seed)

    # Load dataset
    X, y = load_dataset("iris")

    # Preprocess
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Split data into train and test partitions with 80% train and 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )

    # Models
    log_reg = LogisticRegression(random_state=18)
    rf_clf = RandomForestClassifier(random_state=18)

    log_reg_params = {
        "C": [0.01, 0.1, 1, 10, 100],  # Regularization strength
        "solver": ["lbfgs", "newton-cg"],  # Solver algorithm
        "max_iter": [100, 200, 500, 1000],  # Maximum number of iterations
    }

    rf_clf_params = {
        "n_estimators": [50, 100, 200],  # Number of trees
        "max_depth": [None, 5, 10, 20],  # Max depth of each tree
        "min_samples_split": [2, 5, 10],  # Min samples to split
        "min_samples_leaf": [1, 2, 4],  # Min samples at leaf
        "bootstrap":	[True, False],
    }

    # Grid Search with Cross-Validation
    log_reg_grid = GridSearchCV(log_reg, log_reg_params, cv=4, scoring="accuracy")
    log_reg_grid.fit(X_train, y_train)
    best_log_reg = log_reg_grid.best_estimator_

    # Save the results
    log_reg_results = pd.DataFrame(log_reg_grid.cv_results_)
    log_reg_results = log_reg_results.sort_values(by="mean_test_score", ascending=False)
    log_reg_results = log_reg_results[
        [
            "param_C",
            "param_solver",
            "param_max_iter",
            "mean_test_score",
            "std_test_score",
        ]
    ]
    log_reg_results.to_csv("log_reg.csv", sep=";", index=False)
    print("Best Logistic Regression Accuracy: %.2f" % log_reg_grid.best_score_)
    print("Best Logistic Regression Params:", log_reg_grid.best_params_)

    # Grid Search with Cross-Validation
    rf_clf_grid = GridSearchCV(rf_clf, rf_clf_params, cv=4, scoring="accuracy")
    rf_clf_grid.fit(X_train, y_train)
    best_rf_clf = rf_clf_grid.best_estimator_

    # Save the results
    rf_clf_results = pd.DataFrame(rf_clf_grid.cv_results_)
    rf_clf_results = rf_clf_results.sort_values(by="mean_test_score", ascending=False)
    rf_clf_results = rf_clf_results[
        [
            "param_n_estimators",
            "param_max_depth",
            "param_min_samples_split",
            "param_min_samples_leaf",
            "mean_test_score",
            "std_test_score",
        ]
    ]
    rf_clf_results.to_csv("rf_clf.csv", sep=";", index=False)
    print("Best Random Forest Accuracy: %.2f" % rf_clf_grid.best_score_)
    print("Best Random Forest Params:", rf_clf_grid.best_params_)

    # Fit the best model on the entire training set and get the predictions
    final_log_reg = best_log_reg.fit(X_train, y_train)
    final_rf_clf = best_rf_clf.fit(X_train, y_train)

    log_reg_predictions = final_log_reg.predict(X_test)
    rf_clf_predictions = final_rf_clf.predict(X_test)

    # Evaluate final predictions
    print(
        "Logistic Regression Classification Report:\n",
        classification_report(y_test, log_reg_predictions),
    )

    print(
        "Random Forest Classification Report:\n",
        classification_report(y_test, rf_clf_predictions),
    )
    drawPCA()
