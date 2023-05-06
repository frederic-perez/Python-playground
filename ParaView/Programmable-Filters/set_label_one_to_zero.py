"""module docstring should be here"""

import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np

input_data = self.GetInputDataObject(0, 0)
image = vtk.vtkImageData.SafeDownCast(input_data)
#print(image)
point_data = image.GetPointData()
scalar_array = image.GetPointData().GetArray(0)
print(scalar_array)
max_label = int(scalar_array.GetRange()[1])
num_tuples = scalar_array.GetNumberOfTuples()
print(f'» max_label = {max_label}; #tuples = {num_tuples:,}')
label_to_reset = 1 #input('Label to reset: ')
num_pixels_reset = 0
for i in range(0, num_tuples):
    if scalar_array.GetValue(i) == label_to_reset:
        scalar_array.SetValue(i, 0)
        num_pixels_reset += 1

print(f'» #pixels_reset = {num_pixels_reset:,}')

# Set the modified scalar array back to the input dataset
input.GetPointData().SetScalars(array)

# Set the output to be the same as the input
output.ShallowCopy(input)
