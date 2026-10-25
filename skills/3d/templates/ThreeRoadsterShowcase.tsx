import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

interface ColorVariant {
  name: string;
  hex: string;
}

const COLOR_VARIANTS: ColorVariant[] = [
  { name: "Carmine Red", hex: "#d00000" },
  { name: "Obsidian Black", hex: "#111111" },
  { name: "Pearl White", hex: "#f8f9fa" },
  { name: "Pacific Blue", hex: "#0077b6" },
];

export const ThreeRoadsterShowcase: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [activeColor, setActiveColor] = useState<string>(COLOR_VARIANTS[0].hex);
  const bodyMaterialRef = useRef<THREE.MeshPhysicalMaterial | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight || 500;

    // 1. Scene, Camera & Renderer
    const scene = new THREE.Scene();
    scene.background = new THREE.Color("#09090b"); // zinc-950

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(4, 2, 5);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: "high-performance" });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2.0)); // DPR Clamping
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;
    container.appendChild(renderer.domElement);

    // 2. Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.05; // Prevent camera dipping below ground
    controls.minDistance = 3;
    controls.maxDistance = 10;

    // 3. Studio Lighting Rig
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 1.8);
    keyLight.position.set(5, 8, 4);
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0x90e0ef, 0.8);
    fillLight.position.set(-5, 4, -3);
    scene.add(fillLight);

    // 4. Ground Contact Grid / Shadow Plane
    const groundGeo = new THREE.PlaneGeometry(20, 20);
    const groundMat = new THREE.MeshStandardMaterial({ color: "#0c0a09", roughness: 0.8, metalness: 0.2 });
    const groundMesh = new THREE.Mesh(groundGeo, groundMat);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.position.y = -0.01;
    scene.add(groundMesh);

    // 5. Roadster Vehicle Form (Stylized PBR Mesh)
    const carGroup = new THREE.Group();

    // Bodywork with PBR Clearcoat
    const bodyGeo = new THREE.BoxGeometry(3.6, 0.7, 1.6);
    const bodyMat = new THREE.MeshPhysicalMaterial({
      color: new THREE.Color(activeColor),
      metalness: 0.85,
      roughness: 0.15,
      clearcoat: 1.0,
      clearcoatRoughness: 0.04,
      reflectivity: 0.9,
    });
    bodyMaterialRef.current = bodyMat;

    const bodyMesh = new THREE.Mesh(bodyGeo, bodyMat);
    bodyMesh.position.y = 0.6;
    carGroup.add(bodyMesh);

    // Cabin / Windshield
    const cabinGeo = new THREE.CylinderGeometry(0.6, 0.9, 1.4, 4);
    cabinGeo.rotateY(Math.PI / 4);
    const glassMat = new THREE.MeshPhysicalMaterial({
      color: 0x111111,
      metalness: 0.1,
      roughness: 0.1,
      transmission: 0.8,
      transparent: true,
      opacity: 0.9,
    });
    const cabinMesh = new THREE.Mesh(cabinGeo, glassMat);
    cabinMesh.position.set(-0.2, 1.15, 0);
    carGroup.add(cabinMesh);

    scene.add(carGroup);

    // 6. Animation Loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // 7. Responsive Resizing
    const handleResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight || 500;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", handleResize);

    // 8. Lifecycle Memory Cleanup
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", handleResize);
      controls.dispose();
      scene.traverse((obj) => {
        if (obj instanceof THREE.Mesh) {
          obj.geometry.dispose();
          if (Array.isArray(obj.material)) {
            obj.material.forEach((m) => m.dispose());
          } else {
            obj.material.dispose();
          }
        }
      });
      renderer.dispose();
      if (renderer.domElement.parentNode) {
        renderer.domElement.parentNode.removeChild(renderer.domElement);
      }
    };
  }, []);

  // Update paint color dynamically
  const handleColorChange = (hex: string) => {
    setActiveColor(hex);
    if (bodyMaterialRef.current) {
      bodyMaterialRef.current.color.set(hex);
    }
  };

  return (
    <div className="relative w-full h-[550px] bg-zinc-950 rounded-xl overflow-hidden border border-zinc-800">
      <div ref={containerRef} className="w-full h-full" />
      
      {/* UI Control Overlay */}
      <div className="absolute bottom-6 left-6 right-6 flex items-center justify-between p-4 bg-zinc-900/80 backdrop-blur-md rounded-lg border border-zinc-700/60 shadow-lg">
        <div>
          <h3 className="text-sm font-semibold text-zinc-100">Roadster PBR Showcase</h3>
          <p className="text-xs text-zinc-400">Interactive WebGL clearcoat shader</p>
        </div>
        <div className="flex gap-2">
          {COLOR_VARIANTS.map((c) => (
            <button
              key={c.name}
              type="button"
              onClick={() => handleColorChange(c.hex)}
              aria-label={c.name}
              className={`w-6 h-6 rounded-full border-2 transition-transform ${
                activeColor === c.hex ? "scale-125 border-zinc-100 shadow-md" : "border-zinc-700 opacity-80 hover:opacity-100"
              }`}
              style={{ backgroundColor: c.hex }}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
