from flask import Flask
from .extensions import api
from .logic import UPLOAD_FOLDER
from flask_cors import CORS
from .cnn import ns_cnn
from .mobileNetV2 import ns_mobileNetV2
from .inceptionResNetV2 import ns_inceptionResNetV2


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    api.init_app(app)
    
    api.add_namespace(ns_cnn)
    api.add_namespace(ns_mobileNetV2)
    api.add_namespace(ns_inceptionResNetV2)
    
    return app