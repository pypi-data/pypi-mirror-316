from enum import Enum


class GandulaPitchCoordinateCenter(Enum):
    CENTRE_SPOT = 'centre_spot'
    BOTTOM_LEFT_CORNER = 'bottom_left_corner'
    TOP_LEFT_CORNER = 'top_left_corner'


class GandulaPitchSizeType(str, Enum):
    METERS = 'meters'
    YARDS = 'yards'
    CUSTOM = 'custom'
