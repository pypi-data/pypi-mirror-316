from pathlib import Path

import pandas as pd
import typer
from loguru import logger
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import src.entities.params


app = typer.Typer()


class DataPreprocessor:
    def __init__(self, target_column: str):
        self.target_column = target_column
        self.numeric_features = []
        self.categorical_features = []
        self.preprocessor = None

    def fit(self, df: pd.DataFrame):
        """
        Fit the preprocessor on the given DataFrame.
        """
        X, _ = df.drop(columns=[self.target_column]), df[self.target_column]

        self.numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
        self.categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

        numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])
        categorical_transformer = Pipeline(
            steps=[("onehot", OneHotEncoder(handle_unknown="ignore"))]
        )

        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, self.numeric_features),
                ("cat", categorical_transformer, self.categorical_features),
            ]
        )

        self.preprocessor.fit(X)

    def transform(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        """
        Transform the DataFrame using the fitted preprocessor.
        """
        X, y = df.drop(columns=[self.target_column]), df[self.target_column]
        X_processed = pd.DataFrame(self.preprocessor.transform(X))
        return X_processed, y

    def split(
        self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Split the processed features and target into training and testing sets.
        """
        return train_test_split(X, y, test_size=test_size, random_state=random_state)


@app.command()
def main(config_path: Path):
    config = src.entities.params.read_pipeline_params(config_path)

    logger.info(f"Loading dataset from {config.paths.synthetic_data}...")
    df = pd.read_csv(config.paths.synthetic_data)
    logger.debug(f"Dataset shape: {df.shape}")
    logger.success("Dataset loaded successfully.")

    preprocessor = DataPreprocessor(config.target_column)
    preprocessor.fit(df)

    logger.info("Transforming dataset...")
    X_processed, y = preprocessor.transform(df)
    logger.debug(
        f"Processed feature set shape: {X_processed.shape}, Target variable shape: {y.shape}"
    )

    X_train, X_test, y_train, y_test = preprocessor.split(X_processed, y)
    processed_data = {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}
    with open(config.paths.processed_data, "wb") as f:
        pd.to_pickle(processed_data, f)

    logger.success(
        f"Processing dataset complete. Processed dataset saved to {config.paths.processed_data}."
    )


if __name__ == "__main__":
    app()
