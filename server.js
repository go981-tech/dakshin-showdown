const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const { WebSocketServer } = require("ws");

const PORT = Number(process.env.PORT) || 3000;
const ROOT = __dirname;
const PUBLIC_DIR = path.join(ROOT, "public");
const MODULES_DIR = path.join(ROOT, "node_modules");

const CODE_CHARS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";
const ICE_PAYLOAD = {
  iceServers: [
    { urls: ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"] }
  ],
  relay: false
};

const EXT_MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".mjs": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".webmanifest": "application/manifest+json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
  ".glb": "model/gltf-binary",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".mp3": "audio/mpeg",
  ".wav": "audio/wav",
  ".mp4": "video/mp4"
};

const rooms = new Map();
const signals = new Map();

function makeRoomCode() {
  for (let i = 0; i < 64; i++) {
    let code = "";
    for (let j = 0; j < 4; j++) {
      code += CODE_CHARS[crypto.randomInt(CODE_CHARS.length)];
    }
    if (!rooms.has(code)) return code;
  }
  return "DK26";
}

function makeSecret() {
  return crypto.randomBytes(16).toString("hex");
}

function detectMime(filePath, buf) {
  if (buf.length >= 4 && buf[0] === 0x52 && buf[1] === 0x49 && buf[2] === 0x46 && buf[3] === 0x46) {
    return "audio/wav";
  }
  if (buf.length >= 4 && buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47) {
    return "image/png";
  }
  const head = buf.subarray(0, 64).toString("utf8").trimStart();
  if (head.startsWith("<svg")) return "image/svg+xml";
  const ext = path.extname(filePath).toLowerCase();
  return EXT_MIME[ext] || "application/octet-stream";
}

function sendJson(res, status, data) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store"
  });
  res.end(body);
}

function readJsonBody(req) {
  return new Promise((resolve) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}"));
      } catch {
        resolve({});
      }
    });
  });
}

function readRawJsonBody(req) {
  return new Promise((resolve) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      try {
        resolve({ ok: true, value: JSON.parse(Buffer.concat(chunks).toString("utf8") || "null") });
      } catch {
        resolve({ ok: false, value: null });
      }
    });
  });
}

function validateVoiceLines(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  for (const [fighter, lines] of Object.entries(value)) {
    if (fighter === "_meta") {
      if (!lines || typeof lines !== "object" || Array.isArray(lines)) return false;
      if (typeof lines.requireApproved !== "boolean") return false;
      continue;
    }
    if (!fighter || !lines || typeof lines !== "object" || Array.isArray(lines)) return false;
    for (const [lineId, line] of Object.entries(lines)) {
      if (!lineId || !line || typeof line !== "object" || Array.isArray(line)) return false;
      if (typeof line.text !== "string" || typeof line.audio !== "string") return false;
      if (typeof line.approved !== "boolean") return false;
      if ("matchScore" in line && (typeof line.matchScore !== "number" || !Number.isFinite(line.matchScore))) return false;
      if ("speakerScore" in line && (typeof line.speakerScore !== "number" || !Number.isFinite(line.speakerScore))) return false;
    }
  }
  return true;
}

function writeVoiceLinesAtomically(value) {
  const file = path.join(PUBLIC_DIR, "assets", "voice-lines.json");
  const tmp = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(value, null, 2) + "\n", "utf8");
  fs.renameSync(tmp, file);
}

function serveStatic(req, res, pathname) {
  let cleanPath;
  try {
    cleanPath = decodeURIComponent(pathname);
  } catch {
    res.writeHead(400);
    res.end("Bad Request");
    return;
  }
  if (cleanPath === "/") cleanPath = "/index.html";

  let baseDir = PUBLIC_DIR;
  let relPath = cleanPath.replace(/^\/+/, "");
  if (cleanPath.startsWith("/node_modules/")) {
    baseDir = MODULES_DIR;
    relPath = cleanPath.slice("/node_modules/".length);
  }

  const target = path.resolve(baseDir, relPath);
  if (target !== baseDir && !target.startsWith(baseDir + path.sep)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }

  fs.stat(target, (err, stat) => {
    if (err || !stat.isFile()) {
      res.writeHead(404);
      res.end("Not Found");
      return;
    }
    fs.readFile(target, (readErr, buf) => {
      if (readErr) {
        res.writeHead(500);
        res.end("Internal Server Error");
        return;
      }
      res.writeHead(200, {
        "Content-Type": detectMime(target, buf),
        "Content-Length": buf.length,
        "Cache-Control": target.endsWith("index.html") ? "no-cache" : "public, max-age=300"
      });
      res.end(buf);
    });
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);
  const { pathname, searchParams } = url;

  if (pathname === "/api/ice") {
    return sendJson(res, 200, ICE_PAYLOAD);
  }

  if (pathname === "/api/voice-lines") {
    const devOnly = process.env.NODE_ENV !== "production";
    if (!devOnly) return sendJson(res, 404, { error: "Not found" });
    const file = path.join(PUBLIC_DIR, "assets", "voice-lines.json");
    if (req.method === "GET") {
      try {
        const text = fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "");
        return sendJson(res, 200, JSON.parse(text));
      } catch {
        return sendJson(res, 500, { error: "Could not read voice lines" });
      }
    }
    if (req.method === "POST") {
      const parsed = await readRawJsonBody(req);
      if (!parsed.ok) return sendJson(res, 400, { error: "Invalid JSON" });
      if (!validateVoiceLines(parsed.value)) return sendJson(res, 400, { error: "Invalid voice-lines structure" });
      try {
        writeVoiceLinesAtomically(parsed.value);
        return sendJson(res, 200, { ok: true });
      } catch {
        return sendJson(res, 500, { error: "Could not save voice lines" });
      }
    }
    res.writeHead(405, { "Allow": "GET, POST" });
    return res.end();
  }

  if (pathname === "/api/room/close" && req.method === "POST") {
    const code = (searchParams.get("code") || "").toUpperCase();
    const secret = searchParams.get("secret") || "";
    const room = rooms.get(code);
    if (room && room.secret === secret) rooms.delete(code);
    return sendJson(res, 200, { ok: true });
  }

  if (pathname === "/api/room/join") {
    const code = (searchParams.get("code") || "").toUpperCase();
    const room = rooms.get(code);
    if (!room || !room.offer) return sendJson(res, 404, { error: "Room not found or not ready" });
    return sendJson(res, 200, { offer: room.offer, ice: ICE_PAYLOAD });
  }

  if (pathname === "/api/room/answer" && req.method === "POST") {
    const code = (searchParams.get("code") || "").toUpperCase();
    const room = rooms.get(code);
    if (!room) return sendJson(res, 404, { error: "Room not found" });
    const body = await readJsonBody(req);
    room.answer = body.answer || null;
    if (room.ws && room.ws.readyState === 1 && room.answer) {
      room.ws.send(JSON.stringify({ t: "answer", desc: room.answer }));
    }
    if (room.waiters) {
      for (const fn of room.waiters) fn(room.answer);
      room.waiters.clear();
    }
    return sendJson(res, 200, { ok: true });
  }

  if (pathname === "/api/room") {
    const code = (searchParams.get("code") || "").toUpperCase();
    const secret = searchParams.get("secret") || "";
    const action = searchParams.get("action") || "";

    if (req.method === "POST" && action === "answer") {
      const room = rooms.get(code);
      if (!room) return sendJson(res, 404, { error: "Room not found" });
      const body = await readJsonBody(req);
      room.answer = body.answer || null;
      if (room.ws && room.ws.readyState === 1 && room.answer) {
        room.ws.send(JSON.stringify({ t: "answer", desc: room.answer }));
      }
      if (room.waiters) {
        for (const fn of room.waiters) fn(room.answer);
        room.waiters.clear();
      }
      return sendJson(res, 200, { ok: true });
    }

    if (action === "signal") {
      const sid = searchParams.get("sid") || "";
      const kind = searchParams.get("kind") || "";
      const n = searchParams.get("n") || "0";
      const key = `${sid}:${kind}:${n}`;
      if (req.method === "POST") {
        const body = await readJsonBody(req);
        signals.set(key, body.desc || null);
        return sendJson(res, 200, { ok: true });
      }
      const desc = signals.get(key) || null;
      return sendJson(res, 200, { desc });
    }

    if (req.method === "POST") {
      const body = await readJsonBody(req);
      const newCode = makeRoomCode();
      const newSecret = makeSecret();
      rooms.set(newCode, {
        code: newCode,
        secret: newSecret,
        offer: body.offer || null,
        answer: null,
        ws: null,
        waiters: new Set(),
        createdAt: Date.now()
      });
      return sendJson(res, 200, { code: newCode, secret: newSecret });
    }

    if (req.method === "DELETE") {
      const room = rooms.get(code);
      if (room && room.secret === secret) rooms.delete(code);
      return sendJson(res, 200, { ok: true });
    }

    const room = rooms.get(code);
    if (!room) return sendJson(res, 404, { error: "Room not found" });
    if (secret && room.secret === secret) {
      if (room.answer) return sendJson(res, 200, { answer: room.answer });
      const waitSec = Math.min(25, Number(searchParams.get("wait") || 0));
      if (waitSec > 0) {
        return new Promise((resolve) => {
          const onAnswer = (ans) => {
            clearTimeout(timer);
            sendJson(res, 200, { answer: ans || null });
            resolve();
          };
          const timer = setTimeout(() => {
            room.waiters.delete(onAnswer);
            sendJson(res, 200, { answer: null });
            resolve();
          }, waitSec * 1000);
          room.waiters.add(onAnswer);
        });
      }
      return sendJson(res, 200, { answer: null });
    }
    return sendJson(res, 200, { offer: room.offer, ice: ICE_PAYLOAD });
  }

  serveStatic(req, res, pathname);
});

const wss = new WebSocketServer({ noServer: true });

server.on("upgrade", (req, socket, head) => {
  const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);
  if (url.pathname !== "/api/room/ws") {
    socket.destroy();
    return;
  }
  wss.handleUpgrade(req, socket, head, (ws) => {
    const codeParam = (url.searchParams.get("code") || "").toUpperCase();
    const secretParam = url.searchParams.get("secret") || "";

    let room;
    if (codeParam && secretParam) {
      room = rooms.get(codeParam);
      if (!room || room.secret !== secretParam) {
        ws.close(4404, "Room not found");
        return;
      }
      room.ws = ws;
      ws.send(JSON.stringify({ t: "resumed", ready: !!room.offer }));
      if (room.answer) ws.send(JSON.stringify({ t: "answer", desc: room.answer }));
    } else {
      const code = makeRoomCode();
      const secret = makeSecret();
      room = {
        code,
        secret,
        offer: null,
        answer: null,
        ws,
        waiters: new Set(),
        createdAt: Date.now()
      };
      rooms.set(code, room);
      ws.send(JSON.stringify({ t: "room", code, secret, ice: ICE_PAYLOAD }));
    }

    ws.on("message", (raw) => {
      let msg;
      try {
        msg = JSON.parse(String(raw));
      } catch {
        return;
      }
      if (msg.t === "offer") {
        room.offer = msg.desc || null;
        if (ws.readyState === 1) ws.send(JSON.stringify({ t: "ready" }));
      } else if (msg.t === "close") {
        rooms.delete(room.code);
        try { ws.close(1000); } catch {}
      }
    });
  });
});

// Clean stale rooms older than 15 minutes
setInterval(() => {
  const cutoff = Date.now() - 15 * 60 * 1000;
  for (const [code, room] of rooms) {
    if (room.createdAt < cutoff) rooms.delete(code);
  }
}, 60 * 1000).unref();

server.listen(PORT, () => {
  console.log(`Dakshin Showdown server listening on http://localhost:${PORT}`);
});
