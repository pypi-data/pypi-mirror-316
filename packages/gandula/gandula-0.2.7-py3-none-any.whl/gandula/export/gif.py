"""Exports sequences of frames as gifs."""

import io
from pathlib import Path

import imageio
from matplotlib.pyplot import close, savefig
from pygifsicle import optimize

from ..providers.pff.schema.tracking import PFF_Frame
from ..visualization.frame import view_pff_frame


def export_frame_sequence_as_gif(frames: list[PFF_Frame], filename: str, fps=25) -> str:
    """
    Exports a sequence of frames as a GIF file.

    Args:
    ----------
    frames (list of dict): List of frames, each containing player and ball positions.
    filename : (str): Filename to save the GIF.
    fps (int): Frames per second for the GIF.
    """
    images = []

    for frame in frames:
        ax = view_pff_frame(frame)

        fig = ax.get_figure()

        buf = io.BytesIO()
        savefig(buf, format='png')

        buf.seek(0)
        images.append(imageio.mimread(buf))

        close(fig)
        buf.close()

    if not filename.endswith('.gif'):
        filename = f'{filename}.gif'

    with imageio.get_writer(filename, fps=fps, mode='I') as writer:
        for img in images:
            writer.append_data(img)

    optimize(filename)  # shrinks the gif size

    return Path(filename).resolve().as_uri()
