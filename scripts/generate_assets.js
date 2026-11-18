const fs = require("node:fs");
const path = require("node:path");
const zlib = require("node:zlib");

const ROOT = path.resolve(__dirname, "..");
const PUBLIC = path.join(ROOT, "public");

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

// -------- Pure-Node PNG Encoder --------
const CRC_TABLE = new Uint32Array(256);
for (let n = 0; n < 256; n++) {
  let c = n;
  for (let k = 0; k < 8; k++) c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
  CRC_TABLE[n] = c >>> 0;
}
function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
function pngChunk(type, data) {
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length, 0);
  const typeBuf = Buffer.from(type, "ascii");
  const crcBuf = Buffer.alloc(4);
  crcBuf.writeUInt32BE(crc32(Buffer.concat([typeBuf, data])), 0);
  return Buffer.concat([len, typeBuf, data, crcBuf]);
}
function encodePng(w, h, rgba) {
  const stride = w * 4 + 1;
  const raw = Buffer.alloc(stride * h);
  for (let y = 0; y < h; y++) {
    raw[y * stride] = 0;
    rgba.copy(raw, y * stride + 1, y * w * 4, (y + 1) * w * 4);
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(w, 0);
  ihdr.writeUInt32BE(h, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 6; // RGBA
  const idat = zlib.deflateSync(raw, { level: 6 });
  return Buffer.concat([
    Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]),
    pngChunk("IHDR", ihdr),
    pngChunk("IDAT", idat),
    pngChunk("IEND", Buffer.alloc(0)),
  ]);
}

// -------- Tiny 2D Rasterizer --------
class Canvas2D {
  constructor(w, h) {
    this.w = w;
    this.h = h;
    this.buf = Buffer.alloc(w * h * 4);
  }
  blendPixel(x, y, r, g, b, a) {
    if (x < 0 || y < 0 || x >= this.w || y >= this.h || a <= 0) return;
    const i = (y * this.w + x) * 4;
    const alpha = Math.min(1, a);
    const inv = 1 - alpha;
    this.buf[i] = Math.round(this.buf[i] * inv + r * alpha);
    this.buf[i + 1] = Math.round(this.buf[i + 1] * inv + g * alpha);
    this.buf[i + 2] = Math.round(this.buf[i + 2] * inv + b * alpha);
    this.buf[i + 3] = Math.min(255, Math.round(this.buf[i + 3] + (255 - this.buf[i + 3]) * alpha));
  }
  fillRadialBg(c1, c2) {
    const cx = this.w * 0.5, cy = this.h * 0.44, maxR = Math.hypot(this.w, this.h) * 0.6;
    for (let y = 0; y < this.h; y++) {
      for (let x = 0; x < this.w; x++) {
        const t = Math.min(1, Math.hypot(x - cx, y - cy) / maxR);
        const i = (y * this.w + x) * 4;
        this.buf[i] = Math.round(c1[0] + (c2[0] - c1[0]) * t);
        this.buf[i + 1] = Math.round(c1[1] + (c2[1] - c1[1]) * t);
        this.buf[i + 2] = Math.round(c1[2] + (c2[2] - c1[2]) * t);
        this.buf[i + 3] = 255;
      }
    }
  }
  fillEllipse(cx, cy, rx, ry, col, alpha = 1) {
    const x0 = Math.max(0, Math.floor(cx - rx - 2)), x1 = Math.min(this.w - 1, Math.ceil(cx + rx + 2));
    const y0 = Math.max(0, Math.floor(cy - ry - 2)), y1 = Math.min(this.h - 1, Math.ceil(cy + ry + 2));
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2;
        if (d <= 1.05) {
          const edge = d <= 0.94 ? 1 : Math.max(0, (1.05 - d) / 0.11);
          this.blendPixel(x, y, col[0], col[1], col[2], alpha * edge);
        }
      }
    }
  }
  fillRect(x0, y0, w, h, col, alpha = 1) {
    const xa = Math.max(0, Math.floor(x0)), xb = Math.min(this.w - 1, Math.ceil(x0 + w));
    const ya = Math.max(0, Math.floor(y0)), yb = Math.min(this.h - 1, Math.ceil(y0 + h));
    for (let y = ya; y <= yb; y++) {
      for (let x = xa; x <= xb; x++) {
        this.blendPixel(x, y, col[0], col[1], col[2], alpha);
      }
    }
  }
  fillArc(cx, cy, rx, ry, yMinFrac, yMaxFrac, col, alpha = 1) {
    const x0 = Math.max(0, Math.floor(cx - rx - 2)), x1 = Math.min(this.w - 1, Math.ceil(cx + rx + 2));
    const y0 = Math.max(0, Math.floor(cy + ry * yMinFrac)), y1 = Math.min(this.h - 1, Math.ceil(cy + ry * yMaxFrac));
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2;
        if (d <= 1.04) this.blendPixel(x, y, col[0], col[1], col[2], alpha * (d <= 0.94 ? 1 : (1.04 - d) / 0.1));
      }
    }
  }
  strokeLine(x0, y0, x1, y1, r, col, alpha = 1) {
    const steps = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0)));
    for (let i = 0; i <= steps; i++) {
      const t = i / steps;
      this.fillEllipse(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r, r, col, alpha);
    }
  }
  drawGlasses(cx, cy, lensCol, frameCol, shades = false) {
    const ew = 28, eh = 18, sep = 34;
    // Frame
    this.fillRect(cx - sep - ew - 4, cy - eh - 4, ew * 2 + 8, eh * 2 + 8, frameCol);
    this.fillRect(cx + sep - ew - 4, cy - eh - 4, ew * 2 + 8, eh * 2 + 8, frameCol);
    this.fillRect(cx - 10, cy - 5, 20, 6, frameCol);
    if (shades) {
      this.fillRect(cx - sep - ew, cy - eh, ew * 2, eh * 2, lensCol);
      this.fillRect(cx + sep - ew, cy - eh, ew * 2, eh * 2, lensCol);
      this.strokeLine(cx - sep - 14, cy - 10, cx - sep + 8, cy + 8, 2.5, [255, 255, 255], 0.45);
      this.strokeLine(cx + sep - 14, cy - 10, cx + sep + 8, cy + 8, 2.5, [255, 255, 255], 0.45);
    } else {
      this.fillRect(cx - sep - ew, cy - eh, ew * 2, eh * 2, [242, 248, 255], 0.35);
      this.fillRect(cx + sep - ew, cy - eh, ew * 2, eh * 2, [242, 248, 255], 0.35);
    }
  }
}

function drawFighterPortrait(spec) {
  const c = new Canvas2D(256, 256);
  c.fillRadialBg(spec.bg1, spec.bg2);
  // Subtle stage sunburst
  c.fillEllipse(128, 128, 114, 114, spec.glow, 0.22);

  // Shoulders / Shirt / Shawl
  c.fillEllipse(128, 245, 96, 60, spec.shirt);
  if (spec.shawl) {
    c.strokeLine(52, 205, 95, 255, 16, spec.shawl, 0.96);
    c.strokeLine(204, 205, 161, 255, 16, spec.shawl, 0.96);
    if (spec.shawl2) {
      c.strokeLine(60, 212, 95, 255, 6, spec.shawl2, 0.95);
      c.strokeLine(196, 212, 161, 255, 6, spec.shawl2, 0.95);
    }
  }
  // Neck
  c.fillRect(108, 168, 40, 38, spec.skinShade);

  // Ears
  c.fillEllipse(66, 128, 11, 18, spec.skinShade);
  c.fillEllipse(190, 128, 11, 18, spec.skinShade);

  // Head
  c.fillEllipse(128, 120, 58, 68, spec.skin);

  // Forehead markings
  if (spec.tilak) c.fillRect(124, 72, 8, 20, spec.tilak);
  if (spec.pottu) c.fillEllipse(128, 86, 7, 7, spec.pottu);
  if (spec.vibhuti) {
    for (const dy of [-5, 0, 5]) c.strokeLine(104, 80 + dy, 152, 80 + dy, 1.5, [248, 248, 250], 0.9);
  }

  // Hair / Bouffant / Quiff
  if (spec.bun) c.fillEllipse(128, 52, 34, 24, spec.hair);
  if (spec.hairStyle === "swept") {
    c.fillArc(128, 86, 62, 54, -1.0, -0.05, spec.hair);
    c.fillEllipse(128, 60, 52, 22, spec.hair);
  } else if (spec.hairStyle === "parted") {
    c.fillArc(128, 88, 60, 50, -1.0, -0.05, spec.hair);
    c.fillEllipse(102, 66, 36, 16, spec.hair);
    c.fillEllipse(154, 68, 30, 14, spec.hair);
  } else if (spec.hairStyle === "bushy") {
    c.fillEllipse(128, 64, 62, 30, spec.hair);
    c.fillEllipse(84, 82, 24, 26, spec.hair);
    c.fillEllipse(172, 82, 24, 26, spec.hair);
  } else if (spec.hairStyle === "quiff") {
    c.fillArc(128, 88, 58, 48, -1.0, -0.05, spec.hair);
    c.fillEllipse(136, 52, 38, 20, spec.hair);
  } else if (spec.hairStyle === "elder") {
    c.fillEllipse(76, 94, 14, 28, spec.hair);
    c.fillEllipse(180, 94, 14, 28, spec.hair);
    c.fillArc(128, 72, 48, 26, -1.0, 0.1, spec.hair, 0.8);
  }

  // Eyes & Brows
  c.fillEllipse(102, 114, 9, 6, [250, 250, 250]);
  c.fillEllipse(154, 114, 9, 6, [250, 250, 250]);
  c.fillEllipse(102, 114, 4.5, 4.5, [28, 20, 16]);
  c.fillEllipse(154, 114, 4.5, 4.5, [28, 20, 16]);
  c.strokeLine(86, 100, 116, 102, 3.2, spec.hair);
  c.strokeLine(140, 102, 170, 100, 3.2, spec.hair);

  // Nose
  c.strokeLine(128, 114, 128, 134, 3, spec.skinShade);
  c.fillEllipse(128, 135, 8, 5, spec.skinShade, 0.65);

  // Stubble / Beard
  if (spec.beard === "full") {
    c.fillArc(128, 138, 56, 52, 0.0, 1.0, spec.beardCol || spec.hair);
  } else if (spec.beard === "long") {
    c.fillArc(128, 140, 56, 54, 0.0, 1.0, spec.beardCol || spec.hair);
    c.fillEllipse(128, 184, 38, 36, spec.beardCol || spec.hair);
  } else if (spec.beard === "stubble") {
    c.fillArc(128, 138, 55, 48, 0.08, 1.0, spec.beardCol || [50, 38, 32], 0.42);
  }

  // Mouth
  c.strokeLine(112, 152, 144, 150, 3.5, spec.mouth || [125, 48, 48]);
  if (spec.grin) c.strokeLine(116, 151, 140, 149, 2, [250, 245, 240]);

  // Moustache
  if (spec.stache) {
    const mc = spec.beardCol || spec.hair;
    c.fillEllipse(116, 142, 16, 6, mc);
    c.fillEllipse(140, 142, 16, 6, mc);
    if (spec.curledStache) {
      c.strokeLine(100, 142, 92, 134, 3.5, mc);
      c.strokeLine(156, 142, 164, 134, 3.5, mc);
    }
  }

  // Glasses / Shades
  if (spec.glasses) {
    c.drawGlasses(128, 115, spec.lens || [22, 22, 28], spec.frame || [25, 22, 22], !!spec.shades);
  }

  // Podcaster headset for Roast Bro
  if (spec.headset) {
    c.fillEllipse(62, 124, 11, 24, [24, 32, 46]);
    c.fillEllipse(194, 124, 11, 24, [24, 32, 46]);
    c.strokeLine(66, 136, 114, 154, 2.5, [40, 190, 220]);
  }

  return encodePng(256, 256, c.buf);
}

function drawNirmalaPortrait() {
  // Tall card proportion (~576x1600 -> 216x600)
  const w = 216, h = 600;
  const c = new Canvas2D(w, h);
  c.fillRadialBg([118, 22, 34], [40, 6, 14]);
  // Gold zari saree torso
  c.fillEllipse(108, 410, 88, 210, [145, 20, 42]);
  c.strokeLine(42, 250, 165, 570, 22, [235, 185, 58], 0.92);
  c.fillRect(24, 520, 168, 80, [110, 12, 28]);
  // Ledger / GST brief book held up
  c.fillRect(46, 330, 124, 110, [186, 28, 28]);
  c.fillRect(54, 338, 108, 94, [215, 42, 36]);
  c.fillRect(68, 368, 80, 18, [255, 226, 120]);
  // Head & bun
  c.fillEllipse(108, 128, 48, 56, [184, 128, 92]);
  c.fillArc(108, 100, 50, 44, -1.0, -0.05, [35, 28, 26]);
  c.fillEllipse(142, 110, 18, 22, [245, 245, 232]); // jasmine flowers
  c.fillEllipse(108, 96, 6, 6, [210, 20, 20]); // pottu
  c.drawGlasses(108, 122, [240, 248, 255], [190, 150, 45], false);
  c.strokeLine(96, 154, 120, 154, 3, [120, 40, 40]);
  return encodePng(w, h, c.buf);
}

function drawUpiQr() {
  const c = new Canvas2D(256, 256);
  c.fillRect(0, 0, 256, 256, [255, 250, 240]);
  const mod = 8, off = 16, n = 28;
  let seed = 0x517cc1b7;
  const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);
  const drawFinder = (gx, gy) => {
    c.fillRect(off + gx * mod, off + gy * mod, 7 * mod, 7 * mod, [28, 16, 10]);
    c.fillRect(off + (gx + 1) * mod, off + (gy + 1) * mod, 5 * mod, 5 * mod, [255, 250, 240]);
    c.fillRect(off + (gx + 2) * mod, off + (gy + 2) * mod, 3 * mod, 3 * mod, [28, 16, 10]);
  };
  for (let y = 0; y < n; y++) {
    for (let x = 0; x < n; x++) {
      if ((x < 8 && y < 8) || (x >= n - 8 && y < 8) || (x < 8 && y >= n - 8)) continue;
      if (Math.abs(x - 14) < 3 && Math.abs(y - 14) < 3) continue;
      if (rnd() > 0.48) c.fillRect(off + x * mod, off + y * mod, mod, mod, [32, 18, 10]);
    }
  }
  drawFinder(0, 0);
  drawFinder(n - 7, 0);
  drawFinder(0, n - 7);
  c.fillEllipse(128, 128, 22, 22, [217, 119, 6]);
  c.fillEllipse(128, 128, 14, 14, [255, 245, 225]);
  c.fillEllipse(128, 129, 10, 7, [105, 55, 20]);
  return encodePng(256, 256, c.buf);
}

const PORTRAITS = {
  modi: { bg1: [210, 42, 42], bg2: [38, 12, 12], glow: [255, 210, 60], skin: [192, 134, 96], skinShade: [162, 106, 72], hair: [24, 22, 22], hairStyle: "swept", shirt: [242, 242, 240], shawl: [204, 24, 24], shawl2: [22, 22, 22], glasses: true, frame: [28, 28, 32], stache: true, grin: true },
  rahul: { bg1: [196, 30, 38], bg2: [46, 28, 8], glow: [250, 204, 21], skin: [184, 126, 90], skinShade: [152, 98, 66], hair: [24, 20, 18], hairStyle: "parted", shirt: [240, 240, 236], shawl: [185, 28, 28], shawl2: [245, 198, 22], beard: "stubble", shades: true, glasses: true, lens: [25, 22, 22], frame: [212, 165, 42], grin: true },
  didi: { bg1: [34, 148, 86], bg2: [14, 48, 28], glow: [255, 230, 140], skin: [188, 132, 98], skinShade: [158, 104, 74], hair: [42, 38, 38], hairStyle: "swept", bun: true, shirt: [22, 118, 66], shawl: [245, 210, 90], pottu: [200, 16, 24] },
  trump: { bg1: [230, 112, 24], bg2: [52, 18, 6], glow: [255, 185, 65], skin: [176, 118, 82], skinShade: [145, 92, 60], hair: [28, 22, 18], hairStyle: "bushy", shirt: [194, 82, 22], shawl: [240, 180, 62], beard: "full", shades: true, glasses: true, lens: [65, 24, 10], frame: [225, 175, 45], stache: true },
  yogi: { bg1: [185, 26, 26], bg2: [38, 6, 8], glow: [255, 120, 90], skin: [195, 140, 105], skinShade: [165, 112, 80], hair: [220, 222, 226], hairStyle: "swept", shirt: [242, 242, 242], shawl: [195, 24, 24], stache: true, curledStache: true },
  nitin: { bg1: [24, 118, 188], bg2: [12, 32, 64], glow: [250, 200, 60], skin: [188, 132, 94], skinShade: [158, 104, 70], hair: [34, 30, 28], hairStyle: "parted", shirt: [245, 245, 245], shawl: [22, 120, 192], shawl2: [245, 158, 28], beard: "full", shades: true, glasses: true, lens: [20, 28, 38], frame: [185, 185, 195] },
  ravi: { bg1: [218, 38, 38], bg2: [50, 12, 12], glow: [255, 220, 120], skin: [190, 134, 96], skinShade: [160, 106, 72], hair: [28, 24, 22], hairStyle: "parted", shirt: [244, 240, 232], shawl: [215, 32, 32], beard: "stubble", glasses: true, frame: [28, 28, 32], stache: true, tilak: [225, 42, 24] },
  lalu: { bg1: [222, 168, 24], bg2: [48, 22, 6], glow: [240, 60, 40], skin: [180, 122, 88], skinShade: [150, 96, 65], hair: [26, 24, 24], hairStyle: "swept", shirt: [235, 50, 38], shawl: [240, 188, 32], stache: true, curledStache: true, grin: true },
  mbapu: { bg1: [42, 42, 48], bg2: [10, 10, 14], glow: [245, 215, 95], skin: [186, 134, 98], skinShade: [156, 108, 76], hair: [238, 240, 245], hairStyle: "elder", shirt: [24, 24, 28], shawl: [24, 24, 28], beard: "long", beardCol: [238, 240, 245], glasses: true, frame: [18, 18, 20], stache: true },
  amit: { bg1: [228, 118, 24], bg2: [52, 22, 6], glow: [255, 168, 60], skin: [184, 126, 90], skinShade: [154, 98, 66], hair: [32, 28, 26], hairStyle: "parted", shirt: [26, 26, 30], shawl: [238, 124, 28], beard: "full", shades: true, glasses: true, lens: [28, 22, 18], frame: [200, 155, 40], vibhuti: true },
  dhruv: { bg1: [14, 168, 205], bg2: [8, 28, 48], glow: [34, 211, 238], skin: [198, 145, 110], skinShade: [168, 116, 84], hair: [36, 28, 22], hairStyle: "quiff", shirt: [28, 38, 56], shawl: [34, 211, 238], glasses: true, frame: [22, 211, 238], headset: true, grin: true }
};

// -------- Pure-Node WAV Synthesizer --------
const SR = 22050;
function writeWav(samples) {
  const n = samples.length;
  const buf = Buffer.alloc(44 + n * 2);
  buf.write("RIFF", 0);
  buf.writeUInt32LE(36 + n * 2, 4);
  buf.write("WAVE", 8);
  buf.write("fmt ", 12);
  buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20);
  buf.writeUInt16LE(1, 22);
  buf.writeUInt32LE(SR, 24);
  buf.writeUInt32LE(SR * 2, 28);
  buf.writeUInt16LE(2, 32);
  buf.writeUInt16LE(16, 34);
  buf.write("data", 36);
  buf.writeUInt32LE(n * 2, 40);
  for (let i = 0; i < n; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]));
    buf.writeInt16LE(Math.round(s * 32767), 44 + i * 2);
  }
  return buf;
}

function synthTrack(kind) {
  const bpm = kind === "battle" ? 136 : kind === "intro" ? 124 : 114;
  const beat = 60 / bpm;
  const bars = 4;
  const dur = bars * 4 * beat;
  const n = Math.floor(dur * SR);
  const out = new Float32Array(n);
  // Carnatic Shankarabharanam / Hamsadhwani-ish notes (C4, D4, E4, G4, A4, C5, D5, E5)
  const scale = [261.63, 293.66, 329.63, 392.0, 440.0, 523.25, 587.33, 659.25];
  const pattern = kind === "battle"
    ? [0, 2, 3, 5, 4, 3, 2, 1, 0, 3, 5, 7, 6, 5, 3, 2]
    : [0, 2, 4, 3, 2, 1, 0, 2, 3, 5, 4, 2, 1, 2, 0, -1];
  const totalSteps = bars * 4;
  for (let s = 0; s < totalSteps; s++) {
    const start = Math.floor(s * beat * SR);
    const len = Math.floor(beat * SR);
    const note = pattern[s % pattern.length];
    const isKick = (s % 4 === 0) || (kind === "battle" && s % 4 === 2);
    const isParai = (s % 2 === 1);
    for (let i = 0; i < len && start + i < n; i++) {
      const t = i / SR;
      let v = 0;
      if (isKick) {
        const kf = 125 * Math.exp(-t * 24) + 46;
        v += Math.sin(2 * Math.PI * kf * t) * Math.exp(-t * 14) * 0.42;
      }
      if (isParai) {
        v += (Math.sin(2 * Math.PI * 240 * t) * 0.25 + (Math.random() * 2 - 1) * 0.28) * Math.exp(-t * 28);
      }
      if (note >= 0) {
        const f = scale[note] * (kind === "intro" ? 1 : 0.5);
        const env = Math.min(1, t * 40) * Math.exp(-t * (kind === "battle" ? 6.5 : 4.5));
        v += (Math.sin(2 * Math.PI * f * t) * 0.16 + Math.sin(2 * Math.PI * f * 2 * t) * 0.06) * env;
      }
      out[start + i] += v * 0.72;
    }
  }
  return writeWav(out);
}

function synthSfx(name) {
  let seed = 0;
  for (const ch of name) seed = (seed * 31 + ch.charCodeAt(0)) >>> 0;
  const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296) * 2 - 1;

  let dur = 0.35;
  if (/music|bed_|engine_loop|drone/.test(name)) dur = 2.4;
  else if (/charge_|drumroll|jingle_|win|lose|intro|modi|rahul|didi|trump|yogi|nitin|ravi|lalu|mbapu|amit|dhruv|nirmala|gulaam/.test(name)) dur = 0.85;
  else if (/ko|perfect|fight|round_|final_round|time_up|release_|thunder|news_sting|horn_long|boom|bomb/.test(name)) dur = 0.65;
  else if (/ui_tap|ui_select|tick|plop|snap/.test(name)) dur = 0.14;

  const n = Math.floor(dur * SR);
  const out = new Float32Array(n);
  const baseHz = 180 + (seed % 320);

  for (let i = 0; i < n; i++) {
    const t = i / SR;
    const p = t / dur;
    let v = 0;
    if (/hit|slap|thud|block|crate_crash|metal_crunch|stamp_slam/.test(name)) {
      const f = 220 * Math.exp(-t * 22) + 55;
      v = (Math.sin(2 * Math.PI * f * t) * 0.65 + rnd() * 0.38) * Math.exp(-t * 16);
    } else if (/boom|bomb|thunder|pataka|release_/.test(name)) {
      const f = 140 * Math.exp(-t * 5) + 42;
      v = (Math.sin(2 * Math.PI * f * t) * 0.55 + rnd() * 0.55) * Math.exp(-t * 4.5);
    } else if (/chai_ting|cow_bell|bell|kaching|coins|shimmer/.test(name)) {
      const f1 = name.includes("coins") || name.includes("kaching") ? 1320 : 880;
      const f2 = f1 * (p > 0.35 ? 1.5 : 1.25);
      v = (Math.sin(2 * Math.PI * f1 * t) + 0.5 * Math.sin(2 * Math.PI * f2 * t)) * Math.exp(-t * 8) * 0.5;
    } else if (/horn|moo|bark|frog|engine|drone|bed_/.test(name)) {
      const f = name.includes("moo") ? 130 - t * 30 : name.includes("bark") ? 280 - t * 220 : 210 + Math.sin(t * 18) * 18;
      const saw = ((t * f) % 1) * 2 - 1;
      v = saw * 0.36 * Math.sin(Math.PI * Math.min(1, p));
    } else if (/voice\/|round_|final_round|fight|ko|perfect|time_up|you_win|you_lose|jingle_|news_sting/.test(name)) {
      const notes = [baseHz, baseHz * 1.25, baseHz * 1.5, baseHz * 2];
      const f = notes[Math.min(notes.length - 1, Math.floor(p * notes.length))];
      v = (Math.sin(2 * Math.PI * f * t) * 0.45 + Math.sin(2 * Math.PI * f * 1.5 * t) * 0.18) * (1 - p * 0.7);
    } else {
      const f = name.includes("ui_") ? 520 + (name.includes("confirm") ? 220 * Math.floor(p * 2) : 0) : baseHz + 180 * Math.sin(p * Math.PI);
      v = Math.sin(2 * Math.PI * f * t) * Math.exp(-t * 11) * 0.45;
    }
    out[i] = Math.max(-0.9, Math.min(0.9, v));
  }
  return writeWav(out);
}

// 1. Write Portraits & Art
for (const [id, spec] of Object.entries(PORTRAITS)) {
  const png = drawFighterPortrait(spec);
  const out = path.join(PUBLIC, "faces", `${id}.webp`);
  ensureDir(out);
  fs.writeFileSync(out, png);
}
const nirmalaPng = drawNirmalaPortrait();
for (const p of ["art/nirmala.webp", "art/mobile/nirmala.webp"]) {
  const out = path.join(PUBLIC, p);
  ensureDir(out);
  fs.writeFileSync(out, nirmalaPng);
}
const qrOut = path.join(PUBLIC, "art/upi-qr.png");
ensureDir(qrOut);
fs.writeFileSync(qrOut, drawUpiQr());

// 2. Scan main-C7-oASSx.js for every /assets/*.mp3 URL so ZERO 404s occur
const bundle = fs.readFileSync(path.join(PUBLIC, "assets/main-C7-oASSx.js"), "utf8");
const audioUrls = [...new Set(bundle.match(/\/assets\/[a-zA-Z0-9_\/-]+\.mp3/g) || [])];

const trackIntro = synthTrack("intro");
const trackBg = synthTrack("background");
const trackBattle = synthTrack("battle");

let count = 0;
for (const url of audioUrls) {
  const dest = path.join(PUBLIC, url.slice(1));
  ensureDir(dest);
  if (url.includes("/intro-")) fs.writeFileSync(dest, trackIntro);
  else if (url.includes("/background-")) fs.writeFileSync(dest, trackBg);
  else if (url.includes("/battle-")) fs.writeFileSync(dest, trackBattle);
  else fs.writeFileSync(dest, synthSfx(url));
  count++;
}

console.log(`Generated ${Object.keys(PORTRAITS).length} fighter portraits, 3 art files, and ${count} audio files.`);
