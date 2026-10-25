import React, { useState, useEffect, useRef } from "react";
import { motion, useReducedMotion } from "framer-motion";
import { Search, Terminal, ArrowRight, CornerDownLeft, Shield, Sliders, Cpu, Compass } from "lucide-react";

interface CommandItem {
  id: string;
  category: string;
  title: string;
  description: string;
  shortcut: string[];
  safetyTier: "STANDARD" | "GUARDED" | "CRITICAL";
}

const DEFAULT_COMMANDS: CommandItem[] = [
  {
    id: "deploy-edge",
    category: "PIPELINE",
    title: "Deploy Edge Cluster Release",
    description: "Orchestrates multi-region rolling deployment across edge compute nodes.",
    shortcut: ["⌘", "K", "D"],
    safetyTier: "GUARDED",
  },
  {
    id: "run-profiler",
    category: "TELEMETRY",
    title: "Execute Runtime Memory Profiler",
    description: "Captures heap allocation snapshots and analyzes garbage collection pauses.",
    shortcut: ["⌘", "P"],
    safetyTier: "STANDARD",
  },
  {
    id: "flush-cache",
    category: "SYSTEM",
    title: "Purge Global CDN Edge Cache",
    description: "Invalidates all distributed surrogate keys across primary origin shields.",
    shortcut: ["⌘", "⇧", "R"],
    safetyTier: "CRITICAL",
  },
  {
    id: "audit-a11y",
    category: "VERIFICATION",
    title: "Run WCAG 2.2 Accessibility Audit",
    description: "Audits semantic vector contrast, touch targets, and focus traps.",
    shortcut: ["⌘", "A"],
    safetyTier: "STANDARD",
  },
];

/**
 * SpatialCommandPalette
 * Linear / macOS Spotlight caliber spatial command launcher.
 * Features multi-layer Cupertino acrylic glass, specular top-edge refraction,
 * physical 3D keycaps, spring-driven layoutId active pill, and asymmetric metadata pane.
 */
export const SpatialCommandPalette: React.FC<{
  isOpen?: boolean;
  onClose?: () => void;
  onSelectCommand?: (cmd: CommandItem) => void;
}> = ({ isOpen = true, onClose, onSelectCommand }) => {
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const shouldReduceMotion = useReducedMotion();

  const filtered = DEFAULT_COMMANDS.filter(
    (cmd) =>
      cmd.title.toLowerCase().includes(query.toLowerCase()) ||
      cmd.category.toLowerCase().includes(query.toLowerCase())
  );

  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % (filtered.length || 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + (filtered.length || 1)) % (filtered.length || 1));
    } else if (e.key === "Enter" && filtered[selectedIndex]) {
      e.preventDefault();
      onSelectCommand?.(filtered[selectedIndex]);
    } else if (e.key === "Escape") {
      e.preventDefault();
      onClose?.();
    }
  };

  if (!isOpen) return null;

  const activeCommand = filtered[selectedIndex] || filtered[0];

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Command Palette"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        onKeyDown={handleKeyDown}
        className="relative w-full max-w-2xl rounded-2xl overflow-hidden font-sans text-zinc-100 shadow-xl"
        style={{
          backgroundColor: "rgba(18, 18, 22, 0.88)",
          backdropFilter: "blur(32px) saturate(180%)",
          WebkitBackdropFilter: "blur(32px) saturate(180%)",
          border: "1px solid rgba(255, 255, 255, 0.10)",
          boxShadow:
            "inset 0 1px 0 0 rgba(255, 255, 255, 0.16), 0 20px 40px -15px rgba(0, 0, 0, 0.70)",
        }}
      >
        {/* Search Input Bar */}
        <div className="flex items-center gap-3 px-5 py-4 border-b border-zinc-800/80">
          <Search className="w-4 h-4 text-zinc-400" aria-hidden="true" />
          <input
            ref={inputRef}
            id="spatial-command-search"
            aria-label="Search available commands"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a command or query..."
            className="flex-1 bg-transparent text-sm text-white placeholder-zinc-400 focus:outline-none font-medium"
            role="combobox"
            aria-expanded="true"
            aria-controls="command-listbox"
            aria-autocomplete="list"
          />
          <kbd className="px-2 py-0.5 text-[10px] font-mono text-zinc-400 bg-zinc-900 border border-zinc-800 rounded">
            ESC
          </kbd>
        </div>

        {/* Two-Column Asymmetric Layout: Command List (Left) + Context Pane (Right) */}
        <div className="grid grid-cols-1 md:grid-cols-5 min-h-[260px]">
          {/* Left Column: Command List (3 cols) */}
          <div
            id="command-listbox"
            role="listbox"
            className="md:col-span-3 p-2.5 space-y-1 border-r border-zinc-800/60 overflow-y-auto max-h-[320px]"
          >
            {filtered.length === 0 ? (
              <div className="py-12 text-center text-xs font-mono text-zinc-400">
                NO COMMANDS FOUND
              </div>
            ) : (
              filtered.map((cmd, idx) => {
                const isSelected = idx === selectedIndex;
                return (
                  <div
                    key={cmd.id}
                    role="option"
                    aria-selected={isSelected}
                    onMouseEnter={() => setSelectedIndex(idx)}
                    onClick={() => onSelectCommand?.(cmd)}
                    className="relative flex items-center justify-between p-3 rounded-xl cursor-pointer select-none"
                  >
                    {/* Active Background Spring Pill */}
                    {isSelected && (
                      <motion.div
                        layoutId={shouldReduceMotion ? undefined : "active-command-pill"}
                        className="absolute inset-0 rounded-xl bg-white/[0.08] border border-white/10"
                        transition={{ type: "spring", stiffness: 450, damping: 35 }}
                      />
                    )}

                    <div className="relative z-10 flex items-center gap-3">
                      <span className="p-1.5 rounded-lg bg-zinc-900/80 border border-zinc-800 text-zinc-400">
                        <Terminal className="w-3.5 h-3.5 text-zinc-300" aria-hidden="true" />
                      </span>
                      <div className="flex flex-col">
                        <span className="text-[10px] font-mono font-semibold tracking-wider text-zinc-400 uppercase">
                          {cmd.category}
                        </span>
                        <span className="text-xs font-medium text-white tracking-tight">
                          {cmd.title}
                        </span>
                      </div>
                    </div>

                    {/* Physical 3D Shortcut Keycaps */}
                    <div className="relative z-10 flex items-center gap-1">
                      {cmd.shortcut.map((key) => (
                        <kbd
                          key={key}
                          className="px-1.5 py-0.5 text-[10px] font-mono font-semibold text-zinc-300 bg-zinc-900 border-t border-white/10 border-b-2 border-zinc-950 rounded shadow-sm"
                        >
                          {key}
                        </kbd>
                      ))}
                    </div>
                  </div>
                );
              })
            )}
          </div>

          {/* Right Column: Context Preview Pane (2 cols) */}
          <div className="hidden md:flex md:col-span-2 p-5 bg-zinc-950/40 flex-col justify-between">
            {activeCommand ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider">
                    SPECIFICATION
                  </span>
                  <span
                    className={`text-[9px] font-mono px-2 py-0.5 rounded font-bold border ${
                      activeCommand.safetyTier === "CRITICAL"
                        ? "bg-red-500/10 border-red-500/30 text-red-400"
                        : activeCommand.safetyTier === "GUARDED"
                        ? "bg-amber-500/10 border-amber-500/30 text-amber-400"
                        : "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                    }`}
                  >
                    {activeCommand.safetyTier}
                  </span>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-white tracking-tight">
                    {activeCommand.title}
                  </h4>
                  <p className="mt-1.5 text-xs text-zinc-400 leading-relaxed">
                    {activeCommand.description}
                  </p>
                </div>

                <div className="p-3 rounded-lg bg-zinc-900/60 border border-zinc-800 space-y-1.5 font-mono text-[10px]">
                  <div className="flex justify-between text-zinc-400">
                    <span>EXECUTION</span>
                    <span className="text-zinc-200">WORKLET // DIRECT</span>
                  </div>
                  <div className="flex justify-between text-zinc-400">
                    <span>AFFORDANCE</span>
                    <span className="text-zinc-200">SUB-PIXEL CHAIR</span>
                  </div>
                </div>
              </div>
            ) : null}

            {/* Bottom Execute Hint */}
            <div className="pt-3 border-t border-zinc-800/60 flex items-center justify-between text-[11px] font-mono text-zinc-400">
              <span>SELECT</span>
              <span className="flex items-center gap-1 text-zinc-200">
                <CornerDownLeft className="w-3.5 h-3.5" aria-hidden="true" />
                RETURN
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
