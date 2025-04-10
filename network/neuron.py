import random
import subprocess

def Neuron(weight, values):
    values = [str(i) for i in values]
    return float(subprocess.check_output(['./neuron', str(weight)] + values).decode('utf-8').strip())
    
def Build_Neuron(size):
    return [random.uniform(-0.5, 0.5) for _ in range(size)]

def Build_Structure(layers:int, size:int):
    struct = []
    for layer in range(layers):
        c_layer = []
        last_size = size if layer == 0 else len(struct[-1])
        for neuron in range(size):
            c_layer.append(Build_Neuron(last_size))
        struct.append(c_layer)
    return struct

# [print(Build_Structure(3, 5)) for _ in range(1)]