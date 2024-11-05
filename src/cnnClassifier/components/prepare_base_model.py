
import os
import tensorflow as tf
from cnnClassifier.entity.config_entity import PrepareBaseModelConfig
from cnnClassifier.utils.helper import save_model
from tensorflow.keras.metrics import Precision, Recall

class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config
    
    def get_base_model(self):
        self.model = tf.keras.applications.vgg16.VGG16(
            input_shape=self.config.params_image_size,
            weights=self.config.params_weights,
            include_top=self.config.params_include_top
        )
        save_model(path=self.config.base_model_path, model=self.model)
    
    @staticmethod
    def prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate, dropout_rate=0.5):
        if freeze_all:
            for layer in model.layers:
                layer.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                layer.trainable = False

        flatten_in = tf.keras.layers.Flatten()(model.output)
        dense_layer = tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))(flatten_in)
        batch_norm_layer = tf.keras.layers.BatchNormalization()(dense_layer)
        dropout_layer = tf.keras.layers.Dropout(dropout_rate)(batch_norm_layer)

        prediction = tf.keras.layers.Dense(units=classes, activation="softmax")(dropout_layer)

        full_model = tf.keras.models.Model(inputs=model.input, outputs=prediction)

        full_model.compile(
            optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy", Precision(name="precision"), Recall(name="recall")]
        )

        full_model.summary()
        print(full_model.summary())
        return full_model
    
    def update_base_model(self):
        self.full_model = self.prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,  
            freeze_all=True,
            # freeze_till=None,
            freeze_till=10,
            learning_rate=self.config.params_learning_rate,
            dropout_rate=0.5
        )

        save_model(path=self.config.updated_base_model_path, model=self.full_model)
