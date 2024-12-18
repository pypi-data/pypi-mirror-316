from typing import TypeAlias

from ..providers.pff.schema.tracking import (
    PFF_Frame,
)
from ..schemas.frame.schema import GandulaFrame
from ..schemas.pitch import (
    GandulaPitchCoordinateCenter,
    GandulaPitchSize,
    PredefinedGandulaPitchSize,
    transform_coordinates,
)

PlayerIdShirt: TypeAlias = dict[str, tuple[int, bool]]


def _change_pff_frame_pitch_standards(
    frame: PFF_Frame,
    new_size: GandulaPitchSize,
    new_center: GandulaPitchCoordinateCenter,
    current_size: GandulaPitchSize = PredefinedGandulaPitchSize(type='meters'),  # noqa: B008
    current_center: GandulaPitchCoordinateCenter = GandulaPitchCoordinateCenter.CENTRE_SPOT,  # noqa: E501
) -> GandulaFrame:
    """
    Changes the pitch standards of the frame.

    Args:
        frame: A PFF_Frame object.
        new_size: The new pitch size.
        new_center: The new pitch coordinate center.
        current_size: The current pitch size.
        current_center: The current coordinate center.

    Returns:
        A GandulaFrame object with updated coordinates.
    """

    new_frame = frame.copy()

    # List of attributes to transform
    attributes_to_transform = [
        'ball_with_kalman',
        'ball',
        'home_players',
        'away_players',
        'home_players_with_kalman',
        'away_players_with_kalman',
    ]

    for attr_name in attributes_to_transform:
        attr = getattr(new_frame, attr_name, None)
        if attr is None:
            continue  # Skip if the attribute doesn't exist

        # Check if the attribute is a list of objects
        if isinstance(attr, list):
            for obj in attr:
                if (
                    hasattr(obj, 'x')
                    and hasattr(obj, 'y')
                    and obj.x is not None
                    and obj.y is not None
                ):
                    # Transform coordinates
                    x_new, y_new = transform_coordinates(
                        x=obj.x,
                        y=obj.y,
                        from_center=current_center,
                        to_center=new_center,
                        from_pitch_size=current_size,
                        to_pitch_size=new_size,
                    )
                    # Update object with new coordinates
                    obj.x = x_new
                    obj.y = y_new
        else:
            # Single object with x and y attributes
            if (
                hasattr(attr, 'x')
                and hasattr(attr, 'y')
                and attr.x is not None
                and attr.y is not None
            ):
                x_new, y_new = transform_coordinates(
                    x=attr.x,
                    y=attr.y,
                    from_center=current_center,
                    to_center=new_center,
                    from_pitch_size=current_size,
                    to_pitch_size=new_size,
                )
                # Update attribute with new coordinates
                attr.x = x_new
                attr.y = y_new

    # Create and return the updated GandulaFrame
    return GandulaFrame(
        frame=new_frame,
        pitch_center=new_center,
        pitch_size=new_size,
    )
