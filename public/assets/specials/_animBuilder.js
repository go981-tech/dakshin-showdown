import {
  AnimationClip,
  Euler,
  InterpolateSmooth,
  Quaternion,
  QuaternionKeyframeTrack,
  VectorKeyframeTrack
} from "three";

function stripIdx(name) {
  return String(name || "").replace(/_\d+$/, "");
}

function findBone(scene, name) {
  if (!scene) return null;
  const bare = stripIdx(name);
  let found = null;
  scene.traverse((node) => {
    if (!found && (node.isBone || node.name) && stripIdx(node.name) === bare) found = node;
  });
  return found;
}

function normalizeBoneName(name) {
  return stripIdx(String(name || ""));
}

function vec3Tuple(value) {
  if (!value) return [0, 0, 0];
  if (Array.isArray(value)) return [Number(value[0] || 0), Number(value[1] || 0), Number(value[2] || 0)];
  return [
    Number(value.x || 0),
    Number(value.y || 0),
    Number(value.z || 0)
  ];
}

function collectPoseFrame(frame) {
  if (!frame) return { time: 0, bones: {}, hips: null };
  const time = Number(frame.time ?? frame.t ?? 0);
  const bones = frame.bones || frame.pose || frame;
  const hips = frame.hipsOffset || frame.hips || bones.Hips?.position || bones.Hips?.offset || null;
  return { time, bones, hips };
}

function readDelta(frame, boneName) {
  const entry = frame.bones?.[boneName];
  if (Array.isArray(entry)) return entry;
  if (entry?.rotation) return vec3Tuple(entry.rotation);
  if (entry?.euler) return vec3Tuple(entry.euler);
  if (entry?.delta) return vec3Tuple(entry.delta);
  return [0, 0, 0];
}

export function collectRestMap(scene) {
  const restMap = new Map();
  scene?.updateMatrixWorld(true);
  scene?.traverse((node) => {
    if (!node.isBone) return;
    const name = normalizeBoneName(node.name);
    if (!restMap.has(name)) {
      restMap.set(name, {
        bone: node,
        position: node.position.clone(),
        quaternion: node.quaternion.clone()
      });
    }
  });
  return restMap;
}

export function getNormalizedBoneName(name) {
  return normalizeBoneName(name);
}

export function buildCharacterClip(scene, nameOrOptions, maybeDuration, maybeFrames) {
  const options = typeof nameOrOptions === "string"
    ? { name: nameOrOptions, duration: maybeDuration, frames: maybeFrames }
    : (nameOrOptions || {});
  const name = options.name || "south_custom";
  const duration = Number(options.duration ?? options.length ?? 1.2);
  const returnToClean = options.returnToClean !== false;
  const restMap = collectRestMap(scene);
  const suppliedFrames = options.frames || options.keyframes || options.poses || [];
  const frames = [
    { time: 0, bones: {}, hips: null },
    ...suppliedFrames.map(collectPoseFrame),
    ...(returnToClean ? [{ time: duration, bones: {}, hips: null }] : [])
  ]
    .map((frame) => ({ ...frame, time: Math.max(0, Math.min(duration, Number(frame.time || 0))) }))
    .sort((a, b) => a.time - b.time);

  const times = [];
  for (const frame of frames) {
    if (!times.length || Math.abs(times[times.length - 1] - frame.time) > 1e-5) times.push(frame.time);
  }
  if (!times.includes(duration)) times.push(duration);
  times.sort((a, b) => a - b);

  const boneNames = new Set();
  for (const frame of frames) {
    for (const rawName of Object.keys(frame.bones || {})) {
      const boneName = normalizeBoneName(rawName);
      if (restMap.has(boneName)) boneNames.add(boneName);
    }
  }

  const tracks = [];
  const restEuler = new Euler();
  const targetEuler = new Euler();
  const targetQuat = new Quaternion();

  for (const boneName of boneNames) {
    const rest = restMap.get(boneName);
    if (!rest) continue;
    restEuler.setFromQuaternion(rest.quaternion, "XYZ");

    const quats = new Float32Array(times.length * 4);
    for (let i = 0; i < times.length; i++) {
      const time = times[i];
      let before = frames[0];
      let after = frames[frames.length - 1];
      for (let k = 0; k < frames.length - 1; k++) {
        if (time >= frames[k].time && time <= frames[k + 1].time) {
          before = frames[k];
          after = frames[k + 1];
          break;
        }
      }
      const span = Math.max(1e-5, after.time - before.time);
      const rawT = Math.max(0, Math.min(1, (time - before.time) / span));
      const smoothT = rawT * rawT * (3 - 2 * rawT);
      const beforeDelta = readDelta(before, boneName);
      const afterDelta = readDelta(after, boneName);
      targetEuler.set(
        restEuler.x + (beforeDelta[0] + (afterDelta[0] - beforeDelta[0]) * smoothT),
        restEuler.y + (beforeDelta[1] + (afterDelta[1] - beforeDelta[1]) * smoothT),
        restEuler.z + (beforeDelta[2] + (afterDelta[2] - beforeDelta[2]) * smoothT),
        "XYZ"
      );
      targetQuat.setFromEuler(targetEuler);
      const offset = i * 4;
      quats[offset] = targetQuat.x;
      quats[offset + 1] = targetQuat.y;
      quats[offset + 2] = targetQuat.z;
      quats[offset + 3] = targetQuat.w;
    }
    const track = new QuaternionKeyframeTrack(`${rest.bone.name}.quaternion`, times, quats);
    track.setInterpolation(InterpolateSmooth);
    tracks.push(track);
  }

  if (restMap.has("Hips")) {
    const rest = restMap.get("Hips");
    const positions = new Float32Array(times.length * 3);
    for (let i = 0; i < times.length; i++) {
      const time = times[i];
      let before = frames[0];
      let after = frames[frames.length - 1];
      for (let k = 0; k < frames.length - 1; k++) {
        if (time >= frames[k].time && time <= frames[k + 1].time) {
          before = frames[k];
          after = frames[k + 1];
          break;
        }
      }
      const span = Math.max(1e-5, after.time - before.time);
      const rawT = Math.max(0, Math.min(1, (time - before.time) / span));
      const smoothT = rawT * rawT * (3 - 2 * rawT);
      const beforeOffset = vec3Tuple(before.hips || before.bones?.Hips?.position || before.bones?.Hips?.offset);
      const afterOffset = vec3Tuple(after.hips || after.bones?.Hips?.position || after.bones?.Hips?.offset);
      positions[i * 3] = rest.position.x + beforeOffset[0] + (afterOffset[0] - beforeOffset[0]) * smoothT;
      positions[i * 3 + 1] = rest.position.y + beforeOffset[1] + (afterOffset[1] - beforeOffset[1]) * smoothT;
      positions[i * 3 + 2] = rest.position.z + beforeOffset[2] + (afterOffset[2] - beforeOffset[2]) * smoothT;
    }
    const track = new VectorKeyframeTrack(`${rest.bone.name}.position`, times, positions);
    track.setInterpolation(InterpolateSmooth);
    tracks.push(track);
  }

  const clip = new AnimationClip(name, duration, tracks);
  clip.userData = {
    ...(options.userData || {}),
    fighterId: options.fighterId || null,
    kind: options.kind || null,
    restAware: true,
    fxCleanupAt: (options.fxCleanupAt || options.cleanupAt || options.fxTimes || []).map(Number),
    fxCleanup: typeof options.fxCleanup === "function" ? options.fxCleanup : null
  };
  return clip;
}

export function scheduleFXCleanup(clip, elapsed, cleanup) {
  if (!clip?.userData) return false;
  const times = clip.userData.fxCleanupAt || [];
  const callback = cleanup || clip.userData.fxCleanup;
  if (typeof callback !== "function") return false;
  for (const at of times) {
    if (elapsed >= at && elapsed - 0.05 < at) {
      callback(at);
      return true;
    }
  }
  return false;
}

export function cleanStanceClip(scene, name = "south_clean_stance", duration = 0.8) {
  return buildCharacterClip(scene, {
    name,
    duration,
    frames: [{ time: duration * 0.5, bones: {} }],
    returnToClean: true
  });
}
