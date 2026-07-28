from . import aperture
from . import motion
from . import rotation
from . import transfer

from pigeon import BaseMessage
from pydantic import Field


class Absolute(BaseMessage):
    """
    This message includes absolute stage actuator locations.
    """

    linear: dict[str, int] = Field(
        {}, description="The absolute position of linear stages in nanometers."
    )
    rotary: dict[str, float] = Field(
        {}, description="The absolute rotational position of rotary stages in radians."
    )
