import { useEffect, useState } from "react";

import StatusCard from "../components/StatusCard";
import { fetchBackendHealth } from "../services/api";

function DashboardPage() {
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadHealth() {
      try {
        setLoading(true);
        setError("");
        const data = await fetchBackendHealth();
        setHealthData(data);
      } catch (err) {
        setError(err.message || "Unknown error while loading backend status.");
      } finally {
        setLoading(false);
      }
    }

    loadHealth();
  }, []);

  return (
    <div className="dashboard-grid">
      <StatusCard
        title="Frontend"
        value="Running"
        subtitle="React dashboard is available."
      />

      <StatusCard
        title="Backend connection"
        value={loading ? "Checking..." : error ? "Offline" : "Connected"}
        subtitle={
          loading
            ? "Request in progress."
            : error
              ? error
              : `Service: ${healthData?.service} | Status: ${healthData?.status}`
        }
      />

      <StatusCard
        title="Latest inspection"
        value="Not connected yet"
        subtitle="This card will show the newest job in a later day."
      />

      <StatusCard
        title="Inference service"
        value="Not connected yet"
        subtitle="FastAPI integration with the UI comes after backend orchestration."
      />
    </div>
  );
}

export default DashboardPage;