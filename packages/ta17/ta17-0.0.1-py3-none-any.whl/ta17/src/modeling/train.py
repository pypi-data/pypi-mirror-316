from dataclasses import asdict
from pathlib import Path
from typing import Type

import pandas as pd
import typer
from loguru import logger

import src.entities.params
import src.modeling


app = typer.Typer()


@app.command()
def main(config_path: Path):
    config = src.entities.params.read_pipeline_params(config_path)

    logger.info(f"Loading processed data from {config.paths.processed_data}...")
    with open(config.paths.processed_data, "rb") as f:
        processed_data = pd.read_pickle(f)
    logger.success("Processed data loaded successfully.")

    X_train, y_train = processed_data["X_train"], processed_data["y_train"]

    model_classes: dict[str, tuple[Type[src.modeling.BaseModel], src.entities.ModelParams]] = {
        "logistic": (src.modeling.LogisticRegressionModel, config.train_params.logistic_params),
        "random_forest": (
            src.modeling.RandomForestModel,
            config.train_params.random_forest_params,
        ),
        "decision_tree": (
            src.modeling.DecisionTreeModel,
            config.train_params.decision_tree_params,
        ),
    }

    if (model_type := config.train_params.model_type) not in model_classes:
        raise ValueError(f"Unknown model type: {model_type}")

    model_class, params = model_classes[model_type]
    logger.info(f"Initializing the {model_type.capitalize()} model.")
    logger.debug(f"Parameters for model initialization: {params}")

    common_params = {"random_state": config.random_state}
    model = model_class(**{**common_params, **asdict(params)})

    model.fit(X_train, y_train)
    logger.success(f"{config.train_params.model_type.capitalize()} model fitting complete.")

    with open(config.paths.model, "wb") as f:
        pd.to_pickle(model, f)
    logger.success(f"Model saved to {config.paths.model}.")


if __name__ == "__main__":
    app()
