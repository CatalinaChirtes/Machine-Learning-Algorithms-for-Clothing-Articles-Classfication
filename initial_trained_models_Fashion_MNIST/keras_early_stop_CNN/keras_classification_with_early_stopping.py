import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler
from sklearn.metrics import confusion_matrix

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

# Defining a learning rate scheduler
def lr_schedule(epoch):
    if epoch < 100:
        return 0.001  # High learning rate for initial epochs
    else:
        return 0.0001  # Lower learning rate for later epochs

lr_scheduler = LearningRateScheduler(lr_schedule)

# Define early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5)  # Stopping the training if validation loss doesn't improve for 5 epochs

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Training the model with callbacks
history = model.fit(train_images, train_labels, epochs=100, validation_data=(val_images, val_labels),
                    callbacks=[lr_scheduler, early_stopping])

# Evaluating the CNN model on test data
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("Test accuracy:", test_acc)
print("Test loss:", test_loss)

# Displaying accuracy per label
predictions = model.predict(test_images)
predicted_labels = np.argmax(predictions, axis=1)

# Creating the confusion matrix using true labels and predicted labels
conf_matrix = confusion_matrix(test_labels, predicted_labels)
num_labels = len(label_to_clothing)
label_accuracies = {}

for i in range(num_labels):
    label_total = np.sum(conf_matrix[i])
    label_correct = conf_matrix[i][i]
    label_accuracy = label_correct / label_total if label_total > 0 else 0
    label_accuracies[label_to_clothing[i]] = label_accuracy

for label, accuracy in label_accuracies.items():
    print(f"Accuracy for {label}: {accuracy:.4f}")

model.save('keras_fashion_mnist_early_stopping_08_ian.keras')
print("Saving the model as keras_fashion_mnist_early_stopping_08_ian.keras")

# Displaying some test images and predictions
num_rows = 10
num_cols = 7
num_images = num_rows * num_cols

# Visualizing predictions
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



