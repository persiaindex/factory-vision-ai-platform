export async function fetchBackendHealth() {
  const response = await fetch("/backend/health/");

  if (!response.ok) {
    throw new Error(`Backend health request failed with status ${response.status}`);
  }

  return response.json();
}

export async function fetchInspectionJobs() {
  const response = await fetch("/backend/api/inspections/jobs/");

  if (!response.ok) {
    throw new Error(`Inspection jobs request failed with status ${response.status}`);
  }

  return response.json();
}