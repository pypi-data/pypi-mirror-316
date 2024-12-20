def p1():
    lab_1_code = '''Lab 1: Implementing a Simple Perceptron using TensorFlow
Objective:
Understand the basics of neural networks by implementing a simple perceptron and its limitations
on linearly separable vs. non-linearly separable data.
Tasks:
1. Implement a single-layer perceptron using TensorFlow.
2. Train the perceptron on the OR and XOR logic gates: XOR is a non-linearly separable
problem.
3. Evaluate the performance using accuracy, precision, recall, and F1 score.
4. Analyze the model limitations: Explain why the perceptron fails on XOR and suggest
possible solutions (e.g., adding hidden layers).
Steps:
1. Set up the environment:
pip install tensorflow
2. Define the OR and XOR gate datasets:
# Define OR and XOR datasets
X_OR = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
y_OR = np.array([[0], [1], [1], [1]], dtype=np.float32)
X_XOR = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
y_XOR = np.array([[0], [1], [1], [0]], dtype=np.float32)
3. Create a single-layer perceptron model:
import tensorflow as tf
# Function to create and train a single-layer perceptron with improved
accuracy
def train_perceptron(X, y, epochs=100, learning_rate=0.1):
 model = tf.keras.Sequential([
 tf.keras.layers.Dense(1, activation='sigmoid', input_shape=(2,))
 ])
 model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=
 learning_rate),loss='binary_crossentropy',
 metrics=['accuracy'])
 model.fit(X, y, epochs=epochs, verbose=0)
 return model
4. Train the model on OR and XOR datasets:
# Train on OR gate with improved accuracy
model_OR = train_perceptron(X_OR, y_OR, epochs=500, learning_rate=0.5)
# Evaluate on OR
loss_OR, accuracy_OR = model_OR.evaluate(X_OR, y_OR)
print(f"OR Gate Accuracy: {accuracy_OR}")
# Train on XOR gate with improved accuracy (not possible with a singlelayer perceptron)
# However, we can try increasing epochs and learning rate
model_XOR = train_perceptron(X_XOR, y_XOR, epochs=1000, learning_rate=0.8)
# Evaluate on XOR
loss_XOR, accuracy_XOR = model_XOR.evaluate(X_XOR, y_XOR)
print(f"XOR Gate Accuracy: {accuracy_XOR}")
5. Analyze the results:
#Make a prediction using model_OR
input1 = 0
input2 = 0
user_input = np.array([[input1, input2]])
prediction = model_OR.predict(user_input)
if prediction > 0.5:
 print("The model predicts 1 for your input.")
else:
 print("The model predicts 0 for your input.")
#Do the same using model_XOR
• Discuss the success on the OR gate and failure on the XOR gate.
• Explain that the XOR gate cannot be solved by a single-layer perceptron due to nonlinearity, and suggest adding hidden layers as a solution.
'''
    print(lab_1_code)


def p2():
    lab_2_code = '''Lab 2: Building a Multilayer Perceptron (MLP)
Objective:
Learn to build and train a multilayer perceptron (MLP) for more complex classification tasks using
advanced optimization techniques.
Tasks:
1. Create an MLP with additional hidden layers: Introduce batch normalization and dropout.
2. Train the MLP on the Fashion-MNIST dataset, which is more challenging than MNIST.
3. Apply learning rate scheduling to improve training stability.
4. Visualize training progress: Track and plot accuracy, loss, and overfitting behavior.
Steps:
1. Load the Fashion-MNIST dataset:
from tensorflow.keras.datasets import fashion_mnist
# Load dataset
(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
# Normalize data
X_train, X_test = X_train / 255.0, X_test / 255.0
2. Define the MLP model with batch normalization and dropout:
model = tf.keras.Sequential([
 tf.keras.layers.Flatten(input_shape=(28, 28)),
 tf.keras.layers.Dense(128, activation='relu'),
 tf.keras.layers.BatchNormalization(),
 tf.keras.layers.Dropout(0.5),
 tf.keras.layers.Dense(64, activation='relu'),
 tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
metrics=['accuracy'])
3. Implement learning rate scheduling:
lr_schedule = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 1e-3
* 10 ** (epoch / 20))
history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test,
y_test), callbacks=[lr_schedule])
4. Plot training and validation performance:
import matplotlib.pyplot as plt
# Plot accuracy
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
'''
    print(lab_2_code)


def p3():
    lab_3_code = '''Lab 3: Exploring Convolutional Neural Networks (CNN)
Objective:
Explore more advanced convolutional neural network (CNN) architectures and interpret their
behavior.
Tasks:
1. Build a deeper CNN with multiple convolutional layers, max-pooling, and data
augmentation.
2. Train the CNN on the CIFAR-10 dataset, which contains 32x32 color images..
3. Evaluate the model using precision, recall.
Steps:
1. Load and preprocess the CIFAR-10 dataset:
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.metrics import accuracy_score, precision_score, recall_score
# Load CIFAR-10 dataset
(X_train, y_train), (X_test, y_test) = cifar10.load_data()
# Normalize pixel values to be between 0 and 1
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0
# Convert class vectors to binary class matrices (one-hot encoding)
y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)
2. Define a deeper CNN model:
# Define the CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', padding='same',
input_shape=(32, 32, 3)))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))
# Compile the model
model.compile(optimizer='adam',
loss='categorical_crossentropy',metrics=['accuracy'])
3. Evaluate the model using precision, recall, and confusion matrix:
# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=64,
validation_data=(X_test, y_test))
# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print('Test accuracy:', accuracy)
# Make predictions on the test set
y_pred_prob = model.predict(X_test)
y_pred = np.argmax(y_pred_prob, axis=1)
y_true = np.argmax(y_test, axis=1)
# Calculate precision and recall
precision = precision_score(y_true, y_pred, average='macro')
recall = recall_score(y_true, y_pred, average='macro')
print('Precision:', precision)
print('Recall:', recall)
'''
    print(lab_3_code)


def p4():
    lab_4_code = '''Lab 4: Introduction to Recurrent Neural Networks (RNN)
Objective:
Explore the workings of recurrent neural networks (RNNs) and implement them on sequential data,
including more advanced RNN architectures such as LSTMs or GRUs.
Tasks:
1. Implement an advanced RNN architecture: Use Long Short-Term Memory (LSTM) or
Gated Recurrent Units (GRU) for handling sequential dependencies.
2. Train the model on sequential data: Use a real-world sequential dataset such as the IMDB
sentiment analysis dataset.
3. Use word embeddings: Apply an embedding layer to convert text into numerical
representations.
4. Evaluate and visualize model predictions using accuracy, precision, recall, and F1 score.
Steps:
1. Load the IMDB dataset:
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
# Load dataset
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=10000)
# Pad sequences to ensure uniform input size
X_train = pad_sequences(X_train, padding='post', maxlen=500)
X_test = pad_sequences(X_test, padding='post', maxlen=500)
2. Define an LSTM model for sentiment analysis:
from tensorflow.keras.layers import Embedding, LSTM, Dense
# Build the LSTM model
model = tf.keras.Sequential([
Embedding(input_dim=10000, output_dim=128, input_length=500),
LSTM(128, activation='tanh', return_sequences=True),
LSTM(128, activation='tanh'),
Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy',
metrics=['accuracy'])
3. Train the model:
history = model.fit(X_train, y_train, epochs=5, batch_size=64,
validation_data=(X_test, y_test))
4. Evaluate the model using accuracy, precision, recall, and F1 score:
y_pred = model.predict(X_test)
# Binarize predictions
y_pred_bin = (y_pred > 0.5).astype(int)
from sklearn.metrics import accuracy_score, precision_score, recall_score,
f1_score
accuracy = accuracy_score(y_test, y_pred_bin)
precision = precision_score(y_test, y_pred_bin)
recall = recall_score(y_test, y_pred_bin)
f1 = f1_score(y_test, y_pred_bin)
print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1 score: {f1}')
'''
    print(lab_4_code)


def p5():
    lab_5_code = '''Lab 5: Generative Adversarial Networks (GANs)
Objective:
Learn how to implement and train generative adversarial networks (GANs) to generate new data
points, such as images, using a two-network architecture.
Tasks:
1. Implement the basic GAN architecture: Generator and Discriminator networks.
2. Train the GAN on the MNIST dataset to generate new images of digits.
3. Evaluate the model's output: Visualize generated images and calculate Inception score and
Frechet Inception Distance (FID).
Steps:
1. Load the MNIST dataset:
from tensorflow.keras.datasets import mnist
# Load dataset
(X_train, _), (_, _) = mnist.load_data()
# Normalize data
X_train = X_train.astype('float32') / 255.0
2. Define the GAN model:
import tensorflow as tf
from tensorflow.keras.layers import Dense, Reshape, Flatten
from tensorflow.keras.models import Sequential
# Define the generator model
generator = Sequential([
Dense(128, activation='relu', input_dim=100),
Dense(784, activation='sigmoid'),
Reshape((28, 28))
])
# Define the discriminator model
discriminator = Sequential([
Flatten(input_shape=(28, 28)),
Dense(128, activation='relu'),
Dense(1, activation='sigmoid')
])
# Compile the models
discriminator.compile(optimizer='adam', loss='binary_crossentropy',
metrics=['accuracy'])
discriminator.trainable = False
gan = Sequential([generator, discriminator])
gan.compile(optimizer='adam', loss='binary_crossentropy')
3. Train the GAN:
import numpy as np
batch_size = 128
epochs = 10000
for epoch in range(epochs):
  # Train the discriminator
  idx = np.random.randint(0, X_train.shape[0], batch_size)
  real_images = X_train[idx]
  noise = np.random.normal(0, 1, (batch_size, 100))
  generated_images = generator.predict(noise)
  X = np.concatenate([real_images, generated_images])
  y = np.concatenate([np.ones((batch_size, 1)), np.zeros((batch_size, 1))])
  discriminator.train_on_batch(X, y)
  # Train the generator
  noise = np.random.normal(0, 1, (batch_size, 100))
  y_gen = np.ones((batch_size, 1))
  gan.train_on_batch(noise, y_gen)
4. Evaluate and visualize the results:
import matplotlib.pyplot as plt
# Generate new images
noise = np.random.normal(0, 1, (16, 100))
generated_images = generator.predict(noise)
# Plot generated images
fig, axes = plt.subplots(4, 4, figsize=(4, 4))
for i, ax in enumerate(axes.flatten()):
    ax.imshow(generated_images[i], cmap='gray')
    ax.axis('off')
plt.show()
'''
    print(lab_5_code)

