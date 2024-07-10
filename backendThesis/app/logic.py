import os
import numpy as np
import pandas as pd
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import scipy
import json


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def clear_uploads_folder():
    folder_path = 'uploads'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(uploaded_file):
    filename = secure_filename(uploaded_file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    uploaded_file.save(file_path)
    return file_path


def load_cnn_model_category():
    model_category = load_model('CNN Models\CNN_model_26032024_3epochs.keras')
    return model_category


def load_cnn_model_article_type():
    model_article_type = load_model('CNN Models\CNN_model_articles_10epochs_26032024.keras')
    return model_article_type


def load_mobileNetV2_model_category():
    model_category = load_model('MobileNetV2 Models\MobileNetV2_model_20042024_3epochs.keras')
    return model_category


def load_mobileNetV2_model_article_type():
    model_article_type = load_model('MobileNetV2 Models\MobileNetV2_model_20042024_10epochs_article_type.keras')
    return model_article_type


def load_inceptionResNetV2_model_category():
    model_category = load_model('InceptionResNetV2 Models\InceptionResNetV2_model_13052024_3epochs_category.keras')
    return model_category


def load_inceptionResNetV2_model_article_type():
    model_article_type = load_model('InceptionResNetV2 Models\InceptionResNetV2_model_13052024_10epochs_article_type.keras')
    return model_article_type


def predict_image_category_with_dynamic_labels(image_path, model, train_generator):
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    
    # getting the index of the class with the highest probability
    predicted_class = np.argmax(predictions[0]) 
    
    # generating a mapping of class indices to category labels
    class_labels = {i: label for i, label in enumerate(train_generator.class_indices.keys())}

    # getting the corresponding label using the class index
    predicted_label = class_labels[predicted_class]  
    
    # computing the confidence score of the prediction
    confidence = predictions[0][predicted_class]  
    
    return predicted_label, confidence, img_array


def preprocess_image(image_path, target_size=(224, 224)):
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0 
    return img_array


def parse_images_in_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.webp', '.hpg', '.png'))]
    images_data = []
    for file in image_files:
        image_path = os.path.join(folder_path, file)
        images_data.append(image_path)
        
    return images_data


def get_train_generator_category():
    train_data = pd.read_csv('train_data.csv')

    img_width, img_height = 224, 224
    batch_size = 32

    train_datagen = ImageDataGenerator(rescale=1./255,
                                    shear_range=0.2,
                                    zoom_range=0.2,
                                    horizontal_flip=True)

    train_data['id'] = train_data['id'].astype(str) + '.jpg'

    train_generator_category = train_datagen.flow_from_dataframe(
        dataframe=train_data,
        directory='filtered_images',
        x_col="id",
        y_col="subCategory",
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True) 

    return train_generator_category


def get_test_generator_category():
    test_data = pd.read_csv('test_data.csv')

    img_width, img_height = 224, 224
    batch_size = 32

    test_datagen = ImageDataGenerator(rescale=1./255)

    test_data['id'] = test_data['id'].astype(str) + '.jpg'

    test_generator_category = test_datagen.flow_from_dataframe(
        dataframe=test_data,
        directory='filtered_images',
        x_col="id",
        y_col="subCategory",
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False) 

    return test_generator_category


def get_train_generator_article_type():
    train_data = pd.read_csv('train_data.csv')

    img_width, img_height = 224, 224
    batch_size = 32

    train_datagen = ImageDataGenerator(rescale=1./255,
                                    shear_range=0.2,
                                    zoom_range=0.2,
                                    horizontal_flip=True)

    train_data['id'] = train_data['id'].astype(str) + '.jpg'

    train_generator_article_type = train_datagen.flow_from_dataframe(
        dataframe=train_data,
        directory='filtered_images',
        x_col="id",
        y_col="articleType",
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True) 

    return train_generator_article_type


def get_test_generator_article_type():
    test_data = pd.read_csv('test_data.csv')

    img_width, img_height = 224, 224
    batch_size = 32

    test_datagen = ImageDataGenerator(rescale=1./255)

    test_data['id'] = test_data['id'].astype(str) + '.jpg'

    test_generator_article_type = test_datagen.flow_from_dataframe(
        dataframe=test_data,
        directory='filtered_images',
        x_col="id",
        y_col="articleType",
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False) 

    return test_generator_article_type


def predict_image(model_category, model_article_type):
    train_generator_category = get_train_generator_category()
    train_generator_article_type = get_train_generator_article_type()

    images_folder_path = 'uploads'
    images_data = parse_images_in_folder(images_folder_path)
    
    predicted_categories = []
    confidences_categories = []
    predicted_article_types = []
    confidences_article_types = []

    for image_path in images_data:
        predicted_category, confidence_category, img_array = predict_image_category_with_dynamic_labels(image_path, model_category, train_generator_category)
        predicted_article_type, confidence_article_type, _ = predict_image_category_with_dynamic_labels(image_path, model_article_type, train_generator_article_type)
    
        predicted_categories.append(predicted_category)
        confidences_categories.append(float(confidence_category))
        predicted_article_types.append(predicted_article_type)
        confidences_article_types.append(float(confidence_article_type))
        
        print("predicted_category: ", predicted_categories[0])
        print("confidence_category: ", confidences_categories[0])
        print("predicted_article_type: ", predicted_article_types[0])
        print("confidence_article_type: ", confidences_article_types[0])
    
        return {
            "predicted_category": predicted_categories[0],
            "confidence_category": confidences_categories[0],
            "predicted_article_type": predicted_article_types[0],
            "confidence_article_type": confidences_article_types[0]
        }


def calculate_accuracy_per_subcategory(test_generator, model):
    # converting class_labels to a list
    class_labels = list(test_generator.class_indices.keys())

    # predicting probabilities for the test set
    predictions = model.predict(test_generator)

    # getting the predicted labels for each image
    predicted_labels = [class_labels[i] for i in np.argmax(predictions, axis=1)]

    # getting the true labels for each image
    true_labels = [class_labels[i] for i in test_generator.classes]

    # initializing a dictionary to store the counts of correct predictions and total the counts for each subcategory
    subcategory_counts = {class_label: [0, 0] for class_label in class_labels}

    # iterating through each prediction and updating the counts
    for true_label, predicted_label in zip(true_labels, predicted_labels):
        subcategory_counts[true_label][1] += 1
        if true_label == predicted_label:
            subcategory_counts[true_label][0] += 1

    # calculating the accuracy for each subcategory
    subcategory_accuracies = {class_label: (count[0] / count[1]) if count[1] != 0 else 0 for class_label, count in subcategory_counts.items()}

    output = {}
    for class_label, accuracy in subcategory_accuracies.items():
        output[class_label] = accuracy

    return output


def calculate_accuracy_per_subcategory_and_save(test_generator, model, output_file):
    output = calculate_accuracy_per_subcategory(test_generator, model)
    
    with open(output_file, 'w') as f:
        json.dump(output, f)

    return output


def modify_accuracy_keys(accuracies):
    modified_accuracies = {}
    for key, value in accuracies.items():
        modified_key = key.lower().replace(' ', '_')
        modified_accuracies[modified_key] = round(value, 3)
    
    return modified_accuracies
