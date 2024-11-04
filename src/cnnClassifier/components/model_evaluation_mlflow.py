import tensorflow as tf
from cnnClassifier.entity.config_entity import EvaluationConfig
from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.utils.helper import load_model,save_score,save_json
import mlflow
import mlflow.keras
from urllib.parse import urlparse
import keras
from pathlib import Path



class Evaluation:
    def __init__(self,config:EvaluationConfig):
        self.config=config

    def valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

    def evaluation(self):
        self.model= load_model(self.config.path_to_model)
        self.valid_generator()
        self.score= self.model.evaluate(self.valid_generator)
        save_score(self.score)


    def log_into_mlflow(self):
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        
        with mlflow.start_run():
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics(
                {"loss": self.score[0], "accuracy": self.score[1]}
            )
            if tracking_url_type_store != "file":
                mlflow.keras.log_model(self.model, "model", registered_model_name="VGG16Model")
            else:
                mlflow.keras.log_model(self.model, "model")
    


