export type HealthLevel = "excelente" | "boa" | "regular" | "ruim" | "crítica";
export type HiveType = "caixa" | "isca";
export type AnalysisStatus = "pending" | "processed" | "failed";

export interface Hive {
  id: string;
  owner_id: string;
  name: string;
  type: HiveType;
  species: string;
  latitude: number | null;
  longitude: number | null;
  location_description: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface HiveCreate {
  name: string;
  type: HiveType;
  species: string;
  latitude?: number | null;
  longitude?: number | null;
  location_description?: string | null;
  notes?: string | null;
}

export interface Photo {
  id: string;
  filename: string;
  content_type: string;
  size: number;
  uploaded_at: string;
  data_url: string | null;
}

export interface Inspection {
  id: string;
  owner_id: string;
  hive_id: string;
  health: HealthLevel;
  queen_seen: boolean | null;
  honey_level: number | null;
  population_estimate: string | null;
  notes: string | null;
  inspected_at: string;
}

export interface InspectionCreate {
  hive_id: string;
  health: HealthLevel;
  queen_seen?: boolean | null;
  honey_level?: number | null;
  population_estimate?: string | null;
  notes?: string | null;
  inspected_at?: string | null;
}

export interface Product {
  id: number;
  name: string;
  unit: string;
  description: string | null;
  is_active: boolean;
}

export interface Harvest {
  id: string;
  owner_id: string;
  hive_id: string;
  product_id: number;
  quantity: number;
  unit: string;
  quality_notes: string | null;
  harvested_at: string;
}

export interface HarvestCreate {
  hive_id: string;
  product_id: number;
  quantity: number;
  unit?: string | null;
  quality_notes?: string | null;
  harvested_at?: string | null;
}

export interface HarvestSummary {
  period_start: string | null;
  period_end: string | null;
  items: Array<{
    product: string;
    unit: string;
    total_quantity: number;
  }>;
}

export interface DashboardOverview {
  total_hives: number;
  last_inspection: Inspection | null;
  health_alerts: number;
}

export interface AnomalyAlert {
  label: string;
  description: string;
  score: number;
}

export interface AnomalyData {
  has_anomaly?: boolean;
  alerts?: AnomalyAlert[];
  scores?: {
    fungi?: number;
    empty_cells?: number;
    disease_signs?: number;
    [key: string]: number | undefined;
  };
}

export interface PopulationData {
  level?: string;
  density_score?: number;
  estimated_count?: string;
}

export interface MLAnalysisResult {
  anomaly?: AnomalyData;
  population?: PopulationData;
  population_percent?: number;
  [key: string]: unknown;
}

export interface Analysis {
  status: AnalysisStatus;
  model_name: string | null;
  result: MLAnalysisResult | null;
  confidence: number | null;
  error_message: string | null;
  corrected_result: MLAnalysisResult | null;
  correction_notes: string | null;
  corrected_at: string | null;
  processed_at: string | null;
}

export interface AnalysisCorrectionUpdate {
  corrected_result: MLAnalysisResult;
  correction_notes?: string | null;
}
