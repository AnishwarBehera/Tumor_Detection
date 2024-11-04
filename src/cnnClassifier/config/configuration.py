from cnnClassifier.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, MLFLOW_SECRETS_PATH
from cnnClassifier.utils.helper import read_yaml, create_directories
from cnnClassifier.entity.config_entity import DataIngestionConfig,PrepareBaseModelConfig,TrainingConfig,EvaluationConfig
from pathlib import Path
import os

class ConfigurationManager:
    def __init__(self, config_filepath=Path(CONFIG_FILE_PATH), params_filepath=Path(PARAMS_FILE_PATH),mlflow_secrets=Path(MLFLOW_SECRETS_PATH)):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.mlflow=read_yaml(mlflow_secrets)
        create_directories([self.config.artifact_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_url=config.source_url,
            local_data_file=Path(config.local_data_file),
            unzip_dir=Path(config.unzip_dir)
        )

        return data_ingestion_config

    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model
        
        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_classes=self.params.CLASSES
        )

        return prepare_base_model_config
    

    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        params = self.params
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, "kidney-ct-scan-image")
        create_directories([
            Path(training.root_dir)
        ])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            updated_base_model_path=Path(prepare_base_model.updated_base_model_path),
            training_data=Path(training_data),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE
        )

        return training_config
    

    def get_evaluation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_to_model="artifact/training/model.h5",
            training_data="artifact/data_ingestion/kidney-ct-scan-image",
            mlflow_uri=self.mlflow.MLFLOW_TRACKING_URI,
            all_params=self.params,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )
        return eval_config