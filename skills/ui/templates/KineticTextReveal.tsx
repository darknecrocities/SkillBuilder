import React, { useState } from "react";
import { motion, useReducedMotion } from "framer-motion";
import { Sparkles, ArrowRight, CornerDownRight } from "lucide-react";

interface KineticTextRevealProps {
  headline?: string;
  category?: string;
  timestamp?: string;
  description?: string;
  ctaText?: string;
  onCtaClick?: () => void;
}

/**
 * KineticTextReveal
 * Swiss International Editorial typography with architectural clip-path reveals
 * and dynamic variable-weight kinetic interactions powered by Framer Motion.
 */
export const KineticTextReveal: React.FC<KineticTextRevealProps> = ({
  headline = "ARCHITECTURAL SYSTEMATICS",
  category = "ISSUE № 42 // EDITORIAL",
  timestamp = "2026.10.25",
  description = "A departure from synthetic interface homogenization. Establishing structural typography, calibrated grid rhythm, and continuous spring dynamics.",
  ctaText = "EXPLORE SPECIFICATION",
  onCtaClick,
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const shouldReduceMotion = useReducedMotion();

  // Split headline into individual words for staggered clip masking
  const words = headline.split(" ");

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: shouldReduceMotion ? 0 : 0.08,
        delayChildren: shouldReduceMotion ? 0 : 0.1,
      },
    },
  };

  const wordVariants = {
    hidden: {
      y: shouldReduceMotion ? 0 : "110%",
      opacity: shouldReduceMotion ? 0 : 1,
    },
    visible: {
      y: "0%",
      opacity: 1,
      transition: {
        ease: [0.16, 1, 0.3, 1],
        duration: shouldReduceMotion ? 0.2 : 0.75,
      },
    },
  };

  return (
    <div className="w-full max-w-2xl bg-zinc-950 text-zinc-100 p-8 sm:p-12 border border-zinc-800 rounded-2xl font-sans relative overflow-hidden shadow-lg">
      {/* Background Architectural Grid Lines */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage:
            "linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }}
        aria-hidden="true"
      />

      {/* Top Editorial Index Bar */}
      <div className="flex items-center justify-between border-b border-zinc-800/80 pb-4 text-xs font-mono tracking-wider text-zinc-400">
        <span className="flex items-center gap-2">
          <CornerDownRight className="w-3.5 h-3.5 text-zinc-300" aria-hidden="true" />
          {category}
        </span>
        <span className="tabular-nums tracking-normal text-zinc-400 font-mono">
          {timestamp}
        </span>
      </div>

      {/* Hero Masked Typography Area */}
      <div
        className="my-8 cursor-default"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <motion.h1
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="text-4xl sm:text-6xl font-black tracking-tighter leading-[1.05] uppercase select-none flex flex-wrap gap-x-3.5 gap-y-1"
        >
          {words.map((word, wordIndex) => (
            <span
              key={`${word}-${wordIndex}`}
              className="inline-block overflow-hidden py-1"
              style={{ clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)" }}
            >
              <motion.span
                variants={wordVariants}
                className="inline-block transition-all duration-300"
                style={{
                  fontVariationSettings: isHovered
                    ? "'wght' 900, 'wdth' 115"
                    : "'wght' 700, 'wdth' 100",
                  color: isHovered ? "#ffffff" : "#f4f4f5",
                  textShadow: isHovered
                    ? "0 0 24px rgba(255,255,255,0.2)"
                    : "none",
                }}
              >
                {word}
              </motion.span>
            </span>
          ))}
        </motion.h1>
      </div>

      {/* Editorial Body Text */}
      <motion.p
        initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.5, ease: "easeOut" }}
        className="text-sm sm:text-base text-zinc-400 leading-relaxed max-w-xl font-normal"
      >
        {description}
      </motion.p>

      {/* Bottom Footer & Tactical Action */}
      <div className="mt-8 pt-6 border-t border-zinc-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-2 text-xs font-mono text-zinc-400">
          <Sparkles className="w-3.5 h-3.5 text-zinc-300" aria-hidden="true" />
          <span>VARIABLE AXIS // WGHT: 100..900 WDTH: 75..125</span>
        </div>

        <button
          type="button"
          onClick={onCtaClick}
          className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg bg-zinc-100 hover:bg-white text-zinc-950 font-mono text-xs font-semibold tracking-wide transition-all duration-200 active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-400"
        >
          <span>{ctaText}</span>
          <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
        </button>
      </div>
    </div>
  );
};
