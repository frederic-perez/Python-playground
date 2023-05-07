"""module docstring should be here"""

import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np

input_data = self.GetInputDataObject(0, 0)
image = vtk.vtkImageData.SafeDownCast(input_data)
#print(image)
point_data = image.GetPointData()
array = image.GetPointData().GetArray(0)
#print(array)
max_label = int(array.GetRange()[1])
num_tuples = array.GetNumberOfTuples()
print(f'» max_label = {max_label}; #tuples = {num_tuples:,}')

# Convert the VTK image to a numpy array
numpy_array = vtk.util.numpy_support.vtk_to_numpy(image.GetPointData().GetScalars()).reshape(image.GetDimensions(), order='F')

# Create a copy of the numpy array
copy_numpy_array = np.copy(numpy_array)

print(numpy_array.shape)

# Iterate over each voxel in the numpy array
for i in range(1, numpy_array.shape[0]-1):
    for j in range(1, numpy_array.shape[1]-1):
        for k in range(1, numpy_array.shape[2]-1):
            # Check if value of voxel is the same as its neighbors
            if numpy_array[i, j, k] == numpy_array[i-1, j, k] \
                    and numpy_array[i, j, k] == numpy_array[i+1, j, k] \
                    and numpy_array[i, j, k] == numpy_array[i, j-1, k] \
                    and numpy_array[i, j, k] == numpy_array[i, j+1, k] \
                    and numpy_array[i, j, k] == numpy_array[i, j, k-1] \
                    and numpy_array[i, j, k] == numpy_array[i, j, k+1]:
                # Set value of voxel to zero in copy of numpy array
                copy_numpy_array[i, j, k] = 0

# Overwrite the original array
new_array = vtk.util.numpy_support.numpy_to_vtk(copy_numpy_array.ravel(order='F'), deep=True)
for i in range(num_tuples):
    array.SetTuple1(i, new_array.GetTuple1(i))
