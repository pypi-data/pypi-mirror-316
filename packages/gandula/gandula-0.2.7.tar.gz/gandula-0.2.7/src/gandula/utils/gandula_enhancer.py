import pandas as pd

from ..providers.pff.schema.tracking import PFF_Frame
from ..schemas.frame.schema import GandulaFrame
from ..schemas.pitch import (
    GandulaPitchCoordinateCenter,
    GandulaPitchSize,
    PredefinedGandulaPitchSize,
    transform_coordinates,
)
from .pff_tracking_enhancer import (
    _change_pff_frame_pitch_standards,
)


def change_pitch_standards(
    frames: list[PFF_Frame] | tuple[pd.DataFrame, pd.DataFrame],
    pitch_size: GandulaPitchSize,
    pitch_center: GandulaPitchCoordinateCenter,
) -> list[GandulaFrame | tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Changes the pitch standards of the frames.

    Args:
        frames: A list of PFF_Frame objects.
        pitch_size: The new pitch size.
        pitch_center: The new pitch center.

    Returns:
        A list of GandulaFrame objects or a pandas DataFrame.
    """
    # check type of frames
    # TODO: as new providers are added, this will need to be updated
    if isinstance(frames, list):
        if isinstance(frames[0], PFF_Frame):
            new_frames = []
            for frame in frames:
                new_frames.append(
                    _change_pff_frame_pitch_standards(frame, pitch_size, pitch_center)
                )
            return new_frames
        elif isinstance(frames[0], GandulaFrame):
            return _change_gandula_pitch_standards(frames, pitch_size, pitch_center)
        else:
            raise NotImplementedError(
                'Only PFF_Frame and GandulaFrame objects are supported for lists.'
            )
    elif isinstance(frames, tuple):
        metadata_df, players_ball_df = frames
        if not isinstance(metadata_df, pd.DataFrame) or not isinstance(
            players_ball_df, pd.DataFrame
        ):
            raise ValueError('The tuple must contain two pandas DataFrames.')

        # check if there is columns 'pitch_size' and 'pitch_center'
        if 'pitch_size' in metadata_df.columns:
            current_pitch_size = metadata_df['pitch_size'].iloc[0]
        else:  # assumes PFF standard
            current_pitch_size = PredefinedGandulaPitchSize(type='meters')

        if 'pitch_center' in metadata_df.columns:
            current_pitch_center = metadata_df['pitch_center'].iloc[0]
        else:  # assumes PFF standard
            current_pitch_center = GandulaPitchCoordinateCenter.CENTRE_SPOT

        players_ball_df['x'], players_ball_df['y'] = transform_coordinates(
            players_ball_df['x'],
            players_ball_df['y'],
            current_pitch_center,
            pitch_center,
            current_pitch_size,
            pitch_size,
        )

        players_ball_df['ball_x'], players_ball_df['ball_y'] = transform_coordinates(
            players_ball_df['ball_x'],
            players_ball_df['ball_y'],
            current_pitch_center,
            pitch_center,
            current_pitch_size,
            pitch_size,
        )

        metadata_df['pitch_size'] = [pitch_size] * len(metadata_df)
        metadata_df['pitch_center'] = [pitch_center] * len(metadata_df)

        return frames

    raise ValueError(f'Cannot change pitch standards of object of type {type(frames)}')


def _change_gandula_pitch_standards(
    frames: list[GandulaFrame],
    pitch_size: GandulaPitchSize,
    pitch_center: GandulaPitchCoordinateCenter,
) -> list[GandulaFrame]:
    """
    Changes the pitch standards of the frames.

    Args:
        frames: A list of GandulaFrame objects.
        pitch_size: The new pitch size.
        pitch_center: The new pitch center.

    Returns:
        A list of GandulaFrame objects.
    """
    new_frames = []
    for frame in frames:
        new_frame = frame.copy()
        if isinstance(frame.frame, PFF_Frame):
            new_frame = _change_pff_frame_pitch_standards(
                frame.frame,
                pitch_size,
                pitch_center,
                frame.pitch_size,
                frame.pitch_center,
            )
        else:
            raise NotImplementedError('Only PFF_Frame objects are supported.')

        new_frames.append(new_frame)
    return new_frames
