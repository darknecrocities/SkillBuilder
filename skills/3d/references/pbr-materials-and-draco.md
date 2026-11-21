# Physically-Based Rendering (PBR), KTX2 Textures & Draco Compression

> **Objective**: Achieve physical studio lighting realism with minimal asset download weight (`< 5 MB` `.glb` payload) and instant GPU upload.

---

## 1. Physically Based Material Calibration (`MeshPhysicalMaterial`)

| Material Surface | `metalness` | `roughness` | `clearcoat` | `clearcoatRoughness` |
| :--- | :--- | :--- | :--- | :--- |
| **Automotive Clearcoat Paint** | `0.85` | `0.15` | `1.0` | `0.05` |
| **Bead-Blasted Anodized Aluminum** | `0.90` | `0.38` | `0.0` | `—` |
| **Matte Elastomer / Carbon Trim** | `0.0` | `0.78` | `0.0` | `—` |
| **Optical Glass / Acrylic** | `0.0` | `0.05` | `1.0` | `0.02` (`transmission: 0.9`) |

- **3-Point Studio Lighting + HDRI**: Combine a subtle studio `.hdr` environment map (`envMapIntensity: 1.2`) with a warm Key directional light, cool Fill light, and crisp Rim backlight separating dark silhouettes from `#09090b` canvases.

---

## 2. Draco Geometry & KTX2 Basis Texture Pipeline

1. **Draco Mesh Compression**: Cuts `.glb` vertex/index payload by `70–85%`. Host WASM decoders locally (`/draco/`) or pinned CDN and instantiate `DRACOLoader` once as a singleton.
2. **KTX2 / Basis Universal Textures**: Unlike PNG/JPG (which decompress to huge uncompressed RGBA bitmaps in GPU VRAM), `.ktx2` stays GPU-compressed (`BC7`/`ASTC`/`ETC2`), cutting VRAM footprint by `4–6x`.
3. **Power-of-Two Dimensions & Mipmaps**: Keep textures at `512x512` or `1024x1024` (max `2048x2048` for hero albedo) with `anisotropy <= 4`.

```typescript
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath("/draco/");
const ktx2Loader = new KTX2Loader().setTranscoderPath("/basis/").detectSupport(renderer);

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);
gltfLoader.setKTX2Loader(ktx2Loader);
```
