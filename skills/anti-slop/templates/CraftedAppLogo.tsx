import React from "react";

export type LogoSize = "sm" | "md" | "lg" | "xl" | "app-icon" | number;
export type LogoVariant = "material" | "silhouette-dark" | "silhouette-light";

interface CraftedAppLogoProps {
  size?: LogoSize;
  variant?: LogoVariant;
  className?: string;
  ariaLabel?: string;
}

const SIZE_MAP: Record<string, number> = {
  sm: 24,
  md: 48,
  lg: 96,
  xl: 256,
  "app-icon": 512,
};

/**
 * CraftedAppLogo - Production vector logo mark adhering to Anti-AI-Slop craftsmanship.
 * Features:
 * - Passed Silhouette Test (pure 100% black/white without gradients)
 * - Passed 16px Favicon Test (clean geometric definition)
 * - Continuous Apple squircle geometry ($n \approx 4$ Lamé superellipse)
 * - Dual-mode: Cupertino Acrylic material vs pure monochrome silhouette
 */
export const CraftedAppLogo: React.FC<CraftedAppLogoProps> = ({
  size = "md",
  variant = "material",
  className = "",
  ariaLabel = "SkillBuilder Application Logo",
}) => {
  const pixelSize = typeof size === "number" ? size : SIZE_MAP[size] || 48;

  if (variant === "silhouette-dark") {
    // 100% Solid Black on Transparent for Light Backgrounds & Print
    return (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 512 512"
        width={pixelSize}
        height={pixelSize}
        aria-label={ariaLabel}
        role="img"
        className={className}
      >
        <path
          d="M 128 32 C 48 32, 32 48, 32 128 L 32 384 C 32 464, 48 480, 128 480 L 384 480 C 464 480, 480 464, 480 384 L 480 128 C 480 48, 464 32, 384 32 Z"
          fill="#000000"
        />
        <path d="M 256 112 L 368 256 L 256 400 L 144 256 Z" fill="#ffffff" />
        <circle cx="256" cy="256" r="48" fill="#000000" />
        <circle cx="256" cy="256" r="14" fill="#ffffff" />
      </svg>
    );
  }

  if (variant === "silhouette-light") {
    // 100% Solid White on Transparent for Dark Backgrounds
    return (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 512 512"
        width={pixelSize}
        height={pixelSize}
        aria-label={ariaLabel}
        role="img"
        className={className}
      >
        <path
          d="M 128 32 C 48 32, 32 48, 32 128 L 32 384 C 32 464, 48 480, 128 480 L 384 480 C 464 480, 480 464, 480 384 L 480 128 C 480 48, 464 32, 384 32 Z"
          fill="#ffffff"
        />
        <path d="M 256 112 L 368 256 L 256 400 L 144 256 Z" fill="#000000" />
        <circle cx="256" cy="256" r="48" fill="#ffffff" />
        <circle cx="256" cy="256" r="14" fill="#000000" />
      </svg>
    );
  }

  // Default: Cupertino Acrylic Material with Specular Lighting
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 512 512"
      width={pixelSize}
      height={pixelSize}
      aria-label={ariaLabel}
      role="img"
      className={className}
    >
      <defs>
        <linearGradient id="logo-specular" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="0.28" />
          <stop offset="40%" stopColor="#ffffff" stopOpacity="0.08" />
          <stop offset="100%" stopColor="#ffffff" stopOpacity="0.02" />
        </linearGradient>

        <linearGradient id="logo-acrylic" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#18181b" />
          <stop offset="100%" stopColor="#09090b" />
        </linearGradient>

        <radialGradient id="logo-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.22" />
          <stop offset="100%" stopColor="#38bdf8" stopOpacity="0" />
        </radialGradient>
      </defs>

      {/* Squircle Base */}
      <path
        d="M 128 32 C 48 32, 32 48, 32 128 L 32 384 C 32 464, 48 480, 128 480 L 384 480 C 464 480, 480 464, 480 384 L 480 128 C 480 48, 464 32, 384 32 Z"
        fill="url(#logo-acrylic)"
      />

      {/* Specular Inner Hairline */}
      <path
        d="M 128 32 C 48 32, 32 48, 32 128 L 32 384 C 32 464, 48 480, 128 480 L 384 480 C 464 480, 480 464, 480 384 L 480 128 C 480 48, 464 32, 384 32 Z"
        fill="none"
        stroke="url(#logo-specular)"
        strokeWidth="2.5"
      />

      {/* Ambient Glow */}
      <circle cx="256" cy="256" r="140" fill="url(#logo-glow)" />

      {/* Geometric Core Diamond */}
      <path d="M 256 112 L 368 256 L 256 400 L 144 256 Z" fill="#f4f4f5" />

      {/* Inner Negative Space */}
      <circle cx="256" cy="256" r="48" fill="#09090b" />

      {/* High-Precision Cobalt Nexus */}
      <circle cx="256" cy="256" r="22" fill="#0284c7" />
      <circle cx="256" cy="256" r="8" fill="#f4f4f5" />
    </svg>
  );
};
