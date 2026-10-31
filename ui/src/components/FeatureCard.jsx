export default function FeatureCard({ number, title, description }) {
  return (
    <article className="feature-card">
      <p className="feature-number">{number}</p>
      <h3>{title}</h3>
      <p>{description}</p>
    </article>
  );
}
