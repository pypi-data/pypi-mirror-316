import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from src.modeling.base_model import BaseModel


class DecisionTreeModel(BaseModel):
    def __init__(self, criterion: str = "gini", max_depth: int = None, random_state: int = None):
        self.model = DecisionTreeClassifier(
            criterion=criterion, max_depth=max_depth, random_state=random_state
        )

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        """
        Train the Decision Tree model.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X: pd.DataFrame):
        """
        Make predictions using the trained model.
        """
        return self.model.predict(X)
