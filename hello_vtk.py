"""module docstring should be here"""

# This simple example shows how to do basic rendering and pipeline
# creation.

# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingFreeType
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    VTK_UNSIGNED_CHAR,
    vtkLookupTable,
    vtkPoints,
    vtkUnsignedCharArray
)
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPolyData
)
from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
    vtkOutlineCornerFilter,
    vtkSphereSource
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor
)

def image_data_example() -> None:
    """
    Originally based on the code from
    https://examples.vtk.org/site/Python/ImageData/WriteReadVtkImageData/
    """
    colors = vtkNamedColors()

    image_data = vtkImageData()
    offset = 1
    image_data.SetDimensions(4 + offset, 3 + offset, 2 + offset)
    image_data.SetSpacing(1, 1, 1)
    image_data.SetOrigin(0, 0, 0)

    image_data.AllocateScalars(VTK_UNSIGNED_CHAR, 1)

    # Extract information from the vtkImageData object
    origin = image_data.GetOrigin()
    dims = image_data.GetDimensions()
    spacing = image_data.GetSpacing()
    bounds = image_data.GetBounds()
    origin_str = f"Origin: {origin}"
    dims_str = f"Dimensions: {dims}"
    spacing_str = f"Spacing: {spacing}"
    bounds_str = f"Bounds: {bounds}"

    # Calculate the total number of pixels
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
        colors.GetColor3d("Gray"),
        colors.GetColor3d("OrangeRed"),
        colors.GetColor3d("LimeGreen"),
        colors.GetColor3d("RoyalBlue"),
        colors.GetColor3d("White")
    ]
    for i, color in enumerate(palette_colors):
        lookup_table.SetTableValue(i, *color, 1.0)  # (r, g, b, opacity)

    # Create a text actor to display the information
    text_actor = vtkTextActor()
    text_actor.SetInput(f"{origin_str}\n{dims_str}\n{spacing_str}\n{bounds_str}")
    text_actor_property = text_actor.GetTextProperty()
    text_actor_property.SetFontSize(14)
    text_actor_property.SetColor(1.0, 1.0, 1.0)  # White color

    outline_filter = vtkOutlineCornerFilter()
    outline_filter.SetInputData(image_data)

    # Set up the mapper and actor for rendering
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(outline_filter.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 1, 1)

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
    sphere_source.SetRadius(.1)
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

    # -- box begin
    #
    box = vtkCubeSource()
    box.SetXLength(1.0)
    box.SetYLength(1.0)
    box.SetZLength(1.0)
    box.Update()

    box_mapper = vtkPolyDataMapper()
    box_mapper.SetInputConnection(box.GetOutputPort())

    box_actor = vtkActor()
    box_actor.SetMapper(box_mapper)
    box_actor_property = box_actor.GetProperty()
    box_actor_property.SetColor(colors.GetColor3d("White"))
    box_actor_property.SetRepresentationToSurface()
    box_actor_property.SetOpacity(.5)
    #
    # -- box end

    # Create a renderer, render window, and interactor
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.AddActor(glyph_actor)
    renderer.AddActor2D(text_actor)
    renderer.AddActor(box_actor)
    renderer.SetBackground(colors.GetColor3d("MidnightBlue"))  # Charcoal

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
    image_data_example()