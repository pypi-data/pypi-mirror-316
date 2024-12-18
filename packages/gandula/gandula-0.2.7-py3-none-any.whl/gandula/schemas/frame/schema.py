from gandula.providers.pff.schema.tracking import PFF_Frame
from gandula.schemas.pitch import GandulaPitchCoordinateCenter, GandulaPitchSize
from pydantic import BaseModel


class GandulaFrame(BaseModel):
    frame: PFF_Frame  # TODO: When new providers are added, this will need to be updated
    pitch_center: GandulaPitchCoordinateCenter
    pitch_size: GandulaPitchSize
