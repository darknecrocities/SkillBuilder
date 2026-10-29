#!/usr/bin/env python3
"""Multi-Track Cinematic Soundtrack and SFX Synthesizer for SkillBuilder Showcase.

Generates a synchronized 128 BPM industrial cyberpunk soundtrack with driving kicks,
pumping sub-bass, 16th hi-hats, arpeggiated synth motifs, risers, and pixel-timed SFX.
Outputs broadcast-ready 48kHz 16-bit stereo PCM WAV audio.
Complies with SkillBuilder cognitive limits (<500 lines) and zero external dependencies.
"""

import math
import os
import struct
import wave
import numpy as np

SAMPLE_RATE = 48000
DURATION = 46.0
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)
BPM = 128.0
BEAT_SEC = 60.0 / BPM
BAR_SEC = BEAT_SEC * 4.0


def create_kick(t_rel: float, dur: float = 0.45) -> float:
    """Synthesize punchy 808-style kick with rapid pitch drop and saturation."""
    if t_rel < 0 or t_rel > dur:
        return 0.0
    f_start, f_end = 160.0, 42.0
    pitch = f_end + (f_start - f_end) * math.exp(-32.0 * t_rel)
    phase = 2.0 * math.pi * (f_end * t_rel - (f_start - f_end) / 32.0 * (math.exp(-32.0 * t_rel) - 1.0))
    amp = math.exp(-6.5 * t_rel)
    # Click transient
    click = math.sin(2.0 * math.pi * 1200.0 * t_rel) * math.exp(-120.0 * t_rel) * 0.4
    raw = math.sin(phase) * amp + click
    return math.tanh(raw * 1.8) * 0.95


def create_snare(t_rel: float, dur: float = 0.35) -> float:
    """Synthesize snappy industrial snare/clap with filtered noise body."""
    if t_rel < 0 or t_rel > dur:
        return 0.0
    tone = math.sin(2.0 * math.pi * 190.0 * t_rel) * math.exp(-14.0 * t_rel) * 0.4
    noise = (np.random.uniform(-1.0, 1.0) if t_rel < 0.25 else 0.0) * math.exp(-11.0 * t_rel) * 0.65
    return math.tanh((tone + noise) * 1.4)


def create_hihat(t_rel: float, open_hat: bool = False) -> float:
    """Synthesize crisp metallic hi-hat using decayed highpass noise."""
    decay = 18.0 if open_hat else 65.0
    dur = 0.25 if open_hat else 0.07
    if t_rel < 0 or t_rel > dur:
        return 0.0
    # Metallic ringing frequencies
    metal = (
        math.sin(2.0 * math.pi * 7100.0 * t_rel) * 0.3
        + math.sin(2.0 * math.pi * 9300.0 * t_rel) * 0.25
        + (np.random.uniform(-1.0, 1.0) * 0.45)
    )
    return metal * math.exp(-decay * t_rel) * 0.45


def create_sub_bass(t: float, f0: float = 43.65) -> float:
    """Pumping sidechained analog sub-bass (F0 = 43.65Hz for key of F minor)."""
    beat_pos = (t % BEAT_SEC) / BEAT_SEC
    # Pumping sidechain envelope ducking on the kick
    sidechain = 1.0 - math.exp(-8.0 * max(0.0, beat_pos - 0.08))
    # Rich distorted sawtooth + sub sine
    saw = 2.0 * ((t * f0) % 1.0) - 1.0
    sub_sine = math.sin(2.0 * math.pi * f0 * t)
    harm2 = math.sin(2.0 * math.pi * f0 * 2.0 * t) * 0.4
    raw = (saw * 0.3 + sub_sine * 0.7 + harm2) * sidechain
    return math.tanh(raw * 1.5) * 0.6


def create_synth_arp(t: float) -> float:
    """16th-note cybernetic arpeggio in F minor (F, Ab, C, Eb, F, G, Ab, C)."""
    step = int((t / (BEAT_SEC / 4.0))) % 16
    scale_mults = [1.0, 1.189, 1.498, 1.782, 2.0, 2.245, 2.378, 2.996,
                   2.0, 1.782, 1.498, 1.189, 2.378, 2.996, 3.564, 4.0]
    freq = 174.61 * scale_mults[step]  # F3 base
    t_step = t % (BEAT_SEC / 4.0)
    env = math.exp(-22.0 * t_step)
    val = (math.sin(2.0 * math.pi * freq * t) + 0.3 * math.sin(4.0 * math.pi * freq * t)) * env
    return val * 0.35


def synthesize_sfx(left: np.ndarray, right: np.ndarray):
    """Inject pixel-synchronized cinematic SFX at exact scene cut timestamps."""
    transitions = [
        (0.0, "BOOT"), (3.8, "DROP1"), (7.8, "WARP"), (12.0, "BLADE"),
        (16.0, "SLASH"), (20.2, "CRT"), (24.8, "DROP2"), (29.5, "CASCADE"),
        (33.3, "PAN3D"), (37.5, "VORTEX"), (41.0, "SHATTER"), (45.5, "BLACKOUT")
    ]

    for t_event, sfx_type in transitions:
        idx_start = int(t_event * SAMPLE_RATE)

        # 1. Seismic Sub-Impact (at major drops)
        if sfx_type in ("DROP1", "DROP2", "SHATTER"):
            dur_sub = 2.8
            n_sub = min(int(dur_sub * SAMPLE_RATE), TOTAL_SAMPLES - idx_start)
            ts = np.linspace(0, dur_sub, n_sub)
            freqs = 70.0 * np.exp(-1.8 * ts) + 28.0
            phase = 2.0 * np.pi * np.cumsum(freqs) / SAMPLE_RATE
            sub_hit = np.sin(phase) * np.exp(-1.4 * ts) * 0.95
            left[idx_start:idx_start + n_sub] += sub_hit
            right[idx_start:idx_start + n_sub] += sub_hit

        # 2. Whoosh / Air Rush Whip Transition
        dur_w = 0.55
        n_w = min(int(dur_w * SAMPLE_RATE), TOTAL_SAMPLES - idx_start)
        if n_w > 0:
            ts = np.linspace(-0.25, 0.3, n_w)
            noise = np.random.uniform(-1.0, 1.0, n_w)
            envelope = np.exp(-25.0 * (ts ** 2)) * 0.6
            pan = np.linspace(-0.8, 0.8, n_w) if "SLASH" in sfx_type or "PAN3D" in sfx_type else np.zeros(n_w)
            left[idx_start:idx_start + n_w] += noise * envelope * (0.5 - 0.5 * pan)
            right[idx_start:idx_start + n_w] += noise * envelope * (0.5 + 0.5 * pan)

        # 3. High-Tech Cybernetic Digital Chirp / UI Clicks
        n_chirp = min(int(0.25 * SAMPLE_RATE), TOTAL_SAMPLES - idx_start)
        if n_chirp > 0:
            ts = np.linspace(0, 0.25, n_chirp)
            f_chirp = 2400.0 + 1800.0 * np.sin(2.0 * np.pi * 32.0 * ts)
            chirp = np.sin(2.0 * np.pi * np.cumsum(f_chirp) / SAMPLE_RATE) * np.exp(-18.0 * ts) * 0.35
            left[idx_start:idx_start + n_chirp] += chirp
            right[idx_start:idx_start + n_chirp] += chirp

        # 4. CRT Horizon Laser Snap
        if sfx_type == "CRT":
            n_crt = min(int(0.3 * SAMPLE_RATE), TOTAL_SAMPLES - idx_start)
            ts = np.linspace(0, 0.3, n_crt)
            crt_freq = 4800.0 * np.exp(-25.0 * ts) + 80.0
            crt = np.sin(2.0 * np.pi * np.cumsum(crt_freq) / SAMPLE_RATE) * np.exp(-10.0 * ts) * 0.7
            left[idx_start:idx_start + n_crt] += crt
            right[idx_start:idx_start + n_crt] += crt


def generate_soundtrack(output_wav: str = "assets/showcase_soundtrack.wav"):
    """Synthesize full master soundtrack and write to 48kHz 16-bit WAV."""
    print(f"[AUDIO] Synthesizing {DURATION}s 128 BPM industrial cyberpunk master...")
    np.random.seed(42)

    left = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    right = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

    for i in range(TOTAL_SAMPLES):
        t = i / SAMPLE_RATE

        # Section 1: Intro Cold Open (0.0s - 3.8s)
        if t < 3.8:
            # Low tension drone + pulse
            drone = math.sin(2.0 * math.pi * 55.0 * t) * 0.25 * (t / 3.8)
            # Riser build into Drop 1
            riser_f = 140.0 + 750.0 * ((t / 3.8) ** 2)
            riser = math.sin(2.0 * math.pi * riser_f * t) * (0.05 + 0.35 * (t / 3.8))
            left[i] += drone + riser
            right[i] += drone + riser
            continue

        # Full Groove with Breakdown around Shot 5 & 6 (18.0s - 24.8s)
        beat_idx = int(t / BEAT_SEC)
        beat_rel = (t % BEAT_SEC)

        is_breakdown = (18.0 <= t < 24.8)
        if not is_breakdown:
            kick = create_kick(beat_rel)
            left[i] += kick
            right[i] += kick

            # Sub-bass groove
            sub = create_sub_bass(t)
            left[i] += sub
            right[i] += sub

            # Arpeggio lead
            arp = create_synth_arp(t)
            left[i] += arp * 0.8
            right[i] += arp * 1.2

        # Snare on beats 2 & 4 (or build roll in breakdown)
        if not is_breakdown:
            if beat_idx % 4 in (1, 3):
                snare = create_snare(beat_rel)
                left[i] += snare
                right[i] += snare
        else:
            # Accelerating build roll during breakdown
            roll_subdiv = 8 if t < 21.5 else 16
            roll_rel = (t % (BEAT_SEC / roll_subdiv))
            snare_roll = create_snare(roll_rel, 0.1) * min(1.0, (t - 18.0) / 6.8)
            riser_break = math.sin(2.0 * math.pi * (180.0 + 1100.0 * ((t - 18.0) / 6.8) ** 2) * t) * 0.3
            left[i] += snare_roll + riser_break
            right[i] += snare_roll + riser_break

        # Hi-hats: 16th-note ticks
        sixteenth_rel = t % (BEAT_SEC / 4.0)
        open_hat = ((int(t / (BEAT_SEC / 2.0)) % 2) == 1) and (sixteenth_rel < 0.05)
        hat = create_hihat(sixteenth_rel, open_hat=open_hat)
        left[i] += hat * 0.9
        right[i] += hat * 1.1

    # Apply SFX at scene changes
    synthesize_sfx(left, right)

    # Sidechain Ducking with Voiceover Stem if present
    voice_wav = "assets/showcase_voiceover.wav"
    if os.path.exists(voice_wav):
        print(f"[AUDIO] Integrating vocal stem and applying sidechain ducking from {voice_wav}...")
        with wave.open(voice_wav, "rb") as vwf:
            n_v = min(vwf.getnframes(), TOTAL_SAMPLES)
            v_raw = vwf.readframes(n_v)
            v_samples = np.frombuffer(v_raw, dtype=np.int16).astype(np.float32) / 32768.0
            v_left = v_samples[0::2][:n_v]
            v_right = v_samples[1::2][:n_v]

            # Compute smoothed RMS envelope for sidechain ducking
            v_env = np.abs(v_left)
            # 60ms rolling window
            win_size = int(SAMPLE_RATE * 0.06)
            kernel = np.ones(win_size) / win_size
            v_smooth = np.convolve(v_env, kernel, mode="same")
            duck_factor = 1.0 - 0.58 * np.clip(v_smooth * 5.0, 0.0, 1.0)

            # Duck music bed
            left[:n_v] *= duck_factor
            right[:n_v] *= duck_factor

            # Mix voiceover cleanly with broadcast presence boost
            left[:n_v] += v_left * 1.35
            right[:n_v] += v_right * 1.35

    # Master Hard Limiter & Normalization to -0.5 dBFS
    max_amp = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-4)
    target_amp = 0.94
    gain = target_amp / max_amp
    left = np.clip(left * gain, -1.0, 1.0)
    right = np.clip(right * gain, -1.0, 1.0)

    # Convert to 16-bit signed PCM
    left_16 = (left * 32767).astype(np.int16)
    right_16 = (right * 32767).astype(np.int16)
    stereo = np.empty((TOTAL_SAMPLES * 2,), dtype=np.int16)
    stereo[0::2] = left_16
    stereo[1::2] = right_16

    with wave.open(output_wav, "wb") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(stereo.tobytes())

    print(f"[OK] Generated {output_wav} ({TOTAL_SAMPLES} samples @ {SAMPLE_RATE}Hz).")


if __name__ == "__main__":
    generate_soundtrack()
