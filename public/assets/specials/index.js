import { buildCharacterClip, scheduleFXCleanup } from "./_animBuilder.js";
import * as modi from "./modi.js";
import * as rahul from "./rahul.js";
import * as didi from "./didi.js";
import * as trump from "./trump.js";
import * as yogi from "./yogi.js";
import * as nitin from "./nitin.js";
import * as ravi from "./ravi.js";
import * as lalu from "./lalu.js";
import * as mbapu from "./mbapu.js";
import * as amit from "./amit.js";
import * as dhruv from "./dhruv.js";
import * as nirmala from "./nirmala.js";
import * as rangaraj from "./rangaraj.js";

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

export const SPECIAL_MODULES = Object.freeze({
  modi, rahul, didi, trump, yogi, nitin, ravi, lalu, mbapu, amit, dhruv, nirmala, rangaraj
});

export function buildClips(scene, fighterId) {
  if (!scene) return [];
  const ids = fighterId ? [fighterId] : FIGHTER_IDS;
  const clips = [];
  for (const id of ids) {
    const module = SPECIAL_MODULES[id];
    if (!FIGHTER_SPECIALS[id] || !module?.buildClips) continue;
    scene.userData = scene.userData || {};
    scene.userData.fighterId = id;
    clips.push(...module.buildClips(scene));
  }
  return clips;
}

export function triggerSpecialFx(battle, attacker, target, moveId, elapsedSec = 0) {
  const id = attacker?.char?.id;
  const module = id ? SPECIAL_MODULES[id] : null;
  if (!module?.fx) return false;
  const kind = moveId === "finisher" ? "super" : (moveId || "special1");
  module.fx(battle, attacker, target, kind, elapsedSec);
  return true;
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
  if (kind === "finisher") kind = "super";
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
