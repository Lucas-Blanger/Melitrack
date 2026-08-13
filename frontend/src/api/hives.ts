import { getJson, patchJson, postFormData, postJson } from "./http";
import type {
  Analysis,
  AnalysisCorrectionUpdate,
  DashboardOverview,
  Harvest,
  HarvestCreate,
  HarvestSummary,
  Hive,
  HiveCreate,
  Inspection,
  InspectionCreate,
  Photo,
  Product,
} from "../types/hives";

export function listHives() {
  return getJson<Hive[]>("/hives");
}

export function getHive(id: string) {
  return getJson<Hive>(`/hives/${id}`);
}

export function listHivePhotos(hiveId: string) {
  return getJson<Photo[]>(`/hives/${hiveId}/photos`);
}

export function createHive(body: HiveCreate, file?: File) {
  if (!file) {
    return postJson<Hive>("/hives", body);
  }

  const formData = new FormData();
  formData.append("name", body.name);
  formData.append("type", body.type);
  formData.append("species", body.species);
  if (body.latitude !== undefined && body.latitude !== null) {
    formData.append("latitude", String(body.latitude));
  }
  if (body.longitude !== undefined && body.longitude !== null) {
    formData.append("longitude", String(body.longitude));
  }
  if (body.location_description) {
    formData.append("location_description", body.location_description);
  }
  if (body.notes) {
    formData.append("notes", body.notes);
  }
  formData.append("file", file);
  return postFormData<Hive>("/hives", formData);
}

export function listInspectionsByHive(hiveId: string) {
  return getJson<Inspection[]>(`/inspections/hive/${hiveId}`);
}

export function createInspection(body: InspectionCreate) {
  return postJson<Inspection>("/inspections", body);
}

export function uploadInspectionPhoto(inspectionId: string, file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return postFormData(`/inspections/${inspectionId}/photos`, formData);
}

export function getInspectionAnalysis(inspectionId: string) {
  return getJson<Analysis>(`/inspections/${inspectionId}/analysis`);
}

export function correctInspectionAnalysis(
  inspectionId: string,
  body: AnalysisCorrectionUpdate,
) {
  return patchJson<Analysis>(`/inspections/${inspectionId}/analysis/correction`, body);
}

export function listHarvestsByHive(hiveId: string) {
  return getJson<Harvest[]>(`/harvests/hive/${hiveId}`);
}

export function createHarvest(body: HarvestCreate) {
  return postJson<Harvest>("/harvests", body);
}

export function getHarvestSummary() {
  return getJson<HarvestSummary>("/harvests/summary");
}

export function listProducts() {
  return getJson<Product[]>("/products");
}

export function getDashboardOverview() {
  return getJson<DashboardOverview>("/dashboard/overview");
}
