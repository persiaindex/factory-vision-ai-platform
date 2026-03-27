function JobHistoryCard({ jobs }) {
  return (
    <div className="panel-card panel-card--wide">
      <div className="panel-card__header">
        <div>
          <p className="panel-card__eyebrow">Inspection history</p>
          <h2>Recent jobs</h2>
        </div>
      </div>

      {jobs.length === 0 ? (
        <p>No jobs available yet.</p>
      ) : (
        <div className="job-history-table-wrapper">
          <table className="job-history-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>File</th>
                <th>Status</th>
                <th>Detections</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => (
                <tr key={job.id}>
                  <td>{job.id}</td>
                  <td>{job.original_filename}</td>
                  <td>{job.status}</td>
                  <td>{job.detections?.length || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default JobHistoryCard;