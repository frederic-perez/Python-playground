"""module docstring should be here"""

# This simple example shows how to do basic rendering and pipeline
# creation.

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import VTK_UNSIGNED_CHAR
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersSources import vtkOutlineCornerFilter
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera

from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

def image_data_example() -> None:
    """
    Originally based on the code from
    https://examples.vtk.org/site/Python/ImageData/WriteReadVtkImageData/
    """
    colors = vtkNamedColors()
    # Set the background color.
    colors.SetColor("BkgColor", colors.GetColor3d("MidnightBlue"))

    image_data = vtkImageData()
    image_data.SetDimensions(4, 3, 2)
    image_data.SetSpacing(1, 1, 1)
    image_data.SetOrigin(0, 0, 0)

    image_data.AllocateScalars(VTK_UNSIGNED_CHAR, 1)

    outline_filter = vtkOutlineCornerFilter()
    outline_filter.SetInputData(image_data)

    # Set up the mapper and actor for rendering
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(outline_filter.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 1, 1)

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
    box_actor.GetProperty().SetColor(colors.GetColor3d("Orange"))
    box_actor.GetProperty().SetRepresentationToWireframe()
    #
    # -- box end

    # Create a renderer, render window, and interactor
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.AddActor(box_actor)
    renderer.SetBackground(0.1, 0.2, 0.3)  # Set background color

    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(300, 300)  # Set window size

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