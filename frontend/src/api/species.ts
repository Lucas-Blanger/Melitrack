import { postFormData } from "./http";
import type { SpeciesIdentificationResponse } from "../types/species";

export function identifyBeeSpecies(file: File) {
  const formData = new FormData();
  formData.append("image", file);
  return postFormData<SpeciesIdentificationResponse>("/species/identify", formData);
}
