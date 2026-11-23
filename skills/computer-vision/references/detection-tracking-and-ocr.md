# Detection Letterboxing, Multi-Object Tracking & OCR Hygiene

> **Objective**: Prevent aspect-ratio distortion, bounding-box coordinate drift, ID-switching storms, and unreadable OCR inputs.

---

## 1. Aspect-Preserving Letterbox & Un-Scaling

Never warp a `1920x1080` frame directly to `640x640`—squashing aspect ratios degrades small-object recall and skews box geometry. Pad symmetrically with `(114, 114, 114)` and invert the exact scale + padding offsets when emitting boxes:

```python
def letterbox_coords_to_orig(
    xyxy: tuple[float, float, float, float],
    scale: float,
    pad_x: float,
    pad_y: float,
    orig_w: int,
    orig_h: int,
) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = xyxy
    x1 = max(0, min(orig_w, round((x1 - pad_x) / scale)))
    y1 = max(0, min(orig_h, round((y1 - pad_y) / scale)))
    x2 = max(0, min(orig_w, round((x2 - pad_x) / scale)))
    y2 = max(0, min(orig_h, round((y2 - pad_y) / scale)))
    return x1, y1, x2, y2
```

---

## 2. Calibration, NMS & Tracking Stability

| Stage | Failure Mode | Production Fix |
| :--- | :--- | :--- |
| **EXIF Orientation** | Mobile JPEGs rotated 90/270 deg silently | Run `ImageOps.exif_transpose(img)` before `np.asarray(img)` or resizing. |
| **NMS / Confidence** | Duplicate overlapping boxes or spam alerts | Set class-calibrated `conf >= 0.35`, `iou = 0.45`, and cap `max_det <= 100`. |
| **Tracking (ByteTrack / OC-SORT)** | Track ID resets on brief 3-frame occlusion | Set `track_buffer = 30` (`~1s` at 30fps) and keep `match_thresh = 0.8` with low-score second-stage association. |
| **SAM2 Segmentation** | Running full-grid point prompts every frame | Trigger SAM2 only on detector ROI boxes or user clicks; propagate memory bank across keyframes. |

---

## 3. Document & Scene OCR Pre-Processing

1. **Crop First**: Detect document/plate/label ROI with a fast lightweight detector (`YOLO-nano` or contour quad) before invoking PaddleOCR/DocTR.
2. **Contrast & Deskew**: Apply affine perspective warp on 4-point quads and ensure minimum `32px` cap height on text lines; avoid heavy Gaussian blur that erodes thin glyphs.
3. **Structured Parsing**: Validate extracted OCR fields with regex + checksum/Pydantic schema before passing downstream or escalating low-confidence crops (`< 0.80`) to `/vlm-multimodal`.
