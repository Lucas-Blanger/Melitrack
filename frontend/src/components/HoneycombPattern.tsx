export function HoneycombPattern({ opacity = 0.07 }: { opacity?: number }) {
  return (
    <svg
      aria-hidden="true"
      style={{
        position: "absolute",
        inset: 0,
        width: "100%",
        height: "100%",
        opacity,
        pointerEvents: "none",
      }}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <pattern
          id="honeycomb"
          x="0"
          y="0"
          width="56"
          height="97"
          patternUnits="userSpaceOnUse"
        >
          <polygon
            points="28,3 53,17 53,45 28,59 3,45 3,17"
            fill="none"
            stroke="#1D6A4A"
            strokeWidth="1.2"
          />
          <polygon
            points="0,50 25,64 25,92 0,106 -25,92 -25,64"
            fill="none"
            stroke="#1D6A4A"
            strokeWidth="1.2"
          />
          <polygon
            points="56,50 81,64 81,92 56,106 31,92 31,64"
            fill="none"
            stroke="#1D6A4A"
            strokeWidth="1.2"
          />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#honeycomb)" />
    </svg>
  );
}
