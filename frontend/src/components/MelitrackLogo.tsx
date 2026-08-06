import logo from "../assets/Melitrack.png";

export function MelitrackLogo({ size = 120 }: { size?: number }) {
  return <img src={logo} alt="Melitrack" width={size} height={size} />;
}
