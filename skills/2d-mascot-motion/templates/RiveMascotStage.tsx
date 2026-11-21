"use client";

import React, { useEffect, useRef, useState } from "react";
import { useRive, useStateMachineInput, Layout, Fit, Alignment } from "@rive-app/react-canvas";

export type MascotMood = "idle" | "thinking" | "success" | "error";

export interface RiveMascotStageProps {
  src: string;
  stateMachineName?: string;
  mood?: MascotMood;
  trackPointer?: boolean;
  label?: string;
  className?: string;
}

export function RiveMascotStage({
  src,
  stateMachineName = "MascotSM",
  mood = "idle",
  trackPointer = true,
  label = "Application mascot",
  className = "",
}: RiveMascotStageProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReducedMotion(mq.matches);
    const onChange = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  const { rive, RiveComponent } = useRive({
    src,
    stateMachines: stateMachineName,
    autoplay: !reducedMotion,
    layout: new Layout({ fit: Fit.Contain, alignment: Alignment.Center }),
  });

  const isHovered = useStateMachineInput(rive, stateMachineName, "isHovered");
  const isThinking = useStateMachineInput(rive, stateMachineName, "isThinking");
  const lookX = useStateMachineInput(rive, stateMachineName, "lookX");
  const lookY = useStateMachineInput(rive, stateMachineName, "lookY");
  const onSuccess = useStateMachineInput(rive, stateMachineName, "onSuccess");
  const onError = useStateMachineInput(rive, stateMachineName, "onError");

  useEffect(() => {
    if (isThinking) isThinking.value = mood === "thinking";
    if (mood === "success") onSuccess?.fire();
    if (mood === "error") onError?.fire();
  }, [mood, isThinking, onSuccess, onError]);

  useEffect(() => {
    const el = containerRef.current;
    if (!el || !rive || reducedMotion) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) rive.play();
        else rive.pause();
      },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [rive, reducedMotion]);

  useEffect(() => {
    return () => {
      rive?.cleanup();
    };
  }, [rive]);

  const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!trackPointer || reducedMotion || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const nx = Math.max(0, Math.min(100, ((e.clientX - rect.left) / rect.width) * 100));
    const ny = Math.max(0, Math.min(100, ((e.clientY - rect.top) / rect.height) * 100));
    if (lookX) lookX.value = nx;
    if (lookY) lookY.value = 100 - ny;
  };

  return (
    <div
      ref={containerRef}
      role="img"
      aria-label={label}
      onPointerEnter={() => isHovered && (isHovered.value = true)}
      onPointerLeave={() => {
        if (isHovered) isHovered.value = false;
        if (lookX) lookX.value = 50;
        if (lookY) lookY.value = 50;
      }}
      onPointerMove={handlePointerMove}
      className={`relative aspect-square w-full select-none overflow-hidden ${className}`}
    >
      <RiveComponent className="h-full w-full" />
    </div>
  );
}
