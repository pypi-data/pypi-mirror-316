# Generated file. To retain edits, remove this comment.

from pathlib import Path, PurePosixPath
import os
from typing import Dict, Tuple, Optional, List, Any

from importlib_resources import files as file_resources

_pipeline = None

from itkwasm import (
    InterfaceTypes,
    PipelineOutput,
    PipelineInput,
    Pipeline,
    Image,
    Mesh,
)

def cuberille(
    image: Image,
    interpolator: str = "linear",
    iso_surface_value: float = 1,
    quadrilateral_faces: bool = False,
    no_projection: bool = False,
    image_pixel_to_cell_data: bool = False,
    surface_distance_threshold: float = 0.01,
    step_length: float = -1,
    step_relaxation_factor: float = 0.75,
    maximum_steps: int = 150,
) -> Mesh:
    """Create a mesh from an image via cuberille implicit surface polygonization.

    :param image: Input image
    :type  image: Image

    :param interpolator: Interpolation method to use for the image. Valid values: linear, bspline, windowed-sync.
    :type  interpolator: str

    :param iso_surface_value: Value of the iso-surface for which to generate the mesh. Pixels equal to or greater than this value are considered to lie on the surface or inside the resultant mesh.
    :type  iso_surface_value: float

    :param quadrilateral_faces: Generate quadrilateral faces instead of triangle faces.
    :type  quadrilateral_faces: bool

    :param no_projection: Do not project the vertices to the iso-surface.
    :type  no_projection: bool

    :param image_pixel_to_cell_data: Whether the adjacent input pixel value should be saved as cell data in the output mesh.
    :type  image_pixel_to_cell_data: bool

    :param surface_distance_threshold: Threshold for the distance from the rface during vertex projection in pixel units. Smaller is smoother but takes longer.
    :type  surface_distance_threshold: float

    :param step_length: Initial step length for vertex projection in physical units. Default is max spacing * 0.35.
    :type  step_length: float

    :param step_relaxation_factor: The step length relaxation factor during vertex projection. The step length is multiplied by this factor each iteration to allow convergence, [0.0, 1.0].
    :type  step_relaxation_factor: float

    :param maximum_steps: The maximum number of steps used during vertex projection.
    :type  maximum_steps: int

    :return: Output mesh.
    :rtype:  Mesh
    """
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline(file_resources('itkwasm_cuberille_wasi').joinpath(Path('wasm_modules') / Path('cuberille.wasi.wasm')))

    pipeline_outputs: List[PipelineOutput] = [
        PipelineOutput(InterfaceTypes.Mesh),
    ]

    pipeline_inputs: List[PipelineInput] = [
        PipelineInput(InterfaceTypes.Image, image),
    ]

    args: List[str] = ['--memory-io',]
    # Inputs
    args.append('0')
    # Outputs
    mesh_name = '0'
    args.append(mesh_name)

    # Options
    input_count = len(pipeline_inputs)
    if interpolator:
        if interpolator not in ('linear,bspline,windowed-sinc'):
            raise ValueError(f'interpolator must be one of linear,bspline,windowed-sinc')
        args.append('--interpolator')
        args.append(str(interpolator))

    if iso_surface_value:
        args.append('--iso-surface-value')
        args.append(str(iso_surface_value))

    if quadrilateral_faces:
        args.append('--quadrilateral-faces')

    if no_projection:
        args.append('--no-projection')

    if image_pixel_to_cell_data:
        args.append('--image-pixel-to-cell-data')

    if surface_distance_threshold:
        args.append('--surface-distance-threshold')
        args.append(str(surface_distance_threshold))

    if step_length:
        args.append('--step-length')
        args.append(str(step_length))

    if step_relaxation_factor:
        args.append('--step-relaxation-factor')
        args.append(str(step_relaxation_factor))

    if maximum_steps:
        args.append('--maximum-steps')
        args.append(str(maximum_steps))


    outputs = _pipeline.run(args, pipeline_outputs, pipeline_inputs)

    result = outputs[0].data
    return result

