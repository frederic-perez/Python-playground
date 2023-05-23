"""module docstring should be here"""

# Get the input data
input_data = inputs[0]

# Get the dimensions of the input data
dims = input_data.GetDimensions()

# Create a new vtkImageData object with new origin with padding,
# same spacing, and dimensions increased by 2 in each direction
output_data = vtk.vtkImageData()
new_origin = [origin - spacing for origin, spacing in zip(input_data.GetOrigin(), input_data.GetSpacing())]
output_data.SetOrigin(new_origin)
output_data.SetSpacing(input_data.GetSpacing())
output_data.SetDimensions(dims[0]+2, dims[1]+2, dims[2]+2)

# Fill the output data with zeros
output_data.AllocateScalars(vtk.VTK_FLOAT, 1)
output_data.GetPointData().GetScalars().FillComponent(0, 0.0)

# Copy the input data into the output data with an offset of 1 in each direction
for k in range(dims[2]):
    for j in range(dims[1]):
        for i in range(dims[0]):
            output_data.SetScalarComponentFromFloat(i+1, j+1, k+1, 0, input_data.GetScalarComponentAsFloat(i, j, k, 0))

# Set the output of the filter
output.ShallowCopy(output_data)
