import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename
    
    def predict(self):
        try:
            model_path = os.path.join('artifact/training', 'base_model_updated.h5')
            model = load_model(model_path)

            imagename = self.filename
            test_image = image.load_img(imagename, target_size=(224, 224))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)

            result = np.argmax(model.predict(test_image), axis=1)

            if result[0] > 0.5 :
                prediction = 'Tumor'
            else:
                prediction = 'Normal'
            print(f"result {result[0]}")

            return {'prediction': prediction} 
        except Exception as e:
            print(f"Error occurred during prediction: {e}")
            return {'error': str(e)}
