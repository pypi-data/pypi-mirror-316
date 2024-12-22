import json
import pickle

import pandas as pd
import sklearn
import typer
from loguru import logger
from sklearn import ensemble
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from my_module.data_params import PipelineParams, read_pipeline_params

app = typer.Typer()


@app.command()
def main(params_path: str):

    params = read_pipeline_params(params_path)
    train = pd.read_csv(params.data_params.train_data_path)
    x_train = train.drop("target", axis=1)
    y_train = train["target"].values.reshape(-1, 1)

    test = pd.read_csv(params.data_params.test_data_path)
    x_test = test.drop("target", axis=1)
    y_test = test["target"].values.reshape(-1, 1)
    model, y_train, y_test = choose_model(params, y_train, y_test)
    print(type(model).__name__)
    training(model, params, x_train, y_train, x_test, y_test)


def choose_model(params: PipelineParams, y_train, y_test):
    if params.model_params.model_type == "RandomForestClassifier":
        model = ensemble.RandomForestClassifier(
            n_estimators=params.model_params.n_estimators
        )
        y_train = y_train.flatten()
        y_test = y_test.flatten()

    elif params.model_params.model_type == "LogisticRegression":
        model = LogisticRegression(
            random_state=params.random_state, penalty=params.model_params.penalty
        )
        y_train = y_train.flatten()
        y_test = y_test.flatten()

    else:
        model = DecisionTreeClassifier(
            random_state=params.random_state,
            max_depth=params.model_params.max_depth,
            criterion=params.model_params.criterion,
        )
    return model, y_train, y_test


def training(model, params, x_train, y_train, x_test, y_test):

    model.fit(x_train, y_train)
    logger.info(f"Learn model {model}")

    y_test_pred = model.predict_proba(x_test)[:, 1]
    roc_auc = sklearn.metrics.roc_auc_score(y_test, y_test_pred)
    logger.info(f"Got ROC-AUC {roc_auc:.3f}")

    metrics = {"roc-auc": roc_auc}

    with open(params.train_params.model_path, "wb") as fin:
        pickle.dump(model, fin)
    logger.info(f"Saved model to path {params.train_params.model_path}")

    with open(params.train_params.metrics_path, "w") as fin:
        json.dump(metrics, fin)
    logger.info(f"Saved metrics to path {params.train_params.metrics_path}")
    return y_test_pred


if __name__ == "__main__":
    app()
