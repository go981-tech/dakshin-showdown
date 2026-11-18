import * as THREE from 'three';

// Startup, Active, and Recovery are measured in 60fps game ticks (1 tick = 16.67ms)
export const DEFAULT_FRAME_DATA = {
  IDLE:   { totalFrames: 6, frameDuration: 8, loop: true },
  WALK:   { totalFrames: 8, frameDuration: 6, loop: true },
  JUMP:   { totalFrames: 4, frameDuration: 10, loop: false },
  CROUCH: { totalFrames: 2, frameDuration: 6, loop: false },
  HIT:    { totalFrames: 3, frameDuration: 6, loop: false },
  KO:     { totalFrames: 6, frameDuration: 8, loop: false },
  PUNCH: {
    totalFrames: 5,
    frameDuration: 4, // 20 ticks total animation
    loop: false,
    startup: 5,
    active: 4,
    recovery: 11,
    hitbox: { offsetX: 25, offsetY: 30, width: 65, height: 30, damage: 6, hitstun: 14, knockbackX: 4, knockbackY: 0 }
  },
  KICK: {
    totalFrames: 7,
    frameDuration: 5, // 35 ticks total animation
    loop: false,
    startup: 10,
    active: 6,
    recovery: 19,
    hitbox: { offsetX: 30, offsetY: 50, width: 85, height: 40, damage: 11, hitstun: 20, knockbackX: 8, knockbackY: -2 }
  },
  SPECIAL: {
    totalFrames: 10,
    frameDuration: 5, // 50 ticks total animation
    loop: false,
    startup: 14,
    active: 12,
    recovery: 24
  }
};

export const DEFAULT_FRAMES = {
  Punch:   { startup: 4, active: 4, recovery: 8,  damage: 8,  range: 1.3, boxSize: new THREE.Vector3(0.8, 0.6, 0.8) },
  Kick:    { startup: 7, active: 5, recovery: 12, damage: 13, range: 1.7, boxSize: new THREE.Vector3(1.1, 0.7, 0.8) },
  Special: { startup: 12, active: 15, recovery: 20, damage: 28, range: 3.2, boxSize: new THREE.Vector3(2.8, 2.0, 1.5) }
};

export const CHARACTER_GLB_MAP = {
  rahul:    '/characters/01_thalapathy_vijay.glb',
  modi:     '/characters/02_mk_stalin.glb',
  didi:     '/characters/03_j_jayalalithaa.glb',
  trump:    '/characters/04_allu_arjun.glb',
  yogi:     '/characters/05_pinarayi_vijayan.glb',
  nitin:    '/characters/06_dk_shivakumar.glb',
  ravi:     '/characters/07_pawan_kalyan.glb',
  lalu:     '/characters/08_seeman.glb',
  mbapu:    '/characters/09_periyar_ev_ramasamy.glb',
  amit:     '/characters/10_k_annamalai.glb',
  dhruv:    '/characters/11_madan_gowri.glb',
  nirmala:  '/characters/12_nirmala_sitharaman.glb',
  rangaraj: '/characters/13_rangaraj_pandey.glb'
};

export const CAMEO_ASSISTS_3D = {
  sumo: {
    id: 'sumo',
    name: 'FLYING SUMO SUV',
    tag: 'KOOTANI CAMEO',
    desc: 'Classic Kollywood villain Sumo SUV launches from the sky and flips the opponent!'
  },
  squad: {
    id: 'squad',
    name: 'ELECTION FLYING SQUAD',
    tag: 'IT RAID ASSIST',
    desc: 'Squad Van screeches in and confiscates 20% of the opponent\'s Gethu meter!'
  },
  light: {
    id: 'light',
    name: 'STUDIO LIGHT DROP',
    tag: 'SET HAZARD',
    desc: 'Drops a massive 3D theatre rigging spotlight directly onto the enemy!'
  },
  random: {
    id: 'random',
    name: 'RANDOM STAGE HAZARD',
    tag: 'SURPRISE KOOTANI',
    desc: 'Triggers a random 2-second 3D hazard (Sumo SUV, Flying Squad Van, or Studio Light)!'
  }
};

export const TAMIL_ROSTER_3D = [
  {
    id: 'thalapathy_vijay',
    engineId: 'rahul',
    style: 'mass',
    name: 'Thalapathy',
    modelPath: '/characters/01_thalapathy_vijay.glb',
    stats: { hp: 1000, speed: 7.5, power: 1.15, scale: 1.0 },
    special: {
      name: 'TVK Mic Toss & Bubblegum Counter',
      type: 'projectile_3d',
      quote: 'I am waiting!',
      particleColor: 0xffd700
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'mk_stalin',
    engineId: 'modi',
    style: 'heavy',
    name: 'Surya Anna',
    modelPath: '/characters/02_mk_stalin.glb',
    stats: { hp: 1100, speed: 6.0, power: 1.1, scale: 1.0 },
    special: {
      name: 'Rising Sun Cycle Charge',
      type: 'dash_3d',
      quote: 'Ungalil Oruvan!',
      particleColor: 0xff2200
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'j_jayalalitha',
    engineId: 'didi',
    style: 'heavy',
    name: 'Iron Amma',
    modelPath: '/characters/03_j_jayalalithaa.glb',
    stats: { hp: 1200, speed: 5.2, power: 1.3, scale: 0.98 },
    special: {
      name: 'Iron Lady Two-Leaves Shockwave',
      type: 'aoe_3d',
      quote: 'Makkalal Naan, Makkalukkaga Naan!',
      particleColor: 0x00cc44
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'allu_arjun',
    engineId: 'trump',
    style: 'mass',
    name: 'Sandal Raju',
    modelPath: '/characters/04_allu_arjun.glb',
    stats: { hp: 980, speed: 7.8, power: 1.2, scale: 1.0 },
    special: {
      name: 'Red Sandalwood Shoulder-Brush Sweep',
      type: 'melee_3d',
      quote: 'Thaggedhe Le!',
      particleColor: 0xcc3300
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'pinarayi_vijayan',
    engineId: 'yogi',
    style: 'heavy',
    name: 'Lal Captain',
    modelPath: '/characters/05_pinarayi_vijayan.glb',
    stats: { hp: 1150, speed: 5.5, power: 1.2, scale: 1.02 },
    special: {
      name: 'Double-Heart Red Salute Barrier',
      type: 'counter_3d',
      quote: 'Kadakku Purathu!',
      particleColor: 0xd90000
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'dk_shivakumar',
    engineId: 'nitin',
    style: 'heavy',
    name: 'Bande Shiv',
    modelPath: '/characters/06_dk_shivakumar.glb',
    stats: { hp: 1080, speed: 6.2, power: 1.18, scale: 1.03 },
    special: {
      name: 'Kanakapura Bulldozer Slam',
      type: 'dash_3d',
      quote: 'Trouble Troubleshooter Activated!',
      particleColor: 0xffaa00
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'pawan_kalyan',
    engineId: 'ravi',
    style: 'mass',
    name: 'Power Star',
    modelPath: '/characters/07_pawan_kalyan.glb',
    stats: { hp: 950, speed: 8.2, power: 1.22, scale: 1.0 },
    special: {
      name: 'Shattered Glass Tea-Tumbler Hurricane Kick',
      type: 'vortex_3d',
      quote: 'Seize the Ship!',
      particleColor: 0xff0044
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'seeman',
    engineId: 'lalu',
    style: 'orator',
    name: 'Puli Voice',
    modelPath: '/characters/08_seeman.glb',
    stats: { hp: 1020, speed: 6.8, power: 1.25, scale: 1.02 },
    special: {
      name: '150-Decibel Megaphone Sonic Boom',
      type: 'cone_3d',
      quote: 'Thambi! Aamai Kari Saaptiya?!',
      particleColor: 0xffdd00
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'periyar',
    engineId: 'mbapu',
    style: 'heavy',
    name: 'Thatha Reform',
    modelPath: '/characters/09_periyar_ev_ramasamy.glb',
    stats: { hp: 1180, speed: 5.0, power: 1.35, scale: 1.0 },
    special: {
      name: 'Rationalist Walking-Stick Ground Tremor',
      type: 'aoe_3d',
      quote: 'Think For Yourself!',
      particleColor: 0x222222
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'k_annamalai',
    engineId: 'amit',
    style: 'mass',
    name: 'Files IPS',
    modelPath: '/characters/10_k_annamalai.glb',
    stats: { hp: 1050, speed: 7.0, power: 1.2, scale: 1.04 },
    special: {
      name: '500-Page Press Meet Dossier Drop',
      type: 'meteor_3d',
      quote: 'En Mann, En Makkal!',
      particleColor: 0xff6600
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'madan_gowri',
    engineId: 'dhruv',
    style: 'orator',
    name: 'Squad Bro',
    modelPath: '/characters/11_madan_gowri.glb',
    stats: { hp: 900, speed: 8.5, power: 1.05, scale: 0.98 },
    special: {
      name: 'Wikipedia Fact-Spit Rapid Barrage',
      type: 'flurry_3d',
      quote: 'Hello Squad! Idha Pathi Ungaluku Theriyuma?',
      particleColor: 0x00d4ff
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'nirmala_sitharaman',
    engineId: 'nirmala',
    style: 'heavy',
    name: 'Tax Maami',
    modelPath: '/characters/12_nirmala_sitharaman.glb',
    stats: { hp: 1050, speed: 5.8, power: 1.3, scale: 0.97 },
    special: {
      name: '28% GST Caramel Popcorn Tax Drain',
      type: 'debuff_3d',
      quote: 'I Don’t Eat That Much Onion!',
      particleColor: 0x9900ff
    },
    frameData: DEFAULT_FRAMES
  },
  {
    id: 'rangaraj_pandey',
    engineId: 'rangaraj',
    style: 'orator',
    name: 'Rangaraj Studio',
    modelPath: '/characters/13_rangaraj_pandey.glb',
    stats: { hp: 960, speed: 6.9, power: 1.15, scale: 1.0 },
    special: {
      name: 'Kelvikku Enna Bathil Rapid-Fire StunLock',
      type: 'cone_3d',
      quote: 'Point-ku Vaanga!',
      particleColor: 0x0088ff
    },
    frameData: DEFAULT_FRAMES
  }
];

export const ROSTER_3D_BY_ENGINE_ID = Object.fromEntries(
  TAMIL_ROSTER_3D.map((entry) => [entry.engineId, entry])
);
