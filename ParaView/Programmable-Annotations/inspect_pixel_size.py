"""module docstring should be here"""

import vtk

# Get the input image
input_data = self.GetInputDataObject(0, 0)
image = vtk.vtkImageData.SafeDownCast(input_data)

# Get the spacing of the image data
spacing = image.GetSpacing()

# Format the pixel size as a string, using a superscripted 3
pixel_size_str = f'Pixel size (=image\'s spacing): {spacing[0]:.2f} x {spacing[1]:.2f} x {spacing[2]:.2f} mm\u00B3'

to = self.GetTableOutput()
arr = vtk.vtkStringArray()
arr.SetName("Text")
arr.SetNumberOfComponents(1)
arr.InsertNextValue(pixel_size_str)
to.AddColumn(arr)
