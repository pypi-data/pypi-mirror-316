from dataclasses import dataclass, field
from typing import Literal, Union

import marshmallow.validate


@dataclass()
class LogisticTrainParams:
    penalty: str = field(
        default="l2",
        metadata={"validate": marshmallow.validate.OneOf(choices=["l1", "l2", "none"])},
    )
    C: float = field(default=1.0, metadata={"validate": marshmallow.validate.Range(min=0)})


@dataclass()
class RandomForestTrainParams:
    n_estimators: int = field(default=50, metadata={"validate": marshmallow.validate.Range(min=1)})


@dataclass()
class DecisionTreeTrainParams:
    criterion: str = field(
        default="gini",
        metadata={"validate": marshmallow.validate.OneOf(choices=["gini", "entropy"])},
    )
    max_depth: int | None = field(
        default=None, metadata={"validate": marshmallow.validate.Range(min=1)}
    )


ModelParams = Union[LogisticTrainParams, RandomForestTrainParams, DecisionTreeTrainParams]


@dataclass()
class TrainParams:
    model_type: Literal["logistic", "random_forest", "decision_tree"] = field(default="logistic")
    logistic_params: LogisticTrainParams = field(default_factory=LogisticTrainParams)
    random_forest_params: RandomForestTrainParams = field(default_factory=RandomForestTrainParams)
    decision_tree_params: DecisionTreeTrainParams = field(default_factory=DecisionTreeTrainParams)
