import React from "react";
import { motion, useReducedMotion } from "framer-motion";

interface CinematicHeroProps {
  headline: string;
  subheadline: string;
  primaryCtaText: string;
  onPrimaryCtaClick?: () => void;
}

export const CinematicHero: React.FC<CinematicHeroProps> = ({
  headline,
  subheadline,
  primaryCtaText,
  onPrimaryCtaClick,
}) => {
  const shouldReduceMotion = useReducedMotion();
  const words = headline.split(" ");

  return (
    <section className="relative overflow-hidden bg-neutral-950 px-6 py-24 sm:py-32 lg:px-8">
      {/* Subtle Atmospheric Top Light Cone (No Neon Glow) */}
      <div
        className="pointer-events-none absolute -top-40 left-1/2 -z-10 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-neutral-800/20 blur-[120px]"
        aria-hidden="true"
      />

      <div className="mx-auto max-w-4xl text-center">
        {/* Cinematic Blur-to-Focus Headline Reveal */}
        <h1 className="flex flex-wrap justify-center gap-x-3 gap-y-1 text-4xl font-semibold tracking-tight text-neutral-100 sm:text-6xl">
          {words.map((word, index) => (
            <motion.span
              key={index}
              initial={
                shouldReduceMotion
                  ? { opacity: 0 }
                  : { opacity: 0, filter: "blur(12px)", y: 16 }
              }
              animate={{ opacity: 1, filter: "blur(0px)", y: 0 }}
              transition={{
                duration: 0.5,
                delay: index * 0.05,
                ease: [0.16, 1, 0.3, 1],
              }}
              className="inline-block"
            >
              {word}
            </motion.span>
          ))}
        </h1>

        {/* Subtitle with Decelerated Fade */}
        <motion.p
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            duration: 0.6,
            delay: shouldReduceMotion ? 0.1 : 0.35,
            ease: [0.16, 1, 0.3, 1],
          }}
          className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-neutral-400"
        >
          {subheadline}
        </motion.p>

        {/* Tactile Spring Primary Action */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            duration: 0.5,
            delay: shouldReduceMotion ? 0.2 : 0.5,
            ease: [0.16, 1, 0.3, 1],
          }}
          className="mt-10 flex items-center justify-center gap-x-6"
        >
          <motion.button
            whileHover={shouldReduceMotion ? {} : { scale: 1.02 }}
            whileTap={shouldReduceMotion ? {} : { scale: 0.98 }}
            transition={{ type: "spring", stiffness: 450, damping: 30 }}
            onClick={onPrimaryCtaClick}
            className="group relative inline-flex items-center gap-2 rounded-lg border border-white/10 bg-neutral-900 px-5 py-3 text-sm font-medium text-neutral-100 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.1)] transition-colors hover:border-white/20 hover:bg-neutral-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-500 focus-visible:ring-offset-2 focus-visible:ring-offset-neutral-950"
          >
            <span>{primaryCtaText}</span>
            <svg
              className="h-4 w-4 text-neutral-400 transition-transform duration-200 group-hover:translate-x-0.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
};
