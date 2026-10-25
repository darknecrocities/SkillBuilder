import 'dart:math' as math;
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter/physics.dart';
import 'package:flutter/services.dart';

/// IndustrialTactileEncoder
///
/// Production Flutter Mobile Rotary Hardware Encoder inspired by Teenage Engineering.
/// Features physics spring simulations (AnimationController.unbounded),
/// physical detent haptics (HapticFeedback.selectionClick()), CustomPainter dial gauge,
/// and live waveform rendering optimized for Impeller 120Hz GPU pipelines.
class IndustrialTactileEncoder extends StatefulWidget {
  final String label;
  final double min;
  final double max;
  final double defaultValue;
  final String unit;
  final ValueChanged<double>? onValueChanged;

  const IndustrialTactileEncoder({
    super.key,
    this.label = 'FILTER FREQUENCY',
    this.min = 20.0,
    this.max = 20000.0,
    this.defaultValue = 1250.0,
    this.unit = 'Hz',
    this.onValueChanged,
  });

  @override
  State<IndustrialTactileEncoder> createState() => _IndustrialTactileEncoderState();
}

class _IndustrialTactileEncoderState extends State<IndustrialTactileEncoder>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late double _currentValue;
  double _lastHapticAngle = 0.0;
  bool _isBypassed = false;

  static const double _maxAngle = 2.443;
  static const double _minAngle = -2.443;
  static const double _detentStep = 0.1745; // 10 degrees per detent

  @override
  void initState() {
    super.initState();
    _currentValue = widget.defaultValue;
    final initialAngle = _mapValueToAngle(widget.defaultValue);
    _lastHapticAngle = initialAngle;
    _controller = AnimationController.unbounded(value: initialAngle, vsync: this)
      ..addListener(_onControllerTick);
  }

  @override
  void dispose() {
    _controller.removeListener(_onControllerTick);
    _controller.dispose();
    super.dispose();
  }

  double _mapValueToAngle(double value) {
    final norm = (math.log(value) - math.log(widget.min)) /
        (math.log(widget.max) - math.log(widget.min));
    return _minAngle + norm.clamp(0.0, 1.0) * (_maxAngle - _minAngle);
  }

  double _mapAngleToValue(double angle) {
    final norm = (angle - _minAngle) / (_maxAngle - _minAngle);
    return widget.min * math.pow(widget.max / widget.min, norm.clamp(0.0, 1.0));
  }

  void _onControllerTick() {
    final angle = _controller.value;
    final val = _mapAngleToValue(angle);
    if ((val - _currentValue).abs() > 1.0) {
      setState(() => _currentValue = val);
      widget.onValueChanged?.(val);
    }
    if ((angle - _lastHapticAngle).abs() >= _detentStep) {
      HapticFeedback.selectionClick();
      _lastHapticAngle = angle;
    }
  }

  void _onPanUpdate(DragUpdateDetails details) {
    _controller.value =
        (_controller.value - details.delta.dy * 0.015).clamp(_minAngle, _maxAngle);
  }

  void _onPanEnd(DragEndDetails details) {
    final currentAngle = _controller.value;
    final nearestDetent = (currentAngle / _detentStep).round() * _detentStep;
    final targetAngle = nearestDetent.clamp(_minAngle, _maxAngle);
    final velocity = -details.velocity.pixelsPerSecond.dy * 0.015;

    const spring = SpringDescription(mass: 1.0, stiffness: 340.0, damping: 28.0);
    _controller.animateWith(
        SpringSimulation(spring, currentAngle, targetAngle, velocity));
  }

  void _resetToDefault() {
    final targetAngle = _mapValueToAngle(widget.defaultValue);
    const spring = SpringDescription(mass: 1.0, stiffness: 300.0, damping: 24.0);
    _controller.animateWith(
        SpringSimulation(spring, _controller.value, targetAngle, 0.0));
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 320,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: const Color(0xFF09090B),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFF27272A)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                widget.label,
                style: const TextStyle(
                  color: Color(0xFFA1A1AA),
                  fontSize: 11,
                  fontWeight: FontWeight.w600,
                  letterSpacing: 1.2,
                  fontFamily: 'Courier',
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: const Color(0xFF18181B),
                  borderRadius: BorderRadius.circular(4),
                  border: Border.all(color: const Color(0xFF27272A)),
                ),
                child: Text(
                  _isBypassed ? 'BYPASS' : 'ACTIVE',
                  style: TextStyle(
                    color: _isBypassed ? const Color(0xFFA1A1AA) : const Color(0xFF34D399),
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    fontFamily: 'Courier',
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Container(
            height: 48,
            decoration: BoxDecoration(
              color: const Color(0xFF18181B),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: const Color(0xFF27272A)),
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: CustomPaint(
                painter: _WaveformPainter(
                  frequency: _currentValue / widget.max,
                  isBypassed: _isBypassed,
                ),
              ),
            ),
          ),
          const SizedBox(height: 16),
          GestureDetector(
            onPanUpdate: _onPanUpdate,
            onPanEnd: _onPanEnd,
            child: Center(
              child: SizedBox(
                width: 170,
                height: 170,
                child: AnimatedBuilder(
                  animation: _controller,
                  builder: (context, child) => CustomPaint(
                    painter: _EncoderDialPainter(
                      angle: _controller.value,
                      minAngle: _minAngle,
                      maxAngle: _maxAngle,
                    ),
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(height: 12),
          Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.baseline,
                textBaseline: TextBaseline.alphabetic,
                children: [
                  Text(
                    _currentValue.toStringAsFixed(0),
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 30,
                      fontWeight: FontWeight.w700,
                      fontFamily: 'Courier',
                      fontFeatures: [
                        FontFeature.tabularFigures(),
                        FontFeature.slashedZero(),
                      ],
                    ),
                  ),
                  const SizedBox(width: 4),
                  Text(
                    widget.unit,
                    style: const TextStyle(
                      color: Color(0xFFF59E0B),
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                      fontFamily: 'Courier',
                    ),
                  ),
                ],
              ),
              const Text(
                'TACTILE ROTARY ENCODER',
                style: TextStyle(
                  color: Color(0xFF71717A),
                  fontSize: 9,
                  letterSpacing: 1.0,
                  fontFamily: 'Courier',
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          Row(
            children: [
              Expanded(
                child: _buildButton(
                  label: _isBypassed ? 'ENGAGE' : 'BYPASS',
                  isActive: _isBypassed,
                  onTap: () {
                    HapticFeedback.lightImpact();
                    setState(() => _isBypassed = !_isBypassed);
                  },
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _buildButton(
                  label: 'RESET',
                  isActive: false,
                  onTap: () {
                    HapticFeedback.lightImpact();
                    _resetToDefault();
                  },
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildButton({
    required String label,
    required bool isActive,
    required VoidCallback onTap,
  }) {
    return OutlinedButton(
      onPressed: onTap,
      style: OutlinedButton.styleFrom(
        backgroundColor:
            isActive ? const Color(0x33F59E0B) : const Color(0xFF18181B),
        side: const BorderSide(color: Color(0xFF27272A)),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
      ),
      child: Text(
        label,
        style: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w600,
          color: isActive ? const Color(0xFFF59E0B) : const Color(0xFFA1A1AA),
          fontFamily: 'Courier',
        ),
      ),
    );
  }
}

class _WaveformPainter extends CustomPainter {
  final double frequency;
  final bool isBypassed;

  _WaveformPainter({required this.frequency, required this.isBypassed});

  @override
  void paint(Canvas canvas, Size size) {
    final gridPaint = Paint()
      ..color = const Color(0xFF27272A)
      ..strokeWidth = 1.0;
    canvas.drawLine(
        Offset(0, size.height / 2), Offset(size.width, size.height / 2), gridPaint);

    final wavePaint = Paint()
      ..color = isBypassed ? const Color(0xFF71717A) : const Color(0xFFF59E0B)
      ..strokeWidth = 1.8
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    final path = Path();
    const points = 60;
    final amp = isBypassed ? 0.0 : size.height * 0.35;
    final freqFactor = frequency * 14.0 + 1.0;

    for (int i = 0; i <= points; i++) {
      final x = (i / points) * size.width;
      final y = size.height / 2 +
          math.sin((i / points) * math.pi * freqFactor) * amp;
      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    canvas.drawPath(path, wavePaint);
  }

  @override
  bool shouldRepaint(covariant _WaveformPainter oldDelegate) =>
      oldDelegate.frequency != frequency || oldDelegate.isBypassed != isBypassed;
}

class _EncoderDialPainter extends CustomPainter {
  final double angle;
  final double minAngle;
  final double maxAngle;

  _EncoderDialPainter({
    required this.angle,
    required this.minAngle,
    required this.maxAngle,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final outerRadius = size.width / 2;
    final knobRadius = outerRadius * 0.65;

    final tickPaint = Paint()..strokeCap = StrokeCap.round;
    const totalTicks = 29;
    final step = (maxAngle - minAngle) / (totalTicks - 1);

    for (int i = 0; i < totalTicks; i++) {
      final tickAngle = minAngle + i * step - math.pi / 2;
      final isMajor = i % 4 == 0;
      final r1 = outerRadius - 4;
      final r2 = isMajor ? outerRadius - 14 : outerRadius - 9;

      tickPaint
        ..color = isMajor ? const Color(0xFFA1A1AA) : const Color(0xFF3F3F46)
        ..strokeWidth = isMajor ? 1.5 : 1.0;

      canvas.drawLine(
        Offset(center.dx + r1 * math.cos(tickAngle),
            center.dy + r1 * math.sin(tickAngle)),
        Offset(center.dx + r2 * math.cos(tickAngle),
            center.dy + r2 * math.sin(tickAngle)),
        tickPaint,
      );
    }

    final knobPaint = Paint()
      ..shader = const RadialGradient(
        colors: [Color(0xFF27272A), Color(0xFF09090B)],
      ).createShader(Rect.fromCircle(center: center, radius: knobRadius));
    canvas.drawCircle(center, knobRadius, knobPaint);

    final borderPaint = Paint()
      ..color = const Color(0xFF3F3F46)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.5;
    canvas.drawCircle(center, knobRadius, borderPaint);

    canvas.save();
    canvas.translate(center.dx, center.dy);
    canvas.rotate(angle);

    final needlePaint = Paint()
      ..color = const Color(0xFFF59E0B)
      ..strokeCap = StrokeCap.round
      ..strokeWidth = 3.0;

    canvas.drawLine(
      Offset(0, -knobRadius + 6),
      Offset(0, -knobRadius + 20),
      needlePaint,
    );
    canvas.restore();
  }

  @override
  bool shouldRepaint(covariant _EncoderDialPainter oldDelegate) =>
      oldDelegate.angle != angle;
}
