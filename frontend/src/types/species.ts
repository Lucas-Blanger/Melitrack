export interface SpeciesPrediction {
  label: string;
  scientific_name: string;
  confidence: number;
}

export interface SpeciesIdentificationResponse {
  prediction: SpeciesPrediction;
  alternatives: SpeciesPrediction[];
}
