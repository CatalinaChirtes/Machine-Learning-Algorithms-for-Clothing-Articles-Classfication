import numpy as np
from sklearn import svm
from keras.datasets import fashion_mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

# Fashion MNIST data loading and preprocessing
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
x_train = x_train.reshape((-1, 28, 28, 1)).astype('float32') / 255.0
x_test = x_test.reshape((-1, 28, 28, 1)).astype('float32') / 255.0

# CNN Model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Training the CNN
model.fit(x_train, y_train, epochs=10, batch_size=64, validation_data=(x_test, y_test))

# Extracting features using the CNN's intermediate layer
from keras.models import Model
intermediate_layer_model = Model(inputs=model.input, outputs=model.layers[-2].output)

x_train_features = intermediate_layer_model.predict(x_train)
x_test_features = intermediate_layer_model.predict(x_test)

# SVM Model
svm_classifier = svm.SVC(kernel='rbf', gamma='auto')
svm_classifier.fit(x_train_features, y_train)

# Predicting with SVM
y_pred = svm_classifier.predict(x_test_features)

# Evaluating performance
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy on test set:", accuracy)

# Mapping labels to clothing types
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

# Displaying accuracy per label
conf_matrix = confusion_matrix(y_test, y_pred)
num_labels = len(label_to_clothing)
label_accuracies = {}

for i in range(num_labels):
    label_total = np.sum(conf_matrix[i])
    label_correct = conf_matrix[i][i]
    label_accuracy = label_correct / label_total if label_total > 0 else 0
    label_accuracies[label_to_clothing[i]] = label_accuracy

for label, accuracy in label_accuracies.items():
    print(f"Accuracy for {label}: {accuracy:.4f}")

model.save('CNN_SVM.keras')
print("Saving the model as CNN_SVM.keras")

predictions = model.predict(x_test)

# Visualizing predictions
def plot_image(i, predictions_array, true_label):
    img = x_test[i]
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

num_rows = 10
num_cols = 7
num_images = num_rows * num_cols

plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
    plot_image(i, predictions, y_test)
plt.show()

