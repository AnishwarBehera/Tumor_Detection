
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename
        self.model_path = os.path.join('artifact/training', 'model.h5')
        self.model = load_model(self.model_path)  
    
    def predict(self):
        try:
                img_path = self.filename
                img = image.load_img(img_path, target_size=(224, 224))  
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)  
                img_array = img_array / 255.0  

                # Perform prediction
                predictions = self.model.predict(img_array)[0]
                print(f"Prediction probabilities: {predictions}")


                if np.argmax(predictions) == 1:
                    result = "Tumor"
                else:
                    result = "Normal"

                return {"prediction": result, "probabilities": predictions.tolist()}
            
        except Exception as e:
                print(f"Error occurred during prediction: {e}")
                return {"error": str(e)}
