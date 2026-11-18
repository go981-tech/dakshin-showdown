import { buildCharacterClip, scheduleFXCleanup } from "./_animBuilder.js";

export const FIGHTER_IDS = Object.freeze([
  "modi",
  "rahul",
  "didi",
  "trump",
  "yogi",
  "nitin",
  "ravi",
  "lalu",
  "mbapu",
  "amit",
  "dhruv",
  "nirmala",
  "rangaraj"
]);

export const FIGHTER_SPECIALS = Object.freeze({
  modi: { special1: "DRAVIDA PALM", special2: "RED-BLACK STRIKE", super: "VIDIYAL CYCLE RALLY", accent: 0xe11d48 },
  rahul: { special1: "AUDIO LAUNCH PUNCH", special2: "KUTHU FLYING KICK", super: "LEO 1000CR", accent: 0xdc2626 },
  didi: { special1: "AMMA CANTEEN SLAP", special2: "PALLU WHIP KICK", super: "POES GARDEN THRONE", accent: 0x16a34a },
  trump: { special1: "SHOULDER TILT PUNCH", special2: "CHITTOOR KICK", super: "THAGGEDHE LE AXE", accent: 0xea580c },
  yogi: { special1: "LAL SALAM PUNCH", special2: "SILVERLINE KICK", super: "SILVERLINE EXPRESS", accent: 0xb91c1c },
  nitin: { special1: "ORR GRIDLOCK UPPER", special2: "TUNNEL ROAD KICK", super: "SILK BOARD 999", accent: 0x0284c7 },
  ravi: { special1: "PAWAN PUNCH", special2: "POWER STAR KICK", super: "HUNGRY CHEETAH OG", accent: 0xdc2626 },
  lalu: { special1: "SIGNAL PALM", special2: "VAIGAI EXPRESS KICK", super: "MIKE SET PULI ROAR", accent: 0xeab308 },
  mbapu: { special1: "QUESTION EVERYTHING", special2: "FLYING THATHA", super: "VAIKOM TORCH CHAKRA", accent: 0xfacc15 },
  amit: { special1: "ENNA SIR ITHU", special2: "KARNATAKA CADRE KICK", super: "PRESS MEET FILES", accent: 0xf97316 },
  dhruv: { special1: "RED ARROW PUNCH", special2: "VIRAL SHORTS KICK", super: "10M CLICKBAIT HOUNDS", accent: 0x22d3ee },
  nirmala: { special1: "18% POPCORN SLAP", special2: "28% CARAMEL KICK", super: "28% CARAMEL GST BLAST", accent: 0xa855f7 },
  rangaraj: { special1: "ENNA BATHIL", special2: "LIVE BREAK KICK", super: "KELVIKKU ENNA BATHIL", accent: 0x38bdf8 }
});

export const SPECIAL_REGISTRY = FIGHTER_SPECIALS;

function clipFrames(id, kind) {
  const heavy = ["modi", "didi", "yogi", "nitin", "lalu", "mbapu", "nirmala"].includes(id);
  const orator = ["lalu", "mbapu", "dhruv", "rangaraj"].includes(id);
  const rightPower = kind === "special2" ? 1 : kind === "super" ? 1.35 : 0.9;
  const leftPower = kind === "special1" ? 1.15 : kind === "super" ? 1.25 : 0.72;
  const duration = kind === "super" ? 3.0 : kind === "special2" ? 1.45 : 1.25;
  return {
    duration,
    frames: [
      {
        time: duration * 0.18,
        hips: [0, 0.03 * (heavy ? 1.35 : 1), 0],
        bones: {
          Hips: { rotation: [0.04, kind === "special2" ? -0.18 : 0.12, kind === "special2" ? 0.08 : -0.05] },
          Spine: { rotation: [kind === "special1" ? -0.12 : -0.06, kind === "special2" ? 0.22 : -0.12, 0] },
          Spine2: { rotation: [kind === "super" ? -0.16 : -0.08, kind === "special2" ? 0.25 : -0.14, 0] },
          RightArm: { rotation: [-rightPower * 0.7, 0.08, -0.18] },
          RightForeArm: { rotation: [0, -rightPower * 0.7, 0] },
          LeftArm: { rotation: [leftPower * 0.32, -0.18, 0.14] },
          LeftForeArm: { rotation: [0, leftPower * 0.42, 0] }
        }
      },
      {
        time: duration * (kind === "super" ? 0.58 : 0.48),
        hips: [kind === "special2" ? 0.08 : -0.02, heavy ? 0.08 : 0.04, kind === "special1" ? -0.03 : 0],
        bones: {
          Hips: { rotation: [0.08, kind === "special2" ? -0.34 : 0.24, kind === "super" ? 0.12 : 0] },
          Spine: { rotation: [-0.22, kind === "special2" ? 0.38 : -0.28, kind === "super" ? 0.12 : 0] },
          Spine2: { rotation: [-0.28, kind === "special2" ? 0.42 : -0.34, 0] },
          Neck: { rotation: [0.08, kind === "special2" ? -0.18 : 0.12, 0] },
          RightArm: { rotation: [-rightPower * 1.35, 0.18, -0.38] },
          RightForeArm: { rotation: [0, -rightPower * 1.1, 0] },
          RightHand: { rotation: [0, 0, kind === "special1" ? -0.22 : 0] },
          LeftArm: { rotation: [leftPower * 0.58, -0.28, 0.28] },
          LeftForeArm: { rotation: [0, leftPower * 0.72, 0] },
          RightUpLeg: { rotation: [kind === "special2" ? -0.72 : -0.18, 0, kind === "special2" ? -0.12 : 0] },
          RightLeg: { rotation: [kind === "special2" ? 1.05 : 0.22, 0, 0] },
          LeftUpLeg: { rotation: [kind === "special2" ? 0.2 : -0.12, 0, 0.04] },
          LeftLeg: { rotation: [kind === "special1" ? 0.45 : 0.18, 0, 0] }
        }
      },
      {
        time: duration * (kind === "super" ? 0.82 : 0.78),
        hips: [0, 0.02, 0],
        bones: {
          Hips: { rotation: [0.02, kind === "special2" ? -0.12 : 0.08, 0] },
          Spine: { rotation: [-0.08, kind === "special2" ? 0.16 : -0.12, 0] },
          RightArm: { rotation: [-0.42, 0.08, -0.12] },
          RightForeArm: { rotation: [0, -0.38, 0] },
          LeftArm: { rotation: [0.28, -0.12, 0.12] },
          LeftForeArm: { rotation: [0, 0.22, 0] }
        }
      }
    ],
    fxCleanupAt: kind === "super"
      ? [duration * 0.82, duration]
      : [duration * 0.78, duration],
    kind
  };
}

export function buildClips(scene, fighterId) {
  if (!scene) return [];
  const ids = fighterId ? [fighterId] : FIGHTER_IDS;
  const clips = [];
  for (const id of ids) {
    if (!FIGHTER_SPECIALS[id]) continue;
    scene.userData = scene.userData || {};
    scene.userData.fighterId = id;
    for (const kind of ["special1", "special2", "super"]) {
      const preset = clipFrames(id, kind);
      clips.push(buildCharacterClip(scene, {
        name: `south_${kind}_${id}`,
        fighterId: id,
        duration: preset.duration,
        frames: preset.frames,
        fxCleanupAt: preset.fxCleanupAt,
        kind,
        returnToClean: true
      }));
    }
  }
  return clips;
}

export function triggerSpecial(optionsOrId, slot = "special1", scene = null, mixer = null) {
  let id;
  let kind = slot;
  let targetScene = scene;
  let targetMixer = mixer;
  if (typeof optionsOrId === "object" && optionsOrId !== null) {
    id = optionsOrId.id || optionsOrId.fighterId;
    kind = optionsOrId.slot || optionsOrId.kind || kind;
    targetScene = optionsOrId.scene || targetScene;
    targetMixer = optionsOrId.mixer || targetMixer;
  } else {
    id = optionsOrId;
  }
  const name = `south_${kind}_${id}`;
  if (targetMixer?.clipAction) {
    const clip = targetScene?.__southSpecialClips?.[name]
      || targetScene?.userData?.southSpecialClips?.[name];
    const action = clip ? targetMixer.clipAction(clip) : null;
    if (action) {
      action.reset();
      action.setLoop(2201, 1);
      action.clampWhenFinished = true;
      action.fadeIn?.(0.08);
      action.play();
      return action;
    }
  }
  const clip = targetScene?.__southSpecialClips?.[name]
    || targetScene?.userData?.southSpecialClips?.[name]
    || null;
  return clip;
}

export { buildCharacterClip, scheduleFXCleanup };
