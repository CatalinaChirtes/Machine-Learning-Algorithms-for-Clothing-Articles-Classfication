import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler
from tensorflow.keras.utils import to_categorical
import tensorflow as tf

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

model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')  # Output layer with 10 nodes
])

# Compiling the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

# Converting labels to one-hot encoded vectors
train_labels_one_hot = to_categorical(train_labels)
val_labels_one_hot = to_categorical(val_labels)
test_labels_one_hot = to_categorical(test_labels)

early_stopping_per_label = {}
desired_accuracy_per_label = {
    0: 0.85,  # T-shirt/top
    1: 0.85,  # Trouser
    2: 0.85,  # Pullover
    3: 0.85,  # Dress
    4: 0.85,  # Coat
    5: 0.85,  # Sandal
    6: 0.85,  # Shirt
    7: 0.85,  # Sneaker
    8: 0.85,  # Bag
    9: 0.85   # Ankle boot
}

# Creating separate early stopping callbacks for each label based on desired accuracy
for label in range(10):  
    early_stopping_per_label[label] = EarlyStopping(
        monitor=f'val_accuracy_{label}',
        patience=5,  
        mode='max', 
        min_delta=0.001 
    )

# Defining a custom callback to aggregate early stopping conditions
class CustomEarlyStoppingCallback(tf.keras.callbacks.Callback):
    def __init__(self, early_stopping_per_label):
        self.early_stopping_per_label = early_stopping_per_label

    def on_epoch_end(self, epoch, logs=None):
        for label, early_stopping in self.early_stopping_per_label.items():
            current_val_acc = logs.get(f'val_accuracy_{label}', 0)
            if current_val_acc >= desired_accuracy_per_label[label]:
                print(f'Label {label} reached desired accuracy. Stopping training for this label.')
                self.model.stop_training = True 

# Instantiating the custom callback
custom_early_stopping = CustomEarlyStoppingCallback(early_stopping_per_label)

# Training the model with the custom early stopping callback
history = model.fit(train_images, train_labels_one_hot,
                    epochs=100, validation_data=(val_images, val_labels_one_hot),
                    callbacks=[custom_early_stopping])


# Evaluating the CNN model on test data
test_loss, test_acc = model.evaluate(test_images, test_labels_one_hot)
print("Test accuracy:", test_acc)
print("Test loss:", test_loss)

model.save('keras_early_stopping_per_label_100.keras')
print("Saving the model as keras_early_stopping_per_label_100.keras")

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



