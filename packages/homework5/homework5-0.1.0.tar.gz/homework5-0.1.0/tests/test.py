import pandas as pd

from my_module.data_params import read_pipeline_params
from my_module.dataset import generate_data, spliting
from my_module.train import choose_model, training


def test_param():
    a = read_pipeline_params("tests/test_params.yaml")
    assert a.data_params.n_samples == 100


def test_shape():
    a = read_pipeline_params("tests/test_params.yaml")
    data = generate_data(a)
    assert data.shape == (a.data_params.n_samples, a.data_params.n_features + 1)


def test_tain_test_split():
    params = read_pipeline_params("tests/test_params.yaml")
    data = generate_data(params)
    train, test = spliting(data, params)
    assert train.shape == (70, 31)
    assert test.shape == (30, 31)


def test_model_type():
    params = read_pipeline_params("tests/test_params.yaml")
    train = pd.read_csv(params.data_params.train_data_path)
    X_train = train.drop("target", axis=1)
    y_train = train["target"].values.reshape(-1, 1)
    test = pd.read_csv(params.data_params.test_data_path)
    X_test = test.drop("target", axis=1)
    y_test = test["target"].values.reshape(-1, 1)
    model, y_train, y_test = choose_model(params, y_train, y_test)
    assert type(model).__name__ == params.model_params.model_type
