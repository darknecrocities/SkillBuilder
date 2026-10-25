import React, { useState, useCallback } from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { Gesture, GestureDetector } from "react-native-gesture-handler";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  runOnJS,
} from "react-native-reanimated";
import * as Haptics from "expo-haptics";
import Svg, { Line, Polyline, Circle } from "react-native-svg";

interface IndustrialTactileEncoderProps {
  label?: string;
  min?: number;
  max?: number;
  defaultValue?: number;
  unit?: string;
  onValueChange?: (val: number) => void;
}

const MIN_ANGLE = -140;
const MAX_ANGLE = 140;
const DETENT_STEP = 10; // 10 degrees per detent

/**
 * IndustrialTactileEncoder (React Native)
 * Production React Native rotary hardware encoder inspired by Teenage Engineering.
 * Uses Reanimated 3 worklets for 120Hz native UI thread execution,
 * Gesture Handler for zero-bridge latency, and Expo Haptics for tactile detents.
 */
export const IndustrialTactileEncoder: React.FC<IndustrialTactileEncoderProps> = ({
  label = "FILTER FREQUENCY",
  min = 20,
  max = 20000,
  defaultValue = 1250,
  unit = "Hz",
  onValueChange,
}) => {
  const [displayValue, setDisplayValue] = useState(defaultValue);
  const [isBypassed, setIsBypassed] = useState(false);

  // Map initial value to angle (-140 to +140)
  const normInit =
    (Math.log(defaultValue) - Math.log(min)) / (Math.log(max) - Math.log(min));
  const initialAngle = MIN_ANGLE + Math.max(0, Math.min(1, normInit)) * (MAX_ANGLE - MIN_ANGLE);

  const angle = useSharedValue(initialAngle);
  const startAngle = useSharedValue(initialAngle);
  const lastHapticAngle = useSharedValue(initialAngle);

  // Convert angle to logarithmic frequency value
  const updateCalculatedValue = useCallback(
    (deg: number) => {
      const norm = (deg - MIN_ANGLE) / (MAX_ANGLE - MIN_ANGLE);
      const clamped = Math.max(0, Math.min(1, norm));
      const val = Math.round(min * Math.pow(max / min, clamped));
      setDisplayValue(val);
      onValueChange?.(val);
    },
    [min, max, onValueChange]
  );

  const triggerDetentHaptic = () => {
    Haptics.selectionAsync();
  };

  const panGesture = Gesture.Pan()
    .onBegin(() => {
      startAngle.value = angle.value;
    })
    .onUpdate((e) => {
      // 1px vertical drag = 1.2 degrees rotation
      const nextAngle = Math.max(
        MIN_ANGLE,
        Math.min(MAX_ANGLE, startAngle.value - e.translationY * 1.2)
      );
      angle.value = nextAngle;

      // Detent haptic feedback on discrete angular increments
      if (Math.abs(nextAngle - lastHapticAngle.value) >= DETENT_STEP) {
        lastHapticAngle.value = nextAngle;
        runOnJS(triggerDetentHaptic)();
      }

      runOnJS(updateCalculatedValue)(nextAngle);
    })
    .onEnd(() => {
      // Snap to nearest detent tick using physical spring
      const nearestDetent = Math.round(angle.value / DETENT_STEP) * DETENT_STEP;
      const targetAngle = Math.max(MIN_ANGLE, Math.min(MAX_ANGLE, nearestDetent));

      angle.value = withSpring(targetAngle, {
        stiffness: 350,
        damping: 28,
        mass: 1.0,
      });

      runOnJS(updateCalculatedValue)(targetAngle);
    });

  const animatedKnobStyle = useAnimatedStyle(() => ({
    transform: [{ rotate: `${angle.value}deg` }],
  }));

  // Generate 29 dial ticks
  const ticks = Array.from({ length: 29 }, (_, i) => MIN_ANGLE + i * DETENT_STEP);

  // Generate oscilloscope waveform points
  const wavePoints = Array.from({ length: 40 }, (_, i) => {
    const x = (i / 39) * 200;
    const freqFactor = (displayValue / max) * 12 + 1;
    const amp = isBypassed ? 0 : Math.sin((i / 39) * Math.PI * freqFactor) * 12;
    return `${x},${18 + amp}`;
  }).join(" ");

  return (
    <View style={styles.container}>
      {/* Header Bar */}
      <View style={styles.header}>
        <Text style={styles.headerLabel}>{label}</Text>
        <View style={styles.statusBadge}>
          <Text style={[styles.statusText, isBypassed && styles.statusBypassed]}>
            {isBypassed ? "BYPASS" : "ACTIVE"}
          </Text>
        </View>
      </View>

      {/* Waveform Mini-Screen */}
      <View style={styles.screenContainer}>
        <View style={styles.screenHeader}>
          <Text style={styles.screenTitle}>OSC // REALTIME</Text>
          <Text style={styles.screenDb}>{isBypassed ? "0.00 dB" : "-3.20 dB"}</Text>
        </View>
        <Svg width="100%" height={36} viewBox="0 0 200 36">
          <Line x1="0" y1="18" x2="200" y2="18" stroke="#27272a" strokeWidth="1" strokeDasharray="3 3" />
          <Polyline
            fill="none"
            stroke={isBypassed ? "#71717a" : "#f59e0b"}
            strokeWidth="1.8"
            points={wavePoints}
          />
        </Svg>
      </View>

      {/* Rotary Dial Area */}
      <View style={styles.dialWrapper}>
        <Svg width={180} height={180} style={StyleSheet.absoluteFill}>
          {ticks.map((deg) => {
            const rad = ((deg - 90) * Math.PI) / 180;
            const isMajor = deg % 40 === 0;
            const r1 = 86;
            const r2 = isMajor ? 74 : 79;
            const cx = 90;
            const cy = 90;
            const x1 = cx + r1 * Math.cos(rad);
            const y1 = cy + r1 * Math.sin(rad);
            const x2 = cx + r2 * Math.cos(rad);
            const y2 = cy + r2 * Math.sin(rad);

            return (
              <Line
                key={deg}
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke={deg === 0 ? "#f59e0b" : isMajor ? "#a1a1aa" : "#3f3f46"}
                strokeWidth={isMajor ? 1.5 : 1}
              />
            );
          })}
        </Svg>

        <GestureDetector gesture={panGesture}>
          <Animated.View style={[styles.knobBody, animatedKnobStyle]}>
            <View style={styles.knurledRing} />
            <View style={styles.needleIndicator} />
            <View style={styles.centerCap}>
              <Circle r={4} fill="#52525b" />
            </View>
          </Animated.View>
        </GestureDetector>
      </View>

      {/* Tabular Telemetry Value */}
      <View style={styles.valueRow}>
        <Text style={styles.valueNumber}>{displayValue.toLocaleString()}</Text>
        <Text style={styles.valueUnit}>{unit}</Text>
      </View>
      <Text style={styles.valueSubtext}>DETENT STEP: ±{DETENT_STEP}°</Text>

      {/* Action Buttons */}
      <View style={styles.actionsRow}>
        <Pressable
          onPress={() => {
            Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
            setIsBypassed((prev) => !prev);
          }}
          style={[styles.button, isBypassed && styles.buttonActive]}
        >
          <Text style={[styles.buttonText, isBypassed && styles.buttonTextActive]}>
            {isBypassed ? "ENGAGE" : "BYPASS"}
          </Text>
        </Pressable>

        <Pressable
          onPress={() => {
            Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
            angle.value = withSpring(initialAngle, { stiffness: 350, damping: 28 });
            updateCalculatedValue(initialAngle);
          }}
          style={styles.button}
        >
          <Text style={styles.buttonText}>RESET 1.25k</Text>
        </Pressable>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: 320,
    backgroundColor: "#09090b",
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: "#27272a",
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    borderBottomWidth: 1,
    borderBottomColor: "#18181b",
    paddingBottom: 10,
  },
  headerLabel: {
    color: "#a1a1aa",
    fontSize: 11,
    fontFamily: "Courier",
    fontWeight: "700",
    letterSpacing: 1.1,
  },
  statusBadge: {
    backgroundColor: "#18181b",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 4,
    borderWidth: 1,
    borderColor: "#27272a",
  },
  statusText: {
    color: "#34d399",
    fontSize: 10,
    fontFamily: "Courier",
    fontWeight: "700",
  },
  statusBypassed: {
    color: "#a1a1aa",
  },
  screenContainer: {
    marginTop: 12,
    backgroundColor: "#18181b",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#27272a",
    padding: 8,
  },
  screenHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 4,
  },
  screenTitle: {
    color: "#71717a",
    fontSize: 9,
    fontFamily: "Courier",
  },
  screenDb: {
    color: "#a1a1aa",
    fontSize: 9,
    fontFamily: "Courier",
  },
  dialWrapper: {
    width: 180,
    height: 180,
    alignSelf: "center",
    justifyContent: "center",
    alignItems: "center",
    marginVertical: 14,
  },
  knobBody: {
    width: 116,
    height: 116,
    borderRadius: 58,
    backgroundColor: "#18181b",
    borderWidth: 1.5,
    borderColor: "#3f3f46",
    justifyContent: "center",
    alignItems: "center",
  },
  knurledRing: {
    position: "absolute",
    width: 106,
    height: 106,
    borderRadius: 53,
    borderWidth: 1,
    borderColor: "#27272a",
  },
  needleIndicator: {
    position: "absolute",
    top: 6,
    width: 3.5,
    height: 16,
    borderRadius: 2,
    backgroundColor: "#f59e0b",
  },
  centerCap: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: "#09090b",
    borderWidth: 1,
    borderColor: "#27272a",
    justifyContent: "center",
    alignItems: "center",
  },
  valueRow: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "baseline",
    marginTop: 4,
  },
  valueNumber: {
    color: "#ffffff",
    fontSize: 30,
    fontWeight: "700",
    fontFamily: "Courier",
    fontVariant: ["tabular-nums"],
  },
  valueUnit: {
    color: "#f59e0b",
    fontSize: 14,
    fontWeight: "600",
    fontFamily: "Courier",
    marginLeft: 4,
  },
  valueSubtext: {
    color: "#71717a",
    fontSize: 9,
    fontFamily: "Courier",
    textAlign: "center",
    marginTop: 2,
  },
  actionsRow: {
    flexDirection: "row",
    gap: 8,
    marginTop: 14,
  },
  button: {
    flex: 1,
    height: 38,
    borderRadius: 6,
    backgroundColor: "#18181b",
    borderWidth: 1,
    borderColor: "#27272a",
    justifyContent: "center",
    alignItems: "center",
  },
  buttonActive: {
    backgroundColor: "rgba(245, 158, 11, 0.15)",
    borderColor: "rgba(245, 158, 11, 0.4)",
  },
  buttonText: {
    color: "#a1a1aa",
    fontSize: 11,
    fontFamily: "Courier",
    fontWeight: "600",
  },
  buttonTextActive: {
    color: "#f59e0b",
  },
});
