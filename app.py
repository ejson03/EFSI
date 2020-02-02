import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model, model_from_json
from tensorflow.keras.preprocessing import image

# Some utilites
import numpy as np
from datetime import date


# Declare a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/tomato_model.h5'
MODEL_JSON = 'models/tomato_model.json'
# with open(MODEL_JSON, 'r') as jsonf:
#     model = jsonf.read()
#     model = model_from_json(model)
#     model.load_weights(MODEL_PATH)
model = load_model(MODEL_PATH, custom_objects={'KerasLayer':hub.KerasLayer})
model.summary()
classes = ['Tomato___Bacterial_spot' ,  'Tomato___Septoria_leaf_spot',
    'Tomato___Early_blight',    'Tomato___Spider_mites_Two-spotted_spider_mite',
    'Tomato___healthy',         'Tomato___Target_Spot',
    'Tomato___Late_blight',     'Tomato___Tomato_mosaic_virus',
    'Tomato___Leaf_Mold',       'Tomato___Tomato_Yellow_Leaf_Curl_Virus']

def model_predict(img, model):
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x, mode='tf')
    preds = model.predict(x)
   
    return preds


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET'])
def predict():
    today = date.today()
    img_path = os.path.join(f'{today.day}-{today.month}',os.listdir(f'{today.day}-{today.month}')[0])
    img = image.load_img(img_path)
    preds = model_predict(img, model)   
    pred_class = classes[np.argmax(preds)] 
    result = pred_class.replace('_', ' ').capitalize()
    return jsonify(result=result, img=img_path)



if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    predict()
