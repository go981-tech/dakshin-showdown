import { Group } from "three";

export function disposeObject3D(root) {
  if (!root) return;
  const geometries = new Set();
  const materials = new Set();
  const textures = new Set();
  root.traverse((object) => {
    if (object.geometry && !geometries.has(object.geometry)) {
      geometries.add(object.geometry);
      object.geometry.dispose();
    }
    const list = Array.isArray(object.material) ? object.material : [object.material];
    for (const material of list) {
      if (!material || materials.has(material)) continue;
      materials.add(material);
      for (const value of Object.values(material)) {
        if (value?.isTexture && !textures.has(value)) {
          textures.add(value);
          value.dispose();
        }
      }
      material.dispose();
    }
  });
}

export function spawnTransientFx(battle, duration, setup, animate) {
  const scene = battle?.ctx?.arena?.group || battle?.ctx?.scene;
  if (!scene) return null;
  const root = new Group();
  const dir = setup?.attacker?.facing || 1;
  const ax = setup?.attacker?.x || 0;
  const ay = (setup?.attacker?.y || 0) + 1.05;
  const tx = setup?.target?.x ?? ax + dir * 1.4;
  const ty = setup?.target ? (setup.target.y || 0) + 1.05 : ay;
  scene.add(root);
  if (setup?.create) setup.create(root, { dir, ax, ay, tx, ty });
  const started = performance.now();
  const step = () => {
    const p = Math.max(0, Math.min(1, (performance.now() - started) / Math.max(1, duration)));
    animate?.(root, p, { dir, ax, ay, tx, ty });
    if (p < 1) requestAnimationFrame(step);
    else {
      scene.remove(root);
      disposeObject3D(root);
    }
  };
  requestAnimationFrame(step);
  return root;
}
