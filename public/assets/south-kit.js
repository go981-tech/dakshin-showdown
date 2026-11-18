import {
  BoxGeometry,
  CylinderGeometry,
  SphereGeometry,
  ConeGeometry,
  PlaneGeometry,
  TorusGeometry,
  RingGeometry,
  PointLight,
  InstancedMesh,
  Group,
  Mesh,
  SkinnedMesh,
  Skeleton,
  MeshStandardMaterial,
  MeshBasicMaterial,
  Vector3,
  Color,
  CanvasTexture,
  SRGBColorSpace,
  TextureLoader,
  PMREMGenerator,
  Matrix4,
  Euler,
  Quaternion,
  QuaternionKeyframeTrack,
  VectorKeyframeTrack,
  DoubleSide
} from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { DRACOLoader } from "three/addons/loaders/DRACOLoader.js";
import { ROSTER_3D_BY_ENGINE_ID, TAMIL_ROSTER_3D, CHARACTER_GLB_MAP, DEFAULT_FRAMES, DEFAULT_FRAME_DATA } from "./RosterConfig3D.js";
import { Fighter3D, STATES, FightKaroTamil3D } from "./GameEngine3D.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { clone as skeletonClone } from "three/addons/utils/SkeletonUtils.js";

const TEX_VER = "20261126";
const GLB_IDS = ["modi", "rahul", "didi", "yogi", "trump", "nitin", "ravi", "lalu", "mbapu", "amit", "dhruv", "nirmala", "rangaraj"];
const ANIM_DONOR_MAP = { nirmala: "didi", rangaraj: "amit" };
const VESHTI_IDS = new Set(["modi", "yogi", "lalu", "mbapu", "amit", "ravi"]);
const KURTA_IDS = new Set(); // Native OutfitTop on RPM rigs avoids donor sleeve tears & jagged cuffs
const SHAWL_IDS = new Set(["modi", "rahul", "yogi", "ravi", "lalu", "mbapu", "amit"]);
const SHADES_IDS = new Set(["rahul", "trump", "ravi", "amit"]);

function mat(color, roughness = 0.72, metalness = 0.06, extra = {}) {
  return new MeshStandardMaterial({ color, roughness, metalness, ...extra });
}

function addBox(parent, w, h, d, material, x = 0, y = 0, z = 0) {
  const m = new Mesh(new BoxGeometry(w, h, d), material);
  m.position.set(x, y, z);
  m.castShadow = true;
  m.receiveShadow = true;
  parent.add(m);
  return m;
}

function addCyl(parent, rt, rb, h, seg, material, x = 0, y = 0, z = 0) {
  const m = new Mesh(new CylinderGeometry(rt, rb, h, seg), material);
  m.position.set(x, y, z);
  m.castShadow = true;
  m.receiveShadow = true;
  parent.add(m);
  return m;
}

function stripIdx(name) {
  return String(name || "").replace(/_\d+$/, "");
}

function normalizeSceneNames(scene) {
  scene.traverse((o) => {
    if (o.name) o.name = stripIdx(o.name);
  });
}

function findNode(root, bareName) {
  let found = null;
  root.traverse((o) => {
    if (!found && stripIdx(o.name) === bareName) found = o;
  });
  return found;
}

function normalizeClipTracks(clips, hipsScale = 1) {
  const out = [];
  for (const clip of clips || []) {
    const c = clip.clone();
    c.tracks = c.tracks
      .filter((tr) => !/Head(?!Top)[^.]*\.scale$/.test(stripIdx(tr.name.split(".")[0])))
      .map((tr) => {
        const cloned = tr.clone();
        cloned.name = cloned.name.replace(/_\d+\./, ".");
        if (hipsScale !== 1 && /^Hips\.position$/.test(cloned.name)) {
          for (let i = 0; i < cloned.values.length; i++) {
            cloned.values[i] *= hipsScale;
          }
        }
        return cloned;
      });
    out.push(c);
  }
  return out;
}

async function loadSharedTex(loader, url) {
  const tex = await loader.loadAsync(url);
  tex.flipY = false;
  tex.colorSpace = SRGBColorSpace;
  tex.userData.shared = true;
  tex.needsUpdate = true;
  return tex;
}

function bindMeshFromDonor(targetScene, donorScene, meshName, matName) {
  const donorMesh = findNode(donorScene, meshName);
  const bodyMesh = findNode(targetScene, "Body");
  if (!donorMesh || !donorMesh.isSkinnedMesh || !bodyMesh || !bodyMesh.parent) return null;

  const boneMap = new Map();
  targetScene.traverse((o) => {
    if (o.isBone) boneMap.set(stripIdx(o.name), o);
  });

  const srcMat = Array.isArray(donorMesh.material) ? donorMesh.material[0] : donorMesh.material;
  const clonedMat = srcMat.clone();
  clonedMat.name = matName;

  targetScene.updateMatrixWorld(true);
  donorScene.updateMatrixWorld(true);
  const srcHipsY = findNode(donorScene, "Hips")?.getWorldPosition(new Vector3()).y ?? 0.941;
  const tgtHipsY = findNode(targetScene, "Hips")?.getWorldPosition(new Vector3()).y ?? 0.941;
  const hipsDeltaY = tgtHipsY - srcHipsY;

  const geo = donorMesh.geometry.clone();
  // Translate Shawl/Dhoti vertically if target Hips height differs (e.g. modi vs yogi -1cm) so rest skinning matches
  if (Math.abs(hipsDeltaY) > 1e-4 && meshName === "Shawl") {
    const p = geo.attributes.position;
    for (let i = 0; i < p.count; i++) p.setY(i, p.getY(i) + hipsDeltaY);
    p.needsUpdate = true;
  }

  const cloned = new SkinnedMesh(geo, clonedMat);
  cloned.name = meshName;
  cloned.castShadow = true;
  cloned.receiveShadow = true;
  cloned.frustumCulled = false;

  const mappedBones = donorMesh.skeleton.bones.map((b) => boneMap.get(stripIdx(b.name)) || b);
  bodyMesh.parent.add(cloned);
  targetScene.updateMatrixWorld(true);
  // Compute bind inverses in targetScene's OWN rest pose so vertices stay 100% locked without donor offset!
  const rootMat = cloned.matrixWorld;
  const inverses = mappedBones.map((b) => {
    b.updateMatrixWorld(true);
    return new Matrix4().multiplyMatrices(b.matrixWorld, new Matrix4().copy(rootMat).invert()).invert();
  });
  cloned.bind(new Skeleton(mappedBones, inverses), cloned.matrixWorld.clone());
  return cloned;
}

const SCULPT_PROFILES = {
  modi:  { jawW: 0.035, cheekW: 0.03, browZ: 0.03, crownY: 0.00, muscle: 1.08 },
  rahul: { jawW: -0.02, cheekW: 0.015, browZ: 0.04, crownY: 0.02, muscle: 1.14 },
  didi:  { jawW: 0.02, cheekW: 0.02, browZ: 0.01, crownY: 0.00, muscle: 1.00 },
  trump: { jawW: 0.025, cheekW: 0.025, browZ: 0.04, crownY: 0.03, muscle: 1.18 },
  yogi:  { jawW: 0.035, cheekW: 0.03, browZ: 0.03, crownY: 0.01, muscle: 1.08 },
  nitin: { jawW: 0.04, cheekW: 0.035, browZ: 0.03, crownY: 0.01, muscle: 1.12 },
  ravi:  { jawW: 0.02, cheekW: 0.02, browZ: 0.04, crownY: 0.02, muscle: 1.14 },
  lalu:  { jawW: 0.03, cheekW: 0.03, browZ: 0.03, crownY: 0.02, muscle: 1.12 },
  mbapu: { jawW: 0.025, cheekW: 0.02, browZ: 0.025, crownY: 0.00, muscle: 1.00 },
  amit:  { jawW: 0.035, cheekW: 0.03, browZ: 0.04, crownY: 0.02, muscle: 1.15 },
  dhruv: { jawW: -0.015, cheekW: 0.015, browZ: 0.03, crownY: 0.025, muscle: 1.08 }
};

function smoothstep01(a, b, x) {
  const t = Math.max(0, Math.min(1, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
}

function sculptHeadGeometry(mesh, prof) {
  if (!mesh || !mesh.geometry) return;
  mesh.geometry = mesh.geometry.clone();
  const pos = mesh.geometry.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    let x = pos.getX(i);
    let y = pos.getY(i);
    let z = pos.getZ(i);

    // Protect eye socket rim vertices (keep eyeballs aligned & clean!)
    const nearEyeSocket = Math.abs(x) > 0.012 && Math.abs(x) < 0.056 && y > 1.65 && y < 1.715 && z > 0.065;
    if (nearEyeSocket) continue;

    // Jaw width & squareness (lower face)
    const jawW = (1.0 - smoothstep01(1.50, 1.63, y)) * smoothstep01(1.47, 1.54, y) * (z > -0.02 ? 1 : 0.4);
    x *= 1 + prof.jawW * jawW;

    // Cheekbone / zygomatic breadth
    const cheekW = Math.exp(-Math.pow((y - 1.635) / 0.045, 2)) * (z > 0.02 ? 1 : 0.35);
    x *= 1 + prof.cheekW * cheekW;
    if (z > 0.05) z += prof.cheekW * 0.03 * cheekW;

    // Brow & nose ridge projection
    const browW = Math.exp(-Math.pow((y - 1.705) / 0.035, 2)) * smoothstep01(0.07, 0.115, z);
    z += prof.browZ * 0.04 * browW;

    // Hair crown volume
    if (y > 1.735) {
      const cw = smoothstep01(1.735, 1.81, y);
      y += prof.crownY * 0.18 * cw;
      x *= 1 + prof.crownY * 0.25 * cw;
    }

    pos.setXYZ(i, x, y, z);
  }
  pos.needsUpdate = true;
  mesh.geometry.computeVertexNormals();
}

function sculptBodyAndOutfitGeometry(mesh, muscle, mode = "body") {
  if (!mesh || !mesh.geometry) return;
  mesh.geometry = mesh.geometry.clone();
  const pos = mesh.geometry.attributes.position;
  const k = Math.max(0, muscle - 1.0);
  const isCloth = mode === "cloth" || mode === "shawl";

  for (let i = 0; i < pos.count; i++) {
    let x = pos.getX(i);
    let y = pos.getY(i);
    let z = pos.getZ(i);
    const ax = Math.abs(x);

    // Keep inner covered skin (chest/waist & legs under clothes/dhoti/sari) tucked cleanly inside garments!
    if (mode === "body") {
      // Torso skin covered by OutfitTop (except exposed hands |x|>0.56 and neck y>1.43)
      if (ax < 0.21 && y > 0.72 && y < 1.41) {
        x *= 0.84;
        z *= 0.82;
      }
      // Upper arms under full shirt sleeves (0.17..0.44)
      if (ax >= 0.17 && ax < 0.44 && y > 1.26 && y < 1.50) {
        const dy = y - 1.385;
        y = 1.385 + dy * 0.88;
        z *= 0.88;
      }
      // Legs covered by trousers / Dhoti / Sari (y = 0.14..0.95) -> pull cleanly inward so shoes/knees don't clip!
      if (y > 0.14 && y < 0.95 && ax < 0.22) {
        const legCenter = x >= 0 ? 0.085 : -0.085;
        x = legCenter + (x - legCenter) * 0.85;
        z *= 0.85;
      }
    }

    // Muscular forearms & wrists (shirt stays >= body under sleeves, hands stay sharp!)
    if (k > 0.005 && y > 1.24 && y < 1.53 && ax > 0.14 && ax < 0.67) {
      const armEnvelope = smoothstep01(0.14, 0.23, ax) * (1.0 - smoothstep01(0.56, 0.67, ax));
      const bicepBoost = Math.exp(-Math.pow((ax - 0.31) / 0.11, 2)) * 0.9;
      const forearmBoost = Math.exp(-Math.pow((ax - 0.51) / 0.09, 2)) * 0.8;
      const clothPad = isCloth ? 1.08 : 0.95;
      const radialGain = k * (0.42 + 0.45 * bicepBoost + 0.32 * forearmBoost) * armEnvelope * clothPad;
      const dy = y - 1.385;
      y = 1.385 + dy * (1 + radialGain);
      z *= 1 + radialGain * 1.02;
    }

    // Chest / pectorals & broad upper back (OutfitTop/Shawl expand >= body so zero shirt or shawl poke-through!)
    if (k > 0.005 && ax <= 0.24 && y > 1.14 && y < 1.51) {
      const torsoW = smoothstep01(1.14, 1.34, y) * (1.0 - smoothstep01(1.46, 1.52, y));
      const pad = mode === "shawl" ? 1.18 : mode === "cloth" ? 1.05 : 0.92;
      x *= 1 + k * 0.34 * torsoW * pad;
      z *= 1 + k * 0.42 * torsoW * pad;
      if (z > 0.02) z += k * 0.045 * torsoW * pad;
    }

    pos.setXYZ(i, x, y, z);
  }
  pos.needsUpdate = true;
  mesh.geometry.computeVertexNormals();
}

function sculptShawlOutward(mesh) {
  if (!mesh || !mesh.geometry) return;
  mesh.geometry = mesh.geometry.clone();
  mesh.geometry.computeVertexNormals();
  const pos = mesh.geometry.attributes.position;
  const nrm = mesh.geometry.attributes.normal;
  for (let i = 0; i < pos.count; i++) {
    let x = pos.getX(i);
    let y = pos.getY(i);
    let z = pos.getZ(i);
    // Push Shawl gently outward along chest/back & lift shoulder drape slightly so it sits clearly over OutfitTop
    const signZ = z >= 0 ? 1 : -1;
    const ny = y > 1.40 ? 0.012 : 0;
    const nz = Math.abs(z) > 0.02 ? signZ * 0.018 : (nrm ? nrm.getZ(i) * 0.018 : 0);
    const nx = nrm ? nrm.getX(i) * 0.012 : 0;
    pos.setXYZ(i, x + nx, y + ny, z + nz);
  }
  pos.needsUpdate = true;
  mesh.geometry.computeVertexNormals();
}

function attachBonePropWorld(scene, boneName, worldPos, buildFn) {
  const bone = findNode(scene, boneName);
  if (!bone) return;
  scene.updateMatrixWorld(true);
  const localPos = bone.worldToLocal(worldPos.clone());
  const grp = new Group();
  grp.position.copy(localPos);
  buildFn(grp);
  bone.add(grp);
}

function sculptDhotiClearance(mesh) {
  if (!mesh || !mesh.geometry) return;
  mesh.geometry = mesh.geometry.clone();
  const pos = mesh.geometry.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    let x = pos.getX(i);
    let y = pos.getY(i);
    let z = pos.getZ(i);
    if (y < 0.72) {
      const w = 1.0 - smoothstep01(0.08, 0.72, y);
      x *= 1 + 0.22 * w;
      z *= 1 + 0.26 * w;
      if (y < 0.24) y += 0.032 * (1.0 - y / 0.24);
      pos.setXYZ(i, x, y, z);
    }
  }
  pos.needsUpdate = true;
  mesh.geometry.computeVertexNormals();
}

function sculptFighter3D(scene, id) {
  const prof = SCULPT_PROFILES[id] || SCULPT_PROFILES.modi;
  scene.traverse((o) => {
    if (!o.isMesh) return;
    const n = stripIdx(o.name);
    if (n === "Head") {
      sculptHeadGeometry(o, prof);
    } else if (n === "Body") {
      sculptBodyAndOutfitGeometry(o, prof.muscle, "body");
    } else if (n === "OutfitTop" || n === "Blouse" || n === "OutfitBottom") {
      sculptBodyAndOutfitGeometry(o, prof.muscle, "cloth");
    } else if (n === "Shawl") {
      sculptShawlOutward(o);
      sculptBodyAndOutfitGeometry(o, prof.muscle, "shawl");
    } else if (n === "Dhoti") {
      sculptDhotiClearance(o);
    } else if (n === "Sari") {
      // Slightly flare lower Sari hem outward so feet/ankles stay clean
      sculptDhotiClearance(o);
    }
  });

  // Character-specific 3D sculpted props anchored flush on bones with zero floating gap
  if (id === "mbapu") {
    // Sculpted jaw-hugging layered silver-white beard tucked flush under chin (never detached cone!)
    attachBonePropWorld(scene, "Head", new Vector3(0, 1.548, 0.056), (g) => {
      const wb = mat(0xd8d8df, 0.92, 0.0, { envMapIntensity: 0.2 });
      const upper = addCyl(g, 0.044, 0.034, 0.055, 12, wb, 0, -0.008, 0.004);
      upper.scale.set(1.05, 1.0, 0.78);
      const tip = new Mesh(new SphereGeometry(0.034, 12, 10), wb);
      tip.scale.set(0.95, 1.35, 0.72);
      tip.position.set(0, -0.044, 0.002);
      g.add(tip);
      const mL = addCyl(g, 0.011, 0.005, 0.038, 8, wb, 0.020, 0.032, 0.024);
      mL.rotation.z = -1.18;
      const mR = addCyl(g, 0.011, 0.005, 0.038, 8, wb, -0.020, 0.032, 0.024);
      mR.rotation.z = 1.18;
    });
  } else if (id === "trump") {
    // Pushpa Raj signature gold chain resting naturally against chest collar
    attachBonePropWorld(scene, "Spine2", new Vector3(0, 1.430, 0.038), (g) => {
      const gold = mat(0xfacc15, 0.28, 0.85, { emissive: 0x78350f, emissiveIntensity: 0.15 });
      const chain = new Mesh(new TorusGeometry(0.092, 0.009, 8, 22), gold);
      chain.rotation.x = Math.PI / 2.35;
      g.add(chain);
    });
  } else if (id === "amit") {
    // Annamalai signature gold watch on left wrist
    attachBonePropWorld(scene, "LeftForeArm", new Vector3(0.60, 1.38, 0.005), (g) => {
      const gold = mat(0xfacc15, 0.22, 0.9);
      const band = addCyl(g, 0.046, 0.046, 0.028, 14, gold, 0, 0, 0);
      band.rotation.z = Math.PI / 2;
    });
  } else if (id === "dhruv") {
    // Madan Gowri signature studio headphones worn loosely around shoulders/clavicles
    attachBonePropWorld(scene, "Spine2", new Vector3(0, 1.452, 0.026), (g) => {
      const dark = mat(0x1f2937, 0.45, 0.4);
      const cyan = mat(0x22d3ee, 0.25, 0.75, { emissive: 0x0891b2, emissiveIntensity: 0.2 });
      const band = new Mesh(new TorusGeometry(0.118, 0.014, 8, 22), dark);
      band.rotation.x = Math.PI / 2.4;
      g.add(band);
      addCyl(g, 0.026, 0.026, 0.024, 12, cyan, 0.096, -0.025, 0.068).rotation.z = Math.PI / 2;
      addCyl(g, 0.026, 0.026, 0.024, 12, cyan, -0.096, -0.025, 0.068).rotation.z = Math.PI / 2;
    });
  }
}

function applySouthFighterVisuals(scene, id, donorYogi, donorModi, texSet, envMap) {
  // Visibility rules & modular yogi garments + cool hero 3D shades
  const hideMeshes = new Set();
  if (id === "didi") {
    hideMeshes.add("GlassesFrame");
    hideMeshes.add("GlassesLens");
  }
  if (id === "nitin") {
    hideMeshes.add("Glasses");
  }
  if (SHADES_IDS.has(id) && donorModi && !findNode(scene, "Glasses")) {
    bindMeshFromDonor(scene, donorModi, "Glasses", "shades_dark");
  }
  if (VESHTI_IDS.has(id)) {
    hideMeshes.add("OutfitBottom");
    bindMeshFromDonor(scene, donorYogi, "Dhoti", "outfit_bottom");
  }
  if (KURTA_IDS.has(id)) {
    hideMeshes.add("OutfitTop");
    bindMeshFromDonor(scene, donorYogi, "Kurta", "outfit_top");
    bindMeshFromDonor(scene, donorYogi, "Forearms", "AvatarBody");
  }
  if (SHAWL_IDS.has(id)) {
    bindMeshFromDonor(scene, donorYogi, "Shawl", "outfit_shawl");
  }

  scene.traverse((o) => {
    if (!o.isMesh) return;
    const meshName = stripIdx(o.name);
    if (hideMeshes.has(meshName)) {
      o.visible = false;
      return;
    }
    o.castShadow = true;
    o.receiveShadow = true;
    o.frustumCulled = false;

    const mapMat = (srcM) => {
      if (!srcM) return srcM;
      const m = srcM.clone();
      const mn = m.name || "";
      if (envMap && m.isMeshStandardMaterial) {
        m.envMap = envMap;
        m.envMapIntensity = 0.55;
      }
      if (mn === "AvatarHead" && texSet.head) {
        m.map = texSet.head;
        m.color.setRGB(1, 1, 1);
        m.roughness = 0.72;
        m.metalness = 0.0;
        m.envMapIntensity = 0.30;
      } else if (mn === "AvatarBody" && texSet.body) {
        m.map = texSet.body;
        m.color.setRGB(1, 1, 1);
        m.roughness = 0.66;
        m.metalness = 0.0;
        m.envMapIntensity = 0.34;
      } else if ((mn === "outfit_top" || mn === "didi_blouse") && texSet.top) {
        m.map = texSet.top;
        m.color.setRGB(1, 1, 1);
        m.roughness = 0.86;
        m.metalness = 0.0;
        m.envMapIntensity = 0.30;
      } else if ((mn === "outfit_bottom" || mn === "outfit_dhoti" || mn === "didi_sari") && texSet.bottom) {
        m.map = texSet.bottom;
        m.color.setRGB(1, 1, 1);
        m.roughness = 0.86;
        m.metalness = 0.0;
        m.envMapIntensity = 0.30;
      } else if (mn === "outfit_shawl" && texSet.shawl) {
        m.map = texSet.shawl;
        m.color.setRGB(1, 1, 1);
        m.roughness = 0.84;
        m.metalness = 0.0;
        m.envMapIntensity = 0.32;
      } else if (mn === "shades_dark") {
        m.color.setHex(0x11121a);
        m.transparent = true;
        m.opacity = 0.86;
        m.roughness = 0.08;
        m.metalness = 0.65;
        m.envMapIntensity = 1.5;
      } else if (mn === "glasses") {
        m.transparent = true;
        m.opacity = 0.34;
        m.depthWrite = false;
        m.roughness = 0.08;
        m.metalness = 0.25;
        m.envMapIntensity = 1.3;
      } else if (/Eyelashes/.test(mn)) {
        m.color.setRGB(0.04, 0.03, 0.03);
      } else if (/Cornea/.test(mn)) {
        m.roughness = 0.05;
        m.envMapIntensity = 1.2;
      }
      m.needsUpdate = true;
      return m;
    };

    o.material = Array.isArray(o.material) ? o.material.map(mapMat) : mapMat(o.material);
  });

  sculptFighter3D(scene, id);
}

const _loadingCharPromises = new Map();
let _envTex = null;
let _sharedGltfLoader = null;

function getSharedGltfLoader() {
  if (_sharedGltfLoader) return _sharedGltfLoader;
  const draco = new DRACOLoader();
  draco.setDecoderPath("/node_modules/three/examples/jsm/libs/draco/gltf/");
  const loader = new GLTFLoader();
  loader.setDRACOLoader(draco);
  _sharedGltfLoader = loader;
  return loader;
}

const KIT_TO_RPM_BONES = {
  "DEF-spine": "Hips",
  "DEF-spine001": "Spine",
  "DEF-spine002": "Spine1",
  "DEF-spine003": "Spine2",
  "DEF-spine004": "Neck",
  "DEF-spine005": "Neck1",
  "DEF-spine006": "Head",
  "DEF-eyeL": "KitEyeL",
  "DEF-eyeR": "KitEyeR",
  "DEF-shoulderL": "LeftShoulder",
  "DEF-upper_armL": "LeftArm",
  "DEF-forearmL": "LeftForeArm",
  "DEF-handL": "LeftHand",
  "DEF-shoulderR": "RightShoulder",
  "DEF-upper_armR": "RightArm",
  "DEF-forearmR": "RightForeArm",
  "DEF-handR": "RightHand",
  "DEF-thighL": "LeftUpLeg",
  "DEF-shinL": "LeftLeg",
  "DEF-footL": "LeftFoot",
  "DEF-toeL": "LeftToeBase",
  "DEF-thighR": "RightUpLeg",
  "DEF-shinR": "RightLeg",
  "DEF-footR": "RightFoot",
  "DEF-toeR": "RightToeBase"
};

for (const [side, lr] of [["L", "Left"], ["R", "Right"]]) {
  for (const [fn, fc] of [["index", "Index"], ["middle", "Middle"], ["ring", "Ring"], ["pinky", "Pinky"]]) {
    for (const k of ["1", "2", "3"]) {
      KIT_TO_RPM_BONES[`DEF-f_${fn}0${k}${side}`] = `${lr}Hand${fc}${k}`;
    }
  }
  for (const k of ["1", "2", "3"]) {
    KIT_TO_RPM_BONES[`DEF-thumb0${k}${side}`] = `${lr}HandThumb${k}`;
  }
}

function canonKitKey(name) {
  return String(name || "").replace(/\./g, "");
}

function prepareKitCharacterScene(scene, envMap) {
  scene.updateMatrixWorld(true);
  const byName = new Map();
  scene.traverse((o) => {
    if (o.name) byName.set(canonKitKey(o.name), o);
  });

  const attachChild = (childName, parentName) => {
    const child = byName.get(canonKitKey(childName));
    const parent = byName.get(canonKitKey(parentName));
    if (child && parent && child.parent !== parent) {
      parent.attach(child);
    }
  };

  // Assemble anatomical parent-child chain while preserving exact world rest transforms
  attachChild("DEF-spine004", "DEF-spine003");
  attachChild("DEF-jaw", "DEF-spine006");
  attachChild("DEF-eyeL", "DEF-spine006");
  attachChild("DEF-eyeR", "DEF-spine006");
  attachChild("DEF-pelvisL", "DEF-spine");
  attachChild("DEF-pelvisR", "DEF-spine");
  attachChild("DEF-thighL", "DEF-spine");
  attachChild("DEF-thighR", "DEF-spine");
  attachChild("DEF-shoulderL", "DEF-spine003");
  attachChild("DEF-shoulderR", "DEF-spine003");
  attachChild("DEF-upper_armL", "DEF-shoulderL");
  attachChild("DEF-upper_armR", "DEF-shoulderR");
  attachChild("DEF-Cape_01", "DEF-spine003");
  attachChild("DEF-Cape_02", "DEF-Cape_01");
  attachChild("DEF-Cape_03", "DEF-Cape_02");

  for (const side of ["L", "R"]) {
    const hand = `DEF-hand${side}`;
    for (const f of ["index", "middle", "ring", "pinky"]) {
      attachChild(`DEF-f_${f}01${side}`, hand);
    }
    attachChild(`DEF-thumb01${side}`, hand);
    attachChild(`DEF-Prop_${side}`, hand);
  }

  scene.traverse((o) => {
    const key = canonKitKey(o.name);
    if (o.isBone && KIT_TO_RPM_BONES[key]) {
      o.name = KIT_TO_RPM_BONES[key];
    }
    if (!o.isMesh) return;
    o.castShadow = true;
    o.receiveShadow = true;
    o.frustumCulled = false;

    const patchMat = (m) => {
      if (!m || !m.isMeshStandardMaterial) return m;
      if (envMap) {
        m.envMap = envMap;
        m.envMapIntensity = 0.45;
      }
      const mn = m.name || "";
      if (/^(TOP|BOT|SCARF|BDR)/.test(mn) || /Outfit_Main/.test(o.name)) {
        m.side = DoubleSide;
      }
      if (/^LENS\b/.test(mn)) {
        m.roughness = 0.14;
        m.metalness = 0.45;
        m.envMapIntensity = 1.25;
      } else if (/^SKIN/.test(mn)) {
        m.roughness = Math.max(m.roughness, 0.56);
        m.envMapIntensity = 0.3;
      }
      m.needsUpdate = true;
      return m;
    };
    o.material = Array.isArray(o.material) ? o.material.map(patchMat) : patchMat(o.material);
  });

  scene.updateMatrixWorld(true);
}

function collectBoneRestMap(root) {
  root.updateMatrixWorld(true);
  const map = new Map();
  root.traverse((o) => {
    if (!o.isBone) return;
    const nm = stripIdx(o.name);
    if (map.has(nm)) return;
    const worldRestQ = new Quaternion();
    o.getWorldQuaternion(worldRestQ);
    const parentWorldRestQ = new Quaternion();
    if (o.parent) o.parent.getWorldQuaternion(parentWorldRestQ);
    const parentWorldRestQInv = parentWorldRestQ.clone().invert();
    map.set(nm, {
      bone: o,
      localRestQ: o.quaternion.clone(),
      localRestQInv: o.quaternion.clone().invert(),
      worldRestQ,
      parentWorldRestQ,
      parentWorldRestQInv,
      localPos: o.position.clone()
    });
  });
  return map;
}

const _rq = new Quaternion();
const _rDeltaW = new Quaternion();
const _rOut = new Quaternion();

function retargetClipsToKitSkeleton(clips, donorScene, kitScene) {
  normalizeSceneNames(donorScene);
  const srcMap = collectBoneRestMap(donorScene);
  const dstMap = collectBoneRestMap(kitScene);
  const srcHipsPos = srcMap.get("Hips")?.localPos || new Vector3(0, 0.941, 0);
  const dstHipsPos = dstMap.get("Hips")?.localPos || new Vector3(0, 0.841, 0);
  const hipsScale = dstHipsPos.y / (srcHipsPos.y || 0.941);

  const out = [];
  for (const clip of clips || []) {
    const c = clip.clone();
    const tracks = [];
    for (const tr of c.tracks) {
      const cleanName = tr.name.replace(/_\d+\./, ".");
      const dotIdx = cleanName.indexOf(".");
      if (dotIdx <= 0) continue;
      const boneName = cleanName.slice(0, dotIdx);
      const prop = cleanName.slice(dotIdx + 1);
      if (prop === "scale") continue;

      const src = srcMap.get(boneName);
      const dst = dstMap.get(boneName);
      if (!src || !dst) continue;

      if (prop === "quaternion" && tr.values.length >= 4) {
        const vals = new Float32Array(tr.values.length);
        for (let i = 0; i < vals.length; i += 4) {
          _rq.set(tr.values[i], tr.values[i + 1], tr.values[i + 2], tr.values[i + 3]);
          // Convert Mixamo local keyframe into world delta relative to RPM rest, then rebind onto Kit bone rest
          _rDeltaW.copy(src.parentWorldRestQ)
            .multiply(_rq)
            .multiply(src.localRestQInv)
            .multiply(src.parentWorldRestQInv);
          _rOut.copy(dst.parentWorldRestQInv)
            .multiply(_rDeltaW)
            .multiply(dst.parentWorldRestQ)
            .multiply(dst.localRestQ);
          vals[i] = _rOut.x;
          vals[i + 1] = _rOut.y;
          vals[i + 2] = _rOut.z;
          vals[i + 3] = _rOut.w;
        }
        tracks.push(new QuaternionKeyframeTrack(cleanName, tr.times.slice(), vals));
      } else if (prop === "position" && boneName === "Hips") {
        const vals = new Float32Array(tr.values.length);
        for (let i = 0; i < vals.length; i += 3) {
          vals[i]     = (tr.values[i]     - srcHipsPos.x) * hipsScale + dstHipsPos.x;
          vals[i + 1] = (tr.values[i + 1] - srcHipsPos.y) * hipsScale + dstHipsPos.y;
          vals[i + 2] = (tr.values[i + 2] - srcHipsPos.z) * hipsScale + dstHipsPos.z;
        }
        tracks.push(new VectorKeyframeTrack(cleanName, tr.times.slice(), vals));
      }
    }
    c.tracks = tracks;
    out.push(c);
  }
  return out;
}

async function fetchGlbWithProgress(loader, url, onProgress) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} loading ${url}`);
  const total = Number(res.headers.get("content-length")) || 500000;
  const reader = res.body?.getReader();
  if (!reader) {
    const buf = await res.arrayBuffer();
    onProgress?.(92);
    return loader.parseAsync(buf, "");
  }
  const chunks = [];
  let loaded = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    loaded += value.length;
    onProgress?.(Math.min(92, Math.round((loaded / total) * 92)));
  }
  const combined = new Uint8Array(loaded);
  let offset = 0;
  for (const chunk of chunks) {
    combined.set(chunk, offset);
    offset += chunk.length;
  }
  return loader.parseAsync(combined.buffer, "");
}

function ensureEnvMap(renderer) {
  if (renderer && !_envTex) {
    const pmrem = new PMREMGenerator(renderer);
    _envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    pmrem.dispose();
  }
  return _envTex;
}

export async function loadSouthCharacter(id, Vc, Oc, kc, N, at, renderer, onProgress) {
  if (Vc[id]) {
    onProgress?.(100);
    return true;
  }
  if (_loadingCharPromises.has(id)) {
    return _loadingCharPromises.get(id);
  }

  const p = (async () => {
    try {
      const env = ensureEnvMap(renderer);
      const loader = getSharedGltfLoader();
      const kitUrl = CHARACTER_GLB_MAP[id];
      if (!kitUrl) return false;

      const animId = ANIM_DONOR_MAP[id] || id;
      const animUrl = `/models/mobile/${animId}.glb?v=${TEX_VER}`;
      const [kitGltf, donorGltf, propGltf] = await Promise.all([
        fetchGlbWithProgress(loader, `${kitUrl}?v=${TEX_VER}`, onProgress),
        loader.loadAsync(animUrl).catch(() => null),
        id === "yogi" && !Oc.bulldozer
          ? loader.loadAsync(`/models/mobile/bull1.glb?v=${TEX_VER}`).catch(() => null)
          : id === "dhruv" && !Oc.shepherd
          ? loader.loadAsync(`/models/mobile/shepherd.glb?v=${TEX_VER}`).catch(() => null)
          : Promise.resolve(null)
      ]);

      const scene = kitGltf.scene;
      prepareKitCharacterScene(scene, env);

      const clips = donorGltf?.animations?.length
        ? retargetClipsToKitSkeleton(donorGltf.animations, donorGltf.scene, scene)
        : [];

      const legBone = findNode(scene, "LeftUpLeg");
      const legY = legBone ? legBone.getWorldPosition(new Vector3()).y || at : at;
      const def = N?.[id] || {};

      Vc[id] = {
        scene,
        scale: at / legY,
        dance: clips.find((c) => c.name === "dance") ?? null,
        clips: def.fightClips ? clips : []
      };

      if (id === "yogi" && propGltf && !Oc.bulldozer) {
        const bScene = propGltf.scene;
        bScene.traverse((o) => {
          if (o.isMesh) {
            o.castShadow = true;
            o.receiveShadow = true;
            o.frustumCulled = false;
          }
        });
        Oc.bulldozer = bScene;
        kc.bulldozer = propGltf.animations;
      }

      if (id === "dhruv" && propGltf && !Oc.shepherd) {
        const sScene = propGltf.scene;
        sScene.traverse((o) => {
          if (o.isMesh) {
            o.castShadow = true;
            o.receiveShadow = true;
            o.frustumCulled = false;
            const tintDog = (m) => {
              if (!m) return m;
              m.color?.setHex(0xf4efe6);
              m.metalness = 0;
              m.envMapIntensity = 0.35;
              if (m.name && m.name.endsWith("Transparent")) {
                m.transparent = false;
                m.alphaTest = 0.5;
                m.depthWrite = true;
              }
              return m;
            };
            Array.isArray(o.material) ? o.material.forEach(tintDog) : tintDog(o.material);
          }
        });
        Oc.shepherd = sScene;
        kc.shepherd = propGltf.animations;
      }

      onProgress?.(100);
      return true;
    } catch (err) {
      console.warn(`[characters] Failed to load ${id}:`, err);
      return false;
    } finally {
      _loadingCharPromises.delete(id);
    }
  })();

  _loadingCharPromises.set(id, p);
  return p;
}

export async function populateSouthModels(Vc, Oc, kc, N, at, renderer, ids) {
  const list = (ids && ids.length ? ids : ["modi", "rahul"]).filter((id) => id in CHARACTER_GLB_MAP);
  await Promise.all(list.map((id) => loadSouthCharacter(id, Vc, Oc, kc, N, at, renderer)));
  return list.filter((id) => id in Vc);
}

export function buildMarinaStage(group) {
  const sandMat = mat(0xe8c78a, 0.94, 0.02);
  const seaMat = mat(0x0b6fa4, 0.25, 0.18);
  const foamMat = mat(0xecf8ff, 0.6, 0.05);
  const bridgeMat = mat(0xf6f3ea, 0.68, 0.08);
  const redMat = mat(0xc81e1e, 0.62, 0.08);
  const whiteMat = mat(0xfafafa, 0.62, 0.05);
  const trunkMat = mat(0x6e4726, 0.92, 0.02);
  const leafMat = mat(0x1f8a3d, 0.72, 0.04);

  // Bay of Bengal water strip behind the sand
  const sea = new Mesh(new PlaneGeometry(160, 48), seaMat);
  sea.rotation.x = -Math.PI / 2;
  sea.position.set(0, -0.34, -34);
  sea.receiveShadow = true;
  group.add(sea);

  // Surf foam ribbon along shoreline
  for (let i = -3; i <= 3; i++) {
    const foam = new Mesh(new BoxGeometry(18, 0.08, 1.4), foamMat);
    foam.position.set(i * 19, -0.28, -11.5 + Math.sin(i) * 0.4);
    group.add(foam);
  }

  // Golden beach dunes behind arena
  addBox(group, 140, 0.4, 9, sandMat, 0, -0.45, -7);

  // Iconic Napier Bridge white bowstring arches on left background
  const bridge = new Group();
  bridge.position.set(-10, -0.3, -17);
  addBox(bridge, 22, 0.55, 3.2, bridgeMat, 0, 1.2, 0);
  for (const ax of [-6.5, 0, 6.5]) {
    for (let s = 0; s < 9; s++) {
      const a = (s / 8) * Math.PI;
      const px = ax - 2.6 + (s / 8) * 5.2;
      const py = 1.4 + Math.sin(a) * 2.5;
      addBox(bridge, 0.72, 0.34, 0.35, bridgeMat, px, py, 1.4);
      addBox(bridge, 0.72, 0.34, 0.35, bridgeMat, px, py, -1.4);
    }
  }
  group.add(bridge);

  // Marina Lighthouse with red & white bands + rotating beacon beam on right
  const lh = new Group();
  lh.position.set(13.5, -0.3, -21);
  for (let i = 0; i < 6; i++) {
    const rBot = 1.35 - i * 0.07;
    const rTop = 1.28 - i * 0.07;
    addCyl(lh, rTop, rBot, 2.2, 8, i % 2 === 0 ? whiteMat : redMat, 0, 1.1 + i * 2.2, 0);
  }
  addCyl(lh, 1.25, 1.05, 0.5, 12, mat(0x26262b, 0.4, 0.5), 0, 14.3, 0);
  const lantern = new Mesh(
    new CylinderGeometry(0.7, 0.7, 1.2, 12),
    new MeshBasicMaterial({ color: 0xffe484 })
  );
  lantern.position.set(0, 15.1, 0);
  lh.add(lantern);
  const beamGroup = new Group();
  beamGroup.position.set(0, 15.1, 0);
  const beamMat = new MeshBasicMaterial({ color: 0xfef08a, transparent: true, opacity: 0.22, side: DoubleSide, depthWrite: false });
  const beamCone = new Mesh(new ConeGeometry(2.4, 15, 12, 1, true), beamMat);
  beamCone.rotation.z = Math.PI / 2;
  beamCone.position.x = -7.5;
  beamGroup.add(beamCone);
  lh.add(beamGroup);
  const dome = new Mesh(new ConeGeometry(0.95, 0.9, 12), redMat);
  dome.position.set(0, 16.1, 0);
  lh.add(dome);
  group.add(lh);
  group.userData.lighthouseBeam = beamGroup;

  // Coconut Palm Trees framing the promenade
  for (const [px, pz, tilt] of [[-14, -9.5, 0.14], [-9, -10.5, -0.1], [8.5, -10.2, 0.12], [14.5, -9, -0.15]]) {
    const palm = new Group();
    palm.position.set(px, -0.3, pz);
    palm.rotation.z = tilt;
    for (let s = 0; s < 5; s++) {
      addCyl(palm, 0.16 - s * 0.015, 0.19 - s * 0.015, 1.3, 8, trunkMat, Math.sin(s * 0.3) * 0.08, 0.65 + s * 1.22, 0);
    }
    for (let f = 0; f < 6; f++) {
      const frond = new Mesh(new BoxGeometry(2.3, 0.08, 0.45), leafMat);
      frond.position.set(0, 6.4, 0);
      frond.rotation.y = (f / 6) * Math.PI * 2;
      frond.rotation.z = -0.32;
      frond.translateX(1.05);
      palm.add(frond);
    }
    group.add(palm);
  }

  // Anna Square Arch ("அண்ணா சதுக்கம் · MARINA") + MGR Memorial Lotus Canopy
  const arch = new Group();
  arch.position.set(-2.5, -0.3, -15);
  const ivoryMat = mat(0xf6efe0, 0.72, 0.05);
  const goldMat = mat(0xfacc15, 0.4, 0.45);
  addBox(arch, 0.9, 6.2, 0.9, ivoryMat, -3.6, 3.1, 0);
  addBox(arch, 0.9, 6.2, 0.9, ivoryMat, 3.6, 3.1, 0);
  addBox(arch, 8.6, 1.35, 1.0, ivoryMat, 0, 6.2, 0);
  addBox(arch, 8.8, 0.28, 1.15, goldMat, 0, 6.95, 0);
  addSignBoard(arch, "அண்ணா சதுக்கம் · MARINA", "ANNA & MGR MEMORIALS, CHENNAI", "#7c1d18", "#fde047", 6.8, 1.1, 0, 6.2, 0.56);
  group.add(arch);

  const mgr = new Group();
  mgr.position.set(6.5, -0.3, -15.5);
  addCyl(mgr, 2.2, 2.6, 0.6, 12, ivoryMat, 0, 0.3, 0);
  for (let p = 0; p < 6; p++) {
    const a = (p / 6) * Math.PI * 2;
    const petal = new Mesh(new ConeGeometry(0.6, 3.2, 5), ivoryMat);
    petal.position.set(Math.cos(a) * 1.4, 2.1, Math.sin(a) * 1.4);
    petal.rotation.z = -Math.cos(a) * 0.45;
    petal.rotation.x = Math.sin(a) * 0.45;
    mgr.add(petal);
  }
  addCyl(mgr, 0.4, 0.4, 2.8, 10, goldMat, 0, 1.8, 0);
  group.add(mgr);

  // Two Push-Carts selling Sundal & Molaga Bajji (left & right beach promenade)
  const buildPushCart = (px, pz, title, sub, color) => {
    const cart = new Group();
    cart.position.set(px, -0.3, pz);
    addBox(cart, 2.6, 0.85, 1.25, mat(color, 0.78), 0, 0.85, 0);
    addBox(cart, 2.9, 0.14, 1.5, mat(0xdc2626, 0.72), 0, 2.45, 0);
    addCyl(cart, 0.05, 0.05, 1.65, 8, goldMat, -1.2, 1.6, 0.52);
    addCyl(cart, 0.05, 0.05, 1.65, 8, goldMat, 1.2, 1.6, 0.52);
    addCyl(cart, 0.05, 0.05, 1.65, 8, goldMat, -1.2, 1.6, -0.52);
    addCyl(cart, 0.05, 0.05, 1.65, 8, goldMat, 1.2, 1.6, -0.52);
    // Push-cart spoked wooden wheels + kadai pan
    for (const wx of [-0.9, 0.9]) {
      const wheel = new Mesh(new TorusGeometry(0.36, 0.07, 8, 16), mat(0x78350f, 0.85));
      wheel.position.set(wx, 0.36, 0.68);
      cart.add(wheel);
    }
    const kadai = new Mesh(new CylinderGeometry(0.42, 0.24, 0.22, 12), mat(0x374151, 0.35, 0.7));
    kadai.position.set(-0.4, 1.38, 0.1);
    const bajjiTray = new Mesh(new BoxGeometry(0.75, 0.14, 0.5), mat(0xf59e0b, 0.65));
    bajjiTray.position.set(0.55, 1.34, 0.1);
    cart.add(kadai, bajjiTray);
    addSignBoard(cart, title, sub, "#065f46", "#fef08a", 2.7, 0.68, 0, 2.75, 0.58);
    group.add(cart);
  };
  buildPushCart(-10.2, -7.8, "MARINA SUNDAL CART", "BEACH SUNDAL & MANGO · ₹20", 0x1e3a8a);
  buildPushCart(10.4, -7.9, "MOLAGA BAJJI KADAI", "HOT CHILLI BAJJI · ₹15", 0x991b1b);

  // Active 3D Ocean Wave Mesh (washes across stage sand every 20 seconds)
  const waveGroup = new Group();
  const waveBody = new Mesh(
    new BoxGeometry(18, 0.24, 5.2),
    new MeshStandardMaterial({ color: 0x0ea5e9, roughness: 0.15, metalness: 0.25, transparent: true, opacity: 0.72 })
  );
  const waveFoam = new Mesh(
    new BoxGeometry(18.2, 0.28, 0.9),
    new MeshBasicMaterial({ color: 0xf0f9ff, transparent: true, opacity: 0.9 })
  );
  waveFoam.position.set(0, 0.04, 2.4);
  waveGroup.add(waveBody, waveFoam);
  waveGroup.position.set(0, -0.05, -13);
  waveGroup.visible = false;
  group.add(waveGroup);
  group.userData.marinaWave = waveGroup;
}

export function buildBusStandStage(group) {
  // Koyambedu / Kilambakkam Bus Stand (CMBT)
  const concreteMat = mat(0x9ca3af, 0.9, 0.05);
  const darkAsphalt = mat(0x374151, 0.92, 0.04);
  const greenBusMat = mat(0x15803d, 0.42, 0.28);
  const busStripeMat = mat(0xfef08a, 0.45, 0.15);
  const glassMat = new MeshStandardMaterial({ color: 0x0f172a, roughness: 0.15, metalness: 0.85, transparent: true, opacity: 0.85 });
  const tireMat = mat(0x111827, 0.88, 0.05);
  const autoYellow = mat(0xfacc15, 0.38, 0.22);
  const autoBlack = mat(0x18181b, 0.72, 0.15);

  // Terminus Concrete Canopy + Boarding Bays
  addBox(group, 44, 0.35, 16, darkAsphalt, 0, -0.35, -10);
  addBox(group, 34, 0.45, 8.5, concreteMat, 0, 5.8, -12);
  for (const px of [-14, -7, 0, 7, 14]) {
    addBox(group, 0.65, 5.9, 0.65, mat(0xd97706, 0.6), px, 2.75, -12.8);
  }
  addSignBoard(group, "KOYAMBEDU / KILAMBAKKAM CMBT", "BAY 1: MADURAI · BAY 2: TRICHY · TNSTC", "#065f46", "#fde047", 9.5, 1.85, 0, 6.2, -7.6);
  addSignBoard(group, "SETC ULTRA DELUXE", "CHENNAI ↔ SALEM ↔ COIMBATORE", "#7c2d12", "#ffffff", 6.8, 1.35, -10.5, 5.8, -7.6);
  addSignBoard(group, "MOFFUSIL TERMINUS", "PLATFORM 4 · EXPRESS DEPARTURE", "#1e3a8a", "#fde047", 6.8, 1.35, 10.5, 5.8, -7.6);

  // Two Iconic Green Government Buses parked in background
  const buildGovtBus = (bx, bz, ry, routeLabel) => {
    const bus = new Group();
    bus.position.set(bx, -0.3, bz);
    bus.rotation.y = ry;
    addBox(bus, 10.6, 2.55, 2.7, greenBusMat, 0, 1.75, 0);
    addBox(bus, 10.68, 0.38, 2.74, busStripeMat, 0, 1.5, 0);
    addBox(bus, 10.4, 0.25, 2.6, mat(0xf8fafc, 0.6), 0, 3.12, 0);
    addBox(bus, 9.8, 0.85, 2.76, glassMat, 0, 2.38, 0);
    for (const wx of [-3.4, 3.4]) {
      for (const wz of [-1.25, 1.25]) {
        const w = new Mesh(new CylinderGeometry(0.55, 0.55, 0.36, 16), tireMat);
        w.rotation.x = Math.PI / 2;
        w.position.set(wx, 0.55, wz);
        bus.add(w);
      }
    }
    const led = addSignBoard(bus, routeLabel, "GOVERNMENT EXPRESS · TNSTC", "#090d16", "#facc15", 4.2, 0.72, 0, 2.72, 1.4);
    if (led) led.position.z = 1.4;
    group.add(bus);
    return bus;
  };
  buildGovtBus(-8.5, -10.2, 0.14, "KOYAMBEDU ↔ MADURAI");
  buildGovtBus(8.5, -10.2, -0.14, "KILAMBAKKAM ↔ TRICHY");

  // Two 3D Corner Auto-Rickshaws at Left & Right Arena Boundaries
  const buildCornerAuto = (ax, dirToCenter) => {
    const auto = new Group();
    auto.position.set(ax, 0, 0.15);
    auto.rotation.y = dirToCenter > 0 ? 0 : Math.PI;
    addBox(auto, 1.85, 0.72, 1.25, autoYellow, 0, 0.62, 0);
    addBox(auto, 1.95, 0.16, 1.32, autoBlack, 0, 1.72, 0);
    addBox(auto, 0.08, 0.9, 1.24, autoBlack, -0.88, 1.25, 0);
    addBox(auto, 0.08, 0.9, 1.24, glassMat, 0.88, 1.3, 0);
    // Roof pillars + Headlight
    addBox(auto, 0.08, 0.9, 0.08, autoBlack, 0.84, 1.25, 0.58);
    addBox(auto, 0.08, 0.9, 0.08, autoBlack, 0.84, 1.25, -0.58);
    const hl = new Mesh(new SphereGeometry(0.14, 10, 8), new MeshBasicMaterial({ color: 0xfef08a }));
    hl.position.set(0.95, 0.72, 0);
    auto.add(hl);
    // 3 Wheels
    for (const [wx, wz] of [[0.78, 0], [-0.62, 0.62], [-0.62, -0.62]]) {
      const w = new Mesh(new CylinderGeometry(0.28, 0.28, 0.2, 14), tireMat);
      w.rotation.x = Math.PI / 2;
      w.position.set(wx, 0.28, wz);
      auto.add(w);
    }
    group.add(auto);
    return { group: auto, baseX: ax, bumpTimer: 0, headlight: hl };
  };
  group.userData.leftAuto = buildCornerAuto(-7.35, 1);
  group.userData.rightAuto = buildCornerAuto(7.35, -1);
}

export function buildDebateStudioStage(group) {
  // Prime Time News Debate Studio (Chanakya / Arangam)
  const darkFloorMat = mat(0x090d1a, 0.25, 0.65);
  const neonCyan = new MeshBasicMaterial({ color: 0x22d3ee });
  const neonCrimson = new MeshBasicMaterial({ color: 0xe11d48 });
  const neonGold = new MeshBasicMaterial({ color: 0xfacc15 });
  const trussMat = mat(0x1f2937, 0.4, 0.75);

  // Neon 3D Circular Studio Floor
  const disc = new Mesh(new CylinderGeometry(9.6, 10.0, 0.22, 48), darkFloorMat);
  disc.position.set(0, -0.06, 0);
  disc.receiveShadow = true;
  group.add(disc);

  for (const [rad, rMat] of [[8.8, neonCrimson], [6.6, neonCyan], [4.2, neonGold]]) {
    const ring = new Mesh(new RingGeometry(rad - 0.14, rad, 48), rMat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.set(0, 0.06, 0);
    group.add(ring);
  }

  // Overhead Studio Lighting Truss
  addBox(group, 22, 0.35, 0.4, trussMat, 0, 7.6, -4.5);
  for (const lx of [-8, -4, 0, 4, 8]) {
    const lamp = new Mesh(new ConeGeometry(0.32, 0.55, 10), neonGold);
    lamp.position.set(lx, 7.25, -4.5);
    group.add(lamp);
  }

  // Background Neon Debate Pods & Anchor Desk Backdrop
  addBox(group, 7.2, 1.1, 1.6, mat(0x111827, 0.35, 0.5), 0, 0.35, -8.5);
  addBox(group, 7.3, 0.12, 1.68, neonCyan, 0, 0.92, -8.5);

  // Giant LED Screens surrounding the studio that flash "MIC MUTED!" on stun
  const makeLedTex = (title, sub, bg, fg, border) => {
    const c = document.createElement("canvas");
    c.width = 512;
    c.height = 256;
    const g = c.getContext("2d");
    g.fillStyle = bg;
    g.fillRect(0, 0, 512, 256);
    g.strokeStyle = border;
    g.lineWidth = 14;
    g.strokeRect(10, 10, 492, 236);
    g.fillStyle = fg;
    g.textAlign = "center";
    g.textBaseline = "middle";
    g.font = "bold 56px Impact, sans-serif";
    g.fillText(title, 256, 105, 460);
    g.font = "bold 28px sans-serif";
    g.fillStyle = "#ffffff";
    g.fillText(sub, 256, 180, 460);
    const tx = new CanvasTexture(c);
    tx.colorSpace = SRGBColorSpace;
    return tx;
  };

  const liveTex = makeLedTex("ARANGAM PRIME TIME", "LIVE 9 PM DEBATE · CHANAKYA STUDIO", "#0a1026", "#22d3ee", "#facc15");
  const mutedTex = makeLedTex("🔇 MIC MUTED!", "QUIET IN THE STUDIO · ANCHOR CUT", "#7f1d1d", "#fef08a", "#ef4444");

  const ledMaterials = [];
  const screenPlacements = [
    [0, 3.9, -11.5, 0, 9.6, 4.4],
    [-11.2, 3.6, -8.8, 0.42, 7.8, 4.0],
    [11.2, 3.6, -8.8, -0.42, 7.8, 4.0]
  ];
  for (const [sx, sy, sz, ry, sw, sh] of screenPlacements) {
    const lm = new MeshBasicMaterial({ map: liveTex, side: DoubleSide });
    ledMaterials.push(lm);
    const frame = new Group();
    frame.position.set(sx, sy, sz);
    frame.rotation.y = ry;
    addBox(frame, sw + 0.35, sh + 0.35, 0.25, trussMat, 0, 0, -0.15);
    const screen = new Mesh(new PlaneGeometry(sw, sh), lm);
    frame.add(screen);
    group.add(frame);
  }

  group.userData.studioLed = {
    ledMaterials,
    liveTex,
    mutedTex,
    mutedTimer: 0
  };
}

function addSignBoard(parent, title, subtitle, bg, fg, w, h, x, y, z, ry = 0) {
  if (typeof document === "undefined") return null;
  const cvs = document.createElement("canvas");
  cvs.width = 512;
  cvs.height = 160;
  const ctx = cvs.getContext("2d");
  if (!ctx) return null;
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, 512, 160);
  ctx.strokeStyle = fg;
  ctx.lineWidth = 8;
  ctx.strokeRect(8, 8, 496, 144);
  ctx.fillStyle = fg;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.font = 'bold 40px "Noto Sans Tamil", Impact, sans-serif';
  ctx.fillText(title, 256, 62, 468);
  ctx.font = "bold 24px sans-serif";
  ctx.fillStyle = "#ffffff";
  ctx.fillText(subtitle, 256, 118, 468);
  const tex = new CanvasTexture(cvs);
  tex.colorSpace = SRGBColorSpace;
  const m = new Mesh(
    new PlaneGeometry(w, h),
    new MeshBasicMaterial({ map: tex, side: 2 })
  );
  m.position.set(x, y, z);
  m.rotation.y = ry;
  parent.add(m);
  return m;
}

export function decorateMaduraiStage(group) {
  const gopuram = new Group();
  gopuram.position.set(0, -0.3, -44);
  const baseMat = mat(0xd4b895, 0.88, 0.04);
  const goldMat = mat(0xfacc15, 0.35, 0.55);
  const tierColors = [0xb91c1c, 0x0284c7, 0x15803d, 0xd97706, 0x9333ea, 0xe11d48, 0xf59e0b];

  addBox(gopuram, 6.2, 5.2, 4.4, baseMat, -4.8, 2.6, 0);
  addBox(gopuram, 6.2, 5.2, 4.4, baseMat, 4.8, 2.6, 0);
  addBox(gopuram, 15.8, 1.4, 4.6, baseMat, 0, 5.8, 0);

  for (let t = 0; t < 7; t++) {
    const w = 14.4 - t * 1.45;
    const d = 4.0 - t * 0.34;
    const h = 1.65;
    const y = 7.1 + t * 1.58;
    addBox(gopuram, w, h, d, mat(tierColors[t], 0.72, 0.06), 0, y, 0);
    addBox(gopuram, w + 0.35, 0.25, d + 0.35, goldMat, 0, y + h / 2, 0);
  }

  const topY = 7.1 + 7 * 1.58;
  const vault = addCyl(gopuram, 1.15, 1.15, 6.2, 12, mat(0xeab308, 0.45, 0.4), 0, topY + 0.5, 0);
  vault.rotation.z = Math.PI / 2;
  for (let k = -3; k <= 3; k++) {
    const kalasam = new Mesh(new ConeGeometry(0.24, 1.05, 8), goldMat);
    kalasam.position.set(k * 0.85, topY + 1.9, 0);
    gopuram.add(kalasam);
  }

  for (const side of [-1, 1]) {
    for (let i = 0; i < 3; i++) {
      const px = side * (11.5 + i * 3.8);
      addBox(gopuram, 0.85, 5.6, 0.85, baseMat, px, 2.8, 20);
      addBox(gopuram, 1.3, 0.5, 1.3, goldMat, px, 5.75, 20);
    }
    addBox(gopuram, 9.5, 0.7, 1.2, baseMat, side * 15.3, 6.3, 20);
  }

  group.add(gopuram);
}

export function decorateTNagarStage(group) {
  const boards = [
    ["SARAVANA SILKS · தி.நகர்", "RANGANATHAN ST. MEGA STORE", "#991b1b", "#fde047", -18, 6.2, -13.6],
    ["MURUGAN IDLI KADAI", "GHEE PONGAL & JIGARTHANDA", "#065f46", "#ffffff", -6, 5.4, -13.6],
    ["KUMBAKONAM DEGREE KAAPI", "BRASS DAVARA TUMBLER", "#78350f", "#fde047", 6, 5.4, -13.6],
    ["COIMBATORE MESS", "BANANA LEAF SAPAADU", "#1e3a8a", "#fef08a", 18, 6.0, -13.6]
  ];
  for (const [t, s, bg, fg, x, y, z] of boards) {
    addSignBoard(group, t, s, bg, fg, 6.2, 1.85, x, y, z);
  }
  const festColors = [0xfacc15, 0xdc2626, 0x16a34a, 0xec4899, 0x0ea5e9];
  for (let i = 0; i < 16; i++) {
    const flag = new Mesh(
      new ConeGeometry(0.28, 0.65, 4),
      mat(festColors[i % festColors.length], 0.75)
    );
    flag.rotation.x = Math.PI;
    flag.position.set(-18 + i * 2.4, 7.1 - Math.abs(Math.sin(i * 0.7)) * 0.35, -11);
    group.add(flag);
  }
}

export function upgradeSouthCrowd(arena) {
  const count = arena.crowdData.length;
  if (!count || arena.southCrowd) return;

  const veshtiGeo = new CylinderGeometry(0.245, 0.28, 0.44, 8);
  const veshti = new InstancedMesh(veshtiGeo, mat(0xffffff, 0.88, 0.02), count);
  const kasavuGeo = new CylinderGeometry(0.276, 0.285, 0.075, 8);
  const kasavu = new InstancedMesh(kasavuGeo, mat(0xfacc15, 0.55, 0.25), count);

  const towelGeo = new BoxGeometry(0.16, 0.44, 0.48);
  const towels = new InstancedMesh(towelGeo, mat(0xffffff, 0.82, 0.02), count);

  const bunGeo = new SphereGeometry(0.125, 8, 6);
  const hairBuns = new InstancedMesh(bunGeo, mat(0x141214, 0.9, 0.02), count);
  const jasmineGeo = new TorusGeometry(0.115, 0.032, 6, 12);
  const jasmine = new InstancedMesh(jasmineGeo, mat(0xfdfcf5, 0.75, 0.02), count);

  const veshtiColors = [0xfaf6ec, 0xffffff, 0xfef3c7, 0xfaf6ec, 0xb91c1c, 0x047857, 0x1d4ed8, 0x9333ea];
  const towelColors = [0xdc2626, 0x16a34a, 0xfacc15, 0xfef08a, 0xea580c, 0x111827, 0x0284c7, 0xffffff];
  const col = new Color();

  const roles = [];
  const lastHeights = new Float32Array(count).fill(-999);
  const cosR = new Float32Array(count);
  const sinR = new Float32Array(count);
  const mTmp = new Matrix4();
  const eTmp = new Euler();
  for (let i = 0; i < count; i++) {
    const r = arena.crowdData[i];
    const isSaree = i % 3 === 0;
    roles.push(isSaree ? "saree" : "veshti");
    cosR[i] = Math.cos(r.rot);
    sinR[i] = Math.sin(r.rot);
    const vc = isSaree ? veshtiColors[4 + (i % 4)] : veshtiColors[i % 4];
    veshti.setColorAt(i, col.setHex(vc));
    kasavu.setColorAt(i, col.setHex(isSaree ? 0xf59e0b : 0xfde047));
    towels.setColorAt(i, col.setHex(towelColors[i % towelColors.length]));
    hairBuns.setColorAt(i, col.setHex(0x161214));
    jasmine.setColorAt(i, col.setHex(i % 6 === 0 ? 0xfca5a5 : 0xfdfcf5));

    // Pre-seed static transforms so per-frame updates only touch elements[13] (Y height)
    const setMat = (mesh, px, py, pz, rx, ry, rz, s = 1) => {
      if (s === 0) {
        mTmp.makeScale(0, 0, 0);
      } else {
        mTmp.makeRotationFromEuler(eTmp.set(rx, ry, rz));
      }
      mTmp.setPosition(px, py, pz);
      mesh.setMatrixAt(i, mTmp);
    };
    setMat(veshti, r.x, -0.14, r.z, 0, r.rot, 0, 1);
    setMat(kasavu, r.x, -0.31, r.z, 0, r.rot, 0, 1);
    setMat(towels, r.x, 0.17, r.z, 0, r.rot, isSaree ? 0.35 : -0.28, 1);
    if (isSaree) {
      const bz = r.z - cosR[i] * 0.12;
      const bx = r.x - sinR[i] * 0.12;
      setMat(hairBuns, bx, 0.62, bz, 0, r.rot, 0, 1);
      setMat(jasmine, bx, 0.62, bz, Math.PI / 2, r.rot, 0, 1);
    } else {
      setMat(hairBuns, r.x, -5, r.z, 0, 0, 0, 0);
      setMat(jasmine, r.x, -5, r.z, 0, 0, 0, 0);
    }
  }

  for (const m of [veshti, kasavu, towels, hairBuns, jasmine]) {
    m.instanceMatrix.needsUpdate = true;
    m.frustumCulled = false;
    arena.group.add(m);
  }
  arena.southCrowd = { veshti, kasavu, towels, hairBuns, jasmine, roles, lastHeights };
}

export function updateSouthCrowd(arena, _dummy) {
  const sc = arena.southCrowd;
  if (!sc) return;
  const n = arena.crowdData.length;
  const va = sc.veshti.instanceMatrix.array;
  const ka = sc.kasavu.instanceMatrix.array;
  const ta = sc.towels.instanceMatrix.array;
  const ha = sc.hairBuns.instanceMatrix.array;
  const ja = sc.jasmine.instanceMatrix.array;
  let dirty = false;
  let sareeDirty = false;
  for (let i = 0; i < n; i++) {
    const y = arena.crowdHeights[i];
    if (Math.abs(y - sc.lastHeights[i]) < 0.002) continue;
    sc.lastHeights[i] = y;
    const o = i * 16 + 13;
    va[o] = y - 0.14;
    ka[o] = y - 0.31;
    ta[o] = y + 0.17;
    dirty = true;
    if (sc.roles[i] === "saree") {
      ha[o] = y + 0.62;
      ja[o] = y + 0.62;
      sareeDirty = true;
    }
  }
  if (dirty) {
    sc.veshti.instanceMatrix.needsUpdate = true;
    sc.kasavu.instanceMatrix.needsUpdate = true;
    sc.towels.instanceMatrix.needsUpdate = true;
    if (sareeDirty) {
      sc.hairBuns.instanceMatrix.needsUpdate = true;
      sc.jasmine.instanceMatrix.needsUpdate = true;
    }
  }
}

const ACTION_MEMES = {
  modi: [
    { text: "Tamilnattu arasin mudhalamaicharaga...", url: "/assets/memes/modi_1.mp3" },
    { text: "Nermaiyaga seyven endrum urudhi mozhigiren!", url: "/assets/memes/modi_2.mp3" }
  ],
  rahul: [
    { text: "What bro? It's very wrong bro!", url: "/assets/memes/rahul_1.mp3" },
    { text: "En nenjil kudiyirukkum...", url: "/assets/memes/rahul_2.mp3" }
  ],
  didi: [
    { text: "Unmaiyana makkal iyakkam!", url: "/assets/memes/didi_1.mp3" },
    { text: "Naan irukkindra varai, enakkup pinnalum!", url: "/assets/memes/didi_2.mp3" }
  ],
  trump: [
    { text: "Pushpa Pushparaj... Thaggedhe Le!", url: "/assets/memes/trump_1.mp3" },
    { text: "Pushpa ante flower-a? Fireuu!", url: "/assets/memes/trump_2.mp3" }
  ],
  yogi: [
    { text: "Mukhyamantri kaserayil aakam!", url: "/assets/memes/yogi_1.mp3" },
    { text: "Entho undakki kalayam ennanaanu vicharikunnathu!", url: "/assets/memes/yogi_2.mp3" }
  ],
  nitin: [
    { text: "One thing I'd like to tell you — my birthday...", url: "/assets/memes/nitin_1.mp3" },
    { text: "By profession I'm a businessman!", url: "/assets/memes/nitin_2.mp3" }
  ],
  ravi: [
    { text: "Naaku konchem thikka undhi, kaani daniko lekka undhi!", url: "/assets/memes/ravi_1.mp3" },
    { text: "Janamlo unta! Janam la unta!", url: "/assets/memes/ravi_2.mp3" }
  ],
  lalu: [
    { text: "Moondru yaanaigal uyirizhundhirukkindranar!", url: "/assets/memes/lalu_1.mp3" },
    { text: "1500 yaanai irundhuchu... ippa 650 thaan!", url: "/assets/memes/lalu_2.mp3" }
  ],
  mbapu: [
    { text: "Kadavul kitta undiyal vekkiringale — adhu Aathigam!", url: "/assets/memes/mbapu_1.mp3" },
    { text: "Nambamal poottu podringle — adhu thaan Naathigam!", url: "/assets/memes/mbapu_2.mp3" }
  ],
  amit: [
    { text: "Adhukkellam bayappadathinga! Naalaiku onnume illaina...", url: "/assets/memes/amit_1.mp3" },
    { text: "Ellathaiyum paathutten! Ellathaiyum paathachu!", url: "/assets/memes/amit_2.mp3" }
  ],
  dhruv: [
    { text: "Hello everyone, naan Madan Gowri! Hello my dear MG Squad!", url: "/assets/memes/dhruv_1.mp3" },
    { text: "Indha video motivational video-va illa inspirational-a...", url: "/assets/memes/dhruv_2.mp3" }
  ],
  nirmala: [
    { text: "Waise parivar se aati hoon jahan onion rakhte hi nahi!", url: "/assets/memes/nirmala_1.mp3" },
    { text: "Social media: popcorn ke upar bhi daal rahe hain tax!", url: "/assets/memes/nirmala_2.mp3" }
  ],
  rangaraj: [
    { text: "Edhirkatchi thalaivarum pradhanarum pesittu iruppanga!", url: "/assets/memes/rangaraj_1.mp3" },
    { text: "Irandaavadhu point vandhu — Bharat Pradhanam!", url: "/assets/memes/rangaraj_2.mp3" }
  ]
};

const _memeCooldown = [0, 0];
const _memeIdx = [0, 0];
const _memeAudio = new Map();

const SPECIAL_BURST_COLORS = {
  modi: 0xff2200,
  rahul: 0xffd700,
  didi: 0x00cc44,
  trump: 0xcc3300,
  yogi: 0xd90000,
  nitin: 0xffaa00,
  ravi: 0xff0044,
  lalu: 0xffdd00,
  mbapu: 0xfacc15,
  amit: 0xff6600,
  dhruv: 0x00d4ff,
  nirmala: 0xa855f7,
  rangaraj: 0x38bdf8
};
const _burstPos = new Vector3();

function spawnRosterSpecial3D(battle, attacker, opp, cfg, col) {
  const sceneGroup = battle?.ctx?.arena?.group || battle?.ctx?.scene;
  if (!sceneGroup) return;
  const dir = attacker.facing || 1;
  const ax = attacker.x || 0;
  const ay = (attacker.y || 0) + 1.05;
  const tx = opp ? opp.x : ax + dir * 1.4;
  const ty = opp ? (opp.y || 0) + 1.05 : ay;
  const type = cfg?.special?.type || "aoe_3d";

  const fxGroup = new Group();
  const mat = new MeshStandardMaterial({
    color: col,
    emissive: col,
    emissiveIntensity: 0.75,
    roughness: 0.25,
    metalness: 0.6,
    transparent: true,
    opacity: 0.92
  });

  if (type === "projectile_3d") {
    // TVK Mic Toss & Bubblegum Counter
    const mic = new Mesh(new CylinderGeometry(0.05, 0.04, 0.36, 10), mat);
    mic.rotation.z = Math.PI / 2;
    const head = new Mesh(new SphereGeometry(0.11, 12, 10), new MeshStandardMaterial({ color: 0xffffff, emissive: col, emissiveIntensity: 0.6 }));
    head.position.x = dir * 0.2;
    fxGroup.add(mic, head);
    fxGroup.position.set(ax + dir * 0.6, ay + 0.15, 0.32);
  } else if (type === "dash_3d") {
    // Rising Sun Cycle Charge / Kanakapura Bulldozer Slam
    const wheel = new Mesh(new TorusGeometry(0.55, 0.07, 10, 24), mat);
    fxGroup.add(wheel);
    fxGroup.position.set((ax + tx) * 0.5, ay, 0.3);
  } else if (type === "aoe_3d") {
    // Iron Lady Two-Leaves Shockwave / Rationalist Ground Tremor
    const ring = new Mesh(new TorusGeometry(0.95, 0.09, 10, 28), mat);
    ring.rotation.x = Math.PI / 2;
    fxGroup.add(ring);
    fxGroup.position.set(tx, 0.12, 0.2);
  } else if (type === "melee_3d") {
    // Red Sandalwood Shoulder-Brush Sweep
    const log = new Mesh(new BoxGeometry(0.95, 0.22, 0.22), mat);
    log.rotation.z = dir * 0.45;
    fxGroup.add(log);
    fxGroup.position.set(tx, ty, 0.32);
  } else if (type === "counter_3d") {
    // Double-Heart Red Salute Barrier
    const shield = new Mesh(new CylinderGeometry(0.68, 0.68, 0.08, 8), mat);
    shield.rotation.x = Math.PI / 2;
    fxGroup.add(shield);
    fxGroup.position.set(ax + dir * 0.55, ay, 0.35);
  } else if (type === "vortex_3d") {
    // Shattered Glass Tea-Tumbler Hurricane Kick
    for (let i = 0; i < 3; i++) {
      const r = new Mesh(new TorusGeometry(0.35 + i * 0.18, 0.045, 8, 20), mat);
      r.rotation.x = Math.PI / 2;
      r.position.y = (i - 1) * 0.32;
      fxGroup.add(r);
    }
    fxGroup.position.set(tx, ty, 0.28);
  } else if (type === "cone_3d") {
    // 150-Decibel Megaphone Sonic Boom
    for (let i = 0; i < 3; i++) {
      const wave = new Mesh(new TorusGeometry(0.28 + i * 0.22, 0.04, 8, 20), mat);
      wave.rotation.y = Math.PI / 2;
      wave.position.x = dir * i * 0.34;
      fxGroup.add(wave);
    }
    fxGroup.position.set(ax + dir * 0.65, ay + 0.1, 0.3);
  } else if (type === "meteor_3d") {
    // 500-Page Press Meet Dossier Drop
    const dossier = new Mesh(new BoxGeometry(0.62, 0.42, 0.45), mat);
    fxGroup.add(dossier);
    fxGroup.position.set(tx, ty + 0.9, 0.3);
  } else {
    // flurry_3d / debuff_3d: Wikipedia Fact-Spit Rapid Barrage
    for (let i = 0; i < 4; i++) {
      const card = new Mesh(new BoxGeometry(0.36, 0.24, 0.03), mat);
      const ang = (i / 4) * Math.PI * 2;
      card.position.set(Math.cos(ang) * 0.45, Math.sin(ang) * 0.35, 0);
      fxGroup.add(card);
    }
    fxGroup.position.set(tx, ty, 0.34);
  }

  sceneGroup.add(fxGroup);
  const t0 = performance.now();
  const stepFx = () => {
    const p = Math.min(1, (performance.now() - t0) / 420);
    const s = 1 + p * 0.85;
    fxGroup.scale.setScalar(s);
    fxGroup.rotation.z += 0.14 * dir;
    if (type === "projectile_3d") {
      fxGroup.position.x = ax + dir * (0.6 + p * 1.4);
    } else if (type === "meteor_3d") {
      fxGroup.position.y = ty + (1 - p) * 0.95;
    }
    mat.opacity = 0.92 * (1 - p);
    if (p < 1) {
      requestAnimationFrame(stepFx);
    } else {
      sceneGroup.remove(fxGroup);
      mat.dispose();
    }
  };
  requestAnimationFrame(stepFx);
}

export function triggerMemeOnAction(battle, attacker, moveId) {
  if (!battle || !attacker || battle.phase !== "fight") return;
  const now = performance.now();
  const side = attacker.side || 0;
  const isSpecial = ["special1", "special2", "finisher", "uppercut", "roundhouse", "sweep"].includes(moveId);
  const fx = battle.ctx?.fx;
  const id = attacker.char?.id;
  const rosterCfg = id ? ROSTER_3D_BY_ENGINE_ID[id] : null;

  // Signature per-character 3D Special Archetype + elemental burst on every landed special/finisher!
  if (isSpecial && fx && id && SPECIAL_BURST_COLORS[id]) {
    const col = rosterCfg?.special?.particleColor || SPECIAL_BURST_COLORS[id];
    const opp = battle.fighters?.[side === 0 ? 1 : 0];
    const hx = opp ? opp.x : attacker.x + (attacker.facing || 1) * 0.8;
    const hy = opp ? (opp.y + 1.15) : 1.15;
    _burstPos.set(hx, hy, 0.25);
    try {
      fx.shockwave?.(_burstPos, col, 0.28, moveId === "finisher" || moveId === "special2" ? 1.5 : 1.05, true);
      fx.particles?.emit(_burstPos, {
        count: moveId === "finisher" ? 28 : 18,
        speed: 4.8,
        color: col,
        life: 0.45,
        size: 0.2,
        drag: 1.8
      });
      if (moveId === "special1" || moveId === "special2" || moveId === "finisher") {
        spawnRosterSpecial3D(battle, attacker, opp, rosterCfg, col);
      }
    } catch {}
  }

  if (now - _memeCooldown[side] < 2100) return;
  if (!isSpecial && Math.random() > 0.35) return;

  const entries = ACTION_MEMES[id];
  if (!entries || !entries.length) return;

  _memeCooldown[side] = now;
  const lineIdx = _memeIdx[side]++ % entries.length;
  const { text, url } = entries[lineIdx];

  try {
    battle.speech(side, text);
  } catch {}

  const audio = battle.ctx?.audio;
  if (audio && !audio.muted && !audio.clipActive && typeof Audio !== "undefined") {
    if (audio.clipBuffers?.has(url)) {
      audio.playClip?.(url, 0.96);
    } else {
      let el = _memeAudio.get(url);
      if (!el) {
        el = new Audio(url);
        el.volume = 0.95;
        _memeAudio.set(url, el);
      }
      try {
        el.volume = 0.95;
        el.currentTime = 0;
        audio.dipMusic?.(0.06, 1.8);
        el.play().catch(() => {});
      } catch {}
    }
  }
}

/* ============================================================================
 * 1. FDFS KOLLYWOOD HUD: PAAL ABHISHEKAM + YOUTUBE FAN WAR COMMENT FEED
 * ============================================================================ */
let _paalTimers = [0, 0];
export function triggerPaalAbhishekam(side, hits) {
  if (typeof document === "undefined" || hits < 5) return;
  const sideCls = side === 0 ? "left" : "right";
  const sideEl = document.querySelector(`#hud .side.${sideCls}`);
  if (!sideEl) return;
  sideEl.classList.remove("paal-active");
  void sideEl.offsetWidth;
  sideEl.classList.add("paal-active");
  if (_paalTimers[side]) clearTimeout(_paalTimers[side]);
  _paalTimers[side] = setTimeout(() => sideEl.classList.remove("paal-active"), 1800);
}

const FAN_WAR_HANDLES = [
  { name: "@AnilVsAamai", badge: "FDFS", color: "#facc15" },
  { name: "@BlueShirtMaran", badge: "1/5★", color: "#38bdf8" },
  { name: "@RohiniScreen1", badge: "LIVE", color: "#e11d48" },
  { name: "@BoxOfficeTrackerTN", badge: "1000CR", color: "#22c55e" },
  { name: "@FilterKaapiVeriyan", badge: "VIP", color: "#fb923c" },
  { name: "@MemeFactory24x7", badge: "RATIO", color: "#c084fc" }
];

const FAN_WAR_LINES = {
  hit: [
    "Anil vs Aamai war started in comments 🔥",
    "Blue Shirt Maran just gave this combo a 1/5 review 👕",
    "Thalaivar fan tore the Rohini flex banner!",
    "Paal abhishekam milk packets sold out outside!",
    "Mass BGM dropped in my head after that hit 💀",
    "4K HD status edit already uploading on Reels!"
  ],
  combo5: [
    "🥛 PAAL ABHISHEKAM! 5+ HIT COMBO AT ROHINI SCREEN 1!",
    "Blue Shirt Maran walked out of theatre: 'No logic!' 💀",
    "Theater speaker blown out — FDFS roof gone!!"
  ],
  block: [
    "Solid granite block! Zero damage macha 🛡️",
    "Blue Shirt: 'Script predictable, blocked cleanly'"
  ],
  super: [
    "🚨 INTERVAL BLOCK ENERGY! 1000 CRORE LOADING!",
    "Whistle podu!! Screen full confetti & paper bits!"
  ],
  assist: [
    "🚨 KOOTANI CAMEO! Marvel vs Capcom who??",
    "Flying Squad raid in middle of Rohini FDFS!"
  ],
  ko: [
    "SOZHI MUDINJATHU! Theater seats torn up!! 🏆",
    "Pan-India Box Office shattered on Day 1!"
  ]
};

let _lastFanCommentAt = 0;
export function pushFanWarComment(ev = {}) {
  if (typeof document === "undefined") return;
  const feed = document.getElementById("fanwar-feed");
  if (!feed) return;
  const now = performance.now();
  const isHigh = ev.kind === "super" || ev.kind === "ko" || ev.kind === "assist" || (ev.combo >= 5);
  if (!isHigh && now - _lastFanCommentAt < 950) return;
  _lastFanCommentAt = now;

  let pool = FAN_WAR_LINES[ev.kind] || FAN_WAR_LINES.hit;
  if (ev.combo >= 5) pool = FAN_WAR_LINES.combo5;
  const text = ev.custom || pool[Math.floor(Math.random() * pool.length)];
  const author = FAN_WAR_HANDLES[Math.floor(Math.random() * FAN_WAR_HANDLES.length)];

  const item = document.createElement("div");
  item.className = `fan-msg${isHigh ? " hot" : ""}`;
  item.innerHTML = `<div class="fan-thumb" style="border-color:${author.color}"><span>${author.badge}</span></div><div class="fan-body"><b style="color:${author.color}">${author.name}</b><span>${text}</span></div>`;
  feed.appendChild(item);
  while (feed.children.length > 4) feed.firstElementChild.remove();
  setTimeout(() => {
    item.classList.add("fade");
    setTimeout(() => item.remove(), 350);
  }, 4200);
}

/* ============================================================================
 * 2. B KEY: KOOTANI (ALLIANCE) SUMMON / VIP CAMEO 2-SECOND 3D STAGE HAZARDS
 * ============================================================================ */
function buildSumoMesh() {
  const g = new Group();
  const bodyMat = mat(0xf8fafc, 0.35, 0.25);
  const trimMat = mat(0x1f2937, 0.7, 0.15);
  const glassMat = mat(0x0f172a, 0.12, 0.85);
  addBox(g, 2.35, 0.82, 1.25, bodyMat, 0, 0.68, 0);
  addBox(g, 1.55, 0.58, 1.18, bodyMat, -0.18, 1.32, 0);
  addBox(g, 1.62, 0.44, 1.21, glassMat, -0.15, 1.32, 0);
  addBox(g, 2.42, 0.16, 1.3, trimMat, 0, 0.35, 0);
  // Roof luggage rack + twin headlights
  addBox(g, 1.35, 0.12, 1.05, trimMat, -0.2, 1.66, 0);
  const hlMat = new MeshBasicMaterial({ color: 0xfef08a });
  addBox(g, 0.08, 0.16, 0.24, hlMat, 1.18, 0.72, 0.4);
  addBox(g, 0.08, 0.16, 0.24, hlMat, 1.18, 0.72, -0.4);
  for (const [wx, wz] of [[0.72, 0.62], [0.72, -0.62], [-0.72, 0.62], [-0.72, -0.62]]) {
    const w = new Mesh(new CylinderGeometry(0.28, 0.28, 0.2, 14), trimMat);
    w.rotation.x = Math.PI / 2;
    w.position.set(wx, 0.28, wz);
    g.add(w);
  }
  return g;
}

function buildFlyingSquadVan() {
  const g = new Group();
  const vanMat = mat(0xf1f5f9, 0.4, 0.2);
  const stripeMat = mat(0xe11d48, 0.5, 0.2);
  const tireMat = mat(0x111827, 0.85);
  addBox(g, 2.6, 1.15, 1.25, vanMat, 0, 0.85, 0);
  addBox(g, 2.64, 0.22, 1.27, stripeMat, 0, 0.75, 0);
  addBox(g, 0.7, 0.5, 1.18, mat(0x0f172a, 0.15, 0.8), 1.0, 1.15, 0);
  const redBeacon = new Mesh(new BoxGeometry(0.24, 0.18, 0.35), new MeshBasicMaterial({ color: 0xef4444 }));
  redBeacon.position.set(0.3, 1.52, 0.25);
  const blueBeacon = new Mesh(new BoxGeometry(0.24, 0.18, 0.35), new MeshBasicMaterial({ color: 0x3b82f6 }));
  blueBeacon.position.set(0.3, 1.52, -0.25);
  g.add(redBeacon, blueBeacon);
  addSignBoard(g, "ELECTION FLYING SQUAD", "IT RAID · GETHU SEIZE", "#7f1d1d", "#fde047", 1.85, 0.48, -0.1, 1.0, 0.65);
  for (const [wx, wz] of [[0.82, 0.62], [0.82, -0.62], [-0.82, 0.62], [-0.82, -0.62]]) {
    const w = new Mesh(new CylinderGeometry(0.27, 0.27, 0.2, 14), tireMat);
    w.rotation.x = Math.PI / 2;
    w.position.set(wx, 0.27, wz);
    g.add(w);
  }
  return { group: g, redBeacon, blueBeacon };
}

function buildStudioLightRig() {
  const g = new Group();
  const metalMat = mat(0x374151, 0.35, 0.85);
  const bulbMat = new MeshBasicMaterial({ color: 0xfef9c3 });
  addBox(g, 1.7, 0.22, 1.2, metalMat, 0, 0.8, 0);
  const barrel = new Mesh(new CylinderGeometry(0.52, 0.68, 0.95, 14), metalMat);
  barrel.position.set(0, 0.22, 0);
  const lens = new Mesh(new CylinderGeometry(0.62, 0.62, 0.08, 14), bulbMat);
  lens.position.set(0, -0.25, 0);
  const cone = new Mesh(
    new ConeGeometry(1.35, 2.4, 16, 1, true),
    new MeshBasicMaterial({ color: 0xfef08a, transparent: true, opacity: 0.22, side: DoubleSide, depthWrite: false })
  );
  cone.position.set(0, -1.4, 0);
  g.add(barrel, lens, cone);
  return g;
}

export function triggerKootaniAssist(battle, playerSide) {
  if (!battle || battle._kootaniHazard) return false;
  const caster = battle.fighters[playerSide];
  const target = battle.fighters[playerSide === 0 ? 1 : 0];
  if (!caster || !target) return false;

  const picked = (typeof window !== "undefined" && window.__selectedAssist) || "random";
  const pool = ["sumo", "squad", "light"];
  const kind = pool.includes(picked) ? picked : pool[Math.floor(Math.random() * pool.length)];

  const dir = target.x >= caster.x ? 1 : -1;
  const startX = caster.x - dir * 4.5;
  const targetX = target.x;
  const scene = battle.ctx?.scene;
  if (!scene) return false;

  const root = new Group();
  let extra = null;
  if (kind === "sumo") {
    const sumo = buildSumoMesh();
    sumo.rotation.y = dir > 0 ? 0 : Math.PI;
    root.add(sumo);
    extra = { sumo };
  } else if (kind === "squad") {
    const van = buildFlyingSquadVan();
    van.group.rotation.y = dir > 0 ? 0 : Math.PI;
    root.add(van.group);
    extra = van;
  } else {
    const light = buildStudioLightRig();
    const warn = new Mesh(
      new RingGeometry(0.65, 0.95, 24),
      new MeshBasicMaterial({ color: 0xef4444, side: DoubleSide, transparent: true, opacity: 0.8 })
    );
    warn.rotation.x = -Math.PI / 2;
    warn.position.set(0, 0.04, 0);
    root.add(light, warn);
    extra = { light, warn };
  }
  scene.add(root);

  battle._kootaniHazard = {
    kind,
    root,
    extra,
    t: 0,
    duration: 2.0,
    hitAt: 0.85,
    hitDone: false,
    dir,
    startX,
    targetX,
    casterSide: playerSide,
    targetSide: target.side
  };

  const titleMap = {
    sumo: "🚙 KOOTANI: FLYING SUMO ENTRY!<small>Kollywood Villain Assist!</small>",
    squad: "🚨 IT RAID: ELECTION FLYING SQUAD!<small>-20% Opponent Gethu Confiscated!</small>",
    light: "💡 SET HAZARD: GIANT STUDIO LIGHT!<small>Watch Out Overhead!</small>"
  };
  battle.ctx?.hud?.say(titleMap[kind], "cow", 1500);
  battle.ctx?.audio?.newsSting?.();
  if (kind === "sumo") {
    battle.speech?.(playerSide, "Pushpa Pushparaj... Thaggedhe Le!");
    battle.ctx?.audio?.horn?.(0.35);
    battle.ctx?.audio?.playClip?.("/assets/memes/trump_1.mp3", 0.95);
  } else if (kind === "squad") {
    battle.speech?.(playerSide, "Main itna lehsun pyaaz nahi khati hoon ji!");
    battle.ctx?.audio?.playClip?.("/assets/nirmala-Dq7cz8UN.mp3", 0.95);
  } else {
    battle.speech?.(playerSide, "Dhairiyam purusha latchanam! Naan ungalai sollavillai!");
    battle.ctx?.audio?.playClip?.("/assets/rangaraj-super.mp3", 0.95);
  }
  pushFanWarComment({ kind: "assist", attacker: caster.char.id });
  return true;
}

export function updateKootaniAssist(battle, dt) {
  const hz = battle?._kootaniHazard;
  if (!hz) return;
  hz.t += dt;
  const p = Math.min(1, hz.t / hz.duration);
  const target = battle.fighters[hz.targetSide];
  const fx = battle.ctx?.fx;
  const hud = battle.ctx?.hud;
  const audio = battle.ctx?.audio;
  const cam = battle.ctx?.cam;

  if (hz.kind === "sumo") {
    const curX = hz.startX + (hz.targetX + hz.dir * 5.2 - hz.startX) * p;
    const arcY = Math.sin(p * Math.PI) * 3.2;
    hz.root.position.set(curX, arcY, 0.35);
    hz.extra.sumo.rotation.z = hz.dir * (p * Math.PI * 1.4 - 0.3);
  } else if (hz.kind === "squad") {
    const curX = hz.startX + (hz.targetX + hz.dir * 6.5 - hz.startX) * easeOutQuad(p);
    hz.root.position.set(curX, 0, 0.45);
    const blink = Math.floor(hz.t * 14) % 2 === 0;
    hz.extra.redBeacon.visible = blink;
    hz.extra.blueBeacon.visible = !blink;
  } else {
    const dropP = hz.t < hz.hitAt ? hz.t / hz.hitAt : 1;
    const fallY = hz.t < hz.hitAt ? 7.5 * (1 - dropP * dropP * dropP) : 0.3;
    hz.root.position.set(hz.targetX, 0, 0.15);
    hz.extra.light.position.set(0, fallY, 0);
    hz.extra.warn.visible = hz.t < hz.hitAt;
    hz.extra.warn.scale.setScalar(1 + Math.sin(hz.t * 20) * 0.15);
  }

  if (!hz.hitDone && hz.t >= hz.hitAt && target && target.hp > 0) {
    hz.hitDone = true;
    const pos = new Vector3(target.x, 1.15, 0.3);
    const dmg = hz.kind === "light" ? 22 : hz.kind === "sumo" ? 20 : 16;
    target.hp = Math.max(1, target.hp - dmg);
    target.forceState("knockdown");
    target.vx = hz.dir * (hz.kind === "sumo" ? 7.2 : 5.4);
    target.vy = hz.kind === "sumo" ? 8.2 : 5.6;
    target.grounded = false;
    target.downFrames = 0;

    if (hz.kind === "squad") {
      // Election Flying Squad confiscates 20% of opponent's Gethu meter
      target.meter = Math.max(0, target.meter - 20);
    }

    try {
      fx?.hitSpark?.(pos, 1.7, false, hz.dir);
      fx?.shockwave?.(pos, hz.kind === "squad" ? 0xef4444 : 0xfacc15, 0.45, 1.4, true);
      fx?.particles?.emit(pos, { count: 48, speed: 6.5, color: hz.kind === "squad" ? 0x3b82f6 : 0xfacc15, life: 0.65, size: 0.24 });
      cam?.shake?.(0.32, 0.38);
      audio?.boom?.();
      const sc = battle.ctx?.toScreen?.(pos);
      if (sc && hud) {
        const msg = hz.kind === "squad" ? "🚨 IT RAID! -20% GETHU!" : hz.kind === "sumo" ? "🚙 FLYING SUMO SLAM!" : "💡 STUDIO LIGHT CRASH!";
        hud.popup(msg, sc.x, sc.y - 30, "#facc15");
      }
    } catch {}
  }

  if (hz.t >= hz.duration) {
    battle.ctx?.scene?.remove(hz.root);
    battle._kootaniHazard = null;
  }
}

function easeOutQuad(t) {
  return 1 - (1 - t) * (1 - t);
}

/* ============================================================================
 * 3. ARCHETYPE: ORATOR 3D SOUNDWAVE RINGS (J,J,J)
 * ============================================================================ */
export function spawnOratorSoundwave(battle, fighter, moveId) {
  const sceneGroup = battle?.ctx?.arena?.group || battle?.ctx?.scene;
  if (!sceneGroup || !fighter) return;
  const dir = fighter.facing || 1;
  const ax = fighter.x || 0;
  const ay = (fighter.y || 0) + 1.25;
  const color = moveId === "uppercut" ? 0xfacc15 : 0x22d3ee;

  const waveGroup = new Group();
  const mats = [];
  for (let i = 0; i < 3; i++) {
    const rMat = new MeshBasicMaterial({ color, transparent: true, opacity: 0.9 - i * 0.15, side: DoubleSide });
    mats.push(rMat);
    const ring = new Mesh(new TorusGeometry(0.24 + i * 0.12, 0.032, 8, 24), rMat);
    ring.rotation.y = Math.PI / 2;
    ring.position.x = dir * i * 0.24;
    waveGroup.add(ring);
  }
  waveGroup.position.set(ax + dir * 0.55, ay, 0.2);
  sceneGroup.add(waveGroup);

  const t0 = performance.now();
  const stepWave = () => {
    const p = Math.min(1, (performance.now() - t0) / 320);
    waveGroup.position.x = ax + dir * (0.55 + p * 2.15);
    waveGroup.scale.setScalar(1 + p * 1.45);
    for (let i = 0; i < mats.length; i++) mats[i].opacity = (0.9 - i * 0.15) * (1 - p);
    if (p < 1) {
      requestAnimationFrame(stepWave);
    } else {
      sceneGroup.remove(waveGroup);
      mats.forEach((m) => m.dispose());
    }
  };
  requestAnimationFrame(stepWave);
}

/* ============================================================================
 * 4. ACTIVE 3D ARENA HAZARDS (MARINA WAVE, KOYAMBEDU AUTO BOUNCE, STUDIO MIC MUTED)
 * ============================================================================ */
export function updateSouthStageHazards(arena, battle, time, dt) {
  if (typeof window !== "undefined") window.__marinaWaveSlip = false;
  if (!arena || !battle || battle.phase !== "fight") return;
  const stage = arena.stage;
  const stageGroups = arena.themeGroups;

  if (stage === "marina" || stage === "sansad") {
    const mg = stageGroups?.marina;
    if (mg?.userData?.lighthouseBeam) {
      mg.userData.lighthouseBeam.rotation.y = time * 1.4;
    }
    const wave = mg?.userData?.marinaWave;
    if (wave && stage === "marina") {
      const cycle = time % 20;
      if (cycle < 4.5) {
        if (typeof window !== "undefined") window.__marinaWaveSlip = true;
        wave.visible = true;
        const p = cycle / 4.5;
        const wash = Math.sin(p * Math.PI);
        wave.position.z = -12 + wash * 13.0;
        wave.position.y = -0.08 + wash * 0.14;
        if (!arena._waveNotified) {
          arena._waveNotified = true;
          const sc = battle.ctx?.toScreen?.(new Vector3(0, 2.0, 0));
          if (sc) battle.ctx?.hud?.popup("🌊 MARINA WAVE! LOW FRICTION SAND!", sc.x, sc.y, "#38bdf8");
          pushFanWarComment({ kind: "hit", custom: "🌊 Marina Wave hit the beach! Fighters sliding everywhere!" });
        }
      } else {
        wave.visible = false;
        arena._waveNotified = false;
      }
    }
  }

  if (stage === "jantar") {
    // Koyambedu / Kilambakkam Bus Stand: corner Auto-Rickshaw bounce!
    const bg = stageGroups?.jantar;
    const leftAuto = bg?.userData?.leftAuto;
    const rightAuto = bg?.userData?.rightAuto;
    for (const auto of [leftAuto, rightAuto]) {
      if (!auto) continue;
      if (auto.bumpTimer > 0) {
        auto.bumpTimer = Math.max(0, auto.bumpTimer - dt);
        const kick = Math.sin((auto.bumpTimer / 0.35) * Math.PI) * 0.75;
        auto.group.position.x = auto.baseX + (auto.baseX < 0 ? kick : -kick);
        auto.headlight.scale.setScalar(1.6);
      } else {
        auto.group.position.x = auto.baseX;
        auto.headlight.scale.setScalar(1.0);
      }
    }

    if (!battle._autoCooldown) battle._autoCooldown = [0, 0];
    for (const f of battle.fighters) {
      battle._autoCooldown[f.side] = Math.max(0, battle._autoCooldown[f.side] - dt);
      if (Math.abs(f.x) >= 6.05 && battle._autoCooldown[f.side] <= 0 && (f.state === "hitstun" || f.state === "knockdown" || Math.abs(f.vx) > 0.2)) {
        battle._autoCooldown[f.side] = 1.1;
        const dirToCenter = f.x < 0 ? 1 : -1;
        f.x = -dirToCenter * 5.75;
        f.vx = dirToCenter * 8.6;
        f.vy = Math.max(f.vy, 4.6);
        f.grounded = false;
        const auto = dirToCenter > 0 ? leftAuto : rightAuto;
        if (auto) auto.bumpTimer = 0.35;
        try {
          const pos = new Vector3(f.x, 1.1, 0.25);
          battle.ctx?.fx?.hitSpark?.(pos, 1.2, false, dirToCenter);
          battle.ctx?.audio?.hit?.(0.8);
          const sc = battle.ctx?.toScreen?.(pos);
          if (sc) battle.ctx?.hud?.popup("🛺 AUTO RICKSHAW BOUNCE!", sc.x, sc.y - 25, "#facc15");
        } catch {}
      }
    }
  }

  if (stage === "road") {
    // Prime Time Debate Studio: giant LED screens flash "MIC MUTED!" whenever a fighter gets stunned
    const led = stageGroups?.road?.userData?.studioLed;
    if (led) {
      const anyStunned = battle.fighters.some((f) => f.state === "hitstun" || f.state === "knockdown");
      if (anyStunned) {
        if (led.mutedTimer <= 0) {
          const sc = battle.ctx?.toScreen?.(new Vector3(0, 2.4, 0));
          if (sc) battle.ctx?.hud?.popup("🔇 MIC MUTED!", sc.x, sc.y, "#ef4444");
        }
        led.mutedTimer = 1.1;
      } else {
        led.mutedTimer = Math.max(0, led.mutedTimer - dt);
      }
      const tex = led.mutedTimer > 0 ? led.mutedTex : led.liveTex;
      for (const m of led.ledMaterials) {
        if (m.map !== tex) {
          m.map = tex;
          m.needsUpdate = true;
        }
      }
    }
  }
}

/* ============================================================================
 * 5. CENSOR BOARD / ELECTION COMMISSION BOSS AURA + BOX OFFICE TANGISH ROAST
 * ============================================================================ */
export function updateCensorBossMechanic(battle, dt) {
  if (typeof window !== "undefined") window.__censorLock = null;
  const badge = typeof document !== "undefined" ? document.getElementById("censor-lock-badge") : null;
  const boss = battle?.boss;
  if (!boss || battle.phase !== "fight") {
    if (badge) badge.classList.add("hidden");
    return;
  }

  if (!battle._censorState) {
    const ring = new Mesh(
      new RingGeometry(0.95, 1.25, 6),
      new MeshBasicMaterial({ color: 0xef4444, side: DoubleSide, transparent: true, opacity: 0.75 })
    );
    ring.rotation.x = -Math.PI / 2;
    const card = new Mesh(
      new BoxGeometry(0.45, 0.65, 0.06),
      new MeshBasicMaterial({ color: 0xdc2626 })
    );
    card.position.y = 2.35;
    const grp = new Group();
    grp.add(ring, card);
    battle.ctx?.scene?.add(grp);
    battle._censorState = { timer: 5.0, lockRemaining: 0, lockedKey: "kick", brokenCooldown: 0, grp, card, ring };
  }

  const cs = battle._censorState;
  cs.grp.position.set(boss.x, 0.05, 0);
  cs.ring.rotation.z += dt * 1.8;
  cs.card.rotation.y += dt * 3.0;
  cs.card.visible = cs.lockRemaining > 0;

  if (cs.brokenCooldown > 0) cs.brokenCooldown -= dt;
  if (cs.lockRemaining > 0) {
    cs.lockRemaining = Math.max(0, cs.lockRemaining - dt);
    if (typeof window !== "undefined") {
      window.__censorLock = { key: cs.lockedKey, remaining: cs.lockRemaining };
    }
    if (badge) {
      badge.classList.remove("hidden");
      badge.textContent = `🟥 CENSOR RED CARD: ${cs.lockedKey === "kick" ? "KICK [K]" : "SPECIAL [L]"} LOCKED (${cs.lockRemaining.toFixed(1)}s) · GRAB [I] TO BREAK!`;
    }
  } else {
    if (badge) badge.classList.add("hidden");
    if (cs.brokenCooldown <= 0) {
      cs.timer -= dt;
      if (cs.timer <= 0) {
        cs.timer = 7.5;
        cs.lockedKey = cs.lockedKey === "kick" ? "super" : "kick";
        cs.lockRemaining = 4.0;
        const sc = battle.ctx?.toScreen?.(new Vector3(boss.x, 2.5, 0));
        if (sc) battle.ctx?.hud?.popup(`🟥 MODEL CODE RED CARD! ${cs.lockedKey.toUpperCase()} LOCKED!`, sc.x, sc.y, "#ef4444");
        battle.speech?.(boss.side, "Model Code of Conduct! Button CENSORED for 4s!");
        pushFanWarComment({ kind: "super", custom: "🟥 Election Commission Boss showed RED CARD! Grab [I] to break!" });
      }
    }
  }
}

export function onCensorBossGrabBreak(battle, attacker, defender) {
  if (!battle?._censorState || !defender?.isBoss) return;
  const cs = battle._censorState;
  const wasLocked = cs.lockRemaining > 0;
  cs.lockRemaining = 0;
  cs.brokenCooldown = 6.5;
  cs.timer = 7.5;
  if (typeof window !== "undefined") window.__censorLock = null;
  const badge = typeof document !== "undefined" ? document.getElementById("censor-lock-badge") : null;
  if (badge) badge.classList.add("hidden");
  if (wasLocked) {
    defender.hp = Math.max(1, defender.hp - 8);
    const pos = new Vector3(defender.x, 1.5, 0.3);
    battle.ctx?.fx?.shockwave?.(pos, 0xfacc15, 0.45, 1.4, true);
    const sc = battle.ctx?.toScreen?.(pos);
    if (sc) battle.ctx?.hud?.popup("⚖️ CENSOR LOCK BROKEN BY GRAB!", sc.x, sc.y - 30, "#facc15");
    pushFanWarComment({ kind: "super", custom: "⚖️ Player shattered Censor Red Card with a GRAB! Mass comeback!" });
  }
}

export function computeBoxOfficeVerdict(winnerId, loserId, wins, stats = {}) {
  const maxW = Math.max(...(wins || [2, 0]));
  const minW = Math.min(...(wins || [2, 0]));
  const margin = maxW - minW;
  const maxCombo = stats.maxCombo || 0;
  const kicks = stats.kicks || 0;
  const punches = stats.punches || 0;
  const supers = stats.supers || 0;
  const grabs = stats.grabs || 0;

  let crores = 350 + maxW * 200 + margin * 120 + maxCombo * 35 + supers * 80;
  if (crores >= 950) crores = 1000 + (maxCombo * 12);

  let roast = "";
  if (kicks > punches + 3 && kicks >= 5) {
    roast = "Full match verum kaal-la ye adichi jeichitaan! Leg day skipped-aa illa opponent face-aa?!";
  } else if (punches > kicks + 4 && punches >= 6) {
    roast = "Verum kai-la ye kuthu-kuthu-nu kuthitaan! Rohini balcony-la kooda sound kettudhu!";
  } else if (grabs >= 2) {
    roast = "Collar-a pudichu pottu thallitaan macha! Zero chill, full kootani grapple!";
  } else if (supers >= 2) {
    roast = "Gethu meter full-a erichu CGI blast panni thookitaan! Budget ₹1000 Crore!";
  } else if (maxCombo >= 5) {
    roast = `${maxCombo}-Hit Paal Abhishekam combo! Blue Shirt Maran kooda 5/5 kuduthutaan!`;
  } else if (margin >= 2) {
    roast = "Clean sweep macha! Tea kadai-la samosa vaangi kondaadunga!";
  } else {
    roast = "Last second climax twist! Filter kaapi kudichutte nail-biter win!";
  }

  const club = crores >= 1000 ? `₹${crores} CRORE CLUB! 🏆` : `₹${crores} CRORES BLOCKBUSTER!`;
  return {
    crores,
    clubText: `Total Collection: ${club}`,
    roast,
    reviewScore: maxCombo >= 5 || margin >= 2 ? "5/5 VERITHANAM" : "3.5/5 MASS INTERVAL"
  };
}

export function cleanupSouthBattle(battle) {
  if (!battle) return;
  if (battle._kootaniHazard?.root) {
    battle.ctx?.scene?.remove(battle._kootaniHazard.root);
    battle._kootaniHazard = null;
  }
  if (battle._censorState?.grp) {
    battle.ctx?.scene?.remove(battle._censorState.grp);
    battle._censorState = null;
  }
  if (typeof window !== "undefined") {
    window.__censorLock = null;
    window.__marinaWaveSlip = false;
  }
  const badge = typeof document !== "undefined" ? document.getElementById("censor-lock-badge") : null;
  if (badge) badge.classList.add("hidden");
  const feed = typeof document !== "undefined" ? document.getElementById("fanwar-feed") : null;
  if (feed) feed.replaceChildren();
}
