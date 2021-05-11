# TensorFlow is  the open source machine learning library we shall use
import tensorflow as tf

# Keras is TensorFlow's high-level API for deep learning
from tensorflow import keras
# Numpy is a math library
import numpy as np
# Pandas is a data manipulation library 
import pandas as pd
# Matplotlib is a graphing library
import matplotlib.pyplot as plt
# Math is Python's math library
import math

# Set seed for reproducibility
seed = 1337
np.random.seed(seed)
tf.random.set_seed(seed)

# Copied from https://stackoverflow.com/questions/4601373/better-way-to-shuffle-two-numpy-arrays-in-unison
def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

# This will convert our file of [1..16] strings to python lists to a numpy array that is TF friendly...
def file_to_np(filename):
    with open(filename, 'r') as f:
        f_lines = f.readlines()
    f_list = list(map(eval, f_lines))
    f_np = np.array([np.array(fi) for fi in f_list])
    return f_np

# This is the number of training epochs we will use...
# Technically it's a little high (looks like some overfitting)
# if you think of a way to maybe make things better... try it! :-) -MC
e_pochs = 1500
num_samples = 5000
train_size = int(num_samples * 0.6)
test_size = int(num_samples * 0.2)
validate_size = int(num_samples * 0.2) # we let model.fit() do this for us... just define this for now. -MC
# Load the data files... EDIT for your own data! -MC
f_ledoff = file_to_np('led_off.log')[:num_samples]
f_ledon = file_to_np('led_on.log')[:num_samples]

# print("LED")
# print(f_ledoff)

# Setup the training data...
train_data = []
training_data = []
training_labels = []
train_data.append(f_ledoff[:train_size])
train_data.append(f_ledon[:train_size])
for i in range(2):
  for j in range(train_size):
    training_labels.append(i) # Given we process the files sequentially, assign labels 0, 1, ...
    # to the data from each file sequentially...
    training_data.append(train_data[i][j])

# training_data = np.array(training_data)
# training_labels = np.array(training_labels)

# print("training_data")
# print(training_data[0])

# Set aside the test data - this will be used after training to see how we did...
t_data = []
test_data = []
test_labels = []
t_data.append(f_ledoff[train_size:(num_samples - validate_size)])
t_data.append(f_ledon[train_size:(num_samples - validate_size)])
for i in range(2):
  for j in range(test_size):
    test_labels.append(i)
    test_data.append(t_data[i][j])

test_data = np.array(test_data)
test_labels = np.array(test_labels)

print("np.array")
print(test_data)

# We can also add valdiation data - used to assess the model's efficacy during training,
# but we don't use that here, as we let model.fit() do that for us.. but we _could_ define it ... -MC
#v_data = []
#validate_data = []
#validate_labels = []
#v_data.append(f_ledoff[validate_size:])
#v_data.append(f_ledon[validate_size:])
#for i in range(2):
#for j in range(validate_size):
#validate_labels.append(i)
#validate_data.append(v_data[i][j])
#
#validate_data = np.array(validate_data)
#validate_labels = np.array(validate_labels)# Shuffle the data sets so it isn't just 'all 1's then all 0's'...
# This will help with the training, as our data is all linear for now
# training_data, training_labels = unison_shuffled_copies(training_data, training_labels)
# test_data, test_labels = unison_shuffled_copies(test_data, test_labels)
#validate_data, validate_test = unison_shuffled_copies(validate_data, validate_labels)

model = keras.Sequential([
  keras.layers.Flatten(input_shape=(16,)), # using Flatten isn't necessary, but included as it's handy for building out.
  keras.layers.Dense(64, activation=tf.nn.relu), #started at 128, but we don't need that many -MC
  keras.layers.Dense(64, activation=tf.nn.relu), # Second layer for betterment of humanity... -MC
  keras.layers.Dense(2, activation=tf.nn.softmax) # output '0' or '1' for LED off or on respectively -MC
])

model.compile(optimizer=tf.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Lets save our current model state so we can reload it loater
model.save_weights("model_data/pre-fit.weights")

# training_labels = tf.convert_to_tensor(training_labels, dtype=tf.float32);

# print(training_data)

# https://stackoverflow.com/questions/62570936/valueerror-failed-to-convert-a-numpy-array-to-a-tensor-unsupported-object-type
history = model.fit(training_data, training_labels, epochs=e_pochs, validation_split=0.2, verbose=0)

def plot_history(history):
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Loss/accuracy')
    plt.plot(history.epoch, np.array(history.history['loss']),
           label='Train Loss')
    plt.plot(history.epoch, np.array(history.history['val_loss']),
           label = 'Validation Loss')
    plt.plot(history.epoch, np.array(history.history['accuracy']),
           label='Train accuracy')
    plt.plot(history.epoch, np.array(history.history['val_accuracy']),
           label = 'Validation accuracy')
    plt.legend()
    plt.ylim([0, 2])

plot_history(history)

test_loss, test_acc = model.evaluate(test_data, test_labels)
print('Accuracy on testdata:', test_acc * 100, "%")




def convert_credit_rows(row):
  return np.asarray([row['A'], row['B'], row['C'], row['D']], dtype=np.float32)

def convert_credit_rows(row):
  credit_list.append(np.asarray([row['A'], row['B'], row['C'], row['D']], dtype=np.float32))
