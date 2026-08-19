from pydantic import BaseModel, Field


class SpeciesPrediction(BaseModel):
    label: str
    scientific_name: str
    confidence: float = Field(..., ge=0, le=1)


class SpeciesIdentificationResponse(BaseModel):
    prediction: SpeciesPrediction
    alternatives: list[SpeciesPrediction]
