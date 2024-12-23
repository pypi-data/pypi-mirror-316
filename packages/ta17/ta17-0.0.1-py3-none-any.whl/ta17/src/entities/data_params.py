from dataclasses import dataclass, field

import marshmallow.validate


@dataclass()
class DataParams:
    n_samples: int = field(default=100, metadata={"validate": marshmallow.validate.Range(min=1)})
    n_features: int = field(default=20, metadata={"validate": marshmallow.validate.Range(min=1)})
    n_informative: int = field(default=2, metadata={"validate": marshmallow.validate.Range(min=0)})
    n_redundant: int = field(default=2, metadata={"validate": marshmallow.validate.Range(min=0)})
    n_classes: int = field(default=2, metadata={"validate": marshmallow.validate.Range(min=2)})
