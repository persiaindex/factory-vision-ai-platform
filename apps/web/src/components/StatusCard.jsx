function StatusCard({ title, value, subtitle }) {
  return (
    <div className="status-card">
      <p className="status-card__title">{title}</p>
      <h2 className="status-card__value">{value}</h2>
      {subtitle ? <p className="status-card__subtitle">{subtitle}</p> : null}
    </div>
  );
}

export default StatusCard;