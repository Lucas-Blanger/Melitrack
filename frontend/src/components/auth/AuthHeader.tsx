import { MelitrackLogo } from "../MelitrackLogo";

export function AuthHeader({
  title,
  subtitle,
}: {
  title: string;
  subtitle: string;
}) {
  return (
    <div className="flex flex-col items-center mb-7">
      <MelitrackLogo size={76} />
      <h1 className="text-xl font-bold mt-4" style={{ color: "#1D6A4A" }}>
        {title}
      </h1>
      <p className="text-sm text-neutral-500 text-center mt-1.5 leading-relaxed">
        {subtitle}
      </p>
    </div>
  );
}
