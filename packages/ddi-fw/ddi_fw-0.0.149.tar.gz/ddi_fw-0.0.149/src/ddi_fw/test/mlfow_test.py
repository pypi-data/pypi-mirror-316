# import mlflow
# from mlflow import tensorflow
# mlflow.set_tracking_uri("sqlite:///mlflow.db")
# mlflow.set_experiment("multi-class-ddi-classification")


# def mlp_mlflow_run(
#     name,
#     model_params,
#     train_params,
#     train_dataset,
#     val_dataset,
#     test_dataset,
#     y_test,
# ):
#     with mlflow.start_run(run_name=name):
#         mlflow.log_params(model_params)
#         mlflow.log_params(train_params)
#         mlflow.set_tag("model_name", "MLP")

         


#         mlflow.log_metric("accuracy", accuracy)
#         mlflow.tensorflow.log_model(mlp, "tf_models") #folder

import mlflow
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.datasets import fetch_california_housing
import tensorflow_addons as tfa

from tensorflow.keras.callbacks import EarlyStopping
 

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns

from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import MeanSquaredError


mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("income")


dset = fetch_california_housing()
data = dset['data']
y = dset['target']
LABEL = dset['target_names'][0]

NUMERIC_FEATURES = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Longitude', 'Latitude']
FEATURES = NUMERIC_FEATURES

data = pd.DataFrame(data, columns=dset['feature_names'])
data[LABEL] = y

data.head()

train_data, test_data = train_test_split(data, test_size=0.2)
print(f"Train dataset shape: {train_data.shape}")
print(f"Test dataset shape: {test_data.shape}")


X_train, X_val = train_test_split(train_data, test_size=0.2)

sc = StandardScaler()
X_train.loc[:, NUMERIC_FEATURES] = sc.fit_transform(X_train[NUMERIC_FEATURES])
X_val.loc[:, NUMERIC_FEATURES] = sc.transform(X_val[NUMERIC_FEATURES])
test_data.loc[:, NUMERIC_FEATURES] = sc.transform(test_data[NUMERIC_FEATURES])


def build_mlp(params):
    mlp = Sequential([
        Dense(params["layer1_size"], activation=params['activation']),
        Dropout(params['dropout_rate']),
        Dense(params["layer2_size"], activation=params['activation']),
        Dropout(params['dropout_rate']),
        Dense(params["layer3_size"], activation=params['activation']),
        Dense(1, activation='relu')
    ])
    return mlp

def train_mlp(mlp, train_params, train_dataset, val_dataset):
    optimizer = tfa.optimizers.AdamW(
        learning_rate=train_params["learning_rate"],
        weight_decay=train_params["weight_decay"],
    )
    mlp.compile(
        optimizer=optimizer,
        loss=MeanSquaredError(name="mse"),
        metrics=[tf.keras.metrics.RootMeanSquaredError(name="rmse")]
    )

    early = EarlyStopping(
        monitor="val_loss",
        mode="min",
        patience=train_params["early_stop_patience"],
        restore_best_weights=True,
    )
    callback_list = [early]

    hist = mlp.fit(
        train_dataset,
        epochs=train_params["num_epochs"],
        validation_data=val_dataset,
        callbacks=callback_list,
    )
    return mlp


def mlp_mlflow_run(
    name,
    mlp_params,
    train_params,
    train_dataset,
    val_dataset,
    test_dataset,
    y_test,
):
    with mlflow.start_run(run_name=name):
        mlflow.log_params(mlp_params)
        mlflow.log_params(train_params)
        mlflow.set_tag("model_name", "MLP")
        mlp = build_mlp(mlp_params)
        mlp = train_mlp(mlp, train_params, train_dataset, val_dataset)
        test_preds = mlp.predict(test_dataset)
        test_rms = mean_squared_error(
            y_test, test_preds.ravel(), squared=False
        )
        mlflow.log_metric("test_rmse", test_rms)
        mlflow.tensorflow.log_model(mlp, "tf_models")

        
# To TF Dataset
mlp_train_ds = tf.data.Dataset.from_tensor_slices((X_train[FEATURES], X_train[LABEL])).batch(512).shuffle(512*4).prefetch(512)
mlp_val_ds = tf.data.Dataset.from_tensor_slices((X_val[FEATURES], X_val[LABEL])).batch(512).shuffle(512*4).prefetch(512)
mlp_test_ds = tf.data.Dataset.from_tensor_slices(test_data[FEATURES]).batch(512).prefetch(512)

mlp_params = {
    "layer1_size": 512,
    "layer2_size": 128,
    "layer3_size": 64,
    "dropout_rate": 0.3,
    "activation": 'relu'

}
train_params = dict(
    learning_rate=0.001, weight_decay=0.00001, early_stop_patience=10, num_epochs=1000
)

mlp_mlflow_run(
    "mlp_base",
    mlp_params,
    train_params,
    mlp_train_ds,
    mlp_val_ds,
    mlp_test_ds,
    test_data[LABEL],
)