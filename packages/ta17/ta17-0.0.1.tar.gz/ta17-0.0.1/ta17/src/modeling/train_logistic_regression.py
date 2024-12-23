from typing import Literal

import pandas as pd
import sklearn.linear_model

from src.modeling.base_model import BaseModel


class LogisticRegressionModel(BaseModel):
    def __init__(
        self,
        penalty: Literal["l1", "l2", "elasticnet"] | None = "l2",
        C: float = 1,
        random_state: int = 42,
    ):
        self.model = sklearn.linear_model.LogisticRegression(
            penalty=penalty, C=C, random_state=random_state
        )

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        """
        Train the logistic regression model.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X: pd.DataFrame):
        """
        Make predictions using the trained model.
        """
        return self.model.predict(X)
