from fastapi import APIRouter, Depends, File, UploadFile

from apps.auth.models import User
from apps.hives.schemas import SpeciesIdentificationResponse
from apps.hives.services import species_service
from core.dependencies import get_current_user

router = APIRouter(prefix="/species", tags=["species"])


@router.post("/identify", response_model=SpeciesIdentificationResponse)
async def identify_species(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    return await species_service.identify_species(image)
