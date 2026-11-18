const FIGHTER_IDS = Object.freeze([
  "modi", "rahul", "didi", "trump", "yogi", "nitin", "ravi",
  "lalu", "mbapu", "amit", "dhruv", "nirmala", "rangaraj"
]);

const SPECIAL_SLOTS = Object.freeze(["special1", "special2", "super"]);
const SUBTITLE_DURATION_MS = 3000;

let overlay = null;
let voiceLinesPromise = null;
let showcaseTimer = null;
let showcaseResolve = null;
let showcaseRunning = false;
let showcaseCancelled = false;
let showcaseStep = null;
let activeSync = null;
let logs = [];
let events = [];
let showcaseActionTimers = [];
let showcaseActions = [];

function loadVoiceLines() {
  if (!voiceLinesPromise) {
    voiceLinesPromise = fetch("/assets/voice-lines.json")
      .then((response) => {
        if (!response.ok) throw new Error(`voice-lines.json HTTP ${response.status}`);
        return response.json();
      })
      .catch((error) => {
        voiceLinesPromise = null;
        return null;
      });
  }
  return voiceLinesPromise;
}

function ensureOverlay() {
  if (overlay) return overlay;
  overlay = document.createElement("div");
  overlay.id = "south-debug-overlay";
  overlay.setAttribute("role", "status");
  Object.assign(overlay.style, {
    position: "fixed",
    right: "12px",
    bottom: "12px",
    zIndex: "2147483000",
    minWidth: "290px",
    maxWidth: "420px",
    maxHeight: "220px",
    overflow: "auto",
    padding: "8px 10px",
    borderRadius: "8px",
    background: "rgba(12, 12, 16, 0.92)",
    color: "#f8fafc",
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
    fontSize: "11px",
    lineHeight: "1.35",
    border: "1px solid rgba(148, 163, 184, 0.35)",
    boxShadow: "0 6px 24px rgba(0,0,0,.35)",
    pointerEvents: "none"
  });
  document.body.appendChild(overlay);
  return overlay;
}

function removeOverlay() {
  if (overlay?.isConnected) overlay.remove();
  overlay = null;
}

function text(el, label, value) {
  return `${label}: ${value == null || value === "" ? "-" : value}`;
}

function renderOverlay() {
  if (!overlay) return;
  const sync = activeSync;
  const syncDuration = sync?.audioDurationMs;
  const subtitleDuration = sync?.subtitleDurationMs ?? (sync ? SUBTITLE_DURATION_MS : null);
  const mismatch = sync && syncDuration != null
    ? Math.abs(subtitleDuration - syncDuration) > 200
    : false;
  const warnings = logs.filter((entry) => entry.level === "warning" || entry.level === "error").slice(-5);
  const lines = [];
  if (sync) {
    lines.push(`<b>F9 DIALOGUE SYNC</b>`);
    lines.push(text(null, "lineId", sync.lineId));
    lines.push(text(null, "priority", sync.priority));
    lines.push(text(null, "approved", String(sync.approved)));
    lines.push(text(null, "match/speaker", `${sync.matchScore.toFixed(2)} / ${sync.speakerScore.toFixed(2)}`));
    lines.push(text(null, "subtitle", sync.subtitleStartMs == null ? "-" : `${sync.subtitleStartMs.toFixed(0)} -> ${sync.subtitleEndMs.toFixed(0)} ms`));
    lines.push(text(null, "audio", sync.audioStartMs == null ? "-" : `${sync.audioStartMs.toFixed(0)} -> ${sync.audioEndMs.toFixed(0)} ms`));
    if (sync.dropped) lines.push(`<span style="color:#ef4444"><b>RED WARNING: line dropped</b></span>`);
    if (mismatch) lines.push(`<span style="color:#ef4444"><b>RED WARNING: subtitle/audio duration differs ${Math.round(Math.abs(subtitleDuration - syncDuration))}ms</b></span>`);
  } else {
    lines.push("<b>F9 DIALOGUE SYNC</b>");
    lines.push("Waiting for sayLine...");
  }
  if (showcaseRunning) {
    lines.push(`<b>F10 SHOWCASE</b>`);
    lines.push(showcaseStep || "Starting...");
  }
  if (warnings.length) {
    lines.push("<b>WARNINGS</b>");
    for (const warning of warnings) {
      const color = warning.level === "error" ? "#ef4444" : "#facc15";
      lines.push(`<span style="color:${color}">${escapeHtml(warning.message)}</span>`);
    }
  }
  overlay.innerHTML = lines.join("<br>");
}

function escapeHtml(value) {
  return String(value).replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function addLog(level, message, detail) {
  const entry = { level, message, detail };
  logs.push(entry);
  if (logs.length > 40) logs.shift();
  if (level === "warning") console.warn(`[South Debug] ${message}`, detail || "");
  if (level === "error") console.error(`[South Debug] ${message}`, detail || "");
  renderOverlay();
}

function recordDropped(payload) {
  activeSync = {
    lineId: payload.lineId,
    priority: payload.priority,
    approved: payload.approved !== false,
    matchScore: 0,
    speakerScore: 0,
    subtitleStartMs: performance.now(),
    subtitleEndMs: performance.now(),
    audioStartMs: null,
    audioEndMs: null,
    audioDurationMs: null,
    subtitleDurationMs: 0,
    dropped: true
  };
  addLog("warning", `Line dropped: ${payload.lineId}`, payload.reason || "");
  renderOverlay();
}

function recordDialogue(payload) {
  const now = performance.now();
  const entry = payload.entry || {};
  const fighterId = payload.fighterId || "";
  const textMatch = payload.text && entry.text
    ? payload.text === entry.text ? 1 : 0.5
    : entry.text ? 0.5 : 0;
  const matchScore = typeof entry.matchScore === "number" ? entry.matchScore : textMatch;
  const speakerScore = typeof entry.speakerScore === "number"
    ? entry.speakerScore
    : fighterId && payload.expectedFighterId ? (fighterId === payload.expectedFighterId ? 1 : 0) : 1;
  activeSync = {
    lineId: payload.lineId,
    priority: payload.priority,
    approved: entry.approved !== false,
    matchScore,
    speakerScore,
    subtitleStartMs: now,
    subtitleEndMs: now + SUBTITLE_DURATION_MS,
    subtitleDurationMs: SUBTITLE_DURATION_MS,
    audioStartMs: now,
    audioEndMs: null,
    audioDurationMs: null,
    dropped: false,
    audioUrl: entry.audio || null
  };
  if (entry.approved === false) {
    activeSync.dropped = true;
    addLog("warning", `Line dropped or unapproved: ${payload.lineId}`);
  }

  if (entry.audio) {
    const audio = new Audio(entry.audio);
    audio.preload = "metadata";
    audio.addEventListener("loadedmetadata", () => {
      if (!Number.isFinite(audio.duration)) return;
      const durationMs = audio.duration * 1000;
      activeSync.audioDurationMs = durationMs;
      activeSync.audioEndMs = activeSync.audioStartMs + durationMs;
      if (Math.abs(SUBTITLE_DURATION_MS - durationMs) > 200) {
        addLog("error", `Subtitle/audio mismatch: ${Math.round(Math.abs(SUBTITLE_DURATION_MS - durationMs))}ms on ${payload.lineId}`);
      }
      renderOverlay();
    }, { once: true });
    audio.addEventListener("error", () => {
      addLog("error", `Audio failed: ${entry.audio}`);
    }, { once: true });
  }
  renderOverlay();
}

function findBattle() {
  return window.__activeBattle || window.__southDebug?.battle || null;
}

function findMixerAndScene(battle) {
  const scene = battle?.ctx?.scene || battle?.ctx?.arena?.group || null;
  const fighters = battle?.fighters || [];
  for (const fighter of fighters) {
    const candidates = [
      fighter?.mixer,
      fighter?.mesh?.mixer,
      fighter?.model?.mixer,
      fighter?.view?.mixer,
      fighter?.c3d?.mixer,
      fighter?.root?.mixer
    ];
    const mixer = candidates.find((candidate) => candidate && typeof candidate.clipAction === "function");
    if (mixer) return { mixer, scene };
  }
  if (battle?.ctx?.animationMixer && typeof battle.ctx.animationMixer.clipAction === "function") {
    return { mixer: battle.ctx.animationMixer, scene };
  }
  return { mixer: null, scene };
}

function getShowcaseClip(scene, fighterId, slot) {
  const name = `south_${slot}_${fighterId}`;
  if (scene?.__southSpecialClips?.[name]) return scene.__southSpecialClips[name];
  if (scene?.userData?.southSpecialClips?.[name]) return scene.userData.southSpecialClips[name];
  let found = null;
  scene?.traverse?.((node) => {
    if (!found && node?.userData?.southSpecialClips?.[name]) {
      found = node.userData.southSpecialClips[name];
    }
  });
  return found;
}

function wait(ms) {
  return new Promise((resolve) => {
    showcaseResolve = resolve;
    showcaseTimer = window.setTimeout(() => {
      showcaseResolve = null;
      showcaseTimer = null;
      resolve();
    }, ms);
  });
}

async function verifySpecialAudio(battle, fighterId, slot) {
  const lines = await loadVoiceLines();
  const entry = lines?.[fighterId]?.[slot];
  if (!entry?.audio) {
    addLog("warning", `Missing voice audio: ${fighterId}/${slot}`);
    return;
  }
  try {
    const response = await fetch(entry.audio, { method: "HEAD" });
    if (!response.ok) addLog("error", `Audio HTTP ${response.status}: ${entry.audio}`);
  } catch (error) {
    addLog("error", `Audio failure: ${entry.audio}`, error.message);
  }
}

async function runShowcase() {
  if (showcaseRunning) {
    stopShowcase("Cancelled");
    return;
  }
  const battle = findBattle();
  if (!battle) {
    addLog("error", "F10 showcase unavailable: no active battle");
    return;
  }
  showcaseRunning = true;
  showcaseCancelled = false;
  showcaseActions = [];
  showcaseActionTimers = [];
  const { mixer, scene } = findMixerAndScene(battle);
  if (!mixer) addLog("warning", "Missing clipAction mixer on active battle");
  ensureOverlay();

  try {
    for (const fighterId of FIGHTER_IDS) {
      if (showcaseCancelled) break;
      for (const slot of SPECIAL_SLOTS) {
        if (showcaseCancelled) break;
        showcaseStep = `${fighterId} / ${slot}`;
        renderOverlay();
        const clip = getShowcaseClip(scene, fighterId, slot);
        if (!clip) addLog("warning", `Missing clip: south_${slot}_${fighterId}`);
        if (mixer && typeof mixer.clipAction === "function") {
          if (!clip) {
            addLog("warning", `Missing clipActions: south_${slot}_${fighterId}`);
          } else {
            try {
              const action = mixer.clipAction(clip);
              action?.reset?.();
              action?.setLoop?.(2201, 1);
              action?.fadeIn?.(0.06);
              action?.play?.();
              if (action) showcaseActions.push(action);
              showcaseActionTimers.push(window.setTimeout(() => action?.fadeOut?.(0.08), 650));
              showcaseActionTimers.push(window.setTimeout(() => action?.stop?.(), 900));
            } catch (error) {
              addLog("error", `clipAction failed: ${fighterId}/${slot}`, error.message);
            }
          }
        }
        await verifySpecialAudio(battle, fighterId, slot);
        await wait(950);
      }
    }
  } finally {
    const wasCancelled = showcaseCancelled;
    showcaseRunning = false;
    showcaseCancelled = false;
    showcaseTimer = null;
    showcaseStep = wasCancelled ? "Cancelled" : "Complete";
    renderOverlay();
  }
}

function stopShowcase(reason = "Cancelled") {
  showcaseCancelled = true;
  if (showcaseTimer) window.clearTimeout(showcaseTimer);
  for (const timer of showcaseActionTimers) window.clearTimeout(timer);
  showcaseActionTimers = [];
  for (const action of showcaseActions) {
    action?.fadeOut?.(0.08);
    action?.stop?.();
  }
  showcaseActions = [];
  showcaseTimer = null;
  if (showcaseResolve) {
    const resolve = showcaseResolve;
    showcaseResolve = null;
    resolve();
  }
  showcaseRunning = false;
  showcaseStep = reason;
  addLog("warning", `F10 showcase ${reason.toLowerCase()}`);
  renderOverlay();
}

function toggleOverlay() {
  if (overlay) {
    removeOverlay();
  } else {
    ensureOverlay();
    renderOverlay();
  }
}

function onKeyDown(event) {
  if (event.repeat) return;
  if (event.code === "F9") {
    event.preventDefault();
    toggleOverlay();
  } else if (event.code === "F10") {
    event.preventDefault();
    runShowcase();
  } else if (event.code === "Escape" && showcaseRunning) {
    event.preventDefault();
    stopShowcase("Cancelled");
  }
}

function onPageHide() {
  stopShowcase("Stopped on page hide");
  removeOverlay();
  window.removeEventListener("keydown", onKeyDown);
  window.removeEventListener("pagehide", onPageHide);
  window.removeEventListener("beforeunload", onPageHide);
}

export function installSouthDebugTools() {
  if (window.__southDebug) return window.__southDebug;
  window.__southDebug = {
    battle: null,
    setBattle(battle) {
      this.battle = battle;
      window.__activeBattle = battle;
    },
    recordDialogue,
    recordDropped,
    addLog,
    getState() {
      return {
        activeSync,
        showcaseRunning,
        showcaseStep,
        logs: [...logs],
        events: [...events]
      };
    },
    startShowcase: runShowcase,
    stopShowcase
  };
  window.addEventListener("keydown", onKeyDown);
  window.addEventListener("pagehide", onPageHide);
  window.addEventListener("beforeunload", onPageHide);
  return window.__southDebug;
}

installSouthDebugTools();
