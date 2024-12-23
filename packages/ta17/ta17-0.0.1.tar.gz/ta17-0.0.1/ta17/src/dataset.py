from pathlib import Path

import numpy as np
import pandas as pd
import sklearn.datasets
import typer
from loguru import logger

import src.entities.params


app = typer.Typer()


def generate_classification_dataset(
    n_samples=100,
    n_features=20,
    n_informative=2,
    n_redundant=2,
    n_classes=2,
    random_state=None,
    target_column="target",
) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """
    Generate a synthetic dataset for classification using sklearn's make_classification.
    """

    X, y = sklearn.datasets.make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_redundant,
        n_classes=n_classes,
        random_state=random_state,
    )

    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(n_features)])
    df[target_column] = y

    return X, y, df


@app.command()
def main(config_path: Path):
    config = src.entities.params.read_pipeline_params(config_path)

    logger.info("Starting the process of generating a synthetic dataset...")
    logger.debug(f"Parameters for dataset generation: {config.data_params}")
    _, _, dataset = generate_classification_dataset(
        n_samples=config.data_params.n_samples,
        n_features=config.data_params.n_features,
        n_informative=config.data_params.n_informative,
        n_redundant=config.data_params.n_redundant,
        n_classes=config.data_params.n_classes,
        random_state=config.random_state,
        target_column=config.target_column,
    )

    dataset.to_csv(config.paths.synthetic_data, index=False)
    logger.success(
        f"Synthetic dataset generation complete. Dataset saved to {config.paths.synthetic_data}"
    )


if __name__ == "__main__":
    app()
