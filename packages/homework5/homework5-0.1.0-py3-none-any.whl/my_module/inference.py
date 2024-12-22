import pickle

import pandas as pd
import typer
from loguru import logger

from my_module.data_params import read_pipeline_params

app = typer.Typer()


@app.command()
def main(params_path):
    params = read_pipeline_params(params_path)
    model_path = params.train_params.model_path

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    data = pd.read_csv("data/raw/new_data.csv")
    x_new = data.drop(["target"], axis=1)
    predictions = model.predict(x_new)
    logger.success(f"Prediction completed for {len(predictions)} samples")
    df = pd.DataFrame(predictions, columns=["prediction"])
    df.to_csv(params.prediction_path, index=False)


if __name__ == "__main__":
    app()
