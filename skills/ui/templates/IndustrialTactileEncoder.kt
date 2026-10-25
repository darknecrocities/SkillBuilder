package com.skillbuilder.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch
import kotlin.math.*

/**
 * IndustrialTactileEncoder (Jetpack Compose)
 *
 * Production Native Android Rotary Hardware Encoder inspired by Teenage Engineering.
 * Features physical spring simulation (Animatable + spring()), tactile detent haptics
 * (LocalHapticFeedback), hardware-accelerated Canvas oscilloscope, and tabular monospace digits.
 */
@Composable
fun IndustrialTactileEncoder(
    label: String = "FILTER FREQUENCY",
    minVal: Float = 20f,
    maxVal: Float = 20000f,
    defaultValue: Float = 1250f,
    unit: String = "Hz",
    onValueChanged: ((Float) -> Unit)? = null
) {
    val minAngle = -140f
    val maxAngle = 140f
    val detentStep = 10f

    fun valueToAngle(value: Float): Float {
        val norm = (ln(value) - ln(minVal)) / (ln(maxVal) - ln(minVal))
        return minAngle + norm.coerceIn(0f, 1f) * (maxAngle - minAngle)
    }

    fun angleToValue(angle: Float): Float {
        val norm = (angle - minAngle) / (maxAngle - minAngle)
        return minVal * (maxVal / minVal).pow(norm.coerceIn(0f, 1f))
    }

    val initialAngle = remember { valueToAngle(defaultValue) }
    val rotation = remember { Animatable(initialAngle) }
    var displayValue by remember { mutableStateOf(defaultValue) }
    var isBypassed by remember { mutableStateOf(false) }
    var lastHapticAngle by remember { mutableStateOf(initialAngle) }
    val scope = rememberCoroutineScope()
    val haptics = LocalHapticFeedback.current

    Column(
        modifier = Modifier
            .width(320.dp)
            .background(Color(0xFF09090B), RoundedCornerShape(16.dp))
            .border(1.dp, Color(0xFF27272A), RoundedCornerShape(16.dp))
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Top Header
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = label,
                style = TextStyle(
                    color = Color(0xFFA1A1AA),
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace,
                    letterSpacing = 1.1.sp
                )
            )

            Box(
                modifier = Modifier
                    .background(Color(0xFF18181B), RoundedCornerShape(4.dp))
                    .border(1.dp, Color(0xFF27272A), RoundedCornerShape(4.dp))
                    .padding(horizontal = 8.dp, vertical = 3.dp)
            ) {
                Text(
                    text = if (isBypassed) "BYPASS" else "ACTIVE",
                    style = TextStyle(
                        color = if (isBypassed) Color(0xFFA1A1AA) else Color(0xFF34D399),
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        fontFamily = FontFamily.Monospace
                    )
                )
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        // Oscilloscope Mini-Screen
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFF18181B), RoundedCornerShape(8.dp))
                .border(1.dp, Color(0xFF27272A), RoundedCornerShape(8.dp))
                .padding(8.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "OSC // REALTIME",
                    style = TextStyle(color = Color(0xFF71717A), fontSize = 9.sp, fontFamily = FontFamily.Monospace)
                )
                Text(
                    text = if (isBypassed) "0.00 dB" else "-3.20 dB",
                    style = TextStyle(color = Color(0xFFA1A1AA), fontSize = 9.sp, fontFamily = FontFamily.Monospace)
                )
            }

            Canvas(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(36.dp)
            ) {
                // Dashed center grid line
                drawLine(
                    color = Color(0xFF27272A),
                    start = Offset(0f, size.height / 2f),
                    end = Offset(size.width, size.height / 2f),
                    strokeWidth = 1.dp.toPx(),
                    pathEffect = PathEffect.dashPathEffect(floatArrayOf(8f, 8f))
                )

                // Sine wave
                val points = 45
                val amp = if (isBypassed) 0f else size.height * 0.35f
                val freqFactor = (displayValue / maxVal) * 14f + 1f
                val wavePath = Path()

                for (i in 0..points) {
                    val x = (i.toFloat() / points) * size.width
                    val y = size.height / 2f + sin((i.toFloat() / points) * Math.PI.toFloat() * freqFactor) * amp
                    if (i == 0) wavePath.moveTo(x, y) else wavePath.lineTo(x, y)
                }

                drawPath(
                    path = wavePath,
                    color = if (isBypassed) Color(0xFF71717A) else Color(0xFFF59E0B),
                    style = Stroke(width = 1.8.dp.toPx(), cap = StrokeCap.Round)
                )
            }
        }

        Spacer(modifier = Modifier.height(14.dp))

        // Interactive Dial & Knob Area
        Box(
            modifier = Modifier
                .size(170.dp)
                .pointerInput(Unit) {
                    detectDragGestures(
                        onDrag = { change, dragAmount ->
                            change.consume()
                            val nextAngle = (rotation.value - dragAmount.y * 1.0f).coerceIn(minAngle, maxAngle)
                            scope.launch { rotation.snapTo(nextAngle) }

                            // Detent haptic feedback
                            if (abs(nextAngle - lastHapticAngle) >= detentStep) {
                                haptics.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                                lastHapticAngle = nextAngle
                            }

                            val calculated = angleToValue(nextAngle)
                            displayValue = calculated
                            onValueChanged?.invoke(calculated)
                        },
                        onDragEnd = {
                            val nearest = (rotation.value / detentStep).roundToInt() * detentStep
                            val target = nearest.toFloat().coerceIn(minAngle, maxAngle)
                            scope.launch {
                                rotation.animateTo(
                                    targetValue = target,
                                    animationSpec = spring(
                                        dampingRatio = Spring.DampingRatioMediumBouncy,
                                        stiffness = Spring.StiffnessMediumLow
                                    )
                                )
                            }
                            val finalVal = angleToValue(target)
                            displayValue = finalVal
                            onValueChanged?.invoke(finalVal)
                        }
                    )
                },
            contentAlignment = Alignment.Center
        ) {
            Canvas(modifier = Modifier.fillMaxSize()) {
                val center = Offset(size.width / 2f, size.height / 2f)
                val outerRadius = size.width / 2f
                val totalTicks = 29
                val step = (maxAngle - minAngle) / (totalTicks - 1)

                // Radial Tick Marks
                for (i in 0 until totalTicks) {
                    val deg = minAngle + i * step
                    val rad = (deg - 90f) * Math.PI.toFloat() / 180f
                    val isMajor = i % 4 == 0
                    val r1 = outerRadius - 4.dp.toPx()
                    val r2 = if (isMajor) outerRadius - 14.dp.toPx() else outerRadius - 9.dp.toPx()

                    val tickColor = if (deg == 0f) Color(0xFFF59E0B) else if (isMajor) Color(0xFFA1A1AA) else Color(0xFF3F3F46)
                    drawLine(
                        color = tickColor,
                        start = Offset(center.x + r1 * cos(rad), center.y + r1 * sin(rad)),
                        end = Offset(center.x + r2 * cos(rad), center.y + r2 * sin(rad)),
                        strokeWidth = if (isMajor) 1.5.dp.toPx() else 1.dp.toPx(),
                        cap = StrokeCap.Round
                    )
                }

                // Machined Knob Body
                val knobRadius = outerRadius * 0.65f
                drawCircle(color = Color(0xFF18181B), radius = knobRadius, center = center)
                drawCircle(color = Color(0xFF3F3F46), radius = knobRadius, center = center, style = Stroke(1.5.dp.toPx()))

                // Tactical Indicator Needle (Rotated)
                rotate(degrees = rotation.value, pivot = center) {
                    drawLine(
                        color = Color(0xFFF59E0B),
                        start = Offset(center.x, center.y - knobRadius + 6.dp.toPx()),
                        end = Offset(center.x, center.y - knobRadius + 20.dp.toPx()),
                        strokeWidth = 3.dp.toPx(),
                        cap = StrokeCap.Round
                    )
                }

                // Center Cap
                drawCircle(color = Color(0xFF09090B), radius = 20.dp.toPx(), center = center)
                drawCircle(color = Color(0xFF27272A), radius = 20.dp.toPx(), center = center, style = Stroke(1.dp.toPx()))
            }
        }

        Spacer(modifier = Modifier.height(10.dp))

        // Tabular Figures Digital Readout
        Row(
            verticalAlignment = Alignment.Bottom,
            horizontalArrangement = Arrangement.Center
        ) {
            Text(
                text = "%.0f".format(displayValue),
                style = TextStyle(
                    color = Color.White,
                    fontSize = 30.sp,
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace,
                    fontFeatureSettings = "tnum 1, zero 1"
                )
            )
            Spacer(modifier = Modifier.width(4.dp))
            Text(
                text = unit,
                style = TextStyle(
                    color = Color(0xFFF59E0B),
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    fontFamily = FontFamily.Monospace
                )
            )
        }

        Text(
            text = "DETENT STEP: ±10°",
            style = TextStyle(color = Color(0xFF71717A), fontSize = 9.sp, fontFamily = FontFamily.Monospace)
        )

        Spacer(modifier = Modifier.height(14.dp))

        // Action Buttons
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            OutlinedButton(
                onClick = {
                    haptics.performHapticFeedback(HapticFeedbackType.LongPress)
                    isBypassed = !isBypassed
                },
                modifier = Modifier.weight(1f).height(38.dp),
                shape = RoundedCornerShape(6.dp),
                colors = ButtonDefaults.outlinedButtonColors(
                    containerColor = if (isBypassed) Color(0x33F59E0B) else Color(0xFF18181B)
                ),
                border = androidx.compose.foundation.BorderStroke(1.dp, if (isBypassed) Color(0x66F59E0B) else Color(0xFF27272A))
            ) {
                Text(
                    text = if (isBypassed) "ENGAGE" else "BYPASS",
                    style = TextStyle(
                        color = if (isBypassed) Color(0xFFF59E0B) else Color(0xFFA1A1AA),
                        fontSize = 11.sp,
                        fontWeight = FontWeight.SemiBold,
                        fontFamily = FontFamily.Monospace
                    )
                )
            }

            OutlinedButton(
                onClick = {
                    haptics.performHapticFeedback(HapticFeedbackType.LongPress)
                    val target = valueToAngle(defaultValue)
                    scope.launch {
                        rotation.animateTo(
                            targetValue = target,
                            animationSpec = spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMediumLow)
                        )
                    }
                    displayValue = defaultValue
                    onValueChanged?.invoke(defaultValue)
                },
                modifier = Modifier.weight(1f).height(38.dp),
                shape = RoundedCornerShape(6.dp),
                colors = ButtonDefaults.outlinedButtonColors(containerColor = Color(0xFF18181B)),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFF27272A))
            ) {
                Text(
                    text = "RESET 1.25k",
                    style = TextStyle(color = Color(0xFFA1A1AA), fontSize = 11.sp, fontWeight = FontWeight.SemiBold, fontFamily = FontFamily.Monospace)
                )
            }
        }
    }
}
