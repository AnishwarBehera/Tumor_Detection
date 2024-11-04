
from flask import Flask, request, jsonify, render_template,send_from_directory,make_response
import os
from flask_cors import CORS, cross_origin
from cnnClassifier.utils.helper import decodeImage
from cnnClassifier.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg" 
        self.classifier = PredictionPipeline(self.filename)



clApp = ClientApp()

@app.route("/samples/<category>/<filename>")
@cross_origin()
def sample_images(category,filename):
    sample_folder=os.path.join(app.root_path,'templates','samples',category)
    return send_from_directory(sample_folder, filename)

# @app.route("/samples/<category>/<filename>")
# def sample_images(category, filename):
#     sample_folder = os.path.join(app.root_path, 'templates', 'samples', category)
#     response = make_response(send_from_directory(sample_folder, filename))
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '0'
#     return response

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    sample_folders=os.path.join(app.root_path, 'templates', 'samples')
    tumor_images=os.listdir(os.path.join(sample_folders, 'tumor'))
    normal_images=os.listdir(os.path.join(sample_folders, 'normal'))


    return render_template(
        'index.html',
        tumor_images=tumor_images,
        normal_images=normal_images,
        tumor_path='tumor',
        normal_path='normal')


@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRoute():
    os.system("python main.py")
    # os.system("dvc repro")  # Uncomment if using DVC for reproducibility
    return "Training done successfully!"

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    try:
        
        image_file = request.files.get('image')
        if image_file is None:
            return jsonify({'error': 'No image file provided'}), 400

        filename = "inputImage.jpg"
        image_file.save(filename)

        clApp.classifier.filename = filename
        result = clApp.classifier.predict()

        # print(f"Prediction result: {result}")

        return jsonify(result)
    except Exception as e:
        error_message = f"Error occurred during prediction: {e}"
        # print(error_message) 
        return jsonify({'error': error_message}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

