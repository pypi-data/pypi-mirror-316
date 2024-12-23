from dataclasses import dataclass, field
from pathlib import Path

import marshmallow_dataclass
import yaml

from src.entities.data_params import DataParams
from src.entities.paths import Paths
from src.entities.train_params import TrainParams


@dataclass()
class PipelineParams:
    paths: Paths = field(default_factory=Paths)
    train_params: TrainParams = field(default_factory=TrainParams)
    data_params: DataParams = field(default_factory=DataParams)
    random_state: int = field(default=42)
    target_column: str = field(default="target")


PipelineParamsSchema = marshmallow_dataclass.class_schema(PipelineParams)


def read_pipeline_params(path: Path) -> PipelineParams:
    with open(path, "r") as input_stream:
        schema = PipelineParamsSchema()
        return schema.load(yaml.safe_load(input_stream))
