# Physically-Based Rendering (PBR) & Draco Compression

Production 3D assets require physically plausible light transport and compressed delivery pipelines.

---

## 1. PBR Material Setup (`MeshStandardMaterial` / `MeshPhysicalMaterial`)

Parameter | Recommended Range | Purpose
:--- | :--- | :---
`roughness` | `0.1` (glossy) to `0.9` (diffuse) | Microfacet distribution
`metalness` | `0.0` (dielectric) or `1.0` (pure conductor) | Fresnel reflectivity behavior
`envMapIntensity` | `1.0` to `1.5` | Studio HDR ambient reflection strength
`clearcoat` | `0.0` to `1.0` | Secondary specular layer (automotive / glass)

---

## 2. Draco Geometry Compression

Draco drastically compresses glTF buffer data (up to 85% bandwidth reduction):

```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader';

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('/draco/');

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);
```

### Guidelines:
- Place web assembly decoders in public static assets (`/draco/`).
- Defer loading until after initial page render to preserve Core Web Vitals (LCP).
