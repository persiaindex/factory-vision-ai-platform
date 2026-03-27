import { useEffect, useMemo, useState } from "react";

import DetectionsCard from "../components/DetectionsCard";
import JobHistoryCard from "../components/JobHistoryCard";
import LatestInspectionCard from "../components/LatestInspectionCard";
import StatusCard from "../components/StatusCard";
import { fetchBackendHealth, fetchInspectionJobs } from "../services/api";

function DashboardPage() {
  const [healthData, setHealthData] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let intervalId;

    async function loadDashboardData() {
      try {
        const [health, jobsResponse] = await Promise.all([
          fetchBackendHealth(),
          fetchInspectionJobs(),
        ]);

        const normalizedJobs = Array.isArray(jobsResponse)
          ? jobsResponse
          : (jobsResponse.results || []);

        setHealthData(health);
        setJobs(normalizedJobs);
        setError("");
      } catch (err) {
        setError(err.message || "Unknown dashboard loading error.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboardData();
    intervalId = setInterval(loadDashboardData, 2000);

    return () => clearInterval(intervalId);
  }, []);

  const latestJob = useMemo(() => {
    return jobs.length > 0 ? jobs[0] : null;
  }, [jobs]);

  return (
    <div className="dashboard-stack">
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
          title="Latest job status"
          value={latestJob ? latestJob.status : "No jobs"}
          subtitle={latestJob ? latestJob.original_filename : "Waiting for watcher input."}
        />

        <StatusCard
          title="Latest detections"
          value={latestJob ? latestJob.detections?.length || 0 : 0}
          subtitle="Count returned by the current stored inspection result."
        />
      </div>

      <div className="dashboard-panels">
        <LatestInspectionCard latestJob={latestJob} />
        <DetectionsCard latestJob={latestJob} />
        <JobHistoryCard jobs={jobs.slice(0, 10)} />
      </div>
    </div>
  );
}

export default DashboardPage;