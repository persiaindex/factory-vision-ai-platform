function DetectionsCard({ latestJob }) {
  const detections = latestJob?.detections || [];

  return (
    <div className="panel-card">
      <p className="panel-card__eyebrow">Latest detections</p>
      <h2>{detections.length}</h2>

      {detections.length === 0 ? (
        <p>No detections available yet.</p>
      ) : (
        <ul className="detection-list">
          {detections.map((detection) => (
            <li key={detection.id} className="detection-list__item">
              <div>
                <strong>{detection.object_name}</strong>
                <p>confidence: {Number(detection.confidence).toFixed(3)}</p>
                <p>
                  size status:
                  <span className={`size-status-badge size-status-badge--${String(detection.size_status).toLowerCase()}`}>
                    {detection.size_status}
                  </span>
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default DetectionsCard;