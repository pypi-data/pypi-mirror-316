import pandas as pd
import typer
from loguru import logger
from sklearn import datasets, model_selection

from my_module.data_params import PipelineParams, read_pipeline_params, validation

# from src.entities.params import read_pipeline_params

app = typer.Typer()


@app.command()
def main(params_path: str):
    params = read_pipeline_params(params_path)
    validation(params)
    data = generate_data(params)
    spliting(data, params)


def generate_data(params: PipelineParams) -> pd.DataFrame:
    x, y = datasets.make_classification(
        n_samples=params.data_params.n_samples,
        n_features=params.data_params.n_features,
        n_classes=params.data_params.n_classes,
        random_state=params.random_state,
        n_informative=params.data_params.n_informative,
        n_clusters_per_class=params.data_params.n_clusters_per_class,
    )

    data = pd.DataFrame(
        x, columns=[f"feature_{i}" for i in range(params.data_params.n_features)]
    )
    data["target"] = y
    logger.info(f"Got data with shape: {data.shape}")
    return data


def spliting(
    data: pd.DataFrame, params: PipelineParams
) -> tuple[pd.DataFrame, pd.DataFrame]:

    train, test = model_selection.train_test_split(
        data, test_size=params.data_params.test_size, random_state=params.random_state
    )
    logger.info(f"Split data into train ({train.shape}) and test ({test.shape})")

    train.to_csv(params.data_params.train_data_path, index=False)
    logger.info(f"Save train sample to the path: {params.data_params.train_data_path}")

    test.to_csv(params.data_params.test_data_path, index=False)
    logger.info(f"Save test sample to the path: {params.data_params.test_data_path}")
    return train, test


if __name__ == "__main__":
    app()
