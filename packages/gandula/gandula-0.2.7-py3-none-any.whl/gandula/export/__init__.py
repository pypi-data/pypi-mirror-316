"""Modules for exporting data in different formats."""

from typing import Callable, Literal

from pandas import DataFrame

from ..providers.pff.schema.tracking import PFF_Frame
from .dataframe import pff_frames_to_dataframe
from .gif import export_frame_sequence_as_gif
from .png import export_frame_sequence_as_png

ExportFormat = Literal['gif', 'png', 'dataframe']

__all__ = ['export']


_image_exporters: dict[ExportFormat, Callable] = {
    'gif': export_frame_sequence_as_gif,
    'png': export_frame_sequence_as_png,
    'dataframe': pff_frames_to_dataframe,
}


def export(
    frames: list[PFF_Frame] | PFF_Frame,
    *,
    fmt: ExportFormat,
    fps=25,
    filename: str | None = None,
    **kwargs,
) -> str | list[str] | tuple[DataFrame, DataFrame]:
    """Exports a sequence of frames as a GIF or PNG files."""
    if isinstance(frames, PFF_Frame):
        frames = [frames]
    return _image_exporters[fmt](frames, filename=filename, fps=fps, **kwargs)
