import React, { useState } from "react";
import {
  Wifi,
  Bluetooth,
  Radio,
  Sun,
  Volume2,
  Moon,
  Sparkles,
  Sliders,
} from "lucide-react";

interface SpatialControlCenterProps {
  initialBrightness?: number;
  initialVolume?: number;
  onSettingChange?: (key: string, value: boolean | number) => void;
}

/**
 * SpatialControlCenter - Production macOS / visionOS inspired control center.
 * Features:
 * - Multi-layer translucent acrylic materials with backdrop-filter
 * - Apple squircle-proportioned buttons with tactile spring transitions
 * - Specular micro-borders (1px subtle white highlights)
 * - 44x44px minimum touch targets and accessible ARIA attributes
 * - Fluid sliders with continuous feedback
 */
export const SpatialControlCenter: React.FC<SpatialControlCenterProps> = ({
  initialBrightness = 75,
  initialVolume = 60,
  onSettingChange,
}) => {
  const [wifi, setWifi] = useState(true);
  const [bluetooth, setBluetooth] = useState(true);
  const [airdrop, setAirdrop] = useState(false);
  const [focusMode, setFocusMode] = useState(false);
  const [brightness, setBrightness] = useState(initialBrightness);
  const [volume, setVolume] = useState(initialVolume);

  const toggleSetting = (
    key: "wifi" | "bluetooth" | "airdrop" | "focus",
    current: boolean,
    setter: React.Dispatch<React.SetStateAction<boolean>>
  ) => {
    const next = !current;
    setter(next);
    onSettingChange?.(key, next);
  };

  const handleBrightness = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = Number(e.target.value);
    setBrightness(val);
    onSettingChange?.("brightness", val);
  };

  const handleVolume = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = Number(e.target.value);
    setVolume(val);
    onSettingChange?.("volume", val);
  };

  return (
    <section
      aria-label="Spatial Control Center"
      className="w-full max-w-sm rounded-3xl p-5 text-zinc-100 select-none transition-all duration-300 font-sans shadow-lg relative overflow-hidden"
      style={{
        backgroundColor: "rgba(18, 18, 22, 0.72)",
        backdropFilter: "blur(32px) saturate(190%)",
        WebkitBackdropFilter: "blur(32px) saturate(190%)",
        border: "1px solid rgba(255, 255, 255, 0.12)",
        boxShadow:
          "inset 0 1px 1px 0 rgba(255, 255, 255, 0.2), 0 24px 48px -12px rgba(0, 0, 0, 0.65)",
      }}
    >
      {/* Specular Edge Highlight */}
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/25 to-transparent"
        aria-hidden="true"
      />

      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-white/5">
        <div className="flex items-center gap-2">
          <Sliders className="w-4 h-4 text-zinc-400" aria-hidden="true" />
          <h2 className="text-xs font-semibold tracking-wider uppercase text-zinc-400">
            Control Center
          </h2>
        </div>
        <span className="flex items-center gap-1.5 text-xs text-zinc-400">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" aria-hidden="true" />
          Spatial OS
        </span>
      </div>

      {/* Top Grid: Connectivity & Focus */}
      <div className="mt-4 grid grid-cols-2 gap-3">
        {/* 2x2 Network Controls Tile */}
        <div
          className="rounded-2xl p-3 flex flex-col gap-2.5"
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.04)",
            border: "1px solid rgba(255, 255, 255, 0.06)",
          }}
        >
          {/* Wi-Fi Toggle */}
          <button
            type="button"
            onClick={() => toggleSetting("wifi", wifi, setWifi)}
            aria-pressed={wifi}
            className="flex items-center gap-3 p-1 rounded-xl transition-all duration-200 hover:bg-white/5 text-left group min-h-[44px]"
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 ${
                wifi
                  ? "bg-blue-500 text-white shadow-md shadow-blue-500/30"
                  : "bg-white/10 text-zinc-400"
              }`}
            >
              <Wifi className="w-4 h-4" aria-hidden="true" />
            </div>
            <div className="leading-tight">
              <span className="text-xs font-medium block text-zinc-200">
                Wi-Fi
              </span>
              <span className="text-[10px] text-zinc-400">
                {wifi ? "Studio-5G" : "Off"}
              </span>
            </div>
          </button>

          {/* Bluetooth Toggle */}
          <button
            type="button"
            onClick={() => toggleSetting("bluetooth", bluetooth, setBluetooth)}
            aria-pressed={bluetooth}
            className="flex items-center gap-3 p-1 rounded-xl transition-all duration-200 hover:bg-white/5 text-left group min-h-[44px]"
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 ${
                bluetooth
                  ? "bg-blue-500 text-white shadow-md shadow-blue-500/30"
                  : "bg-white/10 text-zinc-400"
              }`}
            >
              <Bluetooth className="w-4 h-4" aria-hidden="true" />
            </div>
            <div className="leading-tight">
              <span className="text-xs font-medium block text-zinc-200">
                Bluetooth
              </span>
              <span className="text-[10px] text-zinc-400">
                {bluetooth ? "AirPods Pro" : "Off"}
              </span>
            </div>
          </button>

          {/* AirDrop Toggle */}
          <button
            type="button"
            onClick={() => toggleSetting("airdrop", airdrop, setAirdrop)}
            aria-pressed={airdrop}
            className="flex items-center gap-3 p-1 rounded-xl transition-all duration-200 hover:bg-white/5 text-left group min-h-[44px]"
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 ${
                airdrop
                  ? "bg-blue-500 text-white shadow-md shadow-blue-500/30"
                  : "bg-white/10 text-zinc-400"
              }`}
            >
              <Radio className="w-4 h-4" aria-hidden="true" />
            </div>
            <div className="leading-tight">
              <span className="text-xs font-medium block text-zinc-200">
                AirDrop
              </span>
              <span className="text-[10px] text-zinc-400">
                {airdrop ? "Contacts" : "Off"}
              </span>
            </div>
          </button>
        </div>

        {/* Focus Mode Card */}
        <button
          type="button"
          onClick={() => toggleSetting("focus", focusMode, setFocusMode)}
          aria-pressed={focusMode}
          className="rounded-2xl p-3 flex flex-col justify-between text-left transition-all duration-200 hover:bg-white/[0.06] group"
          style={{
            backgroundColor: focusMode
              ? "rgba(99, 102, 241, 0.2)"
              : "rgba(255, 255, 255, 0.04)",
            border: focusMode
              ? "1px solid rgba(129, 140, 248, 0.3)"
              : "1px solid rgba(255, 255, 255, 0.06)",
          }}
        >
          <div className="flex items-center justify-between">
            <div
              className={`w-9 h-9 rounded-xl flex items-center justify-center transition-all ${
                focusMode
                  ? "bg-indigo-500 text-white shadow-lg shadow-indigo-500/30"
                  : "bg-white/10 text-zinc-400"
              }`}
            >
              <Moon className="w-4 h-4" aria-hidden="true" />
            </div>
            <span
              className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${
                focusMode
                  ? "bg-indigo-400/20 text-indigo-300"
                  : "bg-white/5 text-zinc-400"
              }`}
            >
              {focusMode ? "Active" : "Ready"}
            </span>
          </div>

          <div>
            <span className="text-sm font-medium block text-zinc-100">
              Focus Mode
            </span>
            <span className="text-xs text-zinc-400">
              {focusMode ? "Do Not Disturb" : "Off"}
            </span>
          </div>
        </button>
      </div>

      {/* Sliders Section: Display Brightness & Sound */}
      <div className="mt-4 flex flex-col gap-3">
        {/* Brightness Slider Card */}
        <div
          className="rounded-2xl p-3 flex flex-col gap-1.5"
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.04)",
            border: "1px solid rgba(255, 255, 255, 0.06)",
          }}
        >
          <div className="flex items-center justify-between text-xs text-zinc-300">
            <span className="flex items-center gap-1.5 font-medium">
              <Sun className="w-3.5 h-3.5 text-amber-400" aria-hidden="true" />
              Display
            </span>
            <span className="text-zinc-400 font-mono text-[11px]">
              {brightness}%
            </span>
          </div>
          <label htmlFor="brightness-slider" className="sr-only">
            Display Brightness
          </label>
          <input
            id="brightness-slider"
            type="range"
            min="0"
            max="100"
            value={brightness}
            onChange={handleBrightness}
            className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-white"
          />
        </div>

        {/* Sound Volume Slider Card */}
        <div
          className="rounded-2xl p-3 flex flex-col gap-1.5"
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.04)",
            border: "1px solid rgba(255, 255, 255, 0.06)",
          }}
        >
          <div className="flex items-center justify-between text-xs text-zinc-300">
            <span className="flex items-center gap-1.5 font-medium">
              <Volume2 className="w-3.5 h-3.5 text-blue-400" aria-hidden="true" />
              Sound
            </span>
            <span className="text-zinc-400 font-mono text-[11px]">
              {volume}%
            </span>
          </div>
          <label htmlFor="volume-slider" className="sr-only">
            Sound Volume
          </label>
          <input
            id="volume-slider"
            type="range"
            min="0"
            max="100"
            value={volume}
            onChange={handleVolume}
            className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-white"
          />
        </div>
      </div>
    </section>
  );
};
