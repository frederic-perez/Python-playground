# Import necessary modules
import vtk
import numpy as np

# Get the input data object
inData = self.GetInputDataObject(0, 0)
dims = inData.GetDimensions()

# Create a reslice object and set the input and output data
reslice = vtk.vtkImageReslice()
reslice.SetInputData(inData)

# Set the reslice transform and the interpolation type
reslice.SetOutputSpacing(2.0, 2.0, 2.0)
reslice.SetInterpolationModeToNearestNeighbor()

# Update and output the resampled data
reslice.Update()
output.ShallowCopy(reslice.GetOutput())
