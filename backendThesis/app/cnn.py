from flask_restx import Resource, Namespace, reqparse
from .logic import predict_image, clear_uploads_folder, allowed_file, save_uploaded_file, load_cnn_model_category, load_cnn_model_article_type, get_train_generator_category, calculate_accuracy_per_subcategory, calculate_accuracy_per_subcategory_and_save, get_test_generator_category, get_test_generator_article_type, modify_accuracy_keys
from .api_models import prediction_model, accuracy_per_category_model, accuracy_per_article_type_model
from flask import request
from werkzeug.datastructures import FileStorage
from keras.models import load_model
import pandas as pd
import json
import os

ns_cnn = Namespace("apiCnnModels", description="Predicting clothing and article types based on a Convolutional Neutral Network (CNN) Model trained from scratch")

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


@ns_cnn.route("/cnnModel")
class CnnPrediction(Resource):

    @ns_cnn.expect(upload_parser)
    @ns_cnn.marshal_with(prediction_model)
    @ns_cnn.response(200, "The request has been fulfilled")
    @ns_cnn.response(400, "Invalid file type")
    @ns_cnn.response(500, "Something went wrong")
    def post(self):
        clear_uploads_folder()
        args = upload_parser.parse_args()
        uploaded_file = args['file']

        if uploaded_file and allowed_file(uploaded_file.filename):
            file_path = save_uploaded_file(uploaded_file)
            model_category = load_cnn_model_category()
            model_article_type = load_cnn_model_article_type()
            prediction = predict_image(model_category, model_article_type)
            return prediction, 200
        else:
            return {"message": "Invalid file type. Allowed types: png, jpg, jpeg, gif, webp"}, 400
    
    
@ns_cnn.route("/accuracyPerCategory")
class AccuracyPerCategory(Resource):
    
    @ns_cnn.response(200, "Accuracy calculated successfully")
    @ns_cnn.response(500, "Error occurred during accuracy calculation")
    def get(self):
        try:
            test_generator = get_test_generator_category()
            model_category = load_cnn_model_category()
            output_file = 'accuracies/accuracy_cnn_model_category.json'
            accuracies = calculate_accuracy_per_subcategory_and_save(test_generator, model_category, output_file)
            return accuracies, 200
        except Exception as e:
            return {"message": str(e)}, 500
        
        
@ns_cnn.route("/accuracyPerCategoryFromLocalFile")
class AccuracyPerCategoryFromLocalFile(Resource):
    
    @ns_cnn.marshal_with(accuracy_per_category_model)
    @ns_cnn.response(200, "Accuracy loaded successfully")
    @ns_cnn.response(500, "Error occurred during loading accuracy")
    def get(self):
        try:
            with open('accuracies/accuracy_cnn_model_category.json', 'r') as f:
                accuracies = json.load(f)
                
            modified_accuracies = modify_accuracy_keys(accuracies)
                
            return modified_accuracies, 200
        except Exception as e:
            return {"message": str(e)}, 500
        
        
@ns_cnn.route("/accuracyPerArticleType")
class AccuracyPerArticleType(Resource):
    
    @ns_cnn.response(200, "Accuracy calculated successfully")
    @ns_cnn.response(500, "Error occurred during accuracy calculation")
    def get(self):
        try:
            test_generator = get_test_generator_article_type()
            model_category = load_cnn_model_article_type()
            output_file = 'accuracies/accuracy_cnn_model_article_type.json'
            accuracies = calculate_accuracy_per_subcategory_and_save(test_generator, model_category, output_file)
            return accuracies, 200
        except Exception as e:
            return {"message": str(e)}, 500
        
        
@ns_cnn.route("/accuracyPerArticleTypeFromLocalFile")
class AccuracyPerArticleTypeFromLocalFile(Resource):
    
    @ns_cnn.marshal_with(accuracy_per_article_type_model)
    @ns_cnn.response(200, "Accuracy loaded successfully")
    @ns_cnn.response(500, "Error occurred during loading accuracy")
    def get(self):
        try:
            with open('accuracies/accuracy_cnn_model_article_type.json', 'r') as f:
                accuracies = json.load(f)
            
            modified_accuracies = modify_accuracy_keys(accuracies)
                
            return modified_accuracies, 200
        except Exception as e:
            return {"message": str(e)}, 500
        