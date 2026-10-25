import React from "react";
import { ArrowUpRight, ShieldCheck } from "lucide-react";

interface AppleGlassCardProps {
  title: string;
  subtitle: string;
  metric: string;
  change: string;
}

/**
 * AppleGlassCard - Production-grade Cupertino acrylic material.
 * Features multi-layer backdrop blur, specular inner border highlights,
 * continuous squircle curvature, and high-contrast typography.
 */
export const AppleGlassCard: React.FC<AppleGlassCardProps> = ({
  title,
  subtitle,
  metric,
  change,
}) => {
  return (
    <div
      className="relative group p-6 rounded-2xl overflow-hidden transition-all duration-300 hover:scale-[1.01] hover:shadow-2xl"
      style={{
        // Real Cupertino Acrylic formula:
        // Translucent dark tint + heavy blur + specular inner edge lighting
        backgroundColor: "rgba(24, 24, 27, 0.65)", // zinc-900 at 65% opacity
        backdropFilter: "blur(24px) saturate(180%)",
        WebkitBackdropFilter: "blur(24px) saturate(180%)",
        border: "1px solid rgba(255, 255, 255, 0.08)",
        boxShadow:
          "inset 0 1px 1px 0 rgba(255, 255, 255, 0.15), 0 20px 40px -15px rgba(0, 0, 0, 0.5)",
      }}
    >
      {/* Specular Edge Highlight Gradient */}
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent"
        aria-hidden="true"
      />

      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="p-2 rounded-xl bg-white/5 border border-white/10 text-zinc-300">
            <ShieldCheck className="w-4 h-4 text-emerald-400" aria-hidden="true" />
          </span>
          <div>
            <h3 className="text-sm font-medium tracking-tight text-zinc-100 font-sans">
              {title}
            </h3>
            <p className="text-xs text-zinc-400">{subtitle}</p>
          </div>
        </div>

        <button
          type="button"
          aria-label="View details"
          className="p-1.5 rounded-full text-zinc-400 hover:text-zinc-100 hover:bg-white/10 transition-colors focus-visible:ring-2 focus-visible:ring-zinc-400"
        >
          <ArrowUpRight className="w-4 h-4" aria-hidden="true" />
        </button>
      </div>

      {/* Metric Display */}
      <div className="mt-6 flex items-baseline justify-between">
        <span className="text-3xl font-semibold tracking-tight text-white font-sans">
          {metric}
        </span>
        <span className="inline-flex items-center text-xs font-medium text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
          {change}
        </span>
      </div>
    </div>
  );
};
