import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from skimage.feature import hog

# Reading the datasets
train = pd.read_csv('RandomForestClassifierMethod/fashion_mnist/fashion-mnist_train.csv')
test = pd.read_csv('RandomForestClassifierMethod/fashion_mnist/fashion-mnist_test.csv')

# Function to compute the HoG features for a single image
def compute_hog_features(image):
    image = image.values.reshape((28, 28))
    features = hog(image, orientations=8, visualize=False)
    return features

# Computing the HoG features for the train set
train_hog = [compute_hog_features(row[1:]) for _, row in train.iterrows()]
train_hog = np.array(train_hog)

# Computing the HoG features for the test set
test_hog = [compute_hog_features(row[1:]) for _, row in test.iterrows()]
test_hog = np.array(test_hog)

# Creating DataFrames for train and test sets with the HoG features
train_hog_df = pd.DataFrame(train_hog)
train_hog_df["label"] = train["label"]

test_hog_df = pd.DataFrame(test_hog)
test_hog_df["label"] = test["label"]

# Separating features and target labels
X_train = train_hog_df.drop('label', axis=1)
y_train = train_hog_df['label']

X_test = test_hog_df.drop('label', axis=1)
y_test = test_hog_df['label']

# Initializing and training RandomForestClassifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Predictions on the test set
predictions = rf_classifier.predict(X_test)
probabilities = rf_classifier.predict_proba(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, predictions)
conf_matrix = confusion_matrix(y_test, predictions)
report = classification_report(y_test, predictions)

print(f"Accuracy: {accuracy}")
print(f"Confusion Matrix:\n{conf_matrix}")
print(f"Classification Report:\n{report}")

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
def plot_image(i, predictions_array, true_label, probabilities):
    img = test.iloc[i, 1:].values.reshape(28, 28) 
    predictions_array, true_label = predictions_array[i], true_label[i]
    prediction_probabilities = probabilities[i]
    
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    
    if predicted_label == true_label:
        color = 'green'
    else:
        color = 'red'
    
    # Mapping labels to clothing types
    predicted_clothing = label_to_clothing[predicted_label]
    true_clothing = label_to_clothing[true_label]
    
    # Displaying confidence and highest probability for each item
    confidence = np.max(prediction_probabilities) * 100
    plt.xlabel(f'Predicted: {predicted_label} ({predicted_clothing})\nTrue: {true_label} ({true_clothing})\nConfidence: {confidence:.2f}%', color=color)
    
    
num_rows = 5
num_cols = 3
num_images = num_rows * num_cols

plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
    plot_image(i, predictions, y_test, probabilities)
plt.show()
