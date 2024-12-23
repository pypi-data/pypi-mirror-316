from dataclasses import dataclass, field


@dataclass()
class Paths:
    synthetic_data: str = field(default="data/raw/dataset.csv")
    processed_data: str = field(default="data/processed/processed_data.pkl")
    model: str = field(default="models/model.pkl")
    reports_path: str = field(default="reports/")
    figures_path: str = field(default="reports/figures/")
    metrics: str = field(default="reports/metrics.json")
