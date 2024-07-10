from PIL import Image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import os

def preprocess_image(image):
    # Converting the image to grayscale
    image = image.convert('L')
    # Resizing the image to 28x28 (similar to training data)
    image = image.resize((28, 28))
    # Converting the image to numpy array and normalizing the pixel values
    image_array = np.array(image)
    image_array = image_array.astype('float32') / 255.0
    # Expanding the dimensions to match the shape of the training data
    image_array = np.expand_dims(image_array, axis=0)
    image_array = np.expand_dims(image_array, axis=-1)
    return image_array

def load_model(model_path):
    # Loading the saved model
    loaded_model = tf.keras.models.load_model(model_path)
    return loaded_model

def predict_image(model, image_array, label_mapping):
    # Making predictions on the image
    predictions = model.predict(image_array)
    # Getting the predicted label and probability
    predicted_label = np.argmax(predictions)
    probability = predictions[0, predicted_label]
    predicted_clothing = label_mapping[predicted_label]
    return predicted_label, probability, predicted_clothing

# Defining a dictionary to map the labels to clothing types
label_to_clothing = {
    0: 'T-shirt/top',
    1: 'Trouser',
    2: 'Pullover',
    3: 'Dress',
    4: 'Coat',
    5: 'Sandal',
    6: 'Shirt',
    7: 'Sneaker',
    8: 'Bag',
    9: 'Ankle boot'
}

def parse_images_in_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.webp', '.hpg'))]
    images_data = []
    for file in image_files:
        image_path = os.path.join(folder_path, file)
        image = Image.open(image_path)
        preprocessed_image = preprocess_image(image)
        images_data.append((image, preprocessed_image))
    return images_data

# Loading the saved model
model_path = 'keras_early_stop_CNN\keras_fashion_mnist_early_stopping_14.keras'
model = load_model(model_path)

# Path to the folder containing images
images_folder_path = 'cloth_dataset/'

# Parsing the images in the folder
images_data = parse_images_in_folder(images_folder_path)

# Iterating through the images and making the predictions
for image, preprocessed_image in images_data:
    predicted_label, probability, predicted_clothing = predict_image(model, preprocessed_image, label_to_clothing)

    print(f"Predicted Clothing for {os.path.basename(image.filename)}: {predicted_clothing}")
    print(f"Probability: {probability * 100:.2f}%")

    # Displaying the image with prediction details
    plt.figure(figsize=(8, 4))

    # Plotting the image
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap=plt.cm.binary)
    plt.xlabel(f'Predicted: {predicted_clothing} ({probability * 100:.2f}%)')
    plt.xticks([])
    plt.yticks([])

    # Plotting the bar chart for the probabilities with correct labels
    predicted_probabilities = model.predict(preprocessed_image).flatten()
    plt.subplot(1, 2, 2)
    plt.bar(range(10), predicted_probabilities)
    plt.xticks(range(10), label_to_clothing.values(), rotation=90)
    plt.ylabel('Probability')

    plt.tight_layout()
    plt.show()