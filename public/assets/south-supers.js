import {
  AdditiveBlending,
  BoxGeometry,
  CanvasTexture,
  CircleGeometry,
  ConeGeometry,
  CylinderGeometry,
  DoubleSide,
  Group,
  Mesh,
  MeshBasicMaterial,
  MeshStandardMaterial,
  OctahedronGeometry,
  PlaneGeometry,
  PointLight,
  Quaternion,
  RingGeometry,
  SphereGeometry,
  Sprite,
  SpriteMaterial,
  SRGBColorSpace,
  TorusGeometry,
  Vector3
} from "three";

const EMPTY_IN = { moveX: 0, up: false, down: false, punch: false, kick: false, grab: false, super: false };
const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
const clampArenaX = (x) => Math.max(-5.8, Math.min(5.8, x));
const easeOut = (t) => 1 - (1 - clamp01(t)) ** 3;
const easeInOut = (t) => {
  const k = clamp01(t);
  return k < 0.5 ? 4 * k * k * k : 1 - (-2 * k + 2) ** 3 / 2;
};

let _glowTex = null;
function glowTex() {
  if (_glowTex) return _glowTex;
  const c = document.createElement("canvas");
  c.width = c.height = 128;
  const g = c.getContext("2d");
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, "rgba(255,255,255,1)");
  gr.addColorStop(0.28, "rgba(255,255,255,0.72)");
  gr.addColorStop(0.65, "rgba(255,255,255,0.18)");
  gr.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = gr;
  g.fillRect(0, 0, 128, 128);
  _glowTex = new CanvasTexture(c);
  _glowTex.colorSpace = SRGBColorSpace;
  _glowTex.userData.shared = true;
  return _glowTex;
}

function makeGlow(color, scale = 1.4, opacity = 0.7) {
  const sp = new Sprite(new SpriteMaterial({
    map: glowTex(),
    color,
    transparent: true,
    opacity,
    blending: AdditiveBlending,
    depthWrite: false
  }));
  sp.scale.setScalar(scale);
  return sp;
}

function bannerTex(w, h, drawFn) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  drawFn(c.getContext("2d"), w, h);
  const tx = new CanvasTexture(c);
  tx.colorSpace = SRGBColorSpace;
  return tx;
}

function stdMat(color, roughness = 0.5, metalness = 0.15, emissive = 0, emissiveIntensity = 0.5, extra = {}) {
  return new MeshStandardMaterial({
    color,
    roughness,
    metalness,
    ...(emissive ? { emissive, emissiveIntensity } : {}),
    ...extra
  });
}

function basicMat(color, extra = {}) {
  return new MeshBasicMaterial({ color, ...extra });
}

class SouthSuperBase {
  constructor(d, h) {
    this.d = d;
    this.h = h;
    this.t = 0;
    this.done = false;
    this.impactDone = false;
    this.timeScale = 1;
    this.casterPose = null;
    this.targetPose = null;
    this.casterClip = null;
    this.targetClip = null;
    this.targetTf = null;
    this.root = new Group();
    this.v1 = new Vector3();
    this.v2 = new Vector3();
    this.v3 = new Vector3();
    this.hpBefore = d.target.hp;
    this.startX = d.caster.x;
    this.targetX0 = d.target.x;
    this.dir = d.target.x >= d.caster.x ? 1 : -1;
    this.fired = new Set();
    d.scene.add(this.root);
    d.audio.charge?.(3.2, "super");
  }

  once(key, at, fn) {
    if (this.t >= at && !this.fired.has(key)) {
      this.fired.add(key);
      fn();
    }
  }

  setTargetFreeze(dt, poseOverrides = {}) {
    const t = this.d.target;
    if (this.impactDone) {
      this.targetPose = null;
      this.targetTf = null;
      t.update(EMPTY_IN, this.d.caster.x);
      return;
    }
    if (t.state === "frozen" && t.y > 0 && !this.targetTf) {
      t.y = Math.max(0, t.y - 5 * dt);
    }
    this.targetPose = this.h.P(this.h.V(this.t, t.char.id), poseOverrides);
  }

  landImpact({ vx = 5.6, vy = 8.4, color = 0xffaa22, flash = "rgba(255,210,120,0.85)", banner = "MASS HIT!", share = null, x = null, y = 1.2 } = {}) {
    if (this.impactDone) return;
    this.impactDone = true;
    const t = this.d.target;
    const s = share ?? this.d.caster.superShare ?? 0.3;
    t.hp = Math.max(0, this.hpBefore - 100 * s);
    if (t.hp <= 0) {
      t.knockOut(this.dir, vx, vy);
    } else {
      t.attack = null;
      t.forceState("knockdown");
      t.vx = this.dir * vx;
      t.vy = vy;
      t.grounded = false;
      t.downFrames = 0;
    }
    const ix = x ?? t.x;
    this.v1.set(ix, y, 0.2);
    this.d.fx.hitSpark(this.v1, 2.0, false, this.dir);
    this.d.fx.particles.emit(this.v1, { count: 140, speed: 10, color, life: 0.85, size: 0.28, gravity: 4, drag: 1.7 });
    this.d.fx.shockwave(this.v1, color, 0.6, 1.3, true);
    this.d.fx.shockwave(this.v2.set(ix, 0.04, 0), color, 0.9, 1.7);
    this.d.flash(flash, 250);
    this.d.cam.shake(0.5, 0.65);
    this.d.audio.boom?.();
    this.d.arena.cheer?.(1.5);
    if (banner) {
      this.d.popup(banner, this.v2.set(ix, 2.6, 0.4), "#" + color.toString(16).padStart(6, "0"));
    }
  }

  dispose() {
    this.d.audio.stopSuperBed?.(0.3);
    this.d.caster.y = 0;
    this.d.caster.x = clampArenaX(this.d.caster.x);
    this.d.scene.remove(this.root);
    const seenGeo = new Set();
    const seenMat = new Set();
    const seenTex = new Set();
    this.root.traverse((obj) => {
      if (obj.geometry && !obj.geometry.userData?.shared && !seenGeo.has(obj.geometry)) {
        seenGeo.add(obj.geometry);
        obj.geometry.dispose();
      }
      const mats = obj.material ? (Array.isArray(obj.material) ? obj.material : [obj.material]) : [];
      for (const m of mats) {
        if (!m || seenMat.has(m)) continue;
        seenMat.add(m);
        for (const v of Object.values(m)) {
          if (v?.isTexture && !v.userData?.shared && !seenTex.has(v)) {
            seenTex.add(v);
            v.dispose();
          }
        }
        m.dispose();
      }
    });
  }
}

/* ============================================================================
 * 1. STALIN ANNA (modi): ECR Morning Cycle Rally + Rising Sun Podium Slam
 * ============================================================================ */
class StalinCycleSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.65;
    this.IMPACT = 3.25;
    this.bike = this.buildBike();
    this.sun = this.buildRisingSun();
    this.root.add(this.bike.group, this.sun.group);
    d.caster.x = clampArenaX(this.targetX0 - this.dir * 3.8);
    d.audio.startSuperBed?.(3.2, "chakra");
  }

  buildBike() {
    const g = new Group();
    const chrome = stdMat(0xe5e7eb, 0.25, 0.85);
    const red = stdMat(0xdc2626, 0.35, 0.25, 0x991b1b, 0.3);
    const tire = stdMat(0x18181b, 0.85, 0.05);
    const wheel = (x) => {
      const wg = new Group();
      wg.position.set(x, 0.34, 0);
      wg.add(new Mesh(new TorusGeometry(0.32, 0.045, 10, 28), tire));
      wg.add(new Mesh(new TorusGeometry(0.27, 0.015, 6, 24), chrome));
      for (let i = 0; i < 6; i++) {
        const sp = new Mesh(new CylinderGeometry(0.008, 0.008, 0.54, 5), chrome);
        sp.rotation.z = (i * Math.PI) / 6;
        wg.add(sp);
      }
      g.add(wg);
      return wg;
    };
    const wRear = wheel(-0.56);
    const wFront = wheel(0.56);
    const bar = (x1, y1, x2, y2, r = 0.024, m = red) => {
      const dx = x2 - x1, dy = y2 - y1;
      const len = Math.hypot(dx, dy);
      const b = new Mesh(new CylinderGeometry(r, r, len, 8), m);
      b.position.set((x1 + x2) / 2, (y1 + y2) / 2, 0);
      b.rotation.z = Math.atan2(dy, dx) - Math.PI / 2;
      g.add(b);
    };
    bar(-0.56, 0.34, -0.08, 0.36);
    bar(-0.08, 0.36, -0.18, 0.78);
    bar(-0.18, 0.78, 0.38, 0.8);
    bar(-0.08, 0.36, 0.38, 0.8);
    bar(0.56, 0.34, 0.36, 0.92, 0.022, chrome);
    bar(-0.56, 0.34, -0.18, 0.78);
    const saddle = new Mesh(new BoxGeometry(0.22, 0.06, 0.14), stdMat(0x111827, 0.7));
    saddle.position.set(-0.22, 0.83, 0);
    const handle = new Mesh(new CylinderGeometry(0.018, 0.018, 0.44, 8), chrome);
    handle.rotation.x = Math.PI / 2;
    handle.position.set(0.36, 0.94, 0);
    const lamp = new Mesh(new SphereGeometry(0.075, 10, 8), basicMat(0xfef08a));
    lamp.position.set(0.45, 0.82, 0);
    const glow = makeGlow(0xfacc15, 0.9, 0.65);
    glow.position.set(0.52, 0.82, 0);
    g.add(saddle, handle, lamp, glow);
    return { group: g, wRear, wFront };
  }

  buildRisingSun() {
    const g = new Group();
    const sunMat = basicMat(0xfacc15, { transparent: true, opacity: 0.92 });
    const disc = new Mesh(new CircleGeometry(2.1, 36, 0, Math.PI), sunMat);
    const core = new Mesh(new CircleGeometry(1.35, 32, 0, Math.PI), basicMat(0xfef9c3));
    core.position.z = 0.02;
    g.add(disc, core);
    for (let i = 0; i < 9; i++) {
      const a = 0.14 + (i / 8) * (Math.PI - 0.28);
      const ray = new Mesh(new ConeGeometry(0.22, 2.2, 4), basicMat(i % 2 ? 0xe11d48 : 0xfacc15, { side: DoubleSide }));
      ray.position.set(Math.cos(a) * 3.1, Math.sin(a) * 3.1, -0.02);
      ray.rotation.z = a - Math.PI / 2;
      g.add(ray);
    }
    const lt = new PointLight(0xf59e0b, 0, 14, 1.5);
    lt.position.set(0, 1.5, 2.5);
    g.add(lt);
    g.position.set(this.targetX0, -2.5, -1.6);
    g.scale.setScalar(0.01);
    return { group: g, light: lt };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, audio, cam, fx, arena, speech, popup } = this.d;
    const d = this.dir;

    this.once("s1", 0.08, () => {
      speech("caster", "Muthuvel Karunanidhi Stalin ennum naan!");
      audio.whoosh?.();
    });
    this.once("s2", 1.45, () => {
      speech("target", "Ayyo bicycle wheelie-aa?!");
      popup("DRAVIDIAN MODEL!", this.v2.set(caster.x, 2.3, 0.3), "#e11d48");
      audio.superRelease?.("chakra");
      cam.shake(0.18, 0.3);
    });
    this.once("s3", this.IMPACT, () => {
      this.landImpact({ vx: 6.0, vy: 9.0, color: 0xfacc15, banner: "RISING SUN SLAM!" });
    });

    this.setTargetFreeze(dt, { headF: -0.35, lShF: 1.0, rShF: 1.1 });

    if (t < 1.45) {
      const u = easeInOut(t / 1.45);
      caster.x = clampArenaX(this.startX - d * 3.8 + d * 2.5 * u);
      caster.y = 0.42;
      caster.facing = d;
      const ped = t * 14;
      this.casterClip = null;
      this.casterPose = this.h.P(this.h.B(t, "modi"), {
        spineF: 0.45,
        headF: -0.15,
        rShF: 1.15,
        rEl: 0.35,
        lShF: 1.15,
        lEl: 0.35,
        rThF: 0.55 + Math.sin(ped) * 0.48,
        rKn: 1.05 - Math.cos(ped) * 0.45,
        lThF: 0.55 - Math.sin(ped) * 0.48,
        lKn: 1.05 + Math.cos(ped) * 0.45
      });
      this.bike.group.visible = true;
      this.bike.group.position.set(caster.x + d * 0.15, 0, 0.04);
      this.bike.group.rotation.set(0, d > 0 ? 0 : Math.PI, 0);
      this.bike.wRear.rotation.z -= dt * 16;
      this.bike.wFront.rotation.z -= dt * 16;
      if (Math.random() < 0.45) {
        fx.particles.emit(this.v1.set(caster.x - d * 0.6, 0.2, 0.05), { count: 2, speed: 2.2, color: 0xfacc15, life: 0.4, size: 0.18 });
      }
      cam.set(this.v2.set(caster.x + d * 1.4, 1.5, 4.6), this.v3.set(caster.x + d * 0.5, 1.1, 0), 5, 42);
    } else if (t < this.IMPACT) {
      const u = (t - 1.45) / (this.IMPACT - 1.45);
      const launch = u < 0.55;
      caster.facing = d;
      if (launch) {
        const k = easeOut(u / 0.55);
        caster.x = clampArenaX(this.targetX0 - d * (1.3 - 0.5 * k));
        caster.y = 2.2 * Math.sin(k * Math.PI * 0.72);
        this.casterPose = null;
        this.casterClip = { name: "butterfly", time: u * 1.1, fade: 0.1 };
        this.bike.group.position.set(caster.x + d * (0.2 + k * 0.6), caster.y * 0.55, 0.05);
        this.bike.group.rotation.set(0, d > 0 ? 0 : Math.PI, 0.55 * k);
      } else {
        const k = easeInOut((u - 0.55) / 0.45);
        caster.x = clampArenaX(this.targetX0 - d * (0.8 - 0.15 * k));
        caster.y = 1.9 * (1 - k);
        this.casterPose = null;
        this.casterClip = { name: "flyingkick", time: k * 0.85, fade: 0.08 };
        this.bike.group.position.set(this.targetX0 - d * (0.9 * (1 - k)), 0.8 * (1 - k) + 0.3, 0.05);
        this.bike.group.rotation.z = -1.1 * k;
      }
      this.bike.wRear.rotation.z -= dt * 26;
      this.bike.wFront.rotation.z -= dt * 26;

      const sg = easeOut(u);
      this.sun.group.scale.setScalar(0.15 + sg * 0.95);
      this.sun.group.position.set(this.targetX0, -0.3 + sg * 0.5, -1.7);
      this.sun.light.intensity = 7 * sg;
      arena.setMood(0.65 * sg);
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.2, 6.2), this.v3.set(target.x, 1.3, 0), 4, 45);
    } else {
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      caster.y = Math.max(0, caster.y - dt * 5);
      this.bike.group.visible = false;
      this.sun.group.position.y = 0.2 - u * 2.2;
      this.sun.light.intensity = 7 * (1 - u);
      arena.setMood(0.65 * (1 - u));
      this.casterClip = { name: "palm", time: 0.4 + u * 0.6, fade: 0.15 };
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.1, 7.2), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) {
      caster.y = 0;
      this.done = true;
    }
  }
}

/* ============================================================================
 * 2. THALAPATHY VJ (rahul): Leo Slow-Mo Blitz + Audio Launch 1000CR Mic Drop
 * ============================================================================ */
class ThalapathyBlitzSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.6;
    this.IMPACT = 3.2;
    this.mic = this.buildMicAndClapper();
    this.cups = this.buildCoffeeCups();
    this.slashRibbons = this.buildRibbons();
    this.root.add(this.mic.group, this.cups, this.slashRibbons);
    d.audio.startSuperBed?.(3.1, "sitar");
  }

  buildMicAndClapper() {
    const g = new Group();
    const pole = new Mesh(new CylinderGeometry(0.025, 0.035, 1.45, 10), stdMat(0xd4af37, 0.25, 0.9));
    pole.position.y = 0.72;
    const base = new Mesh(new CylinderGeometry(0.22, 0.24, 0.05, 16), stdMat(0x18181b, 0.6, 0.4));
    base.position.y = 0.025;
    const head = new Mesh(new SphereGeometry(0.075, 12, 10), stdMat(0xfef08a, 0.3, 0.85, 0xfacc15, 0.5));
    head.position.set(0.08 * this.dir, 1.48, 0);
    g.add(pole, base, head);

    const clap = new Mesh(
      new PlaneGeometry(1.55, 0.82),
      basicMat(0xffffff, {
        map: bannerTex(512, 256, (ctx) => {
          ctx.fillStyle = "#111827";
          ctx.fillRect(0, 0, 512, 256);
          ctx.fillStyle = "#dc2626";
          for (let i = 0; i < 6; i++) {
            ctx.fillRect(i * 90, 0, 45, 42);
          }
          ctx.fillStyle = "#facc15";
          ctx.font = "bold 76px Impact, sans-serif";
          ctx.textAlign = "center";
          ctx.fillText("1000 CR FDFS", 256, 145);
          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 32px Impact, sans-serif";
          ctx.fillText("BLOODY SWEET!", 256, 206);
        }),
        side: DoubleSide,
        transparent: true
      })
    );
    clap.position.set(this.targetX0, 3.2, -0.6);
    clap.visible = false;
    g.add(clap);
    g.position.set(this.startX + this.dir * 0.45, 0, 0.2);
    return { group: g, clap };
  }

  buildCoffeeCups() {
    const g = new Group();
    for (let i = 0; i < 8; i++) {
      const c = new Mesh(new CylinderGeometry(0.09, 0.065, 0.22, 12), stdMat(i % 2 ? 0xdc2626 : 0xfef3c7, 0.35));
      c.position.set(this.targetX0, 1.4, 0);
      g.add(c);
    }
    g.visible = false;
    return g;
  }

  buildRibbons() {
    const g = new Group();
    for (let i = 0; i < 4; i++) {
      const arc = new Mesh(
        new TorusGeometry(1.25, 0.045, 6, 36, Math.PI * 0.85),
        basicMat(i % 2 ? 0xef4444 : 0xfacc15, { transparent: true, opacity: 0.9, blending: AdditiveBlending })
      );
      arc.position.set(this.targetX0, 1.25, 0.25);
      arc.rotation.set(0.3 * i, 0.4 * i, (i * Math.PI) / 4);
      arc.visible = false;
      g.add(arc);
    }
    return g;
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, audio, cam, fx, arena, speech, popup } = this.d;
    const d = this.dir;

    this.once("v1", 0.05, () => {
      speech("caster", "I am waiting!");
      audio.stampSlam?.();
    });
    this.once("v2", 1.2, () => {
      popup("VAATHI SLOW-MO!", this.v2.set(this.targetX0, 2.5, 0.4), "#dc2626");
      audio.whoosh?.();
    });
    this.once("v3", 1.75, () => {
      audio.hit?.(0.95);
      cam.shake(0.2, 0.2);
      fx.hitSpark(this.v1.set(this.targetX0, 1.3, 0.2), 1.3, false, d);
    });
    this.once("v4", 2.45, () => {
      audio.hit?.(1.0);
      cam.shake(0.22, 0.22);
      fx.hitSpark(this.v1.set(this.targetX0, 1.4, 0.2), 1.4, false, -d);
    });
    this.once("v5", this.IMPACT, () => {
      this.timeScale = 1;
      this.landImpact({ vx: 6.4, vy: 9.2, color: 0xfacc15, banner: "I AM WAITING · 1000CR!" });
    });

    this.setTargetFreeze(dt, { headF: -0.25 });

    if (t < 1.2) {
      this.timeScale = 1;
      caster.y = 0;
      this.casterClip = { name: "palm_m", time: t * 0.9, fade: 0.1 };
      cam.set(this.v2.set(caster.x + d * 1.4, 1.4, 3.8), this.v3.set(caster.x, 1.3, 0), 5, 40);
    } else if (t < this.IMPACT) {
      this.timeScale = 0.62;
      this.mic.group.visible = false;
      this.cups.visible = true;
      const u = (t - 1.2) / (this.IMPACT - 1.2);
      this.cups.children.forEach((c, idx) => {
        const ang = u * 4 + idx * ((Math.PI * 2) / 8);
        c.position.set(this.targetX0 + Math.cos(ang) * (0.9 + u * 0.9), 0.7 + ((idx % 3) * 0.45) + Math.sin(u * 6 + idx) * 0.25, Math.sin(ang) * 0.8);
        c.rotation.set(t * 5, t * 4, idx);
      });
      if (u < 0.35) {
        caster.x = clampArenaX(this.targetX0 - d * 0.95);
        caster.facing = d;
        this.casterClip = { name: "jabcross", time: u * 2.2, fade: 0.08 };
        this.slashRibbons.children[0].visible = true;
      } else if (u < 0.72) {
        caster.x = clampArenaX(this.targetX0 + d * 1.0);
        caster.facing = -d;
        caster.y = 0.45;
        this.casterClip = { name: "hurricane_m", time: (u - 0.35) * 2.1, fade: 0.08 };
        this.slashRibbons.children[1].visible = true;
        this.slashRibbons.children[2].visible = true;
      } else {
        caster.x = clampArenaX(this.targetX0 - d * 0.85);
        caster.facing = d;
        caster.y = 0.25;
        this.casterClip = { name: "highkick_m", time: (u - 0.72) * 2.8, fade: 0.06 };
        this.slashRibbons.children[3].visible = true;
      }
      arena.setMood(0.75);
      cam.set(this.v2.set(this.targetX0 + Math.sin(u * Math.PI) * 2.2, 1.9, 4.9), this.v3.set(this.targetX0, 1.25, 0), 4, 44);
    } else {
      this.timeScale = 1;
      caster.facing = d;
      caster.y = Math.max(0, caster.y - dt * 5);
      this.mic.clap.visible = true;
      this.mic.group.visible = true;
      this.mic.group.position.set(0, 0, 0);
      this.mic.clap.position.set(caster.x, 2.7, -0.5);
      this.cups.visible = false;
      this.slashRibbons.visible = false;
      this.casterClip = { name: "flipkick", time: 0.8, fade: 0.2 };
      arena.setMood(0.2);
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 7.0), this.v3.set(target.x, 1.1, 0), 3, 42);
    }
    if (t >= this.END) {
      this.timeScale = 1;
      caster.y = 0;
      this.done = true;
    }
  }
}

/* ============================================================================
 * 3. IRON AMMA (didi): Poes Garden Lion Throne & Amma Canteen Tiffin Rain
 * ============================================================================ */
class IronAmmaSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.6;
    this.IMPACT = 3.2;
    this.throne = this.buildThrone();
    this.tiffins = this.buildTiffins();
    this.crest = this.buildTwoLeafCrest();
    this.root.add(this.throne, this.tiffins, this.crest);
    d.audio.startSuperBed?.(3.0, "chant");
  }

  buildThrone() {
    const g = new Group();
    const gold = stdMat(0xfacc15, 0.3, 0.85, 0x78350f, 0.25);
    const emerald = stdMat(0x047857, 0.45, 0.15);
    const seat = new Mesh(new BoxGeometry(0.95, 0.16, 0.8), gold);
    seat.position.y = 0.08;
    const back = new Mesh(new BoxGeometry(0.9, 1.45, 0.14), emerald);
    back.position.set(0, 0.85, -0.35);
    const rim = new Mesh(new TorusGeometry(0.55, 0.05, 8, 24, Math.PI), gold);
    rim.position.set(0, 1.55, -0.34);
    g.add(seat, back, rim);
    g.position.set(this.startX, 0, -0.15);
    return g;
  }

  buildTiffins() {
    const g = new Group();
    const steel = stdMat(0xe2e8f0, 0.2, 0.92);
    const laptop = stdMat(0x1e293b, 0.35, 0.7);
    for (let i = 0; i < 6; i++) {
      const m = new Mesh(
        i % 2 === 0 ? new CylinderGeometry(0.16, 0.16, 0.34, 14) : new BoxGeometry(0.38, 0.26, 0.04),
        i % 2 === 0 ? steel : laptop
      );
      m.position.set(this.targetX0 + (i - 2.5) * 0.42, 5.2 + i * 0.4, (i % 3 - 1) * 0.25);
      g.add(m);
    }
    g.visible = false;
    return g;
  }

  buildTwoLeafCrest() {
    const g = new Group();
    const leafMat = stdMat(0x16a34a, 0.3, 0.2, 0x15803d, 0.5);
    for (const s of [-1, 1]) {
      const leaf = new Mesh(new ConeGeometry(0.42, 1.35, 6), leafMat);
      leaf.scale.set(1, 1, 0.25);
      leaf.position.set(s * 0.34, 0, 0);
      leaf.rotation.z = -s * 0.45;
      g.add(leaf);
    }
    const base = new Mesh(new CylinderGeometry(0.65, 0.72, 0.2, 20), stdMat(0xfacc15, 0.28, 0.88));
    base.position.y = -0.65;
    g.add(base);
    g.position.set(this.targetX0, 6.2, 0.1);
    g.visible = false;
    return g;
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, fx, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("a1", 0.06, () => {
      speech("caster", "Makkalal Naan! Makkalukkagave Naan!");
      audio.whoosh?.();
    });
    this.once("a2", 1.35, () => {
      popup("AMMA CANTEEN!", this.v2.set(this.targetX0, 2.5, 0.3), "#16a34a");
      audio.hit?.(0.9);
      fx.hitSpark(this.v1.set(this.targetX0, 1.5, 0.2), 1.3, false, d);
    });
    this.once("a3", this.IMPACT, () => {
      this.landImpact({ vx: 5.8, vy: 8.8, color: 0x22c55e, flash: "rgba(180,255,200,0.85)", banner: "TWO-LEAF GAVEL!" });
    });

    this.setTargetFreeze(dt, { spineF: 0.2, headF: -0.2 });

    if (t < 1.35) {
      const u = easeOut(t / 1.35);
      caster.y = 1.25 * u;
      this.throne.position.set(caster.x, caster.y - 0.15, -0.2);
      this.casterClip = { name: "stance", time: t, loop: true, fade: 0.15 };
      arena.setMood(0.5 * u);
      cam.set(this.v2.set(caster.x + d * 1.4, 2.0, 4.5), this.v3.set(caster.x, caster.y + 1.0, 0), 4, 42);
    } else if (t < this.IMPACT) {
      const u = (t - 1.35) / (this.IMPACT - 1.35);
      caster.y = 1.25;
      this.throne.position.set(caster.x, caster.y - 0.15, -0.2);
      this.casterClip = { name: u < 0.55 ? "palm_m" : "snapkick2", time: u * 1.6, fade: 0.1 };
      this.tiffins.visible = u < 0.72;
      this.tiffins.children.forEach((m, idx) => {
        const drop = clamp01(u * 1.5 - idx * 0.08);
        m.position.y = 4.5 * (1 - drop) + 0.4;
        m.rotation.set(t * 4, t * 5 + idx, 0);
      });
      this.crest.visible = u >= 0.45;
      if (this.crest.visible) {
        const k = easeInOut((u - 0.45) / 0.55);
        this.crest.position.set(this.targetX0, 5.2 * (1 - k * k) + 0.75, 0.1);
        this.crest.scale.setScalar(1 + 0.45 * k);
      }
      arena.setMood(0.7);
      cam.set(this.v2.set((caster.x + this.targetX0) / 2, 2.4, 6.2), this.v3.set(this.targetX0, 1.3, 0), 4, 45);
    } else {
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      caster.y = Math.max(0, 1.25 * (1 - u * 1.5));
      this.throne.position.set(caster.x, caster.y - 0.15, -0.2);
      this.tiffins.visible = false;
      this.crest.position.y = 0.75 + u * 2.5;
      this.crest.scale.setScalar(Math.max(0.01, 1.45 * (1 - u)));
      this.casterClip = { name: "palm", time: u * 0.9, fade: 0.15 };
      arena.setMood(0.7 * (1 - u));
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 6.9), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) {
      caster.y = 0;
      this.done = true;
    }
  }
}

/* ============================================================================
 * 4. PUSHPA RAJ (trump): "Thaggedhe Le" Shoulder Tilt + Red Sandalwood Axe
 * ============================================================================ */
class PushpaSandalSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.6;
    this.IMPACT = 3.25;
    this.logs = this.buildLogsAndAxe();
    this.root.add(this.logs.group);
    d.audio.startSuperBed?.(3.0, "chant");
  }

  buildLogsAndAxe() {
    const g = new Group();
    const sandalMat = stdMat(0x991b1b, 0.75, 0.05, 0x450a0a, 0.35);
    const arr = [];
    for (let i = 0; i < 6; i++) {
      const log = new Mesh(new CylinderGeometry(0.16, 0.18, 1.45, 10), sandalMat);
      log.position.set(this.targetX0 + (i - 2.5) * 0.55, 0.8 + i * 0.35, -0.4);
      log.rotation.set(0.4 * i, 0.3 * i, 1.2);
      log.visible = false;
      g.add(log);
      arr.push(log);
    }
    const axe = new Group();
    const handle = new Mesh(new CylinderGeometry(0.032, 0.038, 1.05, 8), stdMat(0x78350f, 0.8));
    handle.position.y = 0.45;
    const blade = new Mesh(new BoxGeometry(0.38, 0.28, 0.05), stdMat(0xf8fafc, 0.2, 0.92, 0xea580c, 0.4));
    blade.position.set(0.16, 0.88, 0);
    axe.add(handle, blade);
    axe.position.set(this.startX, 1.3, 0.2);
    axe.visible = false;
    g.add(axe);
    return { group: g, logs: arr, axe };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, fx, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("p1", 0.06, () => {
      speech("caster", "Pushpa ante flower anukunnava? FIRE!");
      audio.stampSlam?.();
    });
    this.once("p2", 1.5, () => {
      popup("RED SANDAL STORM!", this.v2.set(this.targetX0, 2.5, 0.3), "#ea580c");
      audio.hit?.(0.95);
      fx.hitSpark(this.v1.set(this.targetX0, 1.3, 0.2), 1.4, false, d);
    });
    this.once("p3", this.IMPACT, () => {
      this.landImpact({ vx: 6.5, vy: 8.8, color: 0xf97316, banner: "PUSHPA FIRE!!" });
    });

    this.setTargetFreeze(dt, { headF: -0.4 });

    if (t < 1.35) {
      // Iconic Thaggedhe Le skewed-shoulder hand-under-chin pose!
      this.casterClip = null;
      const chinSwipe = Math.sin(clamp01(t / 0.9) * Math.PI * 0.5);
      this.casterPose = this.h.P(this.h.B(t, "trump"), {
        spineS: -0.22 * d,
        headS: 0.18 * d,
        rShO: 0.55,
        rShF: 1.55 * chinSwipe,
        rEl: 1.95 * chinSwipe,
        lShO: 0.25,
        lShF: 0.25
      });
      arena.setMood(0.55);
      if (Math.random() < 0.45) {
        fx.particles.emit(this.v1.set(caster.x, 1.1, 0.1), { count: 2, speed: 2.2, color: 0xea580c, life: 0.5, size: 0.22 });
      }
      cam.set(this.v2.set(caster.x + d * 1.1, 1.55, 3.2), this.v3.set(caster.x, 1.4, 0), 5, 38);
    } else if (t < this.IMPACT) {
      const u = (t - 1.35) / (this.IMPACT - 1.35);
      this.casterPose = null;
      this.logs.axe.visible = true;
      this.logs.axe.position.set(caster.x + d * 0.55, caster.y + 1.25, 0.22);
      this.logs.axe.rotation.z = -d * (1.2 + Math.sin(u * 14) * 1.1);
      for (let i = 0; i < this.logs.logs.length; i++) {
        const lg = this.logs.logs[i];
        lg.visible = true;
        const p = (u * 1.4 + i * 0.15) % 1;
        lg.position.set(caster.x + (this.targetX0 - caster.x) * p, 0.7 + Math.sin(p * Math.PI) * 1.4 + i * 0.12, (i % 3 - 1) * 0.25);
        lg.rotation.x += dt * 7;
        lg.rotation.z += dt * 5;
      }
      if (u < 0.6) {
        caster.x = clampArenaX(this.startX + (this.targetX0 - d * 1.1 - this.startX) * easeOut(u / 0.6));
        this.casterClip = { name: u < 0.3 ? "hook" : "uppercut", time: u * 2.2, fade: 0.08 };
      } else {
        const k = (u - 0.6) / 0.4;
        caster.x = clampArenaX(this.targetX0 - d * (1.1 - 0.5 * k));
        caster.y = 2.3 * Math.sin(k * Math.PI * 0.7);
        this.casterClip = { name: "dropkick", time: k * 0.85, fade: 0.06 };
      }
      arena.setMood(0.75);
      cam.set(this.v2.set((caster.x + this.targetX0) / 2, 2.1, 5.4), this.v3.set(this.targetX0, 1.25, 0), 4, 44);
    } else {
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      caster.y = Math.max(0, caster.y - dt * 5);
      this.logs.group.visible = false;
      this.casterClip = null;
      this.casterPose = this.h.P(this.h.B(t, "trump"), { spineS: -0.22 * d, rShF: 1.5, rEl: 1.9 });
      arena.setMood(0.75 * (1 - u));
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 6.8), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) {
      caster.y = 0;
      this.done = true;
    }
  }
}

/* ============================================================================
 * 5. PINARAYI (yogi): "Kadakku Purathu!" + Kerala Palms & SilverLine Bullet Express
 * ============================================================================ */
class PinarayiSilverLineSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.65;
    this.IMPACT = 3.25;
    this.train = this.buildSilverLine();
    this.root.add(this.train.group);
    d.audio.startSuperBed?.(3.0, "engine");
  }

  buildSilverLine() {
    const g = new Group();
    const railMat = stdMat(0xcbd5e1, 0.25, 0.9);
    for (const z of [-0.45, 0.45]) {
      const r = new Mesh(new BoxGeometry(16, 0.06, 0.08), railMat);
      r.position.set(0, 0.03, z);
      g.add(r);
    }
    const bullet = new Group();
    const nose = new Mesh(new ConeGeometry(0.68, 1.85, 16), stdMat(0xf8fafc, 0.25, 0.35));
    nose.rotation.z = -Math.PI / 2;
    nose.position.set(1.5, 0.85, 0);
    const body = new Mesh(new BoxGeometry(3.2, 1.32, 1.28), stdMat(0xf8fafc, 0.3, 0.3));
    body.position.set(-0.35, 0.85, 0);
    const stripe = new Mesh(new BoxGeometry(3.3, 0.22, 1.31), stdMat(0xdc2626, 0.35, 0.2, 0x991b1b, 0.35));
    stripe.position.set(-0.35, 0.78, 0);
    const headLight = new Mesh(new SphereGeometry(0.14, 10, 8), basicMat(0xfef08a));
    headLight.position.set(2.35, 0.72, 0);
    bullet.add(nose, body, stripe, headLight);
    bullet.position.set(-10 * this.dir, 0, -0.1);
    if (this.dir < 0) bullet.rotation.y = Math.PI;
    g.add(bullet);
    return { group: g, bullet };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, fx, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("y1", 0.06, () => {
      speech("caster", "Kadakku Purathu!");
      audio.stampSlam?.();
    });
    this.once("y2", 1.35, () => {
      popup("SILVERLINE K-RAIL EXPRESS!", this.v2.set(this.targetX0, 2.6, 0.3), "#dc2626");
      audio.whoosh?.();
      cam.shake(0.35, 0.4);
      fx.hitSpark(this.v1.set(this.targetX0, 1.1, 0.1), 1.5, false, d);
    });
    this.once("y3", this.IMPACT, () => {
      this.landImpact({ vx: 6.2, vy: 8.6, color: 0xdc2626, banner: "KADAKKU PURATHU!" });
    });

    if (t < 1.35) {
      this.setTargetFreeze(dt, { headF: -0.3 });
      this.casterClip = { name: "spinback", time: t * 0.85, fade: 0.1 };
      arena.setMood(0.5);
      cam.set(this.v2.set(caster.x + d * 1.2, 1.5, 3.6), this.v3.set(caster.x, 1.35, 0), 5, 40);
    } else if (t < this.IMPACT) {
      const u = (t - 1.35) / (this.IMPACT - 1.35);
      const bx = (-10 + 22 * easeInOut(clamp01(u * 1.25))) * d;
      this.train.bullet.position.x = this.targetX0 + bx - 2.5 * d;
      const launch = Math.sin(clamp01((u - 0.15) / 0.85) * Math.PI);
      this.targetTf = { x: this.targetX0, y: launch * 2.3, z: 0, yaw: u * 4.5, roll: u * 3.1 };
      this.setTargetFreeze(dt, { spineF: 0.4 });
      caster.x = clampArenaX(this.targetX0 - d * (1.2 - 0.4 * u));
      caster.y = launch * 1.8;
      this.casterClip = { name: u < 0.5 ? "thrustkick" : "roundhouse_m", time: u * 1.8, fade: 0.08 };
      arena.setMood(0.7);
      cam.set(this.v2.set(this.targetX0, 2.2, 6.2), this.v3.set(this.targetX0, 1.4, 0), 4, 46);
    } else {
      this.targetTf = null;
      this.setTargetFreeze(dt);
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      caster.y = Math.max(0, caster.y - dt * 6);
      this.train.group.visible = false;
      this.casterClip = { name: "elbowupper", time: 0.6 + u * 0.5, fade: 0.15 };
      arena.setMood(0.7 * (1 - u));
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 6.9), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) {
      caster.y = 0;
      this.targetTf = null;
      this.done = true;
    }
  }
}

/* ============================================================================
 * 6. DK SHIVAKUMAR (nitin): Silk Board 999s Signal + Resort Volvo + Granite Bande
 * ============================================================================ */
class DksSilkBoardSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.65;
    this.IMPACT = 3.25;
    this.props = this.buildSilkBoardProps();
    this.root.add(this.props.group);
    d.audio.startSuperBed?.(3.0, "engine");
  }

  buildSilkBoardProps() {
    const g = new Group();
    // 1. Traffic signal gantry
    const pole = new Mesh(new CylinderGeometry(0.06, 0.08, 3.3, 10), stdMat(0x334155, 0.5, 0.6));
    pole.position.set(this.targetX0 + this.dir * 1.15, 1.65, -0.4);
    const box = new Mesh(new BoxGeometry(0.55, 1.15, 0.35), stdMat(0x0f172a, 0.4, 0.5));
    box.position.set(this.targetX0 + this.dir * 1.15, 2.75, -0.4);
    const redLight = new Mesh(new SphereGeometry(0.16, 12, 10), basicMat(0xef4444));
    redLight.position.set(this.targetX0 + this.dir * 1.15, 3.05, -0.2);
    g.add(pole, box, redLight);

    // 2. Kanakapura Granite Bande (Monolith)
    const bande = new Mesh(
      new OctahedronGeometry(1.15, 1),
      stdMat(0x64748b, 0.9, 0.1, 0x0284c7, 0.25)
    );
    bande.scale.set(1.15, 1.35, 0.95);
    bande.position.set(this.targetX0, 6.2, 0.05);
    bande.visible = false;
    g.add(bande);

    // 3. Resort Volvo Coach
    const bus = new Group();
    const shell = new Mesh(new BoxGeometry(2.8, 1.25, 1.15), stdMat(0x0284c7, 0.25, 0.55));
    shell.position.y = 0.85;
    const win = new Mesh(new BoxGeometry(2.4, 0.48, 1.18), basicMat(0x0f172a));
    win.position.y = 1.05;
    bus.add(shell, win);
    bus.position.set(this.startX - this.dir * 6, 0, -0.15);
    bus.visible = false;
    g.add(bus);

    return { group: g, bande, bus };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, fx, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("d1", 0.06, () => {
      speech("caster", "One thing I would like to tell you...");
      audio.stampSlam?.();
    });
    this.once("d2", 1.35, () => {
      popup("KANAKAPURA BANDE + RESORT VOLVO!", this.v2.set(this.targetX0, 2.7, 0.4), "#0284c7");
      audio.whoosh?.();
    });
    this.once("d3", this.IMPACT, () => {
      speech("caster", "By profession I am a businessman!");
      this.landImpact({ vx: 6.0, vy: 8.8, color: 0x38bdf8, banner: "BANDE CRUSH!" });
    });

    this.setTargetFreeze(dt, { headF: -0.35 });

    if (t < 1.35) {
      this.casterClip = { name: "quadpunch", time: t * 1.1, fade: 0.1 };
      arena.setMood(0.45);
      cam.set(this.v2.set(caster.x + d * 1.3, 1.6, 4.3), this.v3.set((caster.x + this.targetX0) / 2, 1.5, 0), 4, 43);
    } else if (t < this.IMPACT) {
      const u = (t - 1.35) / (this.IMPACT - 1.35);
      this.props.bande.visible = true;
      this.props.bus.visible = true;
      const drop = easeInOut(clamp01((u - 0.15) / 0.85));
      this.props.bande.position.y = 5.8 * (1 - drop * drop) + 0.9;
      this.props.bande.rotation.y += dt * 2.5;
      this.props.bus.position.x = this.targetX0 - d * (5.5 * (1 - drop));
      caster.x = clampArenaX(this.startX + (this.targetX0 - d * 1.1 - this.startX) * easeOut(u));
      this.casterClip = { name: u < 0.5 ? "mmaround" : "sidekick", time: u * 1.7, fade: 0.08 };
      arena.setMood(0.7);
      cam.set(this.v2.set(this.targetX0, 2.3, 5.8), this.v3.set(this.targetX0, 1.5, 0), 4, 45);
    } else {
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      this.props.bande.scale.setScalar(Math.max(0.01, 1.2 * (1 - u)));
      this.props.bus.visible = false;
      this.casterClip = { name: "uppercut", time: 0.7, fade: 0.2 };
      arena.setMood(0.7 * (1 - u));
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 6.8), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) this.done = true;
  }
}

/* ============================================================================
 * 7. POWER STAR PK (ravi): OG Crimson Katana Slashes & Gabbar Singh Swag
 * ============================================================================ */
class PowerStarOGSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.65;
    this.IMPACT = 3.25;
    this.arcs = this.buildKatanaArcs();
    this.root.add(this.arcs.group);
    d.audio.startSuperBed?.(3.1, "chakra");
  }

  buildKatanaArcs() {
    const g = new Group();
    const slashes = [];
    for (let i = 0; i < 5; i++) {
      const m = new Mesh(
        new TorusGeometry(1.35, 0.04, 6, 36, Math.PI * 0.9),
        basicMat(i % 2 ? 0xdc2626 : 0xffffff, { transparent: true, opacity: 0.95, blending: AdditiveBlending })
      );
      m.position.set(this.targetX0, 1.25, 0.22);
      m.rotation.set(0.5 * i, 0.45 * i, -0.7 + i * 0.62);
      m.visible = false;
      g.add(m);
      slashes.push(m);
    }
    const blade = new Mesh(new BoxGeometry(1.15, 0.045, 0.025), stdMat(0xf8fafc, 0.15, 0.95, 0xdc2626, 0.7));
    blade.position.set(this.startX, 1.3, 0.2);
    g.add(blade);
    return { group: g, slashes, blade };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, fx, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("k1", 0.06, () => {
      speech("caster", "Seize the Ship!");
      audio.whoosh?.();
    });
    this.once("k2", 1.25, () => {
      popup("HUNGRY CHEETAH · OG SLASH!", this.v2.set(this.targetX0, 2.5, 0.4), "#dc2626");
      audio.hit?.(0.9);
      fx.hitSpark(this.v1.set(this.targetX0, 1.3, 0.2), 1.4, false, d);
    });
    this.once("k3", 2.15, () => {
      audio.hit?.(1.0);
      fx.hitSpark(this.v1.set(this.targetX0, 1.4, 0.2), 1.5, false, -d);
    });
    this.once("k4", this.IMPACT, () => {
      this.timeScale = 1;
      this.landImpact({ vx: 6.4, vy: 8.9, color: 0xef4444, flash: "rgba(255,140,140,0.85)", banner: "SEIZE THE SHIP!" });
    });

    this.setTargetFreeze(dt, { headF: -0.25 });

    if (t < 1.2) {
      this.casterClip = { name: "twirl", time: t * 1.1, fade: 0.1 };
      this.arcs.blade.position.set(caster.x + d * 0.55, 1.25, 0.2);
      this.arcs.blade.rotation.z = t * 6;
      arena.setMood(0.6);
      cam.set(this.v2.set(caster.x + d * 1.2, 1.45, 3.6), this.v3.set(caster.x, 1.3, 0), 5, 40);
    } else if (t < this.IMPACT) {
      this.timeScale = 0.72;
      const u = (t - 1.2) / (this.IMPACT - 1.2);
      const stepIdx = Math.min(4, Math.floor(u * 5));
      for (let i = 0; i <= stepIdx; i++) this.arcs.slashes[i].visible = true;
      const side = stepIdx % 2 === 0 ? -1 : 1;
      caster.x = clampArenaX(this.targetX0 + side * 0.95);
      caster.facing = -side;
      caster.y = stepIdx === 2 ? 0.65 : 0;
      const clips = ["spinflip", "hurricane", "highkick", "upper", "palm"];
      this.casterClip = { name: clips[stepIdx], time: (u * 5 - stepIdx) * 0.85, fade: 0.05 };
      this.arcs.blade.position.set(caster.x - side * 0.65, caster.y + 1.25, 0.2);
      this.arcs.blade.rotation.z = side * 0.6 + u * 12;
      arena.setMood(0.85);
      cam.set(this.v2.set(this.targetX0, 1.9, 4.9), this.v3.set(this.targetX0, 1.25, 0), 4, 44);
    } else {
      this.timeScale = 1;
      caster.facing = d;
      caster.y = 0;
      this.arcs.group.visible = false;
      this.casterClip = { name: "dance", time: t - this.IMPACT, loop: true, fade: 0.2 };
      arena.setMood(0.3);
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 6.9), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) {
      this.timeScale = 1;
      caster.y = 0;
      this.done = true;
    }
  }
}

/* ============================================================================
 * 8. SEEMAN ANNA (lalu): Stadium Horn-Speaker Mic Set + Roaring Golden Puli
 * ============================================================================ */
class SeemanMikeSetSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.65;
    this.IMPACT = 3.25;
    this.stage = this.buildMikeStage();
    this.root.add(this.stage.group);
    d.audio.startSuperBed?.(3.0, "chant");
  }

  buildMikeStage() {
    const g = new Group();
    const podium = new Mesh(new BoxGeometry(1.15, 0.85, 0.8), stdMat(0xb91c1c, 0.65));
    podium.position.set(this.startX, 0.42, -0.15);
    g.add(podium);
    const pole = new Mesh(new CylinderGeometry(0.04, 0.05, 3.1, 8), stdMat(0xe5e7eb, 0.4, 0.7));
    pole.position.set(this.startX - this.dir * 0.9, 1.55, -0.5);
    g.add(pole);
    for (let i = 0; i < 3; i++) {
      const horn = new Mesh(new ConeGeometry(0.28, 0.5, 12, 1, true), stdMat(0xfacc15, 0.35, 0.6, 0x000000, 0, { side: DoubleSide }));
      horn.rotation.z = -Math.PI / 2 * this.dir;
      horn.position.set(this.startX - this.dir * 0.7, 2.2 + i * 0.42, -0.5);
      g.add(horn);
    }
    const waves = [];
    for (let i = 0; i < 4; i++) {
      const w = new Mesh(new TorusGeometry(0.55, 0.055, 8, 28), basicMat(i % 2 ? 0xfacc15 : 0xef4444, { transparent: true, opacity: 0.9, blending: AdditiveBlending }));
      w.rotation.y = Math.PI / 2;
      w.position.set(this.startX, 1.4, 0.15);
      w.visible = false;
      g.add(w);
      waves.push(w);
    }
    const tiger = new Mesh(
      new PlaneGeometry(2.1, 2.1),
      basicMat(0xffffff, {
        map: bannerTex(256, 256, (ctx) => {
          ctx.fillStyle = "#b91c1c";
          ctx.beginPath();
          ctx.arc(128, 128, 120, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = "#facc15";
          ctx.lineWidth = 10;
          ctx.stroke();
          ctx.fillStyle = "#facc15";
          ctx.font = "bold 52px Impact, sans-serif";
          ctx.textAlign = "center";
          ctx.fillText("PULI", 128, 122);
          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 28px Impact, sans-serif";
          ctx.fillText("ROAR!!", 128, 170);
        }),
        transparent: true,
        side: DoubleSide
      })
    );
    tiger.position.set(this.startX, 1.4, 0.1);
    tiger.visible = false;
    g.add(tiger);
    return { group: g, waves, tiger };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, fx, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("l1", 0.06, () => {
      speech("caster", "Oru thadava saappittu 27,000 vidhaigal vidhaikkudhu!");
      audio.stampSlam?.();
    });
    this.once("l2", 1.35, () => {
      popup("27,000 VIDHAI SOUNDWAVES!", this.v2.set(this.targetX0, 2.5, 0.4), "#facc15");
      audio.whoosh?.();
    });
    this.once("l3", this.IMPACT, () => {
      this.landImpact({ vx: 6.2, vy: 8.8, color: 0xfacc15, banner: "PULI ROAR!!" });
    });

    this.setTargetFreeze(dt, { headF: -0.35 });

    if (t < 1.35) {
      caster.y = 0.85 * easeOut(t / 0.5);
      this.casterClip = { name: "longhook", time: t * 1.0, fade: 0.1 };
      arena.setMood(0.5);
      cam.set(this.v2.set(caster.x + d * 1.4, 2.1, 4.4), this.v3.set(caster.x, 1.5, 0), 4, 42);
    } else if (t < this.IMPACT) {
      const u = (t - 1.35) / (this.IMPACT - 1.35);
      this.stage.waves.forEach((w, i) => {
        w.visible = true;
        const p = (u * 2.2 + i * 0.25) % 1;
        w.position.set(this.startX + (this.targetX0 - this.startX) * p, 1.35, 0.15);
        w.scale.setScalar(0.5 + p * 1.6);
      });
      this.stage.tiger.visible = u > 0.55;
      if (this.stage.tiger.visible) {
        const k = (u - 0.55) / 0.45;
        this.stage.tiger.position.set(caster.x + (this.targetX0 - caster.x) * k, 1.45, 0.15);
        this.stage.tiger.scale.setScalar(0.8 + k * 0.6);
      }
      caster.x = clampArenaX(this.startX + (this.targetX0 - d * 0.9 - this.startX) * easeInOut(u));
      caster.y = 0.85 * (1 - u);
      this.casterClip = { name: u < 0.5 ? "bodypunch" : "roundhouse", time: u * 1.7, fade: 0.08 };
      arena.setMood(0.7);
      cam.set(this.v2.set((caster.x + this.targetX0) / 2, 2.0, 5.6), this.v3.set(this.targetX0, 1.25, 0), 4, 44);
    } else {
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      caster.y = 0;
      this.stage.group.visible = false;
      this.casterClip = { name: "palm", time: 0.4 + u * 0.5, fade: 0.15 };
      arena.setMood(0.7 * (1 - u));
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 6.9), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) {
      caster.y = 0;
      this.done = true;
    }
  }
}

/* ============================================================================
 * 9. PERIYAR (mbapu): Vaikom Flame Torch + Shattering Iron Dogma Chains
 * ============================================================================ */
class PeriyarTorchSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.75;
    this.IMPACT = 3.3;
    this.props = this.buildTorchAndChains();
    this.root.add(this.props.group);
    d.audio.startSuperBed?.(3.2, "chant");
  }

  buildTorchAndChains() {
    const g = new Group();
    const torch = new Group();
    const stick = new Mesh(new CylinderGeometry(0.035, 0.045, 1.15, 8), stdMat(0x27272a, 0.7));
    stick.position.y = 0.55;
    const cup = new Mesh(new ConeGeometry(0.14, 0.25, 10), stdMat(0xfacc15, 0.3, 0.85));
    cup.rotation.z = Math.PI;
    cup.position.y = 1.18;
    const flame = makeGlow(0xfacc15, 1.35, 0.9);
    flame.position.y = 1.38;
    torch.add(stick, cup, flame);
    torch.position.set(this.startX, 1.1, 0.2);
    g.add(torch);

    const chains = [];
    const chainMat = stdMat(0x52525b, 0.45, 0.85);
    for (let i = 0; i < 5; i++) {
      const ring = new Mesh(new TorusGeometry(0.65, 0.055, 8, 22), chainMat);
      ring.position.set(this.targetX0, 0.45 + i * 0.35, 0);
      ring.rotation.set(Math.PI / 2 + (i % 2 ? 0.35 : -0.35), 0.3 * i, 0);
      g.add(ring);
      chains.push(ring);
    }
    return { group: g, torch, chains };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, fx, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("b1", 0.06, () => {
      speech("caster", "Nambamal poottu podringle — adhu thaan Naathigam!");
      audio.whoosh?.();
    });
    this.once("b2", 1.45, () => {
      popup("SUYAMARIYADHAI THEEPANDHAM!", this.v2.set(caster.x, 2.8, 0.3), "#facc15");
      audio.charge?.(1.5, "chakra");
    });
    this.once("b3", this.IMPACT, () => {
      this.landImpact({
        vx: 7.5,
        vy: 9.2,
        share: caster.superShare ?? 0.3,
        color: 0xfacc15,
        banner: "SUYAMARIYADHAI!"
      });
    });

    this.setTargetFreeze(dt, { headF: -0.3 });

    if (t < 1.45) {
      const u = easeOut(t / 1.45);
      caster.y = 1.05 * u;
      this.casterClip = { name: u < 0.5 ? "armsup" : "lotus", time: t, loop: true, fade: 0.15 };
      this.props.torch.position.set(caster.x + d * 0.42, caster.y + 0.9, 0.22);
      arena.setMood(0.65 * u);
      cam.set(this.v2.set(caster.x + d * 1.4, 2.0, 4.4), this.v3.set(caster.x, caster.y + 1.0, 0), 4, 42);
    } else if (t < this.IMPACT) {
      const u = (t - 1.45) / (this.IMPACT - 1.45);
      caster.x = clampArenaX(this.startX + (this.targetX0 - d * 0.95 - this.startX) * easeInOut(u));
      caster.y = 1.05 * (1 - u * 0.6);
      this.casterClip = { name: u < 0.55 ? "hurricane" : "flyingkick", time: u * 1.6, fade: 0.08 };
      this.props.torch.position.set(caster.x + d * 0.5, caster.y + 1.05, 0.2);
      this.props.torch.rotation.z = -d * u * 10;
      this.props.chains.forEach((c, i) => {
        c.rotation.z += dt * (i % 2 ? 4 : -4);
      });
      arena.setMood(0.8);
      cam.set(this.v2.set((caster.x + this.targetX0) / 2, 2.1, 5.4), this.v3.set(this.targetX0, 1.3, 0), 4, 44);
    } else {
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      caster.y = 0;
      this.props.chains.forEach((c, i) => {
        c.position.y += dt * (2.5 + i);
        c.position.x += dt * ((i % 2 ? 1 : -1) * 3.5);
        c.scale.setScalar(Math.max(0.01, 1 - u));
      });
      this.props.torch.position.set(caster.x + d * 0.35, 0.9, 0.2);
      this.props.torch.rotation.z = 0;
      this.casterClip = { name: "bow", time: Math.min(1.5, u * 1.4), fade: 0.15 };
      arena.setMood(0.8 * (1 - u));
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 7.0), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) {
      caster.y = 0;
      this.done = true;
    }
  }
}

/* ============================================================================
 * 10. ANNAMALAI (amit): 12 Reporter Mics Press Meet + DMK Files Avalanche
 * ============================================================================ */
class AnnamalaiPressSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.65;
    this.IMPACT = 3.25;
    this.press = this.buildPressMeet();
    this.root.add(this.press.group);
    d.audio.startSuperBed?.(3.0, "chant");
  }

  buildPressMeet() {
    const g = new Group();
    const micColors = [0xdc2626, 0x0284c7, 0xfacc15, 0x16a34a, 0xf97316, 0x7c3aed];
    const mics = new Group();
    for (let i = 0; i < 10; i++) {
      const a = -0.8 + (i / 9) * 1.6;
      const stick = new Mesh(new CylinderGeometry(0.018, 0.018, 1.15, 6), stdMat(0x18181b, 0.5));
      stick.rotation.z = -0.75 * this.dir;
      stick.position.set(Math.cos(a) * 0.75 * this.dir, 0.9 + (i % 3) * 0.14, Math.sin(a) * 0.6);
      const cube = new Mesh(new BoxGeometry(0.14, 0.14, 0.14), basicMat(micColors[i % micColors.length]));
      cube.position.copy(stick.position).add(new Vector3(-0.35 * this.dir, 0.36, 0));
      mics.add(stick, cube);
    }
    mics.position.set(this.startX + this.dir * 0.65, 0, 0.15);
    g.add(mics);

    const files = [];
    for (let i = 0; i < 8; i++) {
      const folder = new Mesh(new BoxGeometry(0.55, 0.14, 0.42), stdMat(i % 2 ? 0xdc2626 : 0xf97316, 0.6));
      folder.position.set(this.targetX0 + ((i % 3) - 1) * 0.35, 5.5 + i * 0.45, ((i % 2) - 0.5) * 0.25);
      folder.visible = false;
      g.add(folder);
      files.push(folder);
    }
    return { group: g, mics, files };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, fx, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("m1", 0.06, () => {
      speech("caster", "Ellathaiyum paathutten! Ellathaiyum paathachu!");
      audio.stampSlam?.();
    });
    this.once("m2", 1.35, () => {
      popup("TOP SECRET FILES AVALANCHE!", this.v2.set(this.targetX0, 2.5, 0.4), "#f97316");
      audio.hit?.(0.95);
    });
    this.once("m3", this.IMPACT, () => {
      this.landImpact({ vx: 6.1, vy: 8.8, color: 0xf97316, banner: "PRESS MEET CHECKMATE!" });
    });

    this.setTargetFreeze(dt, { headF: -0.3 });

    if (t < 1.35) {
      this.casterClip = { name: t < 0.7 ? "rhguard" : "palm", time: t * 1.1, fade: 0.1 };
      arena.setMood(0.5);
      cam.set(this.v2.set(caster.x + d * 1.5, 1.65, 3.9), this.v3.set(caster.x, 1.3, 0), 4, 41);
    } else if (t < this.IMPACT) {
      const u = (t - 1.35) / (this.IMPACT - 1.35);
      this.press.mics.visible = false;
      this.press.files.forEach((f, i) => {
        f.visible = true;
        const drop = clamp01(u * 1.5 - i * 0.07);
        f.position.y = 5.4 * (1 - drop) + 0.35 + i * 0.14;
        f.rotation.y += dt * 3;
      });
      caster.x = clampArenaX(this.startX + (this.targetX0 - d * 0.9 - this.startX) * easeOut(u));
      this.casterClip = { name: u < 0.55 ? "sbcombo" : "sidekick", time: u * 1.8, fade: 0.08 };
      arena.setMood(0.72);
      cam.set(this.v2.set((caster.x + this.targetX0) / 2, 2.1, 5.5), this.v3.set(this.targetX0, 1.3, 0), 4, 44);
    } else {
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      this.press.files.forEach((f, i) => {
        f.position.x += dt * d * (3 + i * 0.6);
        f.position.y += dt * 2.5;
        f.scale.setScalar(Math.max(0.01, 1 - u));
      });
      this.casterClip = { name: "palm", time: 0.5, fade: 0.15 };
      arena.setMood(0.72 * (1 - u));
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 6.9), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) this.done = true;
  }
}

/* ============================================================================
 * 11. MG NA (dhruv): Studio Ring Light + Red Clickbait Arrows + 10M Play Meteor
 * ============================================================================ */
class MgNaYouTubeSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.65;
    this.IMPACT = 3.25;
    this.yt = this.buildStudioAndHounds();
    this.root.add(this.yt.group);
    d.audio.startSuperBed?.(3.0, "engine");
  }

  buildStudioAndHounds() {
    const g = new Group();
    // Ring Light on Tripod
    const ring = new Mesh(new TorusGeometry(0.45, 0.04, 10, 28), basicMat(0x22d3ee));
    ring.position.set(this.startX + this.dir * 0.75, 1.65, 0.35);
    const stand = new Mesh(new CylinderGeometry(0.02, 0.03, 1.45, 6), stdMat(0x18181b, 0.6));
    stand.position.set(this.startX + this.dir * 0.75, 0.72, 0.35);
    g.add(ring, stand);

    // 3 Red Clickbait Arrows
    const arrows = [];
    for (let i = 0; i < 3; i++) {
      const ar = new Group();
      const shaft = new Mesh(new BoxGeometry(0.65, 0.16, 0.08), basicMat(0xef4444));
      const tip = new Mesh(new ConeGeometry(0.24, 0.36, 4), basicMat(0xef4444));
      tip.rotation.z = -Math.PI / 2;
      tip.position.x = 0.45;
      ar.add(shaft, tip);
      ar.position.set(this.startX, 1.4 + i * 0.35, 0.2);
      ar.visible = false;
      g.add(ar);
      arrows.push(ar);
    }

    // Gold 10M Play Button + White Rajapalayam Hounds
    const play = new Group();
    const plaque = new Mesh(new BoxGeometry(1.6, 1.15, 0.18), stdMat(0xfacc15, 0.2, 0.9, 0xca8a04, 0.4));
    const tri = new Mesh(new ConeGeometry(0.32, 0.42, 3), basicMat(0xffffff));
    tri.rotation.z = -Math.PI / 2;
    tri.position.z = 0.12;
    play.add(plaque, tri);
    play.position.set(this.targetX0, 6.2, 0.1);
    play.visible = false;
    g.add(play);

    const hound = new Group();
    const hMat = stdMat(0xf8fafc, 0.45);
    const torso = new Mesh(new BoxGeometry(0.75, 0.32, 0.24), hMat);
    const head = new Mesh(new BoxGeometry(0.28, 0.22, 0.2), hMat);
    head.position.set(0.45 * this.dir, 0.16, 0);
    hound.add(torso, head);
    hound.position.set(this.startX, 0.55, 0.3);
    hound.visible = false;
    g.add(hound);

    return { group: g, ring, stand, arrows, play, hound };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, fx, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("u1", 0.06, () => {
      speech("caster", "Hello everyone, naan Madan Gowri! Hello my dear MG Squad!");
      audio.whoosh?.();
    });
    this.once("u2", 1.35, () => {
      popup("10M VIEWS · RED CLICKBAIT ARROWS!", this.v2.set(this.targetX0, 2.5, 0.4), "#22d3ee");
      audio.hit?.(0.95);
    });
    this.once("u3", this.IMPACT, () => {
      this.landImpact({ vx: 6.2, vy: 8.8, color: 0x22d3ee, flash: "rgba(180,245,255,0.85)", banner: "10M GOLD PLAY SLAM!" });
    });

    this.setTargetFreeze(dt, { headF: -0.35 });

    if (t < 1.35) {
      this.casterClip = { name: t < 0.7 ? "bxguard" : "bxjab", time: t * 1.2, fade: 0.1 };
      arena.setMood(0.55);
      cam.set(this.v2.set(caster.x + d * 1.4, 1.65, 3.8), this.v3.set(caster.x, 1.35, 0), 4, 41);
    } else if (t < this.IMPACT) {
      const u = (t - 1.35) / (this.IMPACT - 1.35);
      this.yt.arrows.forEach((a, i) => {
        a.visible = true;
        const p = clamp01(u * 1.4 - i * 0.12);
        a.position.set(caster.x + (this.targetX0 - caster.x) * p, 1.0 + i * 0.38, 0.15);
        a.rotation.z = d > 0 ? 0 : Math.PI;
      });
      this.yt.play.visible = u > 0.35;
      this.yt.hound.visible = u > 0.35;
      if (this.yt.play.visible) {
        const k = easeInOut((u - 0.35) / 0.65);
        this.yt.play.position.y = 5.4 * (1 - k * k) + 0.9;
        this.yt.hound.position.set(caster.x + (this.targetX0 - caster.x) * k, 0.55 + Math.sin(k * Math.PI) * 0.9, 0.3);
      }
      caster.x = clampArenaX(this.startX + (this.targetX0 - d * 1.0 - this.startX) * easeOut(u));
      this.casterClip = { name: u < 0.55 ? "bxflurry" : "flyingkick", time: u * 1.8, fade: 0.08 };
      arena.setMood(0.72);
      cam.set(this.v2.set((caster.x + this.targetX0) / 2, 2.1, 5.6), this.v3.set(this.targetX0, 1.3, 0), 4, 44);
    } else {
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      this.yt.group.visible = false;
      this.casterClip = { name: "crescent", time: 0.6, fade: 0.15 };
      arena.setMood(0.72 * (1 - u));
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 6.9), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) this.done = true;
  }
}

/* ============================================================================
 * 12. TAX MAAMI (nirmala): 28% Caramel Popcorn & Bahi-Khata GST Blast
 * ============================================================================ */
class NirmalaGstSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.35;
    this.IMPACT = 2.95;
    this.ledger = this.buildLedger();
    this.root.add(this.ledger.group);
    d.audio.startSuperBed?.(2.8, "tariff");
  }

  buildLedger() {
    const g = new Group();
    const coverTex = bannerTex(256, 320, (ctx, w, h) => {
      ctx.fillStyle = "#991b1b";
      ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = "#facc15";
      ctx.lineWidth = 10;
      ctx.strokeRect(10, 10, w - 20, h - 20);
      ctx.fillStyle = "#fef08a";
      ctx.textAlign = "center";
      ctx.font = "bold 36px Impact, sans-serif";
      ctx.fillText("28% GST", w / 2, 110);
      ctx.fillText("CARAMEL", w / 2, 165);
      ctx.fillText("VASOOL!", w / 2, 220);
    });
    const book = new Mesh(
      new BoxGeometry(1.75, 2.25, 0.35),
      [
        stdMat(0x7f1d1d, 0.5),
        stdMat(0x7f1d1d, 0.5),
        stdMat(0xfef3c7, 0.8),
        stdMat(0xfef3c7, 0.8),
        new MeshBasicMaterial({ map: coverTex }),
        stdMat(0x7f1d1d, 0.5)
      ]
    );
    book.position.set(this.targetX0, 6.5, 0.15);
    const popcornRing = [];
    for (let i = 0; i < 6; i++) {
      const sp = new Mesh(new SphereGeometry(0.18, 8, 8), stdMat(0xfde047, 0.7));
      g.add(sp);
      popcornRing.push(sp);
    }
    g.add(book);
    return { group: g, book, popcornRing };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("n1", 0.08, () => {
      speech("caster", "Main itna lehsun pyaaz nahi khati hoon ji!");
      audio.stampSlam?.();
    });
    this.once("n2", 1.3, () => {
      popup("BAHI-KHATA 28% SLAB!", this.v2.set(this.targetX0, 2.6, 0.3), "#facc15");
      audio.whoosh?.();
    });
    this.once("n3", this.IMPACT, () => {
      this.landImpact({ vx: 5.5, vy: 8.6, color: 0xa855f7, flash: "rgba(250,204,21,0.85)", banner: "28% GST VASOOL!" });
    });

    this.setTargetFreeze(dt, { headF: -0.3 });
    this.ledger.popcornRing.forEach((sp, i) => {
      const a = t * 4 + (i / 6) * Math.PI * 2;
      sp.position.set(this.targetX0 + Math.cos(a) * 1.1, 1.3 + Math.sin(t * 6 + i) * 0.35, Math.sin(a) * 0.7);
    });

    if (t < 1.3) {
      this.casterClip = { name: "palm_m", time: t * 0.9, fade: 0.1 };
      arena.setMood(0.55);
      cam.set(this.v2.set(caster.x + d * 1.4, 1.55, 3.9), this.v3.set(caster.x, 1.3, 0), 4, 42);
    } else if (t < this.IMPACT) {
      const u = (t - 1.3) / (this.IMPACT - 1.3);
      this.ledger.book.position.y = 6.5 * (1 - u * u) + 1.05;
      this.ledger.book.rotation.y = u * Math.PI * 2;
      this.casterClip = { name: "snapkick2", time: u * 1.0, fade: 0.08 };
      arena.setMood(0.7);
      cam.set(this.v2.set((caster.x + this.targetX0) / 2, 2.2, 5.8), this.v3.set(this.targetX0, 1.4, 0), 4, 44);
    } else {
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      this.ledger.group.visible = false;
      this.casterClip = { name: "palm", time: 0.5, fade: 0.15 };
      arena.setMood(0.7 * (1 - u));
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 6.8), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) this.done = true;
  }
}

/* ============================================================================
 * 13. RANGARAJ STUDIO (rangaraj): Kelvikku Enna Bathil Rapid-Fire Debate Lock
 * ============================================================================ */
class RangarajDebateSuper extends SouthSuperBase {
  constructor(d, h) {
    super(d, h);
    this.END = 4.4;
    this.IMPACT = 3.0;
    this.studio = this.buildStudio();
    this.root.add(this.studio.group);
    d.audio.startSuperBed?.(2.9, "sitar");
  }

  buildStudio() {
    const g = new Group();
    const rings = [];
    for (let i = 0; i < 4; i++) {
      const r = new Mesh(new TorusGeometry(0.45 + i * 0.18, 0.045, 8, 24), basicMat(i % 2 ? 0x38bdf8 : 0xef4444));
      r.rotation.y = Math.PI / 2;
      r.visible = false;
      g.add(r);
      rings.push(r);
    }
    const micTex = bannerTex(512, 160, (ctx, w, h) => {
      ctx.fillStyle = "#090d1a";
      ctx.fillRect(0, 0, w, h);
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 10;
      ctx.strokeRect(8, 8, w - 16, h - 16);
      ctx.fillStyle = "#facc15";
      ctx.textAlign = "center";
      ctx.font = "bold 44px Impact, sans-serif";
      ctx.fillText("KELVIKKU ENNA BATHIL?!", w / 2, 72);
      ctx.fillStyle = "#ef4444";
      ctx.font = "bold 30px sans-serif";
      ctx.fillText("🔇 OPPONENT MIC MUTED!", w / 2, 126);
    });
    const screen = new Mesh(new PlaneGeometry(3.8, 1.2), new MeshBasicMaterial({ map: micTex, side: DoubleSide }));
    screen.position.set(this.targetX0, 3.1, -0.8);
    g.add(screen);
    return { group: g, rings, screen };
  }

  step(dt) {
    this.t += dt;
    const t = this.t;
    const { caster, target, cam, arena, audio, speech, popup } = this.d;
    const d = this.dir;

    this.once("r1", 0.08, () => {
      speech("caster", "Dhairiyam purusha latchanam! Naan ungalai sollavillai!");
      audio.whoosh?.();
    });
    this.once("r2", 1.35, () => {
      popup("🔇 MIC MUTED IN STUDIO!", this.v2.set(this.targetX0, 2.5, 0.3), "#38bdf8");
      audio.hit?.(0.95);
    });
    this.once("r3", this.IMPACT, () => {
      this.landImpact({ vx: 5.8, vy: 8.5, color: 0x38bdf8, flash: "rgba(56,189,248,0.85)", banner: "PRIME TIME CHECKMATE!" });
    });

    this.setTargetFreeze(dt, { headF: -0.35 });
    if (t < 1.35) {
      this.casterClip = { name: "jab", time: (t * 2) % 0.8, fade: 0.08 };
      arena.setMood(0.55);
      cam.set(this.v2.set(caster.x + d * 1.4, 1.6, 3.8), this.v3.set(caster.x, 1.3, 0), 4, 42);
    } else if (t < this.IMPACT) {
      const u = (t - 1.35) / (this.IMPACT - 1.35);
      this.studio.rings.forEach((r, i) => {
        r.visible = true;
        const p = clamp01(u * 1.5 - i * 0.14);
        r.position.set(caster.x + (this.targetX0 - caster.x) * p, 1.25, 0.2);
        r.scale.setScalar(1 + p * 1.6);
      });
      this.casterClip = { name: "sidekick", time: u * 0.9, fade: 0.08 };
      arena.setMood(0.72);
      cam.set(this.v2.set((caster.x + this.targetX0) / 2, 2.1, 5.6), this.v3.set(this.targetX0, 1.3, 0), 4, 44);
    } else {
      const u = clamp01((t - this.IMPACT) / (this.END - this.IMPACT));
      this.studio.group.visible = false;
      this.casterClip = { name: "elbowupper", time: 0.5, fade: 0.15 };
      arena.setMood(0.72 * (1 - u));
      cam.set(this.v2.set((caster.x + target.x) / 2, 2.0, 6.8), this.v3.set(target.x, 1.0, 0), 3, 42);
    }
    if (t >= this.END) this.done = true;
  }
}

export function createSouthSuper(ctx, helpers) {
  switch (ctx.caster.char.id) {
    case "modi": return new StalinCycleSuper(ctx, helpers);
    case "rahul": return new ThalapathyBlitzSuper(ctx, helpers);
    case "didi": return new IronAmmaSuper(ctx, helpers);
    case "trump": return new PushpaSandalSuper(ctx, helpers);
    case "yogi": return new PinarayiSilverLineSuper(ctx, helpers);
    case "nitin": return new DksSilkBoardSuper(ctx, helpers);
    case "ravi": return new PowerStarOGSuper(ctx, helpers);
    case "lalu": return new SeemanMikeSetSuper(ctx, helpers);
    case "mbapu": return new PeriyarTorchSuper(ctx, helpers);
    case "amit": return new AnnamalaiPressSuper(ctx, helpers);
    case "nirmala": return new NirmalaGstSuper(ctx, helpers);
    case "rangaraj": return new RangarajDebateSuper(ctx, helpers);
    case "dhruv":
    default:
      return new MgNaYouTubeSuper(ctx, helpers);
  }
}
