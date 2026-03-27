import { useState } from "react";

import { INSPECTION_FRAME_HEIGHT, INSPECTION_FRAME_WIDTH } from "../config/dashboard";

function LatestInspectionCard({ latestJob }) {
  const [imageSize, setImageSize] = useState({ width: 0, height: 0 });

  if (!latestJob) {
    return (
      <div className="panel-card panel-card--wide">
        <h2>Latest inspection</h2>
        <p>No inspection jobs yet.</p>
      </div>
    );
  }

  const detections = latestJob.detections || [];

  function handleImageLoad(event) {
    setImageSize({
      width: event.target.naturalWidth,
      height: event.target.naturalHeight,
    });
  }

  return (
    <div className="panel-card panel-card--wide">
      <div className="panel-card__header">
        <div>
          <p className="panel-card__eyebrow">Latest inspection</p>
          <h2>{latestJob.original_filename}</h2>
        </div>
        <span className={`job-status-badge job-status-badge--${latestJob.status.toLowerCase()}`}>
          {latestJob.status}
        </span>
      </div>

      {latestJob.source_image_url ? (
        <div
          className="inspection-image-stage"
          style={{
            "--inspection-frame-width": `${INSPECTION_FRAME_WIDTH}px`,
            "--inspection-frame-height": `${INSPECTION_FRAME_HEIGHT}px`,
          }}
        >
          <img
            className="latest-inspection-image"
            src={latestJob.source_image_url}
            alt={latestJob.original_filename}
            onLoad={handleImageLoad}
          />

          {imageSize.width > 0 && imageSize.height > 0 ? (
            <svg
              className="inspection-overlay"
              viewBox={`0 0 ${imageSize.width} ${imageSize.height}`}
              preserveAspectRatio="xMidYMid meet"
            >
              {detections.map((detection, index) => {
                const x = Number(detection.bbox_x_min);
                const y = Number(detection.bbox_y_min);
                const width = Number(detection.bbox_x_max) - Number(detection.bbox_x_min);
                const height = Number(detection.bbox_y_max) - Number(detection.bbox_y_min);
                const label = `${detection.object_name} ${Number(detection.confidence).toFixed(2)}`;

                return (
                  <g key={detection.id ?? index}>
                    <rect
                      className="inspection-overlay__box"
                      x={x}
                      y={y}
                      width={width}
                      height={height}
                    />
                    <text
                      className="inspection-overlay__label"
                      x={x}
                      y={Math.max(18, y - 6)}
                    >
                      {label}
                    </text>
                  </g>
                );
              })}
            </svg>
          ) : null}
        </div>
      ) : (
        <p>No image available.</p>
      )}

      <div className="latest-inspection-meta">
        <p><strong>Created:</strong> {latestJob.created_at}</p>
        <p><strong>Started:</strong> {latestJob.processing_started_at || "-"}</p>
        <p><strong>Finished:</strong> {latestJob.processing_finished_at || "-"}</p>
        {latestJob.error_message ? <p><strong>Error:</strong> {latestJob.error_message}</p> : null}
      </div>
    </div>
  );
}

export default LatestInspectionCard;