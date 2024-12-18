import pandas as pd
from gandula.schemas.pitch.enums import GandulaPitchCoordinateCenter
from gandula.schemas.pitch.schema import GandulaPitchSize


def _to_absolute_coordinates(
    x: float | pd.Series,
    y: float | pd.Series,
    center: GandulaPitchCoordinateCenter,
    pitch_size: GandulaPitchSize,
) -> tuple[float, float]:
    """
    Converts pitch coordinates to absolute coordinates.

    We'll use the bottom_left_corner as the absolute coordinate system because
    it has the simplest mapping (origin at the bottom-left corner,
    axes increasing right and up).

    Args:
        x: The x-coordinate.
        y: The y-coordinate.
        center: The center of the pitch coordinates.
        pitch_size: The size of the pitch.

    Returns:
        The absolute coordinates.
    """
    x_axis = pitch_size.x_axis
    y_axis = pitch_size.y_axis

    if center == GandulaPitchCoordinateCenter.CENTRE_SPOT:
        x_abs = x + x_axis / 2
        y_abs = y + y_axis / 2
    elif center == GandulaPitchCoordinateCenter.BOTTOM_LEFT_CORNER:
        x_abs = x
        y_abs = y
    elif center == GandulaPitchCoordinateCenter.TOP_LEFT_CORNER:
        x_abs = x
        y_abs = y_axis - y
    else:
        raise ValueError(f'Unknown coordinate center: {center}')

    return x_abs, y_abs


def _from_absolute_coordinates(
    x_abs: float | pd.Series,
    y_abs: float | pd.Series,
    center: GandulaPitchCoordinateCenter,
    pitch_size: GandulaPitchSize,
) -> tuple[float, float]:
    """
    Converts absolute coordinates to pitch coordinates.

    We'll use the bottom_left_corner as the absolute coordinate system because
    it has the simplest mapping (origin at the bottom-left corner,
    axes increasing right and up).

    Args:
        x_abs: The absolute x-coordinate.
        y_abs: The absolute y-coordinate.
        center: The center of the pitch coordinates.
        pitch_size: The size of the pitch.

    Returns:
        The pitch coordinates.
    """
    x_axis = pitch_size.x_axis
    y_axis = pitch_size.y_axis

    if center == GandulaPitchCoordinateCenter.CENTRE_SPOT:
        x = x_abs - x_axis / 2
        y = y_abs - y_axis / 2
    elif center == GandulaPitchCoordinateCenter.BOTTOM_LEFT_CORNER:
        x = x_abs
        y = y_abs
    elif center == GandulaPitchCoordinateCenter.TOP_LEFT_CORNER:
        x = x_abs
        y = y_axis - y_abs
    else:
        raise ValueError(f'Unknown coordinate center: {center}')

    return x, y


def _scale_coordinates(
    x_abs: float | pd.Series,
    y_abs: float | pd.Series,
    from_pitch_size: GandulaPitchSize,
    to_pitch_size: GandulaPitchSize,
) -> tuple[float, float]:
    """
    Scales coordinates from one pitch size to another.

    Args:
        x_abs: The absolute x-coordinate.
        y_abs: The absolute y-coordinate.
        from_pitch_size: The size of the original pitch.
        to_pitch_size: The size of the target pitch.

    Returns:
        The scaled coordinates.
    """

    x_scale = to_pitch_size.x_axis / from_pitch_size.x_axis
    y_scale = to_pitch_size.y_axis / from_pitch_size.y_axis

    x_scaled = x_abs * x_scale
    y_scaled = y_abs * y_scale

    return x_scaled, y_scaled


def transform_coordinates(
    x: float | pd.Series,
    y: float | pd.Series,
    from_center: GandulaPitchCoordinateCenter,
    to_center: GandulaPitchCoordinateCenter,
    from_pitch_size: GandulaPitchSize,
    to_pitch_size: GandulaPitchSize,
) -> tuple[float, float]:
    # Convert to absolute coordinates
    x_abs, y_abs = _to_absolute_coordinates(x, y, from_center, from_pitch_size)

    # Scale coordinates for pitch size change
    x_scaled, y_scaled = _scale_coordinates(
        x_abs, y_abs, from_pitch_size, to_pitch_size
    )

    # Convert from absolute coordinates to target coordinate center
    x_new, y_new = _from_absolute_coordinates(
        x_scaled, y_scaled, to_center, to_pitch_size
    )

    return x_new, y_new
