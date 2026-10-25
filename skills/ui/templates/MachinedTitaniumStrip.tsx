import React, { useState, useRef, useEffect, useCallback } from "react";
import { motion, useMotionValue, useSpring, useTransform, useReducedMotion } from "framer-motion";
import { Volume2, Mic, Activity, Radio, Power, Disc } from "lucide-react";

interface MachinedTitaniumStripProps {
  channelName?: string;
  channelIndex?: string;
  defaultDb?: number;
  onDbChange?: (db: number) => void;
  enableAcousticFeedback?: boolean;
}

/**
 * Zero-Dependency Synthesized Acoustic Click Engine
 * Generates an instantaneous 1.2ms mechanical click impulse (2.4kHz) via Web Audio API.
 */
class SynthesizedTactileSound {
  private ctx: AudioContext | null = null;

  public playClick(pitch = 2400, gainLevel = 0.035) {
    if (typeof window === "undefined") return;
    try {
      if (!this.ctx) {
        const AudioCtx =
          window.AudioContext ||
          (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
        this.ctx = new AudioCtx();
      }
      if (this.ctx.state === "suspended") {
        this.ctx.resume();
      }

      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const filter = this.ctx.createBiquadFilter();

      filter.type = "bandpass";
      filter.frequency.setValueAtTime(pitch, now);
      filter.Q.setValueAtTime(3.5, now);

      osc.type = "triangle";
      osc.frequency.setValueAtTime(pitch, now);

      gain.gain.setValueAtTime(gainLevel, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.0016);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.0018);
    } catch {
      // Audio gracefully bypassed if muted or disabled
    }
  }
}

const audioClick = new SynthesizedTactileSound();

/**
 * MachinedTitaniumStrip
 * Ultra-premium mastering-grade Channel Strip inspired by Nagra & Teenage Engineering.
 * Features sub-pixel directional specular highlights, recessed fader cavity,
 * 16-segment LED meter with phosphor decay, and zero-dependency synthetic clicks.
 */
export const MachinedTitaniumStrip: React.FC<MachinedTitaniumStripProps> = ({
  channelName = "PRE-AMP // CH.01",
  channelIndex = "01",
  defaultDb = 0,
  onDbChange,
  enableAcousticFeedback = true,
}) => {
  const [currentDb, setCurrentDb] = useState(defaultDb);
  const [isMuted, setIsMuted] = useState(false);
  const [isPhantomOn, setIsPhantomOn] = useState(false);
  const shouldReduceMotion = useReducedMotion();

  // Fader track height: 180px (-36dB to +12dB)
  // 0dB is at 45px from top
  const trackHeight = 180;
  const initialFaderPos = ((12 - defaultDb) / 48) * trackHeight;
  const faderY = useMotionValue(initialFaderPos);
  const smoothFaderY = useSpring(faderY, {
    stiffness: shouldReduceMotion ? 1000 : 380,
    damping: shouldReduceMotion ? 100 : 30,
    mass: 1.0,
  });

  const lastDetentRef = useRef<number>(initialFaderPos);

  const updateDbFromPosition = useCallback(
    (pos: number) => {
      const normalized = Math.max(0, Math.min(1, pos / trackHeight));
      // +12dB (top) down to -36dB (bottom)
      const calculatedDb = Math.round((12 - normalized * 48) * 10) / 10;
      setCurrentDb(calculatedDb);
      onDbChange?.(calculatedDb);

      // Acoustic click when crossing 0dB detent
      const zeroDbPos = (12 / 48) * trackHeight;
      if (Math.abs(pos - zeroDbPos) < 4 && Math.abs(lastDetentRef.current - zeroDbPos) >= 4) {
        if (enableAcousticFeedback) audioClick.playClick(2800, 0.05);
      }
      lastDetentRef.current = pos;
    },
    [trackHeight, onDbChange, enableAcousticFeedback]
  );

  const handleDrag = (_: MouseEvent | TouchEvent | PointerEvent, info: { point: { y: number } }) => {
    updateDbFromPosition(faderY.get());
  };

  const handleToggleMute = () => {
    if (enableAcousticFeedback) audioClick.playClick(1900, 0.04);
    setIsMuted((prev) => !prev);
  };

  const handleTogglePhantom = () => {
    if (enableAcousticFeedback) audioClick.playClick(3200, 0.04);
    setIsPhantomOn((prev) => !prev);
  };

  // 16-Segment LED Peak Meter calculation
  const totalLeds = 16;
  const activeLeds = isMuted ? 0 : Math.max(0, Math.min(totalLeds, Math.round(((currentDb + 36) / 48) * totalLeds)));

  return (
    <div
      className="relative w-full max-w-[280px] rounded-2xl p-5 select-none font-sans overflow-hidden"
      style={{
        backgroundColor: "#08090a", // Cold obsidian titanium tint
        border: "1px solid rgba(255, 255, 255, 0.08)",
        boxShadow:
          "inset 0 1px 0 0 rgba(255, 255, 255, 0.12), inset 0 -1px 0 0 rgba(0, 0, 0, 0.5), 0 24px 48px -12px rgba(0, 0, 0, 0.8)",
      }}
    >
      {/* Procedural Anodized Metal Noise Overlay */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.02] mix-blend-overlay"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
        }}
        aria-hidden="true"
      />

      {/* Top Header Bar */}
      <div className="flex items-center justify-between border-b border-zinc-900 pb-3">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-amber-500" />
          <span className="text-[11px] font-mono font-bold tracking-wider text-zinc-400">
            {channelName}
          </span>
        </div>
        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-zinc-400">
          ID::{channelIndex}
        </span>
      </div>

      {/* Main Console Bay (Split: Fader on Left, LED Meter on Right) */}
      <div className="mt-5 flex gap-4">
        {/* Left: Recessed Fader Track */}
        <div className="flex-1 flex flex-col items-center">
          <div className="text-[9px] font-mono text-zinc-400 mb-1 flex justify-between w-full px-1">
            <span>+12</span>
            <span className="text-amber-500 font-bold">0dB</span>
            <span>-36</span>
          </div>

          <div
            className="relative w-12 rounded-lg flex justify-center py-2"
            style={{
              height: `${trackHeight + 36}px`,
              backgroundColor: "#050506",
              boxShadow:
                "inset 0 2px 6px 0 rgba(0,0,0,0.85), inset 0 1px 1px 0 rgba(0,0,0,0.9), 0 1px 0 0 rgba(255,255,255,0.06)",
            }}
          >
            {/* Center Slider Slit */}
            <div className="absolute top-4 bottom-4 w-1 bg-zinc-950 rounded-full border border-zinc-800" />

            {/* Fader Handle */}
            <motion.div
              drag="y"
              dragConstraints={{ top: 0, bottom: trackHeight }}
              dragElastic={0}
              dragMomentum={false}
              onDrag={handleDrag}
              style={{ y: smoothFaderY }}
              className="absolute top-2 w-10 h-7 rounded bg-gradient-to-b from-zinc-700 via-zinc-800 to-zinc-900 border border-zinc-600 shadow-[0_4px_10px_rgba(0,0,0,0.6)] cursor-grab active:cursor-grabbing flex items-center justify-center"
            >
              {/* Knurled Metallic Grips */}
              <div className="flex flex-col gap-0.5 w-6">
                <div className="h-0.5 bg-zinc-500 rounded-full" />
                <div className="h-0.5 bg-amber-500 rounded-full" />
                <div className="h-0.5 bg-zinc-500 rounded-full" />
              </div>
            </motion.div>
          </div>
        </div>

        {/* Right: 16-Segment Phosphor LED Peak Meter */}
        <div className="w-12 flex flex-col items-center">
          <span className="text-[9px] font-mono text-zinc-400 mb-1">METER</span>
          <div
            className="w-8 rounded-lg p-1.5 flex flex-col-reverse justify-between"
            style={{
              height: `${trackHeight + 36}px`,
              backgroundColor: "#050506",
              boxShadow: "inset 0 2px 6px rgba(0,0,0,0.85), 0 1px 0 rgba(255,255,255,0.06)",
            }}
          >
            {Array.from({ length: totalLeds }, (_, i) => {
              const isLit = i < activeLeds;
              const isRed = i >= 14;
              const isAmber = i >= 11 && i < 14;

              let activeColor = "#10b981"; // Emerald
              if (isRed) activeColor = "#ef4444"; // Ruby Peak
              else if (isAmber) activeColor = "#f59e0b"; // Amber Warning

              return (
                <div
                  key={i}
                  className="w-full h-1.5 rounded-sm transition-colors duration-75"
                  style={{
                    backgroundColor: isLit ? activeColor : "#18181b",
                    boxShadow: isLit ? `0 0 6px ${activeColor}80` : "none",
                  }}
                />
              );
            })}
          </div>
        </div>
      </div>

      {/* Tabular Telemetry dB Readout */}
      <div className="mt-4 p-2.5 rounded-xl bg-zinc-900/60 border border-zinc-800 flex items-baseline justify-between font-mono">
        <span className="text-[10px] text-zinc-400">GAIN TRIM</span>
        <div className="flex items-baseline gap-1">
          <span className="text-xl font-bold text-white tabular-nums">
            {currentDb > 0 ? `+${currentDb.toFixed(1)}` : currentDb.toFixed(1)}
          </span>
          <span className="text-xs text-amber-500 font-semibold">dB</span>
        </div>
      </div>

      {/* Mechanical Punch Toggle Buttons */}
      <div className="mt-4 pt-3 border-t border-zinc-900 grid grid-cols-2 gap-2">
        <button
          type="button"
          onClick={handleToggleMute}
          className={`h-9 rounded-lg font-mono text-xs font-semibold flex items-center justify-center gap-1.5 transition-all active:translate-y-0.5 border ${
            isMuted
              ? "bg-red-500/20 border-red-500/40 text-red-400"
              : "bg-zinc-900 hover:bg-zinc-850 border-zinc-800 text-zinc-400 hover:text-zinc-200"
          }`}
          style={{
            borderBottomWidth: "2px",
            borderBottomColor: isMuted ? "#7f1d1d" : "#18181b",
          }}
        >
          <Volume2 className="w-3.5 h-3.5" aria-hidden="true" />
          {isMuted ? "MUTED" : "MUTE"}
        </button>

        <button
          type="button"
          onClick={handleTogglePhantom}
          className={`h-9 rounded-lg font-mono text-xs font-semibold flex items-center justify-center gap-1.5 transition-all active:translate-y-0.5 border ${
            isPhantomOn
              ? "bg-amber-500/20 border-amber-500/40 text-amber-400"
              : "bg-zinc-900 hover:bg-zinc-850 border-zinc-800 text-zinc-400 hover:text-zinc-200"
          }`}
          style={{
            borderBottomWidth: "2px",
            borderBottomColor: isPhantomOn ? "#78350f" : "#18181b",
          }}
        >
          <Power className="w-3.5 h-3.5" aria-hidden="true" />
          {isPhantomOn ? "+48V ON" : "+48V"}
        </button>
      </div>
    </div>
  );
};
