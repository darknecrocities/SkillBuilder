# Mathematical Easing Curves & Kinetic Camera Motion

Precise mathematical formulations for motion curves used across programmatic animation.

---

## 1. Snap Easing (`cubic-bezier(.7, 0, .2, 1)`)

High-velocity initial launch with sharp deceleration and zero overshoot:

```python
import math

def ease_snap(u: float) -> float:
    """Awesome Claude cubic-bezier(.7, 0, .2, 1) snap curve approximation."""
    u = max(0.0, min(1.0, u))
    return 1.0 - math.pow(1.0 - u, 4.0) if u > 0.5 else 4.0 * math.pow(u, 3.0)
```

## 2. Quintic Smoothstep (`6u^5 - 15u^4 + 10u^3`)

$C^2$-continuous curve guaranteeing zero acceleration discontinuities at start and finish:

```python
def ease_quintic(u: float) -> float:
    """Continuous quintic smoothstep curve."""
    u = max(0.0, min(1.0, u))
    return u * u * u * (u * (u * 6.0 - 15.0) + 10.0)
```

## 3. Long-Tail Deceleration (`cubic-bezier(.16, 1, .3, 1)`)

Used for rolling metric counters and giant numbers:

```python
def ease_longtail(u: float) -> float:
    """Long-tail slow settle curve for counters."""
    u = max(0.0, min(1.0, u))
    return 1.0 - math.pow(1.0 - u, 3.5)
```

## 4. 3D Split-Flap Perspective Flip

Simulates a physical mechanical card or flipboard rotating around the X-axis:

$$\text{scale\_y}(p) = \sin\left(p \cdot \frac{\pi}{2}\right) \quad \text{for } p \in [0.0, 1.0]$$

```python
from PIL import Image, ImageDraw, ImageFont

def render_3d_flip(text: str, font: ImageFont.FreeTypeFont, progress: float,
                   color=(255, 255, 255, 255)) -> Image.Image:
    """Render a text token vertically squashed by 3D perspective rotation."""
    p = max(0.0, min(1.0, progress))
    scale_y = math.sin(p * math.pi * 0.5)

    # Render base text on sub-canvas
    bbox = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0] + 16, bbox[3] - bbox[1] + 16
    base = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(base).text((tw // 2, th // 2), text, font=font, fill=color, anchor="mm")

    # Squash vertically along horizontal hinge
    new_h = max(2, int(th * scale_y))
    return base.resize((tw, new_h), Image.BILINEAR)
```

## 5. Continuous Harmonic Camera Drift

Prevents static, frozen camera positioning:

$$\Delta x(t) = A_x \sin(\omega_x t), \quad \Delta y(t) = A_y \cos(\omega_y t)$$

Recommended parameters for 1080p:
$$A_x = 6.0\text{px}, \quad \omega_x = 1.25\text{ rad/s}, \quad A_y = 3.8\text{px}, \quad \omega_y = 0.95\text{ rad/s}$$
