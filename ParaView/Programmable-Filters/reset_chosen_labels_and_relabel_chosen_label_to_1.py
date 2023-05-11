"""module docstring should be here"""

import vtk

input_data = self.GetInputDataObject(0, 0)
image = vtk.vtkImageData.SafeDownCast(input_data)
#print(image)
point_data = image.GetPointData()
scalar_array = image.GetPointData().GetArray(0)
#print(scalar_array)
max_label = int(scalar_array.GetRange()[1])
num_tuples = scalar_array.GetNumberOfTuples()
print(f'» max_label = {max_label}; #tuples = {num_tuples:,}')
labels_to_reset = 1, 2, 3, 5
label_to_relabel_to_1 = 4
num_pixels_reset = 0
new_array_np = vtk.util.numpy_support.vtk_to_numpy(scalar_array)
for i in range(0, num_tuples):
    label_value = scalar_array.GetValue(i)
    if label_value in labels_to_reset:
        new_array_np[i] = 0
        num_pixels_reset += 1
    elif label_value == label_to_relabel_to_1:
        new_array_np[i] = 1

print(f'» #pixels_reset = {num_pixels_reset:,}')

output.PointData.append(new_array_np, "new_array")
