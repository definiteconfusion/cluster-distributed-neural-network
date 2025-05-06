import random
import subprocess

def Neuron(weight, values):
    values = [str(i) for i in values]
    return float(subprocess.check_output(['./neuron', str(weight)] + values).decode('utf-8').strip())
    
def Build_Layer(size):
    return [random.uniform(-0.5, 0.5) for _ in range(size)]

def Build_Structure(layers, size):
    return [[Build_Layer(size) for _ in range(layer)] for layer in layers][0]