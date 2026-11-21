# Three.js Performance Optimization & 60fps/120fps Budgets

> **Objective**: Guarantee sustained 60fps (`<= 16.6ms` frame budget) or 120fps ProMotion (`<= 8.33ms`) across desktop and mobile WebGL viewports without thermal throttling or VRAM leaks.

---

## 1. Frame & Draw-Call Budgets

| Tier | Frame Budget | Max Draw Calls | Max Triangles | DPR Clamp |
| :--- | :--- | :--- | :--- | :--- |
| **ProMotion 120Hz** | `8.33 ms` | `<= 50` calls | `<= 100k` tris | `Math.min(dpr, 2.0)` |
| **Standard 60Hz** | `16.6 ms` | `<= 100` calls | `<= 200k` tris | `Math.min(dpr, 2.0)` |
| **Mobile Fallback** | `33.3 ms` | `<= 40` calls | `<= 50k` tris | `Math.min(dpr, 1.5)` |

---

## 2. Critical WebGL Optimization Patterns

1. **Zero Per-Frame Heap Allocations (`useFrame` / `tick`)**:
   Never call `new THREE.Vector3()`, `new THREE.Matrix4()`, or `new THREE.Color()` inside the render loop — GC pauses stutter animations. Pre-allocate scratch vectors outside `tick()` and mutate in-place.
2. **Geometry Instancing (`InstancedMesh`)**:
   Merge repeated props (bolts, grid ticks, particles, forest trees) into a single `THREE.InstancedMesh` so 1,000 objects render in **1 draw call**.
3. **Contact Shadows Over Dynamic Shadow Cascades**:
   Dynamic multi-cascade shadow maps kill mobile fill-rate. Use baked `ContactShadows` or a soft radial ground texture for stationary product plinths.
4. **Pause Off-Screen Canvases**:
   Combine `IntersectionObserver` + `document.visibilityState` to suspend `requestAnimationFrame` when the 3D showcase scrolls out of view or the tab backgrounds.

---

## 3. Deterministic VRAM Disposal & Context Loss Recovery

```typescript
export function disposeSceneResources(scene: THREE.Scene, renderer: THREE.WebGLRenderer) {
  scene.traverse((obj) => {
    if (obj instanceof THREE.Mesh) {
      obj.geometry?.dispose();
      const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
      for (const mat of mats) {
        if (!mat) continue;
        Object.values(mat).forEach((val) => {
          if (val && typeof (val as THREE.Texture).dispose === "function") {
            (val as THREE.Texture).dispose();
          }
        });
        mat.dispose();
      }
    }
  });
  renderer.dispose();
}
```
Always attach a `webglcontextlost` listener (`e.preventDefault()`) so mobile tab backgrounding recovers cleanly.
