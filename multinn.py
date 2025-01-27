# Rodrigues, Blaise
# 1001-759-552
# 2020_10_25
# Assignment-03-01

# %tensorflow_version 2.x
import tensorflow as tf
import numpy as np


class MultiNN(object):
    def __init__(self, input_dimension):
        """
        Initialize multi-layer neural network
        :param input_dimension: The number of dimensions for each input data sample
        """
        self.input_dimension = input_dimension
        self.weights = list()
        self.biases = list()
        self.transfer_functions = list()
        

    def add_layer(self, num_nodes, transfer_function="Linear"):
        """
         This function adds a dense layer to the neural network
         :param num_nodes: number of nodes in the layer
         :param transfer_function: Activation function for the layer. Possible values are:
        "Linear", "Relu","Sigmoid".
         :return: None
         """
        if not self.weights:
            weight = tf.Variable(np.random.randn(self.input_dimension, num_nodes), trainable = True)
        else:
            weight = tf.Variable(np.random.randn(self.weights[-1].shape[1], num_nodes), trainable = True)
        bias = tf.Variable(np.random.randn(num_nodes, ), trainable = True)
        self.biases.append(bias)
        self.weights.append(weight)
        self.transfer_functions.append(transfer_function.lower())
        

    def get_weights_without_biases(self, layer_number):
        """
        This function should return the weight matrix (without biases) for layer layer_number.
        layer numbers start from zero.
         :param layer_number: Layer number starting from layer 0. This means that the first layer with
          activation function is layer zero
         :return: Weight matrix for the given layer (not including the biases). Note that the shape of the weight matrix should be
          [input_dimensions][number of nodes]
         """
        return self.weights[layer_number]

    
    def get_biases(self, layer_number):
        """
        This function should return the biases for layer layer_number.
        layer numbers start from zero.
        This means that the first layer with activation function is layer zero
         :param layer_number: Layer number starting from layer 0
         :return: Weight matrix for the given layer (not including the biases).
         Note that the biases shape should be [1][number_of_nodes]
         """
        return self.biases[layer_number]
    

    def set_weights_without_biases(self, weights, layer_number):
        """
        This function sets the weight matrix for layer layer_number.
        layer numbers start from zero.
        This means that the first layer with activation function is layer zero
         :param weights: weight matrix (without biases). Note that the shape of the weight matrix should be
          [input_dimensions][number of nodes]
         :param layer_number: Layer number starting from layer 0
         :return: none
         """
        self.weights[layer_number] = weights
        
        
    def set_biases(self, biases, layer_number):
        """
        This function sets the biases for layer layer_number.
        layer numbers start from zero.
        This means that the first layer with activation function is layer zero
        :param biases: biases. Note that the biases shape should be [1][number_of_nodes]
        :param layer_number: Layer number starting from layer 0
        :return: none
        """
        self.biases[layer_number] = biases
        

    def calculate_loss(self, y, y_hat):
        """
        This function calculates the sparse softmax cross entropy loss.
        :param y: Array of desired (target) outputs [n_samples]. This array includes the indexes of
         the desired (true) class.
        :param y_hat: Array of actual output values [n_samples][number_of_classes].
        :return: loss
        """
        return tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=y_hat))
    

    def predict(self, X):
        """
        Given array of inputs, this function calculates the output of the multi-layer network.
        :param X: Array of input [n_samples,input_dimensions].
        :return: Array of outputs [n_samples,number_of_classes ]. This array is a numerical array.
        """
        output = tf.Variable(X)
        for layer in range(len(self.weights)):
            predicted_output = tf.add(tf.matmul(output, self.get_weights_without_biases(layer)), self.get_biases(layer))
            if self.transfer_functions[layer] == "linear":
                output = predicted_output
            elif self.transfer_functions[layer] == "relu":
                output = tf.nn.relu(predicted_output) 
            elif self.transfer_functions[layer] == "sigmoid":
                output = tf.nn.sigmoid(predicted_output)
        return output     
                         

    def train(self, X_train, y_train, batch_size, num_epochs, alpha=0.8):
        """
         Given a batch of data, and the necessary hyperparameters,
         this function trains the neural network by adjusting the weights and biases of all the layers.
         :param X: Array of input [n_samples,input_dimensions]
         :param y: Array of desired (target) outputs [n_samples]. This array includes the indexes of
         the desired (true) class.
         :param batch_size: number of samples in a batch
         :param num_epochs: Number of times training should be repeated over all input data
         :param alpha: Learning rate
         :return: None
         """
        for _ in range(num_epochs):
            for i in range(0, len(X_train), batch_size):
                batch = batch_size + i
                x_batch = tf.Variable(X_train[i:batch, :])
                y_batch = tf.Variable(y_train[i:batch])

                with tf.GradientTape(persistent = True) as tape:
                    tape.watch(self.weights)
                    tape.watch(self.biases)
                    predict = self.predict(x_batch)
                    loss = self.calculate_loss(y_batch, predict)

                for layer in range(len(self.weights)):
                    layer_weight = tf.scalar_mul(alpha, tape.gradient(loss, self.get_weights_without_biases(layer)))
                    layer_bias = tf.scalar_mul(alpha, tape.gradient(loss, self.get_biases(layer)))
                    weight = tf.subtract(self.get_weights_without_biases(layer), layer_weight)
                    bias = tf.subtract(self.get_biases(layer), layer_bias)
                    self.set_weights_without_biases(weight, layer)
                    self.set_biases(bias, layer)
                                              
                
    def calculate_percent_error(self, X, y):
        """
        Given input samples and corresponding desired (true) output as indexes,
        this method calculates the percent error.
        For each input sample, if the predicted class output is not the same as the desired class,
        then it is considered one error. Percent error is number_of_errors/ number_of_samples.
        Note that the predicted class is the index of the node with maximum output.
        :param X: Array of input [n_samples,input_dimensions]
        :param y: Array of desired (target) outputs [n_samples]. This array includes the indexes of
        the desired (true) class.
        :return percent_error
        """
        predicted_output = self.predict(X).numpy()
        predicted_out = np.argmax(predicted_output, axis = 1)
        error = 0
        for i in range(len(predicted_output)):
            if predicted_out[i]!=y[i]:
                error = error + 1
        percent_error = (error / len(predicted_output))
        return percent_error
    

    def calculate_confusion_matrix(self, X, y):
        """
        Given input samples and corresponding desired (true) outputs as indexes,
        this method calculates the confusion matrix.
        :param X: Array of input [n_samples,input_dimensions]
        :param y: Array of desired (target) outputs [n_samples]. This array includes the indexes of
        the desired (true) class.
        :return confusion_matrix[number_of_classes,number_of_classes].
        Confusion matrix should be shown as the number of times that
        an image of class n is classified as class m.
        """
        predicted_output = self.predict(X).numpy()
        predicted_out = np.argmax(predicted_output, axis = 1) 
        confusion_matrix = np.zeros((len(np.unique(y)), len(np.unique(y))))
        for i in range(len(y)):
            row = y[i]
            column = predicted_out[i]
            confusion_matrix[row.astype(int)][column.astype(int)] += 1
        return confusion_matrix

