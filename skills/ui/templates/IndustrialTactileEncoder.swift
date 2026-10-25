import SwiftUI
import UIKit

/// IndustrialTactileEncoder (SwiftUI)
///
/// Production Native iOS Rotary Hardware Encoder inspired by Teenage Engineering.
/// Features physical spring dynamics (withAnimation(.spring)), rigid detent haptics
/// (UIImpactFeedbackGenerator), Canvas-accelerated GPU waveform rendering, and monospaced digits.
public struct IndustrialTactileEncoder: View {
    public var label: String
    public var minVal: Double
    public var maxVal: Double
    public var defaultValue: Double
    public var unit: String
    public var onValueChanged: ((Double) -> Void)?

    @State private var currentAngle: Double = 0.0
    @State private var startAngle: Double = 0.0
    @State private var lastHapticAngle: Double = 0.0
    @State private var displayValue: Double = 1250.0
    @State private var isBypassed: Bool = false

    private let minAngle: Double = -140.0
    private let maxAngle: Double = 140.0
    private let detentStep: Double = 10.0 // degrees per detent tick
    private let hapticEngine = UIImpactFeedbackGenerator(style: .rigid)

    public init(
        label: String = "FILTER FREQUENCY",
        minVal: Double = 20.0,
        maxVal: Double = 20000.0,
        defaultValue: Double = 1250.0,
        unit: String = "Hz",
        onValueChanged: ((Double) -> Void)? = nil
    ) {
        self.label = label
        self.minVal = minVal
        self.maxVal = maxVal
        self.defaultValue = defaultValue
        self.unit = unit
        self.onValueChanged = onValueChanged
    }

    private func angleToValue(_ angle: Double) -> Double {
        let norm = (angle - minAngle) / (maxAngle - minAngle)
        let clamped = max(0.0, min(1.0, norm))
        return minVal * pow(maxVal / minVal, clamped)
    }

    private func valueToAngle(_ value: Double) -> Double {
        let norm = (log(value) - log(minVal)) / (log(maxVal) - log(minVal))
        let clamped = max(0.0, min(1.0, norm))
        return minAngle + clamped * (maxAngle - minAngle)
    }

    public var body: some View {
        VStack(spacing: 12) {
            // Header Bar
            HStack {
                Text(label)
                    .font(.system(size: 11, weight: .bold, design: .monospaced))
                    .foregroundColor(Color(white: 0.65))
                    .tracking(1.1)

                Spacer()

                Text(isBypassed ? "BYPASS" : "ACTIVE")
                    .font(.system(size: 10, weight: .bold, design: .monospaced))
                    .foregroundColor(isBypassed ? Color(white: 0.65) : Color(red: 0.20, green: 0.83, blue: 0.60))
                    .padding(.horizontal, 8)
                    .padding(.vertical, 3)
                    .background(Color(red: 0.09, green: 0.09, blue: 0.11))
                    .cornerRadius(4)
                    .overlay(
                        RoundedRectangle(cornerRadius: 4)
                            .stroke(Color(white: 0.15), lineWidth: 1)
                    )
            }
            .padding(.bottom, 4)

            // Oscilloscope Canvas Screen
            VStack(spacing: 4) {
                HStack {
                    Text("OSC // REALTIME")
                    Spacer()
                    Text(isBypassed ? "0.00 dB" : "-3.20 dB")
                }
                .font(.system(size: 9, design: .monospaced))
                .foregroundColor(Color(white: 0.50))

                Canvas { context, size in
                    // Grid reference line
                    var gridPath = Path()
                    gridPath.move(to: CGPoint(x: 0, y: size.height / 2))
                    gridPath.addLine(to: CGPoint(x: size.width, y: size.height / 2))
                    context.stroke(
                        gridPath,
                        with: .color(Color(white: 0.15)),
                        style: StrokeStyle(lineWidth: 1, dash: [3, 3])
                    )

                    // Waveform line
                    var wavePath = Path()
                    let points = 50
                    let amp = isBypassed ? 0.0 : size.height * 0.35
                    let freqFactor = (displayValue / maxVal) * 14.0 + 1.0

                    for i in 0...points {
                        let x = (Double(i) / Double(points)) * size.width
                        let y = size.height / 2.0 + sin((Double(i) / Double(points)) * .pi * freqFactor) * amp
                        if i == 0 {
                            wavePath.move(to: CGPoint(x: x, y: y))
                        } else {
                            wavePath.addLine(to: CGPoint(x: x, y: y))
                        }
                    }

                    context.stroke(
                        wavePath,
                        with: .color(isBypassed ? Color(white: 0.45) : Color(red: 0.96, green: 0.62, blue: 0.04)),
                        style: StrokeStyle(lineWidth: 1.8, lineCap: .round)
                    )
                }
                .frame(height: 38)
            }
            .padding(8)
            .background(Color(red: 0.09, green: 0.09, blue: 0.11))
            .cornerRadius(8)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color(white: 0.15), lineWidth: 1)
            )

            // Interactive Rotary Dial Area
            ZStack {
                // Dial Gauge Ticks
                Canvas { context, size in
                    let center = CGPoint(x: size.width / 2, y: size.height / 2)
                    let outerRadius = size.width / 2
                    let totalTicks = 29
                    let step = (maxAngle - minAngle) / Double(totalTicks - 1)

                    for i in 0..<totalTicks {
                        let deg = minAngle + Double(i) * step
                        let rad = (deg - 90.0) * .pi / 180.0
                        let isMajor = i % 4 == 0
                        let r1 = outerRadius - 4
                        let r2 = isMajor ? outerRadius - 14 : outerRadius - 9

                        var path = Path()
                        path.move(to: CGPoint(x: center.x + r1 * cos(rad), y: center.y + r1 * sin(rad)))
                        path.addLine(to: CGPoint(x: center.x + r2 * cos(rad), y: center.y + r2 * sin(rad)))

                        let tickColor = (deg == 0)
                            ? Color(red: 0.96, green: 0.62, blue: 0.04)
                            : (isMajor ? Color(white: 0.65) : Color(white: 0.25))

                        context.stroke(
                            path,
                            with: .color(tickColor),
                            style: StrokeStyle(lineWidth: isMajor ? 1.5 : 1.0, lineCap: .round)
                        )
                    }
                }
                .frame(width: 170, height: 170)

                // Machined Metal Knob
                ZStack {
                    Circle()
                        .fill(
                            RadialGradient(
                                colors: [Color(white: 0.15), Color(white: 0.05)],
                                center: .center,
                                startRadius: 5,
                                endRadius: 55
                            )
                        )
                        .overlay(Circle().stroke(Color(white: 0.25), lineWidth: 1.5))
                        .frame(width: 110, height: 110)

                    // Knurled Texture Ring
                    Circle()
                        .stroke(Color(white: 0.18), lineWidth: 1)
                        .frame(width: 98, height: 98)

                    // Tactical Amber Needle
                    Capsule()
                        .fill(Color(red: 0.96, green: 0.62, blue: 0.04))
                        .frame(width: 3.5, height: 16)
                        .offset(y: -40)

                    // Center Cap
                    Circle()
                        .fill(Color(red: 0.05, green: 0.05, blue: 0.06))
                        .overlay(Circle().stroke(Color(white: 0.15), lineWidth: 1))
                        .frame(width: 40, height: 40)
                }
                .rotationEffect(.degrees(currentAngle))
                .gesture(
                    DragGesture(minimumDistance: 0)
                        .onChanged { value in
                            if startAngle == 0.0 && currentAngle != 0.0 {
                                startAngle = currentAngle
                            }
                            let nextAngle = max(minAngle, min(maxAngle, startAngle - Double(value.translation.height) * 1.0))
                            currentAngle = nextAngle

                            // Discrete tactile detent haptics
                            if abs(nextAngle - lastHapticAngle) >= detentStep {
                                hapticEngine.impactOccurred()
                                lastHapticAngle = nextAngle
                            }

                            let newVal = angleToValue(nextAngle)
                            displayValue = newVal
                            onValueChanged?(newVal)
                        }
                        .onEnded { _ in
                            startAngle = 0.0
                            let nearest = (currentAngle / detentStep).rounded() * detentStep
                            let clamped = max(minAngle, min(maxAngle, nearest))

                            withAnimation(.spring(response: 0.32, dampingFraction: 0.75)) {
                                currentAngle = clamped
                            }

                            let finalVal = angleToValue(clamped)
                            displayValue = finalVal
                            onValueChanged?(finalVal)
                        }
                )
            }
            .frame(width: 170, height: 170)
            .padding(.vertical, 8)

            // Tabular Telemetry Value Readout
            VStack(spacing: 2) {
                HStack(alignment: .firstTextBaseline, spacing: 4) {
                    Text(String(format: "%.0f", displayValue))
                        .font(.system(size: 30, weight: .bold, design: .monospaced))
                        .monospacedDigit()
                        .foregroundColor(.white)

                    Text(unit)
                        .font(.system(size: 14, weight: .semibold, design: .monospaced))
                        .foregroundColor(Color(red: 0.96, green: 0.62, blue: 0.04))
                }

                Text("DETENT STEP: ±10°")
                    .font(.system(size: 9, design: .monospaced))
                    .foregroundColor(Color(white: 0.45))
            }

            // Tactical Punch Buttons
            HStack(spacing: 8) {
                Button(action: {
                    hapticEngine.impactOccurred()
                    isBypassed.toggle()
                }) {
                    Text(isBypassed ? "ENGAGE" : "BYPASS")
                        .font(.system(size: 11, weight: .bold, design: .monospaced))
                        .foregroundColor(isBypassed ? Color(red: 0.96, green: 0.62, blue: 0.04) : Color(white: 0.65))
                        .frame(maxWidth: .infinity)
                        .frame(height: 38)
                        .background(isBypassed ? Color(red: 0.96, green: 0.62, blue: 0.04).opacity(0.15) : Color(red: 0.09, green: 0.09, blue: 0.11))
                        .cornerRadius(6)
                        .overlay(
                            RoundedRectangle(cornerRadius: 6)
                                .stroke(isBypassed ? Color(red: 0.96, green: 0.62, blue: 0.04).opacity(0.4) : Color(white: 0.15), lineWidth: 1)
                        )
                }

                Button(action: {
                    hapticEngine.impactOccurred()
                    let targetAngle = valueToAngle(defaultValue)
                    withAnimation(.spring(response: 0.35, dampingFraction: 0.72)) {
                        currentAngle = targetAngle
                    }
                    displayValue = defaultValue
                    onValueChanged?(defaultValue)
                }) {
                    Text("RESET 1.25k")
                        .font(.system(size: 11, weight: .bold, design: .monospaced))
                        .foregroundColor(Color(white: 0.65))
                        .frame(maxWidth: .infinity)
                        .frame(height: 38)
                        .background(Color(red: 0.09, green: 0.09, blue: 0.11))
                        .cornerRadius(6)
                        .overlay(
                            RoundedRectangle(cornerRadius: 6)
                                .stroke(Color(white: 0.15), lineWidth: 1)
                        )
                }
            }
            .padding(.top, 4)
        }
        .padding(16)
        .frame(width: 320)
        .background(Color(red: 0.04, green: 0.04, blue: 0.04))
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color(white: 0.15), lineWidth: 1)
        )
        .onAppear {
            hapticEngine.prepare()
            currentAngle = valueToAngle(defaultValue)
            displayValue = defaultValue
        }
    }
}
