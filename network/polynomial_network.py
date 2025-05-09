import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from random import random as rnd
def create_heatmaps_for_matrices(matrices, cmap='coolwarm', figsize_per_matrix=(5, 4), 
                                 max_cols=3, global_scale=False, show_colorbar=False, save_path=None):
    n = len(matrices)
    cols = min(n, max_cols)
    rows = (n + cols - 1) // cols  # Ceiling division
    
    # Calculate the figure size
    fig_width = figsize_per_matrix[0] * cols
    fig_height = figsize_per_matrix[1] * rows
    
    # Create the figure and axes - careful with the dimensions
    fig = plt.figure(figsize=(fig_width, fig_height))
    
    # Calculate global min and max if needed
    if global_scale:
        global_min = min(np.min(matrix) for matrix in matrices)
        global_max = max(np.max(matrix) for matrix in matrices)
        norm = Normalize(vmin=global_min, vmax=global_max)
    
    # Create each heatmap
    for i, matrix in enumerate(matrices):
        # Create a subplot for this matrix
        ax = fig.add_subplot(rows, cols, i + 1)  # 1-based indexing for add_subplot
        
        # Find the min and max for this matrix
        v_min = np.min(matrix)
        v_max = np.max(matrix)
        
        # Create the heatmap
        if global_scale:
            im = ax.imshow(matrix, cmap=cmap, norm=norm)
            title_suffix = f" (global scale: {global_min:.2f} to {global_max:.2f})"
        else:
            im = ax.imshow(matrix, cmap=cmap, vmin=v_min, vmax=v_max)
            title_suffix = f" (V_min: {v_min:.2f}, V_max: {v_max:.2f})"
        
        # Add a colorbar to each heatmap (optional)
        if show_colorbar:
            plt.colorbar(im, ax=ax)
        
        # Set title and axis labels
        ax.set_title(f"Matrix {i+1}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        
        # Optional: show grid lines
        ax.set_xticks(np.arange(matrix.shape[1]))
        ax.set_yticks(np.arange(matrix.shape[0]))
        ax.grid(False)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    else:
        plt.show()

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
        adapt_sigmoid = lambda x, t=5: 2 / t*x**3
        def net_mse(matrices):
            # Create a copy to avoid modifying the original list
            matrices_copy = matrices.copy()
            
            # Get the first matrix
            first_matrix = matrices_copy[0]
            
            # Start with the transpose of the first matrix
            current = np.transpose(first_matrix)  # Shape: (1,3)
            
            # Multiply with the second matrix
            if len(matrices_copy) > 1:
                current = np.dot(current, matrices_copy[1])  # (1,3) dot (3,1) = (1,1)
            
            # If there are more matrices, we need to adjust dimensions
            for i in range(2, len(matrices_copy)):
                # For subsequent multiplications, we need to transpose the next matrix
                # to match dimensions: (1,1) dot (1,3) = (1,3)
                current = np.dot(current, np.transpose(matrices_copy[i]))

            for i in range(len(current)):
                current[i] = np.abs(current[i])
                
            return current
        
        def sum_nested(mat):
            sig = 0
            for list in mat:
                sig+=sum(list)
            return sig
        NetWeight = np.sum(net_mse(self.network))
        Error = ((self.last_output - expectation) / expectation)**2
        # Grad = NetWeight * Error
        Grad = NetWeight * Error
        layer_sums = []
        for layer in self.network:
            layer_sums.append(sum_nested(layer))
        total_sum = sum(layer_sums)
        # Layer
        for i in range(len(self.network)):
            # Neuron
            for j in range(self.network[i].shape[0]):
                    # Weight
                for k in range(self.network[i].shape[1]):
                    adf = adapt_sigmoid((layer_sums[i]) / (total_sum)) * adapt_sigmoid((sum(self.network[i][j])) / (layer_sums[i])) * Grad + lr
                    self.network[i][j][k] *= adf
            
            
        pass
    
Net = Network()
Net.create_random_weights([5, 5, 5], 1)

diffs = []

for i, layer in enumerate(Net.network):
    print(f"Layer {i}:\n{layer}\n")
training_data = [([2], 4), ([3], 9), ([4], 16), ([5], 25)]
for input_val, expected in training_data:
    for _ in range(10):  # epochs
        Net.forcycle(input_val)
        Net.backcycle(expected, lr=0.1)

print(Net.forcycle([7]), "Expected:", 49)  

for i, layer in enumerate(Net.network):
    print(f"Layer {i}:\n{layer}\n")