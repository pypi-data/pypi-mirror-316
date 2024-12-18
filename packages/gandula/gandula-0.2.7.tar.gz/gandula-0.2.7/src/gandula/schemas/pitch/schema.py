from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, model_validator

from .enums import GandulaPitchSizeType


class BaseGandulaPitchSize(BaseModel):
    type: GandulaPitchSizeType

    class Config:
        discriminator = 'type'


class PredefinedGandulaPitchSize(BaseGandulaPitchSize):
    type: Literal[GandulaPitchSizeType.METERS, GandulaPitchSizeType.YARDS]
    x_axis: int = None
    y_axis: int = None

    @model_validator(mode='before')
    def set_predefined_dimensions(cls, values):
        size_type = values.get('type')
        if size_type == GandulaPitchSizeType.METERS:
            values['x_axis'] = 105
            values['y_axis'] = 68
        elif size_type == GandulaPitchSizeType.YARDS:
            values['x_axis'] = 115
            values['y_axis'] = 74
        else:
            raise ValueError(f'Invalid type {size_type}')
        return values


class CustomGandulaPitchSize(BaseGandulaPitchSize):
    type: Literal[GandulaPitchSizeType.CUSTOM]
    x_axis: int = Field(..., description='Custom x-axis length')
    y_axis: int = Field(..., description='Custom y-axis length')

    @model_validator(mode='before')
    def validate_custom_dimensions(cls, values):
        # Proceed with validation
        if values.get('x_axis') is None or values.get('y_axis') is None:
            raise ValueError('Custom pitch size must have x_axis and y_axis')
        if values.get('x_axis') <= 0 or values.get('y_axis') <= 0:
            raise ValueError('Custom pitch size must be positive')
        return values


GandulaPitchSize = Annotated[
    Union[PredefinedGandulaPitchSize, CustomGandulaPitchSize],
    Field(discriminator='type'),
]
