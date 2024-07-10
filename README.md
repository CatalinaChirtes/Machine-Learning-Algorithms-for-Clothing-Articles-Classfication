# Machine Learning Algorithms for Clothing Articles Classification
This comparative analysis investigates the performances and effectiveness at the clothing classification task of three proposed Convolutional Neural Networks (CNN) based algorithms.

## The proposed Machine Learning algorithms include:
- a CNN model created from scratch
- a MobileNetV2-based model fine-tuned on our dataset
- an InceptionResNetV2-based model fine-tuned on our dataset

## Selected Dataset:
We initially experimented on the [Fashion-MNIST](https://www.tensorflow.org/datasets/catalog/fashion_mnist) dataset, but after encountering a few limitations, we decided to choose a better one, so Param Aggarwals' [Fashion Product Images (Small)](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small) proved to be the best selection for our study. 
A little preprocessing was needed to eliminate the unnecessary data, obtaining a final dataset of about 27.932 entries split into 5 categories, and 24 article types.
