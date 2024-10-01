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
    vtkPoints
)
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPolyData
)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
    vtkOutlineCornerFilter,
    vtkSphereSource
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
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
    image_data.SetDimensions(4, 3, 2)
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
    # Create a glyph to represent each point as a sphere
    glyph = vtkGlyph3D()
    glyph.SetSourceConnection(sphere_source.GetOutputPort())
    glyph.SetInputData(point_polydata)
    glyph.Update()
    # Create a mapper
    glyph_mapper = vtkPolyDataMapper()
    glyph_mapper.SetInputConnection(glyph.GetOutputPort())
    # Create an actor
    glyph_actor = vtkActor()
    glyph_actor.SetMapper(glyph_mapper)

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
    box_actor_property.SetColor(colors.GetColor3d("Orange"))
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