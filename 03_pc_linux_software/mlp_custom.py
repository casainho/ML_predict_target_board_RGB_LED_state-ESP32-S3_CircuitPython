import numpy as np

class MLP:
    
  def __init__(self, weights, biases):
    self.weights = weights
    self.biases = biases
    self.num_layers = len(weights)  # Assuming weights holds all layer weights

  def relu(self, x):
    return np.maximum(0, x)
  
  def activation_function(self, x):
    return self.relu(x)

  def predict(self, X):
    # Forward propagation

    layer = X

    for num_layer in range(self.num_layers):
      # multiply each layer weights by the input (matrix multiplication)
      layer = np.dot(layer, self.weights[num_layer])
      
      # add the bias
      layer += self.biases[num_layer]
      
      # apply the activation function
      layer = self.activation_function(layer)
    
    return layer
  
  
  def predict(self, X):
    layer = X  # Start with input layer (X)
    for layer_index in range(self.num_layers):
      # Apply activation to current layer
      layer = self.activation_function(np.dot(layer, self.weights[layer_index]) + self.biases[layer_index])
    return layer