# Three.js Performance Optimization & 60fps Budgets

WebGL rendering loops must maintain a strict 60fps (16.6ms frame budget) or 120fps (8.33ms on ProMotion displays).

---

## 1. Frame Budget Breakdown

Budget Target | Frame Time | Permissible Draw Calls | Geometry Limits
:--- | :--- | :--- | :---
Standard 60fps | 16.6ms | $\le 100$ calls | $\le 200\text{k}$ triangles
ProMotion 120fps | 8.33ms | $\le 50$ calls | $\le 100\text{k}$ triangles
Low-Tier Mobile | 30fps fallback | $\le 40$ calls | $\le 50\text{k}$ triangles

---

## 2. Essential Optimization Patterns

1. **Geometry Instancing (`InstancedMesh`)**:
   Instead of creating 1,000 distinct `Mesh` objects with individual draw calls, use a single `THREE.InstancedMesh`.
2. **Frustum Culling**:
   Ensure `mesh.frustumCulled = true` (default). Do not disable frustum culling unless vertex shaders deform bounds.
3. **Texture Sizing & Power of Two**:
   Use power-of-two dimensions (512x512, 1024x1024, 2048x2048) and generate mipmaps automatically (`texture.generateMipmaps = true`).
4. **Disposal Lifecycle**:
   Always dispose unused geometries, textures, and materials when unmounting components to avoid VRAM memory leaks:
   ```javascript
   geometry.dispose();
   material.dispose();
   texture.dispose();
   ```
