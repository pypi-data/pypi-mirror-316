"""Exports frames and events as pngs."""

from pathlib import Path

from matplotlib.pyplot import close, savefig

from ..providers.pff.schema.tracking import PFF_Frame
from ..visualization.frame import view_pff_frame


def export_frame_sequence_as_png(
    frames: list[PFF_Frame], filename: str, **kwargs
) -> list[str]:
    """Exports a sequence of frames as PNG files.

    Args:
    -----
    frames (list of dict): List of frames, each containing player and ball positions.
    filename : (str): Path to save the PNG files.
    """
    paths = []

    if filename.endswith('.png'):
        filename = filename[:-4]

    for index, frame in enumerate(frames):
        ax = view_pff_frame(frame)
        fig = ax.get_figure()
        filepath = f'{filename}_{index}.png'
        savefig(filepath, bbox_inches='tight', dpi=100)
        paths.append(Path(filepath).resolve().as_uri())
        close(fig)

    return paths
