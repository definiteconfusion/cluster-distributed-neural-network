import numpy as np
import matplotlib.pyplot as plt

class Network:
    def __init__(self):
        self.network:list = []
        self.last_output:float = 0
        pass
    
    def create_random_weights(self, sizes=[3,3], init_size=1):
        weights = []
        weights.append(np.random.rand(sizes[0], init_size))
        for i in range(1, len(sizes)):
            layer = 2 * np.random.rand(sizes[i], sizes[i-1]) - 1
            weights.append(layer)
        self.network = weights
        pass
    
    def forcycle(self, inputs:list) -> float:
        sigmoid = lambda x: 1 / (1 + np.exp(np.clip(-x, -709, 709)))
        
        output = inputs
        for layer in self.network:
            # Calculate the weighted sum using np.dot
            output = np.dot(layer, output)
            # Apply the sigmoid activation function
            output = sigmoid(output)
        
        self.last_output = sum(output)
        return self.last_output
    
    def backcycle(self, expectation:float, lr:float=0.1):
        
        driven_sigmoid = lambda x, g=0.1: g * (1 / (1 + np.exp(-x))) - (g / 2)
        
        if abs(expectation) < 1e-10:
            Error = self.last_output - expectation
        else:
            Error = (self.last_output - expectation) / expectation
        Adjustor = -Error / (1 + abs(Error))
        # Adjustor = driven_sigmoid(Error, 1)
        # Adjustor = np.log((round(Error, 5) + 1) / (1 - round(Error, 5)))
        layer_iotas = []
        for layer in self.network:
            layer_iota = 0
            for neuron in layer:
                for weight in neuron:
                    layer_iota += abs(weight)
            layer_iotas.append(layer_iota)
        sigma_s = sum(layer_iotas) + 1e-10
        layer_budgets = [Adjustor * (1 - (layer_iota / sigma_s)) + lr for layer_iota in layer_iotas]
        for i, layer in enumerate(self.network):
            for j, neuron_idx in enumerate(range(len(layer))):
                total_neuron_weight = sum(layer[neuron_idx])
                for k, weight_idx in enumerate(range(len(layer[neuron_idx]))):
                    # Directly update the network weights
                    # print(abs(layer_budgets[i]))
                    # print(total_neuron_weight)
                    self.network[i][neuron_idx][weight_idx] *= ((1 - (1 / abs(layer_budgets[i]))) * (self.network[i][neuron_idx][weight_idx] / total_neuron_weight))
        pass
    
Net = Network()
Net.create_random_weights([3, 3, 3], 1)

x = [30]
y = 0.5
diffs = []
for i in range(100):
    Net.forcycle(x)
    # if Net.last_output - 0.5 < 0.05:
    #     break
    print(Net.last_output)
    diffs.append(y - Net.last_output)# if 0.5 - Net.last_output < 10 else "EVR"
    Net.backcycle(y, 0.01)
    
print(Net.last_output, "-"*50)
plt.plot(diffs)
plt.title("Error")
plt.xlabel("Epoch")
plt.ylabel("Error")
plt.show()