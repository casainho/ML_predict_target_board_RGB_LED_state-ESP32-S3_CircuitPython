from ulab import numpy as np

class MLP:
  def __init__(self, input_size, hidden_size, output_size):
    # Initialize weights and biases with random values
    self.weights = [np.random.rand(input_size, hidden_size),
                     np.random.rand(hidden_size, output_size)]
    self.biases = [np.zeros((hidden_size, 1)), np.zeros((output_size, 1))]

  def relu(self, x):
    # ReLU activation function (max(0, x))
    return np.maximum(0, x)

  def predict(self, X):
    # Forward propagation
    layer1 = self.relu(np.dot(X, self.weights[0]) + self.biases[0])
    output = self.relu(np.dot(layer1, self.weights[1]) + self.biases[1])
    return output