from random import random as rnd

class Network:
    def __init__(self, num_hidden:int=3, layer_size:int=3):
        self.num_hidden = num_hidden
        self.layer_size = layer_size
        self.structure = []
        self.build_structure()
        pass
    
    def build_structure(self):
        """Builds the structure of the network."""
        last_size = 1
        struct = []
        for layer in range(self.num_hidden):
            layer = []
            for _ in range(self.layer_size):
                layer.append([rnd() for _ in range(last_size)])
            struct.append(layer)
            last_size = self.layer_size
        self.structure = struct
        pass
    
    def cycle(self, inputs:list) -> float:
        """Cycles through the network with the given inputs."""
        output = inputs
        for layer in self.structure:
            print("New" + "*"*30)
            output = self.process_layer(layer, output)
        return sum(output)

    def process_layer(self, layer:list, inputs:list, bias:float=0) -> list:
        
        """ 
            ### For First Layer
            ```python
            layer = [[0.6301584142230672], [0.563562200812521], [0.6243787063451764]]
            inputs = [30]
            ```
            
            ### For the Rest
            ```python
            layer = [[0.5795700509374085, 0.7506977561324698, 0.13508899267972818], [0.7695778180849661, 0.8720645856534509, 0.9250370011082741], [0.12456551222671497, 0.5706038424626213, 0.18113586576298046]]
            inputs = [3.713545001897626, 5.913009498552027, 2.6622805217039893]
            ```
        """
        
        """Processes a single layer of the network."""
        
        # In theory should multiply each weight from a neuron by the its input value
        w_mult = lambda t1, t2: sum([t1[x] * t2[x] for x in range(len(t1))])
        out = []
        for neuron in layer:
            print(neuron)
            print(inputs)
            #                                                                                               -- Check Output
            out.append(w_mult(neuron, inputs))
        return sum(out) + bias
    
    def backcycle(self, output:float, expectation:float, lr:float=0.1):
        """Backpropagates the error through the network."""
        
        # Calculate the output error
        if abs(expectation) < 1e-10:
            Error = output - expectation
        else:
            Error = (output - expectation) / expectation
            
        # Calculates the overall adjustment factor
        Adjustor = -Error / (1 + abs(Error))
        
        # Calculates \iota for each layer
        layer_iotas = []
        for layer in self.structure:
            layer_iota = 0
            for neuron in layer:
                for weight in neuron:
                    layer_iota += abs(weight)
            layer_iotas.append(layer_iota)
        
        # Calculates \Sigma for the network
        sigma_s = sum(layer_iotas) + 1e-10
        
        # Utiliy functions
        Neuro_Adjustor = lambda x, a: [(1 - (1 / (abs(a)))) * i for i in x]
        Layer_Adjustor = lambda lay, total: 1 - (lay / total)
        
        neo = []
        
        # Adjust the weights
        for i, layer in enumerate(self.structure):
            curr_lay = []
            for neuron in layer:
                neuron_budget = Adjustor * Layer_Adjustor(layer_iotas[i], sigma_s) + lr
                # print(f"Neuron Budget: {neuron_budget}")
                neuron = Neuro_Adjustor(neuron, neuron_budget)
                curr_lay.append(neuron)
            neo.append(curr_lay)
        self.structure = neo
        pass

test = Network()
fc = test.cycle([30])
print(fc, "--"*20)
fi = test.structure
test.backcycle(fc, 0.5, 0.01)
print(test.cycle([30]), "--"*20)