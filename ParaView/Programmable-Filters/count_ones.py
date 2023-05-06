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
num_tuples = scalar_array.GetNumberOfTuples()
scalar_array_np = vtk.util.numpy_support.vtk_to_numpy(scalar_array)
num_ones = np.count_nonzero(scalar_array_np == 1)
print(f'#ones = {num_ones:,}, {100*num_ones/num_tuples:.1f}% of {num_tuples:,} tuples')
