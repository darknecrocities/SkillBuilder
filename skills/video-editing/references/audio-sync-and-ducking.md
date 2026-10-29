# Audio-Visual BPM Grid Synchronization & Broadcast Mastering

Guide for musical tempo locking, broadcast vocal dynamics, and automated sidechain ducking.

---

## 1. Musical BPM Grid Synchronization

Choreograph scene transitions and camera pans to musical downbeats:

$$\text{Seconds Per Beat} = \frac{60}{\text{BPM}}$$
$$\text{Seconds Per Bar (4 Beats)} = \frac{240}{\text{BPM}}$$
$$\text{Frames Per Bar (@ 30 FPS)} = \text{round}\left(\frac{240}{\text{BPM}} \times 30\right)$$

### Reference Tempo Table

| BPM | Beat Duration | Bar Duration (4/4) | Frames Per Beat (30 FPS) | Frames Per Bar (30 FPS) |
| :---: | :---: | :---: | :---: | :---: |
| **120** | 0.5000s | 2.0000s | 15 frames | 60 frames |
| **128** | 0.4688s | 1.8750s | 14 frames | 56 frames |
| **140** | 0.4286s | 1.7143s | 13 frames | 51 frames |

---

## 2. Broadcast Vocal Chain

Raw text-to-speech output often contains low-frequency pops and uneven dynamics. Process every voiceover segment through a broadcast chain:

```bash
ffmpeg -y -i raw_voice.mp3 \
  -af "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-40dB:stop_periods=-1:stop_duration=0.18:stop_threshold=-40dB,\
highpass=f=90,\
equalizer=f=3200:t=q:w=1.2:g=2.5,\
acompressor=threshold=-18dB:ratio=3.2:attack=8:release=80,\
volume=1.15" \
  -ar 48000 -ac 1 clean_voice.wav
```

1. **`silenceremove`**: Trims leading and trailing silence while preserving natural pauses.
2. **`highpass=90Hz`**: Removes microphone plosives and sub-bass rumble.
3. **`equalizer=3.2kHz`**: Lifts presence and consonant intelligibility.
4. **`acompressor`**: LA-2A style optical dynamic smoothing.

---

## 3. Sidechain Ducking Formula

Whenever vocal amplitude exceeds speech threshold, duck the music bed by $-6.5\text{dB}$:

$$\text{Ducking Multiplier} = 10^{-\frac{6.5}{20}} \approx 0.473$$

Smooth ducking with an attack envelope (12ms) and release envelope (180ms) to avoid audible pumping.
