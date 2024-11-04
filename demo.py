


import os
import yaml
import mlflow

# Load MLflow configuration from YAML file
with open("mlflow.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

os.environ["MLFLOW_TRACKING_URI"] = config["MLFLOW_TRACKING_URI"]
os.environ["MLFLOW_TRACKING_USERNAME"] = config["MLFLOW_TRACKING_USERNAME"]
os.environ["MLFLOW_TRACKING_PASSWORD"] = config["MLFLOW_TRACKING_PASSWORD"]



print("Current MLflow tracking URI:", mlflow.get_tracking_uri())

