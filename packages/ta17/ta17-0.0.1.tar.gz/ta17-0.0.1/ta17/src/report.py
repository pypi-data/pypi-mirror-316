import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import sklearn.metrics
import typer
from loguru import logger

import src.entities.params
from src.modeling import BaseModel


MARKDOWN_TEMPLATE = """# Model Performance Report for {model_type}

## Classification Report
{report}
## Confusion Matrix
![Confusion Matrix](./figures/{model_type}_confusion_matrix.png)

## ROC Curve
![ROC Curve](./figures/{model_type}_roc_curve.png)

**AUC:** {roc_auc:.2f}
"""


app = typer.Typer()


def save_metrics(y_test, predictions, metrics_path):
    metrics = {
        "accuracy": sklearn.metrics.accuracy_score(y_test, predictions),
        "precision": sklearn.metrics.precision_score(y_test, predictions, average="weighted"),
        "recall": sklearn.metrics.recall_score(y_test, predictions, average="weighted"),
        "f1_score": sklearn.metrics.f1_score(y_test, predictions, average="weighted"),
        "roc_auc": sklearn.metrics.roc_auc_score(y_test, predictions),
    }

    with open(metrics_path, "w") as f:
        json.dump(metrics, f)

    return metrics


def save_classification_report(y_test, predictions, model_type, report_path):
    report = sklearn.metrics.classification_report(y_test, predictions)
    with open(f"{report_path}/{model_type}_classification_report.txt", "w") as f:
        f.write(report)
    return report


def generate_markdown_report(model_type, roc_auc, report, report_path):
    markdown_content = MARKDOWN_TEMPLATE.format(
        model_type=model_type, roc_auc=roc_auc, report=report
    )
    with open(f"{report_path}/{model_type}_report.md", "w") as f:
        f.write(markdown_content)


def plot_confusion_matrix(y_test, predictions, model_type, figures_path):
    cm = sklearn.metrics.confusion_matrix(y_test, predictions)
    disp = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.title(f"Confusion Matrix for {model_type}")
    plt.savefig(f"{figures_path}/{model_type}_confusion_matrix.png")
    plt.close()


def plot_roc_curve(y_test, predictions, model_type, figures_path):
    fpr, tpr, _ = sklearn.metrics.roc_curve(y_test, predictions)
    roc_auc = sklearn.metrics.auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color="blue", lw=2, label=f"ROC curve (area = {roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], color="red", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"Receiver Operating Characteristic for {model_type}")
    plt.legend(loc="lower right")
    plt.savefig(f"{figures_path}/{model_type}_roc_curve.png")
    plt.close()
    return roc_auc


@app.command()
def main(config_path: Path):
    config = src.entities.params.read_pipeline_params(config_path)

    logger.info(f"Loading model from {config.paths.model}...")
    with open(config.paths.model, "rb") as f:
        model: BaseModel = pd.read_pickle(f)
    logger.success("Model loaded successfully.")

    logger.info(f"Loading processed data from {config.paths.processed_data}...")
    with open(config.paths.processed_data, "rb") as f:
        processed_data = pd.read_pickle(f)

    X_test: pd.DataFrame = processed_data["X_test"]
    y_test: pd.DataFrame = processed_data["y_test"]
    logger.debug(
        f"Dataset loaded successfully with feature set shape: {X_test.shape}, Target variable shape: {y_test.shape}"
    )
    logger.success("Processed data loaded successfully.")

    predictions = model.predict(X_test)

    logger.info("Calculating metrics...")
    logger.debug(f"Accuracy: {sklearn.metrics.accuracy_score(y_test, predictions):.2f}")
    logger.debug(sklearn.metrics.classification_report(y_test, predictions))

    save_metrics(y_test, predictions, config.paths.metrics)
    logger.success("Metrics saved successfully.")

    report = save_classification_report(
        y_test, predictions, config.train_params.model_type, config.paths.reports_path
    )

    plot_confusion_matrix(
        y_test, predictions, config.train_params.model_type, config.paths.figures_path
    )
    roc_auc = plot_roc_curve(
        y_test, predictions, config.train_params.model_type, config.paths.figures_path
    )

    generate_markdown_report(
        config.train_params.model_type, roc_auc, report, config.paths.reports_path
    )
    logger.success("Report generated successfully.")


if __name__ == "__main__":
    app()
