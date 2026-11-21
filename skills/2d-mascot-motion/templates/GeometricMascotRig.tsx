"use client";

import React, { useEffect, useId, useRef, useState } from "react";

export type RigMood = "idle" | "thinking" | "success" | "error";

export interface GeometricMascotRigProps {
  mood?: RigMood;
  size?: number;
  label?: string;
}

export function GeometricMascotRig({
  mood = "idle",
  size = 160,
  label = "Geometric sentinel mascot",
}: GeometricMascotRigProps) {
  const uid = useId().replace(/:/g, "");
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [gaze, setGaze] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReducedMotion(mq.matches);
    const onChange = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (reducedMotion || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const dx = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
    const dy = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
    setGaze({
      x: Math.max(-5, Math.min(5, dx * 5)),
      y: Math.max(-4, Math.min(4, dy * 4)),
    });
  };

  const accentColor =
    mood === "error" ? "#f43f5e" : mood === "success" ? "#10b981" : mood === "thinking" ? "#f59e0b" : "#38bdf8";

  return (
    <div
      ref={containerRef}
      onPointerMove={handlePointerMove}
      onPointerLeave={() => setGaze({ x: 0, y: 0 })}
      style={{ width: size, height: size }}
      className="inline-flex items-center justify-center select-none"
    >
      <svg
        viewBox="0 0 128 128"
        width={size}
        height={size}
        role="img"
        aria-label={label}
        className="overflow-visible"
      >
        <defs>
          <clipPath id={`chassis-${uid}`}>
            <rect x="22" y="26" width="84" height="78" rx="26" />
          </clipPath>
        </defs>

        <ellipse cx="64" cy="112" rx="30" ry="5" fill="#09090b" opacity="0.35" />

        <g
          style={{
            transform:
              !reducedMotion && mood === "thinking"
                ? "rotate(-4deg)"
                : !reducedMotion && mood === "success"
                  ? "translateY(-3px) scale(1.03)"
                  : "none",
            transformOrigin: "64px 72px",
            transition: reducedMotion ? "none" : "transform 220ms cubic-bezier(0.175, 0.885, 0.32, 1.275)",
          }}
        >
          <line x1="64" y1="14" x2="64" y2="26" stroke="#52525b" strokeWidth="3" strokeLinecap="round" />
          <circle cx="64" cy="12" r="4" fill={accentColor} />

          <g clipPath={`url(#chassis-${uid})`}>
            <rect x="22" y="26" width="84" height="78" rx="26" fill="#18181b" />
            <path d="M 74 26 L 106 26 L 106 104 L 62 104 Z" fill="#121215" />
          </g>
          <rect
            x="22"
            y="26"
            width="84"
            height="78"
            rx="26"
            fill="none"
            stroke="rgba(255,255,255,0.16)"
            strokeWidth="1.5"
          />

          <rect x="34" y="42" width="60" height="34" rx="14" fill="#09090b" stroke="#27272a" strokeWidth="1.5" />

          <g
            style={{
              transform: `translate(${gaze.x}px, ${gaze.y}px)`,
              transition: reducedMotion ? "none" : "transform 120ms ease-out",
            }}
          >
            {mood === "error" ? (
              <>
                <path d="M 45 55 L 53 63 M 53 55 L 45 63" stroke={accentColor} strokeWidth="2.5" strokeLinecap="round" />
                <path d="M 75 55 L 83 63 M 83 55 L 75 63" stroke={accentColor} strokeWidth="2.5" strokeLinecap="round" />
              </>
            ) : (
              <>
                <circle cx="49" cy="59" r="5" fill={accentColor} />
                <circle cx="79" cy="59" r="5" fill={accentColor} />
              </>
            )}
          </g>

          <path
            d={mood === "success" ? "M 54 88 Q 64 95 74 88" : "M 56 89 L 72 89"}
            fill="none"
            stroke="#a1a1aa"
            strokeWidth="2.5"
            strokeLinecap="round"
          />
        </g>
      </svg>
    </div>
  );
}
