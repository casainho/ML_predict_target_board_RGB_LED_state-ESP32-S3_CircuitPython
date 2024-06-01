from ulab import numpy as np

class MLP:

  def __init__(self, weights, biases, classes):
    self._weights = weights
    self._biases = biases
    self._num_layers = len(self._biases)
    self._classes = classes

  def relu(self, x):
    return np.maximum(0, x)

  def activation_function(self, x):
    return self.relu(x)

  def predict(self, X):
    layer = X
    weights = self._weights.copy()
    biases = self._biases.copy()
    
    for layer_index in range(self._num_layers):
      layer = np.dot(layer, weights[layer_index]) + biases[layer_index]

      # using identity activation function, so no need to call the activation_function()
      # layer = self.relu(layer)

    node_number = np.argmax(layer.tolist())
    return self._classes[node_number], node_number