export function Card({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`bg-white rounded-xl border ${className}`}
      style={{ borderColor: "#e8e4dc" }}
    >
      {children}
    </div>
  );
}
