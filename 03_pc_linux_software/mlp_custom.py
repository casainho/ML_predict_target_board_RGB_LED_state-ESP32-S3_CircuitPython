import numpy as np

class MLP:

  def __init__(self, weights, biases):
    self.weights = weights
    self.biases = biases
    self.num_layers = len(self.biases)

  def relu(self, x):
    return np.maximum(0, x)

  def activation_function(self, x):
    return self.relu(x)

  def predict(self, X):
    layer = X
    for layer_index in range(self.num_layers):
      layer = np.dot(layer, self.weights[layer_index]) + self.biases[layer_index]
      layer = self.activation_function(layer)
      
    node_number = np.argmax(layer[0].tolist())
    return layer #node_number