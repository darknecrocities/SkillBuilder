import React, { useRef } from "react";
import { motion, useMotionValue, useSpring, useTransform, useReducedMotion } from "framer-motion";
import { Compass, ExternalLink, Cpu } from "lucide-react";

interface MagneticSpatialCardProps {
  category?: string;
  title?: string;
  status?: string;
  description?: string;
  metrics?: { label: string; value: string }[];
  onAction?: () => void;
}

/**
 * MagneticSpatialCard
 * 3D Spatial Perspective Card with dynamic specular glare tracking,
 * zero-re-render physics-based spring rotation, and parallax depth elevation.
 */
export const MagneticSpatialCard: React.FC<MagneticSpatialCardProps> = ({
  category = "HARDWARE TELEMETRY",
  title = "Neural Compute Core NX-8",
  status = "OPTIMAL",
  description = "High-throughput edge accelerator. Sub-millisecond latency inference pipeline with real-time thermal throttling.",
  metrics = [
    { label: "THROUGHPUT", value: "842 TOPS" },
    { label: "LATENCY", value: "0.82 ms" },
    { label: "THERMAL", value: "48.5 °C" },
  ],
  onAction,
}) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const shouldReduceMotion = useReducedMotion();

  // Normalized pointer coordinates from card center (-0.5 to +0.5)
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  // Smooth springs for spatial tilt
  const springConfig = {
    stiffness: shouldReduceMotion ? 1000 : 260,
    damping: shouldReduceMotion ? 100 : 22,
    mass: 1.0,
  };
  const smoothX = useSpring(mouseX, springConfig);
  const smoothY = useSpring(mouseY, springConfig);

  // 3D Rotations (degrees)
  const rotateX = useTransform(smoothY, [-0.5, 0.5], [14, -14]);
  const rotateY = useTransform(smoothX, [-0.5, 0.5], [-14, 14]);

  // Dynamic Specular Glare Coordinates (%)
  const glareX = useTransform(smoothX, [-0.5, 0.5], ["0%", "100%"]);
  const glareY = useTransform(smoothY, [-0.5, 0.5], ["0%", "100%"]);

  const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!cardRef.current || shouldReduceMotion) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    mouseX.set(x);
    mouseY.set(y);
  };

  const handlePointerLeave = () => {
    mouseX.set(0);
    mouseY.set(0);
  };

  return (
    <div
      style={{ perspective: 1000 }}
      className="w-full max-w-md select-none"
    >
      <motion.div
        ref={cardRef}
        onPointerMove={handlePointerMove}
        onPointerLeave={handlePointerLeave}
        style={{
          rotateX: shouldReduceMotion ? 0 : rotateX,
          rotateY: shouldReduceMotion ? 0 : rotateY,
          transformStyle: "preserve-3d",
        }}
        className="relative rounded-2xl bg-zinc-950 p-7 border border-zinc-800 text-zinc-100 shadow-xl overflow-hidden transition-shadow duration-300 hover:shadow-xl"
      >
        {/* Dynamic Specular Radial Glare */}
        <motion.div
          className="pointer-events-none absolute -inset-px rounded-2xl opacity-0 transition-opacity duration-300 group-hover:opacity-100 hover:opacity-100"
          style={{
            background: useTransform(
              [glareX, glareY],
              ([x, y]) =>
                `radial-gradient(circle at ${x} ${y}, rgba(255,255,255,0.08) 0%, transparent 65%)`
            ),
          }}
          aria-hidden="true"
        />

        {/* Floating Content Layer (Elevated in 3D Space) */}
        <div style={{ transform: "translateZ(30px)" }} className="relative z-10">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-zinc-900 pb-4">
            <div className="flex items-center gap-2">
              <span className="p-2 rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-400">
                <Cpu className="w-4 h-4 text-zinc-300" aria-hidden="true" />
              </span>
              <span className="text-xs font-mono font-medium tracking-wider text-zinc-400 uppercase">
                {category}
              </span>
            </div>

            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              {status}
            </span>
          </div>

          {/* Title & Description */}
          <div className="mt-5">
            <h3 className="text-xl font-bold tracking-tight text-white font-sans">
              {title}
            </h3>
            <p className="mt-2 text-xs leading-relaxed text-zinc-400">
              {description}
            </p>
          </div>

          {/* Metric Telemetry Grid */}
          <div className="mt-6 grid grid-cols-3 gap-2 p-3 rounded-xl bg-zinc-900/60 border border-zinc-800/80">
            {metrics.map((m) => (
              <div key={m.label} className="flex flex-col">
                <span className="text-[9px] font-mono font-semibold tracking-wider text-zinc-400 uppercase">
                  {m.label}
                </span>
                <span className="mt-1 text-sm font-bold font-mono text-zinc-100 tabular-nums">
                  {m.value}
                </span>
              </div>
            ))}
          </div>

          {/* Footer Action */}
          <div className="mt-6 flex items-center justify-between pt-4 border-t border-zinc-900">
            <div className="flex items-center gap-1.5 text-[11px] font-mono text-zinc-400">
              <Compass className="w-3.5 h-3.5 text-zinc-400" aria-hidden="true" />
              <span>SPATIAL MATRIX 3D</span>
            </div>

            <button
              type="button"
              onClick={onAction}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-zinc-850 hover:bg-zinc-800 border border-zinc-700/80 text-xs font-medium text-zinc-200 transition-colors active:scale-95 focus-visible:ring-2 focus-visible:ring-zinc-400"
            >
              <span>INSPECT</span>
              <ExternalLink className="w-3 h-3 text-zinc-400" aria-hidden="true" />
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};
