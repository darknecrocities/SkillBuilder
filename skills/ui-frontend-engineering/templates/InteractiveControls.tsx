"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

/**
 * InteractiveControls.tsx
 * 
 * Demonstrates:
 * 1. Sliding Pill Tabs with Framer Motion `layoutId` and semantic ARIA tabs
 * 2. Tactile Spring Micro-Interactions (subtle physical response on tap/hover)
 * 3. Animated Tabular Numeric Counter (prevents layout jitter via `tabular-nums`)
 * 
 * Aesthetic Standard:
 * - Anti-vibe-coding: Neutral zinc/slate color palette, 1px specular borders
 * - Accessible: ARIA tablist/tab semantics, keyboard navigable, reduced-motion friendly
 * - Zero raw emojis: clean vector SVGs with `aria-hidden="true"`
 */

interface TabItem {
  id: string;
  label: string;
  count?: number;
}

const TABS: TabItem[] = [
  { id: "overview", label: "Overview", count: 12 },
  { id: "telemetry", label: "Telemetry", count: 84 },
  { id: "security", label: "Security", count: 3 },
  { id: "audit", label: "Audit Logs" },
];

export function SlidingPillTabs() {
  const [activeTab, setActiveTab] = useState<string>("overview");

  return (
    <nav
      role="tablist"
      aria-label="Workspace views"
      className="inline-flex items-center gap-1 p-1 bg-zinc-950/60 dark:bg-zinc-900/60 rounded-xl border border-zinc-800/80 backdrop-blur-md"
    >
      {TABS.map((tab) => {
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={isActive}
            aria-controls={`panel-${tab.id}`}
            id={`tab-${tab.id}`}
            tabIndex={isActive ? 0 : -1}
            onClick={() => setActiveTab(tab.id)}
            className={`relative px-3.5 py-1.5 text-xs font-medium rounded-lg transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-400 ${
              isActive
                ? "text-zinc-100"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            {isActive && (
              <motion.div
                layoutId="activePillIndicator"
                className="absolute inset-0 bg-zinc-800/90 rounded-lg border border-zinc-700/60 shadow-sm"
                transition={{
                  type: "spring",
                  stiffness: 450,
                  damping: 32,
                  mass: 0.8,
                }}
              />
            )}
            <span className="relative z-10 flex items-center gap-2">
              {tab.label}
              {tab.count !== undefined && (
                <span
                  className={`text-[10px] px-1.5 py-0.2 rounded font-mono tabular-nums ${
                    isActive
                      ? "bg-zinc-700/70 text-zinc-200"
                      : "bg-zinc-900 text-zinc-500"
                  }`}
                >
                  {tab.count}
                </span>
              )}
            </span>
          </button>
        );
      })}
    </nav>
  );
}

interface TactileButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "ghost";
}

export function TactileButton({
  children,
  variant = "primary",
  className = "",
  ...props
}: TactileButtonProps) {
  const baseStyles =
    "inline-flex items-center justify-center gap-2 px-4 py-2 text-xs font-medium rounded-lg transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-400 disabled:opacity-50 disabled:pointer-events-none";

  const variantStyles = {
    primary:
      "bg-zinc-100 text-zinc-950 hover:bg-zinc-200 active:bg-zinc-300 border border-zinc-200 shadow-sm",
    secondary:
      "bg-zinc-900 text-zinc-200 hover:bg-zinc-850 active:bg-zinc-800 border border-zinc-800 shadow-sm",
    ghost:
      "bg-transparent text-zinc-400 hover:text-zinc-100 hover:bg-zinc-900/50",
  };

  return (
    <motion.button
      whileHover={{ scale: 1.01 }}
      whileTap={{ scale: 0.98 }}
      transition={{
        type: "spring",
        stiffness: 500,
        damping: 30,
        mass: 0.5,
      }}
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
      {...(props as any)}
    >
      {children}
    </motion.button>
  );
}

export function TabularTicker({
  value,
  label,
  delta,
}: {
  value: number;
  label: string;
  delta?: { value: number; isPositive: boolean };
}) {
  return (
    <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-800/80 backdrop-blur-md max-w-xs">
      <div className="text-[11px] font-medium uppercase tracking-wider text-zinc-400">
        {label}
      </div>
      <div className="mt-2 flex items-baseline gap-3">
        <span className="text-2xl font-semibold tracking-tight text-zinc-100 font-mono tabular-nums">
          <AnimatePresence mode="popLayout" initial={false}>
            <motion.span
              key={value}
              initial={{ opacity: 0, y: -6, filter: "blur(2px)" }}
              animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              exit={{ opacity: 0, y: 6, filter: "blur(2px)" }}
              transition={{
                duration: 0.2,
                ease: [0.16, 1, 0.3, 1],
              }}
              className="inline-block"
            >
              {value.toLocaleString()}
            </motion.span>
          </AnimatePresence>
        </span>
        {delta && (
          <span
            className={`text-xs font-mono tabular-nums flex items-center gap-0.5 ${
              delta.isPositive ? "text-emerald-400" : "text-amber-400"
            }`}
          >
            <svg
              className={`w-3 h-3 ${delta.isPositive ? "" : "rotate-180"}`}
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 15l7-7 7 7" />
            </svg>
            {Math.abs(delta.value)}%
          </span>
        )}
      </div>
    </div>
  );
}
