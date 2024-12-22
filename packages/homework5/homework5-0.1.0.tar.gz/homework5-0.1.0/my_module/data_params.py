import sys
from dataclasses import dataclass, field

import marshmallow.validate
import yaml
from loguru import logger
from marshmallow_dataclass import class_schema


@dataclass()
class DataParams:
    raw_data_path: str
    train_data_path: str
    test_data_path: str
    n_samples: int = field(
        default=100, metadata={"validate": marshmallow.validate.Range(min=1)}
    )
    n_features: int = field(
        default=10, metadata={"validate": marshmallow.validate.Range(min=1)}
    )
    test_size: float = field(
        default=0.3, metadata={"validate": marshmallow.validate.Range(min=0.001)}
    )
    n_classes: int = field(
        default=2, metadata={"validate": marshmallow.validate.Range(min=2)}
    )
    n_clusters_per_class: int = field(
        default=2, metadata={"validate": marshmallow.validate.Range(min=2)}
    )
    n_informative: int = field(
        default=2, metadata={"validate": marshmallow.validate.Range(min=2)}
    )


@dataclass()
class TrainParams:
    model_path: str
    metrics_path: str


@dataclass()
class ModelParams:
    model_type: str = field(
        default="LogisticRegression",
        metadata={
            "validate": marshmallow.validate.OneOf(
                [
                    "LogisticRegression",
                    "RandomForestClassifier",
                    "DecisionTreeClassifier",
                ]
            )
        },
    )
    penalty: str = field(
        default="l2",
        metadata={
            "validate": marshmallow.validate.OneOf(["l2", "l1", "elasticnet", "none"])
        },
    )
    n_estimators: int = field(
        default=50, metadata={"validate": marshmallow.validate.Range(min=1)}
    )
    criterion: str = field(
        default="gini",
        metadata={"validate": marshmallow.validate.OneOf(["gini", "entropy"])},
    )
    max_depth: int = field(
        default=None, metadata={"validate": marshmallow.validate.Range(min=1)}
    )


@dataclass()
class PipelineParams:
    train_params: TrainParams
    data_params: DataParams
    random_state: int
    model_params: ModelParams
    prediction_path: str


PipelineParamsSchema = class_schema(PipelineParams)


def read_pipeline_params(path: str) -> PipelineParams:
    with open(path, "r") as input_stream:
        schema = PipelineParamsSchema()
        return schema.load(yaml.safe_load(input_stream))


def validation(params):
    if (
        params.data_params.n_classes * params.data_params.n_clusters_per_class
        > 2**params.data_params.n_informative
    ):
        logger.exception(
            f"n_classes ({params.data_params.n_classes}) *"
            f" n_clusters_per_class ({params.data_params.n_clusters_per_class}) "
            f"must be smaller or equal to 2^n_informative"
            f" ({2 ** params.data_params.n_informative})."
        )
        sys.exit(
            f"n_classes ({params.data_params.n_classes}) * "
            f"n_clusters_per_class ({params.data_params.n_clusters_per_class}) "
            f"must be smaller or equal to 2^n_informative"
            f" ({2 ** params.data_params.n_informative})."
        )
