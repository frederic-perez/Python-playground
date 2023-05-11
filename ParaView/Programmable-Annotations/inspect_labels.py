"""module docstring should be here"""

import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np

input_data = self.GetInputDataObject(0, 0)
image = vtk.vtkImageData.SafeDownCast(input_data)
#print(image)
point_data = image.GetPointData()
scalar_array = image.GetPointData().GetArray(0)
#print(scalar_array)
max_label = int(scalar_array.GetRange()[1])
num_tuples = scalar_array.GetNumberOfTuples()
string = '$ID$ | # | %'  # f'max_label = {max_label}; #tuples = {num_tuples:,}'
scalar_array_np = vtk.util.numpy_support.vtk_to_numpy(scalar_array)
for label in range(0, max_label + 1):
    acc = np.count_nonzero(scalar_array_np == label)
    string += f'\n{label} | {acc:,} | {100*acc/num_tuples:.1f}'

to = self.GetTableOutput()
arr = vtk.vtkStringArray()
arr.SetName("Text")
arr.SetNumberOfComponents(1)
arr.InsertNextValue(string)
to.AddColumn(arr)
