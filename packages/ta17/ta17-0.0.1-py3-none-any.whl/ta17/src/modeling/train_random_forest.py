import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.modeling.base_model import BaseModel


class RandomForestModel(BaseModel):
    def __init__(self, n_estimators: int = 100, random_state: int = None):
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train the Random Forest model."""
        self.model.fit(X_train, y_train)

    def predict(self, X: pd.DataFrame):
        """Make predictions using the trained model."""
        return self.model.predict(X)
