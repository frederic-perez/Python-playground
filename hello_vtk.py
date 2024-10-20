"""module docstring should be here"""

# This simple example shows how to do basic rendering and pipeline
# creation.

# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingFreeType
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2

from enum import Enum
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    VTK_UNSIGNED_CHAR,
    vtkLookupTable,
    vtkPoints,
    vtkUnsignedCharArray
)
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPiecewiseFunction,
    vtkPolyData
)
from vtkmodules.vtkFiltersCore import vtkExtractEdges
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import (
    # vtkOutlineCornerFilter, We now favor vtkOutlineFilter
    vtkSphereSource
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkGlyph3DMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
    vtkVolume,
    vtkVolumeProperty
)
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkSmartVolumeMapper

class Dimensionality(Enum):
    two_d = '2D'
    three_d = '3D'

def image_data_example(dimensionality: Dimensionality) -> None:
    """
    Originally based on the code from
    https://examples.vtk.org/site/Python/ImageData/WriteReadVtkImageData/
    """
    colors = vtkNamedColors()

    color_x = colors.GetColor3d("OrangeRed")
    color_y = colors.GetColor3d("LimeGreen")
    color_z = colors.GetColor3d("RoyalBlue")
    color_black = colors.GetColor3d("Black")
    color_gray = colors.GetColor3d("Gray")
    color_white = colors.GetColor3d("White")

    axes_actor = vtkAxesActor()
    axes_actor.SetTotalLength(1, 1, 1)  # Set the length of the axes
    axes_actor.SetShaftType(vtkAxesActor.CYLINDER_SHAFT)
    axes_actor.SetAxisLabels(0)  # Set to 0 to disable axis labels
    axes_actor.GetXAxisShaftProperty().SetColor(color_x)
    axes_actor.GetXAxisTipProperty().SetColor(color_x)
    axes_actor.GetYAxisShaftProperty().SetColor(color_y)
    axes_actor.GetYAxisTipProperty().SetColor(color_y)
    axes_actor.GetZAxisShaftProperty().SetColor(color_z)
    axes_actor.GetZAxisTipProperty().SetColor(color_z)

    image_data = vtkImageData()
    offset = 1
    image_data.SetDimensions(
        1 + offset,
        1 + offset,
        1 if dimensionality.value == Dimensionality.two_d.value else 1 + offset) # (4 + offset, 3 + offset, 2 + offset))

    image_data.SetSpacing(1, 1, 1)
    image_data.SetOrigin(0, 0, 0)

    image_data.AllocateScalars(VTK_UNSIGNED_CHAR, 1)

    # Calculate the total number of pixels
    dims = image_data.GetDimensions()
    total_points = dims[0] * dims[1] * dims[2]

    # Create an array to store pixel values
    scalar_array = vtkUnsignedCharArray()
    scalar_array.SetName("Scalars")
    scalar_array.SetNumberOfComponents(1)  # Single component per point
    scalar_array.SetNumberOfTuples(total_points)  # Total number of pixels
    scalar_array.Fill(0)

    index = image_data.ComputePointId((0, 0, 0))
    scalar_array.SetValue(index, 4)

    for z in 0,:
        for y in 0,:
            for x in range(1, dims[0]):
                index = z * dims[1] * dims[0] + y * dims[0] + x  # (z * width * height + y * width + x)
                scalar_array.SetValue(index, 1)

    for z in 0,:
        for y in range(1, dims[1]):
            for x in 0,:
                index = z * dims[1] * dims[0] + y * dims[0] + x  # (z * width * height + y * width + x)
                scalar_array.SetValue(index, 2)

    for z in range(1, dims[2]):
        for y in 0,:
            for x in 0,:
                index = z * dims[1] * dims[0] + y * dims[0] + x  # (z * width * height + y * width + x)
                scalar_array.SetValue(index, 3)

    # Attach array to image data
    image_data.GetPointData().SetScalars(scalar_array)

    # Optionally, you can print the values to verify
    for z in range(dims[2]):
        for y in range(dims[1]):
            for x in range(dims[0]):
                val = image_data.GetScalarComponentAsDouble(x, y, z, 0)
                print(f"Value at ({x}, {y}, {z}): {val}")

    # Map the scalar data using a lookup table
    lookup_table = vtkLookupTable()
    lookup_table.SetNumberOfTableValues(5)
    lookup_table.Build()

    # Define colors for each index
    palette_colors = [
        color_gray,
        color_x,
        color_y,
        color_z,
        color_white
    ]
    for i, color in enumerate(palette_colors):
        lookup_table.SetTableValue(i, *color, 1.0)  # (r, g, b, opacity)

    # Extract information from the vtkImageData object
    spacing = image_data.GetSpacing()
    bounds = image_data.GetBounds()
    scalars = image_data.GetPointData().GetScalars()
    scalars_range = scalars.GetRange()
    scalars_type_str = scalars.GetDataTypeAsString()
    dims_str = f"Dimensions: {dims}"
    spacing_str = f"Spacing: {spacing}"
    bounds_str = f"Bounds: [{bounds[0]}, {bounds[1]}] x [{bounds[2]}, {bounds[3]}] x [{bounds[4]}, {bounds[5]}]"
    delta_str = f"Delta: [{bounds[1] - bounds[0]}, {bounds[3] - bounds[2]}, {bounds[5] - bounds[4]}]"
    scalars_range_str = f"Scalars range: {scalars_range} [{scalars_type_str}]"

    # Create a text actor to display the information
    text_actor = vtkTextActor()
    text_actor.SetTextScaleModeToNone()
    text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
    text_actor.SetInput(f"{dims_str}\n{spacing_str}\n{bounds_str}\n{delta_str}\n{scalars_range_str}")
    text_actor_property = text_actor.GetTextProperty()
    text_actor_property.SetFontSize(14)
    text_actor_property.SetColor(*color_white)
    # Set the position with margins (e.g., 0.1 for left margin and 0.1 for bottom margin)
    left_margin = 0.01
    bottom_margin = left_margin * 1024 / 576
    text_actor.SetPosition(left_margin, bottom_margin)

    outline_filter = vtkOutlineFilter()  # vtkOutlineCornerFilter()
    outline_filter.SetInputData(image_data)

    # Set up the mapper and actor for rendering
    outline_mapper = vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

    outline_actor = vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(color_white)
    outline_actor.GetProperty().SetLineWidth(3)  # Optionally, set the line width for better visibility

    #
    # Create a vtkPoints object to hold the voxel centers
    #
    points = vtkPoints()
    # Loop through the image data and get the center of each voxel
    for z in range(dims[2]):
        for y in range(dims[1]):
            for x in range(dims[0]):
                # Get the voxel center in world coordinates
                center = [0, 0, 0]
                image_data.GetPoint(image_data.ComputePointId([x, y, z]), center)
                # Add the point to vtkPoints
                points.InsertNextPoint(center)
    # Create a vtkPolyData object to hold the points
    point_polydata = vtkPolyData()
    point_polydata.SetPoints(points)
    # Create the sphere source
    sphere_source = vtkSphereSource()
    sphere_source.SetRadius(.075)
    sphere_source.SetThetaResolution(20)  # Increase theta resolution
    sphere_source.SetPhiResolution(20)  # Increase phi resolution
    # Create a mapper
    glyph_mapper = vtkGlyph3DMapper()
    glyph_mapper.SetInputData(image_data)
    glyph_mapper.SetSourceConnection(sphere_source.GetOutputPort())
    glyph_mapper.SetLookupTable(lookup_table)
    glyph_mapper.SetScalarRange(0, 4)  # Map from 0 to 4
    glyph_mapper.ScalarVisibilityOn()
    glyph_mapper.SetColorModeToMapScalars()
    # Create an actor
    glyph_actor = vtkActor()
    glyph_actor.SetMapper(glyph_mapper)
    glyph_actor.GetProperty().SetSpecular(0.65)
    glyph_actor.GetProperty().SetSpecularPower(100)  # Set the specular power, larger values mean more shiny

    # -- edges begin
    #
    extract_edges = vtkExtractEdges()
    extract_edges.SetInputData(image_data)

    edges_mapper = vtkPolyDataMapper()
    edges_mapper.SetInputConnection(extract_edges.GetOutputPort())

    edges_actor = vtkActor()
    edges_actor.SetMapper(edges_mapper)
    edges_actor.GetProperty().SetColor(color_white)
    edges_actor.GetProperty().SetLineWidth(1)  # Optionally, set the line width for better visibility
    #
    # -- edges end

    # -- volume begin
    #
    volume_mapper = vtkSmartVolumeMapper()
    volume_mapper.SetInputData(image_data)

    volume_actor = vtkVolume()
    volume_actor.SetMapper(volume_mapper)

    color_func = vtkColorTransferFunction()
    color_func.AddRGBPoint(0.0, *color_black)
    color_func.AddRGBPoint(1.0, *color_x)
    color_func.AddRGBPoint(2.0, *color_y)
    color_func.AddRGBPoint(3.0, *color_z)
    color_func.AddRGBPoint(4.0, *color_white)
    color_func.AddRGBPoint(5.0, *color_black)

    opacity_func = vtkPiecewiseFunction()
    opacity_func.AddPoint(0.0, 0.0)
    opacity_func.AddPoint(1.0, 0.75)
    opacity_func.AddPoint(2.0, 0.75)
    opacity_func.AddPoint(3.0, 0.75)
    opacity_func.AddPoint(4.0, 0.75)
    opacity_func.AddPoint(5.0, 0.0)

    volume_property = vtkVolumeProperty()
    volume_property.SetColor(color_func)
    volume_property.SetScalarOpacity(opacity_func)
    volume_property.SetInterpolationTypeToNearest()

    volume_actor.SetProperty(volume_property)
    #
    # -- volume end

    # Create a renderer, render window, and interactor
    renderer = vtkRenderer()
    renderer.AddActor2D(text_actor)
    renderer.AddActor(axes_actor)
    renderer.AddActor(edges_actor)
    renderer.AddActor(glyph_actor)
    renderer.AddActor(outline_actor)
    renderer.AddActor(volume_actor)
    renderer.SetBackground(colors.GetColor3d("MidnightBlue"))  # Charcoal

    # Configure the camera
    center = (
        (bounds[1] + bounds[0]) / 2.0,
        (bounds[3] + bounds[2]) / 2.0,
        (bounds[5] + bounds[4]) / 2.0
    )
    camera = renderer.GetActiveCamera()
    if dimensionality.value == Dimensionality.two_d.value:
        z_offset = 3.  # Adjust as needed for how far away the camera is
        camera.SetPosition(
            center[0],
            center[1],
            center[2] + z_offset)
        camera.SetFocalPoint(center)
        camera.SetViewUp(0, 1, 0)
    else:
        distance_multiplier = 1.5  # Adjust as needed for how far away the camera is
        camera.SetPosition(
            center[0] + distance_multiplier * 0.9 * (bounds[1] - bounds[0]),
            center[1] + distance_multiplier * 1.2 * (bounds[3] - bounds[2]),
            center[2] + distance_multiplier * 0.1 * (bounds[5] - bounds[4]))
        camera.SetFocalPoint(center)
        camera.SetViewUp(0, 0, 1)

    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(1024, 576)  # Set window size

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    style = vtkInteractorStyleTrackballCamera()
    interactor.SetInteractorStyle(style)

    # Start the rendering
    interactor.Initialize()
    render_window.Render()
    interactor.Start()

if __name__ == '__main__':
    image_data_example(Dimensionality.two_d)
    image_data_example(Dimensionality.three_d)