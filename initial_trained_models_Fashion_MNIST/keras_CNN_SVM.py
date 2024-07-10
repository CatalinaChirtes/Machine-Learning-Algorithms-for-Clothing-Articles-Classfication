import numpy as np
from sklearn import svm
from tensorflow import keras
from keras.datasets import fashion_mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Loading the Fashion MNIST dataset
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# The mapping of labels to clothing types
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

# Preprocessing the data
train_images = train_images.reshape((train_images.shape[0], 28, 28, 1)) / 255.0
test_images = test_images.reshape((test_images.shape[0], 28, 28, 1)) / 255.0

# Splitting the data into train and validation sets
train_images, val_images, train_labels, val_labels = train_test_split(train_images, train_labels, test_size=0.2)

# Defining the CNN model
model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Training the CNN model
history = model.fit(train_images, train_labels, epochs=20, validation_data=(val_images, val_labels))

# Extracting features using the CNN's intermediate layer
from keras.models import Model
intermediate_layer_model = Model(inputs=model.input, outputs=model.layers[-2].output)

train_images_features = intermediate_layer_model.predict(train_images)
test_images_features = intermediate_layer_model.predict(test_images)

# SVM Model
svm_classifier = svm.SVC(kernel='rbf', gamma='auto')
svm_classifier.fit(train_images_features, train_labels)

# Predicting with SVM
label_pred = svm_classifier.predict(test_images_features)

# Evaluating the CNN model on the test data
accuracy = accuracy_score(test_labels, label_pred)
print("Accuracy on test set:", accuracy)

# Displaying the accuracy per label
conf_matrix = confusion_matrix(test_labels, label_pred)
num_labels = len(label_to_clothing)
label_accuracies = {}

for i in range(num_labels):
    label_total = np.sum(conf_matrix[i])
    label_correct = conf_matrix[i][i]
    label_accuracy = label_correct / label_total if label_total > 0 else 0
    label_accuracies[label_to_clothing[i]] = label_accuracy

for label, accuracy in label_accuracies.items():
    print(f"Accuracy for {label}: {accuracy:.4f}")

model.save('keras_CNN_SVM_20.keras')
print("Saving the model as keras_CNN_SVM_20.keras")

# Displaying some test images and predictions
num_rows = 10
num_cols = 7
num_images = num_rows * num_cols

predictions = model.predict(test_images)

# Visualizing the predictions
def plot_image(i, predictions_array, true_label):
    img = test_images[i]
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img.reshape(28, 28), cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    predicted_clothing = label_to_clothing[predicted_label]
    true_clothing = label_to_clothing[true_label]
    
    if predicted_label == true_label:
        color = 'green'
    else:
        color = 'red'
    
    # Computing the confidence scores
    predicted_prob = np.max(predictions_array) * 100
    
    plt.xlabel(f'Predicted: {predicted_clothing} ({predicted_prob:.2f}%)\nTrue: {true_clothing}', color=color)

plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
    plot_image(i, predictions, test_labels)
plt.show()



