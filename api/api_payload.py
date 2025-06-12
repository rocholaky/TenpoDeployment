from typing import List

from pydantic import BaseModel, field_validator


class PredictionBody(BaseModel):
    """
    Represents the body of a prediction request.
    """

    inputs: List[float]

    @field_validator("inputs")
    def validate_inputs(cls, v: list[float]) -> list[float]:
        """
        Validate that inputs are a list of floats.
        """

        if not isinstance(v, list):
            raise ValueError("Inputs must be a list.")
        if len(v) == 0:
            raise ValueError("Inputs cannot be an empty list.")
        if not all(isinstance(i, float) for i in v):
            raise ValueError("All inputs must be floats.")
        return v
        return v
