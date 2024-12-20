from pydantic import BaseModel


class Vector4(BaseModel):
    """
    A class representing a 4-dimensional vector.

    Attributes:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.
        z (float): The z-coordinate of the vector.
        w (float): The w-coordinate of the vector.
    """

    X: float
    Y: float
    Z: float
    W: float
