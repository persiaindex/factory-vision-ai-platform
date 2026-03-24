export async function fetchBackendHealth() {
  const response = await fetch("/backend/health/");

  if (!response.ok) {
    throw new Error(`Backend health request failed with status ${response.status}`);
  }

  return response.json();
}