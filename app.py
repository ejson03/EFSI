import os
import sys
import json

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
import owncloud
import urllib.request

# Declare a flask app
app = Flask(__name__)

with open('credentials.txt','r') as f:
    f = f.read()
    username, password = f.split(' ')

def setup():
    today = date.today()
    oc = owncloud.Client('http://localhost/owncloud')
    oc.login(username, password)
    file = f'{today.day}-{today.month}/image.jpg'
    link_info = oc.share_file_with_link(f'{file}')
    link = link_info.get_link()[-15:]
    link = f'http://localhost/owncloud/index.php/apps/files_sharing/ajax/publicpreview.php?x=1920&y=505&a=true&file=image.jpg&t={link}&scalingup=0'
    return link

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
    #ztoday = date.today()
    #img_path = os.path.join(f'{today.day}-{today.month}',os.listdir(f'{today.day}-{today.month}')[0])
    link, url= setup()
    if os.path.exists(f'{today.day}-{today.month}'):
        os.mkdir(f'{today.day}-{today.month}')
        os.chdir(f'{today.day}-{today.month}')

    img = image.load_img(img_path)
    preds = model_predict(img, model)   
    pred_class = classes[np.argmax(preds)] 
    result = pred_class.replace('_', ' ').capitalize()
    link=setup()
    return render_template('index.html',user_image= link,response=json.dumps(result))


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    index()
    #app.run(debug=True)
