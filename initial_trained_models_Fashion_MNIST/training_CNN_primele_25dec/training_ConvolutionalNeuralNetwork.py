import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import fashion_mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator

# Loading the Fashion MNIST dataset directly from Keras
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

# Normalizing the pixel values to be between 0 and 1
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Reshaping data for CNN
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

# Converting labels to categorical one-hot encoding
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Splitting training set into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
)

# Fitting the data generator
datagen.fit(X_train)

# Creating a CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

# Compiling the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Training the model with augmented data
history = model.fit(datagen.flow(X_train, y_train, batch_size=64),
                    steps_per_epoch=len(X_train) / 64, epochs=300,
                    validation_data=(X_val, y_val))

# Evaluating the model on the test set
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test loss: {test_loss}')
print(f'Test accuracy: {test_acc}')

# Saving the model
model.save('improved_fashion_mnist_model.h5')
print("Saving the model as improved_fashion_mnist_model.h5")

# Making predictions
predictions = model.predict(x_test)

# Defining a dictionary to map labels to clothing types
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

# Visualizing results
def plot_image(i, predictions_array, true_label):
    img = x_test[i].reshape(28, 28)
    predictions_array, true_label = predictions_array[i], np.argmax(true_label[i])
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    predicted_clothing = label_to_clothing[predicted_label]
    true_clothing = label_to_clothing[true_label]
    
    if predicted_label == true_label:
        color = 'green'
    else:
        color = 'red'
    
    # Computing the confidence scores
    predicted_prob = np.max(predictions_array) * 100
    true_prob = predictions_array[true_label] * 100
    
    plt.xlabel(f'Predicted: {predicted_clothing} ({predicted_prob:.2f}%)\nTrue: {true_clothing} ({true_prob:.2f}%)', color=color)

num_rows = 10
num_cols = 7
num_images = num_rows * num_cols

plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
    plot_image(i, predictions, y_test)
plt.show()

