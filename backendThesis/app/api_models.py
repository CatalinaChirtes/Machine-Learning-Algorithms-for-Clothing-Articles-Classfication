from flask_restx import fields
from .extensions import api


prediction_model = api.model('PredictionModel', 
{
    'predicted_category': fields.String(description='Predicted clothing category'),
    'confidence_category': fields.Float(description='Confidence score for predicted category'),
    'predicted_article_type': fields.String(description='Predicted article type'),
    'confidence_article_type': fields.Float(description='Confidence score for predicted article type')
})


accuracy_per_category_model = api.model('AccuracyPerCategoryModel',
{
    'bags': fields.Float(description='Accuracy for Bags category'),
    'bottomwear': fields.Float(description='Accuracy for Bottomwear category'),
    'dress': fields.Float(description='Accuracy for Dress category'),
    'shoes': fields.Float(description='Accuracy for Shoes category'),
    'topwear': fields.Float(description='Accuracy for Topwear category')
})


accuracy_per_article_type_model = api.model('AccuracyPerArticleTypeModel',
{
    'backpacks': fields.Float(description='Accuracy for Backpacks category'),
    'capris': fields.Float(description='Accuracy for Capris category'),
    'casual_shoes': fields.Float(description='Accuracy for Casual Shoes category'),
    'clutches': fields.Float(description='Accuracy for Clutches category'),
    'dresses': fields.Float(description='Accuracy for Dresses category'),
    'flats': fields.Float(description='Accuracy for Flats category'),
    'flip_flops': fields.Float(description='Accuracy for Flip Flops category'),
    'formal_shoes': fields.Float(description='Accuracy for Formal Shoes category'),
    'handbags': fields.Float(description='Accuracy for Handbags category'),
    'heels': fields.Float(description='Accuracy for Heels category'),
    'jackets': fields.Float(description='Accuracy for Jackets category'),
    'jeans': fields.Float(description='Accuracy for Jeans category'),
    'laptop_bag': fields.Float(description='Accuracy for Laptop Bag category'),
    'leggings': fields.Float(description='Accuracy for Leggings category'),
    'sandals': fields.Float(description='Accuracy for Sandals category'),
    'shirts': fields.Float(description='Accuracy for Shirts category'),
    'shorts': fields.Float(description='Accuracy for Shorts category'),
    'skirts': fields.Float(description='Accuracy for Skirts category'),
    'sports_shoes': fields.Float(description='Accuracy for Sports Shoes category'),
    'sweaters': fields.Float(description='Accuracy for Sweaters category'),
    'tops': fields.Float(description='Accuracy for Tops category'),
    'track_pants': fields.Float(description='Accuracy for Track Pants category'),
    'trousers': fields.Float(description='Accuracy for Trousers category'),
    'tshirts': fields.Float(description='Accuracy for Tshirts category')
})