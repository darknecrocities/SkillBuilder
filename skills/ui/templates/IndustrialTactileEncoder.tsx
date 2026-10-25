import React, { useState, useRef, useEffect, useCallback } from "react";
import { motion, useMotionValue, useSpring, useTransform, useReducedMotion } from "framer-motion";
import { Activity, Disc, RotateCcw, Volume2, Radio } from "lucide-react";

interface IndustrialTactileEncoderProps {
  label?: string;
  min?: number;
  max?: number;
  defaultValue?: number;
  step?: number;
  unit?: string;
  onValueChange?: (val: number) => void;
}

/**
 * IndustrialTactileEncoder
 * Tactile Rotary Hardware Encoder inspired by Dieter Rams & Teenage Engineering.
 * Features drag-rotary interaction, physical spring detent physics, SVG tick dial,
 * dynamic oscilloscope waveform, and tabular telemetry readout.
 */
export const IndustrialTactileEncoder: React.FC<IndustrialTactileEncoderProps> = ({
  label = "FILTER FREQUENCY",
  min = 20,
  max = 20000,
  defaultValue = 1250,
  step = 10,
  unit = "Hz",
  onValueChange,
}) => {
  const [currentValue, setCurrentValue] = useState(defaultValue);
  const [isBypassed, setIsBypassed] = useState(false);
  const shouldReduceMotion = useReducedMotion();

  // Angular rotation in degrees (-140 to +140)
  const initialAngle = ((defaultValue - min) / (max - min)) * 280 - 140;
  const rawAngle = useMotionValue(initialAngle);
  
  // Spring dynamics: critically damped mechanical feel
  const springAngle = useSpring(rawAngle, {
    stiffness: shouldReduceMotion ? 1000 : 380,
    damping: shouldReduceMotion ? 100 : 28,
    mass: 1.0,
  });

  const pointerOriginY = useRef<number | null>(null);
  const startAngleRef = useRef<number>(initialAngle);

  // Synchronize numeric value when angle changes
  const updateValueFromAngle = useCallback(
    (deg: number) => {
      const normalized = (deg + 140) / 280;
      const clamped = Math.max(0, Math.min(1, normalized));
      // Logarithmic scale for audio frequency
      const calculated = Math.round(min * Math.pow(max / min, clamped) / step) * step;
      setCurrentValue(calculated);
      onValueChange?.(calculated);
    },
    [min, max, step, onValueChange]
  );

  const handlePointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    pointerOriginY.current = e.clientY;
    startAngleRef.current = rawAngle.get();
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
  };

  const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (pointerOriginY.current === null) return;
    const deltaY = pointerOriginY.current - e.clientY;
    // 1px delta = 1.2 degrees of rotation
    const nextAngle = Math.max(-140, Math.min(140, startAngleRef.current + deltaY * 1.2));
    rawAngle.set(nextAngle);
    updateValueFromAngle(nextAngle);
  };

  const handlePointerUp = (e: React.PointerEvent<HTMLDivElement>) => {
    pointerOriginY.current = null;
    try {
      (e.target as HTMLElement).releasePointerCapture(e.pointerId);
    } catch {
      // Pointer capture released automatically
    }
  };

  // Keyboard accessibility
  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    let delta = 0;
    if (e.key === "ArrowUp" || e.key === "ArrowRight") delta = 14;
    if (e.key === "ArrowDown" || e.key === "ArrowLeft") delta = -14;
    if (delta !== 0) {
      e.preventDefault();
      const nextAngle = Math.max(-140, Math.min(140, rawAngle.get() + delta));
      rawAngle.set(nextAngle);
      updateValueFromAngle(nextAngle);
    }
  };

  // Generate 29 tick marks around dial (-140 to +140 deg, step 10)
  const ticks = Array.from({ length: 29 }, (_, i) => -140 + i * 10);

  // Dynamic waveform coordinates for oscilloscope
  const wavePoints = Array.from({ length: 48 }, (_, i) => {
    const x = (i / 47) * 160;
    const freqFactor = (currentValue / max) * 12 + 1;
    const amp = isBypassed ? 0 : Math.sin((i / 47) * Math.PI * freqFactor) * 14;
    return `${x},${20 + amp}`;
  }).join(" ");

  return (
    <div className="w-full max-w-sm rounded-xl bg-zinc-950 p-5 border border-zinc-800 text-zinc-100 font-sans shadow-xl">
      {/* Top Header & Telemetry Mode */}
      <div className="flex items-center justify-between border-b border-zinc-900 pb-3">
        <div className="flex items-center gap-2">
          <Radio className="w-4 h-4 text-amber-500 animate-pulse" aria-hidden="true" />
          <span className="text-xs font-mono font-semibold tracking-wider text-zinc-400 uppercase">
            {label}
          </span>
        </div>
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-mono bg-zinc-900 border border-zinc-800 text-zinc-300">
          <Activity className="w-3 h-3 text-emerald-400" aria-hidden="true" />
          {isBypassed ? "BYPASS" : "ACTIVE"}
        </span>
      </div>

      {/* Oscilloscope Mini-Screen */}
      <div className="mt-4 rounded-lg bg-zinc-900/80 border border-zinc-800/80 p-3 relative overflow-hidden">
        <div className="flex items-center justify-between text-[10px] font-mono text-zinc-400 mb-1">
          <span>OSC // REALTIME</span>
          <span>{isBypassed ? "0.00 dB" : "-3.20 dB"}</span>
        </div>
        <svg
          className="w-full h-10 overflow-visible"
          viewBox="0 0 160 40"
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          {/* Subtle oscilloscope grid lines */}
          <line x1="0" y1="20" x2="160" y2="20" stroke="#27272a" strokeDasharray="2 2" strokeWidth="1" />
          <line x1="80" y1="0" x2="80" y2="40" stroke="#27272a" strokeDasharray="2 2" strokeWidth="1" />
          {/* Waveform trace */}
          <polyline
            fill="none"
            stroke={isBypassed ? "#71717a" : "#f59e0b"}
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            points={wavePoints}
          />
        </svg>
      </div>

      {/* Main Rotary Control Area */}
      <div className="mt-6 flex flex-col items-center">
        <div
          role="slider"
          tabIndex={0}
          aria-label={label}
          aria-valuemin={min}
          aria-valuemax={max}
          aria-valuenow={currentValue}
          aria-valuetext={`${currentValue} ${unit}`}
          onKeyDown={handleKeyDown}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onPointerCancel={handlePointerUp}
          className="relative w-44 h-44 flex items-center justify-center cursor-grab active:cursor-grabbing select-none focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-500 rounded-full"
        >
          {/* Outer Dial Gauge Tick Marks */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 176 176">
            {ticks.map((deg) => {
              const rad = ((deg - 90) * Math.PI) / 180;
              const isMajor = deg % 40 === 0;
              const r1 = 82;
              const r2 = isMajor ? 72 : 76;
              const cx = 88;
              const cy = 88;
              const x1 = cx + r1 * Math.cos(rad);
              const y1 = cy + r1 * Math.sin(rad);
              const x2 = cx + r2 * Math.cos(rad);
              const y2 = cy + r2 * Math.sin(rad);

              return (
                <line
                  key={deg}
                  x1={x1}
                  y1={y1}
                  x2={x2}
                  y2={y2}
                  stroke={deg === 0 ? "#f59e0b" : isMajor ? "#71717a" : "#3f3f46"}
                  strokeWidth={isMajor ? 1.5 : 1}
                />
              );
            })}
          </svg>

          {/* Machined Metal Rotary Knob */}
          <motion.div
            style={{ rotate: springAngle }}
            className="w-28 h-28 rounded-full bg-gradient-to-b from-zinc-800 to-zinc-950 border border-zinc-700/80 shadow-[0_8px_20px_rgba(0,0,0,0.6)] flex items-center justify-center relative"
          >
            {/* Concentric knurled texture ring */}
            <div className="absolute inset-1.5 rounded-full border border-zinc-700/40 bg-zinc-900/60" />

            {/* Tactical High-Contrast Needle Indicator */}
            <div className="absolute top-2.5 w-1 h-5 rounded-full bg-amber-500" />

            {/* Center Cap */}
            <div className="w-12 h-12 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center text-zinc-500">
              <Disc className="w-5 h-5 text-zinc-600" aria-hidden="true" />
            </div>
          </motion.div>
        </div>

        {/* Tabular Digital Value Readout */}
        <div className="mt-4 flex flex-col items-center">
          <div className="flex items-baseline gap-1 font-mono">
            <span className="text-3xl font-bold tracking-tight text-white tabular-nums">
              {currentValue.toLocaleString()}
            </span>
            <span className="text-sm font-semibold text-amber-500 uppercase">{unit}</span>
          </div>
          <span className="text-[10px] font-mono text-zinc-400 mt-0.5 tracking-wider">
            DETENT STEP: ±{step} {unit}
          </span>
        </div>
      </div>

      {/* Bottom Controls / Tactile Punch Buttons */}
      <div className="mt-6 pt-4 border-t border-zinc-900 grid grid-cols-2 gap-2">
        <button
          type="button"
          onClick={() => setIsBypassed((prev) => !prev)}
          className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-mono font-medium transition-all duration-150 active:scale-95 border ${
            isBypassed
              ? "bg-amber-500/10 border-amber-500/30 text-amber-400"
              : "bg-zinc-900 border-zinc-800 text-zinc-400 hover:text-zinc-200"
          }`}
        >
          <Volume2 className="w-3.5 h-3.5" aria-hidden="true" />
          {isBypassed ? "ENGAGE" : "BYPASS"}
        </button>

        <button
          type="button"
          onClick={() => {
            rawAngle.set(initialAngle);
            updateValueFromAngle(initialAngle);
          }}
          className="flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-mono font-medium bg-zinc-900 hover:bg-zinc-850 border border-zinc-800 text-zinc-400 hover:text-zinc-200 transition-all duration-150 active:scale-95"
        >
          <RotateCcw className="w-3.5 h-3.5" aria-hidden="true" />
          RESET 1.25k
        </button>
      </div>
    </div>
  );
};
