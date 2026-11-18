import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export const STATES = {
  IDLE: 'Idle',
  WALK: 'Walk',
  JUMP: 'Jump',
  CROUCH: 'Crouch',
  PUNCH: 'Punch',
  KICK: 'Kick',
  SPECIAL: 'Special',
  HIT: 'Hit',
  KO: 'KO'
};

export class Fighter3D {
  constructor(scene, config, isPlayerOne = true) {
    this.scene = scene;
    this.name = config.name;
    this.id = config.id;
    this.style = config.style || 'mass'; // 'mass' | 'orator' | 'heavy'
    this.stats = config.stats; // { hp, speed, power, scale }
    this.specialData = config.special;
    this.frameData = config.frameData;

    // 3D Transform & Physics (2.5D plane: X = horizontal, Y = vertical, Z = locked at 0)
    this.position = new THREE.Vector3(isPlayerOne ? -4 : 4, 0, 0);
    this.velocity = new THREE.Vector3(0, 0, 0);
    this.facing = isPlayerOne ? 1 : -1; // 1 faces +X (right), -1 faces -X (left)
    this.isGrounded = true;

    // Combat & Gethu Meter
    this.hp = config.stats.hp;
    this.maxHp = config.stats.hp;
    this.gethu = 0; // 0 to 100
    this.isGethuOverload = false;
    this.state = STATES.IDLE;
    this.stateTimer = 0;
    this.comboString = [];
    this.superArmorFrames = 0;
    this.hitRegistered = false;

    // Three.js Components
    this.mesh = null;
    this.mixer = null;
    this.actions = {};
    this.activeAction = null;
    this.bones = {}; // Stores rightHand, rightFoot, spine for 3D hitboxes

    // 3D Bounding Boxes (Hurtbox = body, Hitbox = active weapon/limb)
    this.hurtbox = new THREE.Box3();
    this.hitbox = new THREE.Box3();
    this.isHitboxActive = false;

    // Optional Debug Visualizers
    this.hurtboxHelper = new THREE.Box3Helper(this.hurtbox, 0x00ff00);
    this.hitboxHelper = new THREE.Box3Helper(this.hitbox, 0xff0000);
    this.hurtboxHelper.visible = Boolean(config.debugBoxes);
    this.hitboxHelper.visible = Boolean(config.debugBoxes);
    if (this.scene) {
      this.scene.add(this.hurtboxHelper, this.hitboxHelper);
    }
  }

  async loadModel(glbPath) {
    const loader = new GLTFLoader();
    const gltf = await loader.loadAsync(glbPath);

    this.mesh = gltf.scene;
    this.mesh.scale.setScalar(this.stats.scale || 1.0);
    this.mesh.position.copy(this.position);
    this.mesh.rotation.y = this.facing === 1 ? Math.PI / 2 : -Math.PI / 2;

    // Map rig bones to attach 3D hitboxes dynamically
    this.mesh.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
      }
      if (child.isBone) {
        const boneName = child.name.toLowerCase();
        if (boneName.includes('hand_r') || boneName.includes('righthand') || boneName === 'def-handr' || boneName === 'def-hand.r') this.bones.rightHand = child;
        if (boneName.includes('foot_r') || boneName.includes('rightfoot') || boneName === 'def-footr' || boneName === 'def-foot.r') this.bones.rightFoot = child;
        if (boneName.includes('spine') || boneName.includes('chest')) this.bones.torso = child;
      }
    });

    // Setup 3D Animation Mixer & Clips
    this.mixer = new THREE.AnimationMixer(this.mesh);
    gltf.animations.forEach((clip) => {
      this.actions[clip.name] = this.mixer.clipAction(clip);
    });

    if (this.scene) {
      this.scene.add(this.mesh);
    }
    this.changeState(STATES.IDLE);
  }

  changeState(newState) {
    if (this.state === STATES.KO) return;
    if (this.state === newState) return;

    this.state = newState;
    this.stateTimer = 0;
    this.hitRegistered = false;
    this.isHitboxActive = false;

    if (newState === STATES.PUNCH || newState === STATES.KICK) {
      this.comboString.push(newState === STATES.PUNCH ? 'J' : 'K');
      if (this.comboString.length > 3) this.comboString.shift();
      // Heavyweights gain Super Armor frames on K,K heavy attacks
      if (this.style === 'heavy' && newState === STATES.KICK && this.comboString.slice(-2).join('') === 'KK') {
        this.superArmorFrames = 8;
      }
      // Orators project mid-range 3D soundwave rings on J,J,J jab string
      if (this.style === 'orator' && newState === STATES.PUNCH && this.scene) {
        this.spawnSoundwaveRing();
      }
    } else if (newState === STATES.IDLE || newState === STATES.HIT || newState === STATES.KO) {
      this.comboString = [];
      this.superArmorFrames = 0;
    }

    // Smooth 3D Skeletal Crossfade (0.12s blend time)
    const nextAction = this.actions[newState];
    if (nextAction) {
      nextAction.reset();
      if ([STATES.PUNCH, STATES.KICK, STATES.SPECIAL, STATES.HIT, STATES.KO].includes(newState)) {
        nextAction.setLoop(THREE.LoopOnce, 1);
        nextAction.clampWhenFinished = true;
      } else {
        nextAction.setLoop(THREE.LoopRepeat);
      }

      if (this.activeAction) {
        this.activeAction.crossFadeTo(nextAction, 0.12, true);
      }
      nextAction.play();
      this.activeAction = nextAction;
    }
  }

  spawnSoundwaveRing() {
    const ringGeo = new THREE.TorusGeometry(0.32, 0.045, 8, 24);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0x22d3ee, transparent: true, opacity: 0.9 });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.y = Math.PI / 2;
    ring.position.set(this.position.x + this.facing * 0.7, this.position.y + 1.25, 0);
    this.scene.add(ring);
    const start = performance.now();
    const step = () => {
      const p = Math.min(1, (performance.now() - start) / 280);
      ring.position.x += this.facing * 0.14;
      ring.scale.setScalar(1 + p * 1.4);
      ringMat.opacity = 0.9 * (1 - p);
      if (p < 1) requestAnimationFrame(step);
      else {
        this.scene.remove(ring);
        ringGeo.dispose();
        ringMat.dispose();
      }
    };
    requestAnimationFrame(step);
  }

  update(delta, gravity = -28, stageOptions = {}) {
    if (!this.mesh) return;

    // 1. Advance 3D Animation Mixer (Boost speed by 30% during Gethu Overload)
    const speedMultiplier = this.isGethuOverload ? 1.3 : 1.0;
    if (this.mixer) this.mixer.update(delta * speedMultiplier);
    if (this.superArmorFrames > 0) this.superArmorFrames--;

    // 2. Apply 3D Physics (Locked on Z = 0 plane for 2.5D fighting)
    if (!this.isGrounded) {
      this.velocity.y += gravity * delta;
    } else if (stageOptions.waveSlipActive) {
      // Marina Beach wave washes onto sand every 20s, reducing friction
      this.velocity.x *= Math.pow(0.96, delta * 60);
    }
    this.position.x += this.velocity.x * delta;
    this.position.y += this.velocity.y * delta;

    // Floor & Arena Wall Clamp
    if (this.position.y <= 0) {
      this.position.y = 0;
      this.velocity.y = 0;
      this.isGrounded = true;
      if (this.state === STATES.JUMP) this.changeState(STATES.IDLE);
    }
    if (stageOptions.busStandBounce && Math.abs(this.position.x) > 8.5) {
      // Koyambedu Bus Stand: corner auto-rickshaw bounces knocked fighter back to center
      this.velocity.x = -Math.sign(this.position.x) * 10;
      this.velocity.y = Math.max(this.velocity.y, 6);
      this.isGrounded = false;
      this.position.x = Math.sign(this.position.x) * 8.45;
    } else {
      this.position.x = THREE.MathUtils.clamp(this.position.x, -9, 9);
    }

    // Sync Mesh Transform & Orientation
    this.mesh.position.copy(this.position);
    this.mesh.rotation.y = this.facing === 1 ? Math.PI / 2 : -Math.PI / 2;

    // 3. Update 3D Hurtbox (Body Volume)
    const crouchOffset = this.state === STATES.CROUCH ? 1.1 : 2.0;
    this.hurtbox.setFromCenterAndSize(
      new THREE.Vector3(this.position.x, this.position.y + crouchOffset / 2, 0),
      new THREE.Vector3(0.9, crouchOffset, 0.9)
    );

    // 4. Evaluate Frame Data (60fps frame counter equivalent)
    this.stateTimer += delta * 60 * speedMultiplier;
    this.evaluateCombatFrames();
  }

  evaluateCombatFrames() {
    const attackStates = [STATES.PUNCH, STATES.KICK, STATES.SPECIAL];
    if (!attackStates.includes(this.state)) {
      this.isHitboxActive = false;
      this.hitbox.makeEmpty();
      return;
    }

    const data = this.frameData[this.state];
    const currentFrame = Math.floor(this.stateTimer);

    // Orators extend mid-range hitbox reach on jab strings
    const rangeBoost = this.style === 'orator' && this.state === STATES.PUNCH ? 1.35 : 0;

    // Active Hitbox Window
    if (currentFrame >= data.startup && currentFrame <= data.startup + data.active) {
      this.isHitboxActive = true;
      const worldPos = new THREE.Vector3();

      // Track 3D Bone Position if rigged, else fallback to front offset
      if (this.style === 'orator' && this.state === STATES.PUNCH) {
        worldPos.set(this.position.x + this.facing * (data.range + rangeBoost), this.position.y + 1.25, 0);
      } else if (this.state === STATES.PUNCH && this.bones.rightHand) {
        this.bones.rightHand.getWorldPosition(worldPos);
      } else if (this.state === STATES.KICK && this.bones.rightFoot) {
        this.bones.rightFoot.getWorldPosition(worldPos);
      } else {
        worldPos.set(
          this.position.x + this.facing * data.range,
          this.position.y + 1.2,
          0
        );
      }

      const boxSize = rangeBoost > 0
        ? new THREE.Vector3(data.boxSize.x + rangeBoost, data.boxSize.y, data.boxSize.z)
        : data.boxSize;
      this.hitbox.setFromCenterAndSize(worldPos, boxSize);
    } else {
      this.isHitboxActive = false;
      this.hitbox.makeEmpty();
    }

    // Recovery Finished -> Return to Idle
    const totalFrames = data.startup + data.active + data.recovery;
    if (currentFrame >= totalFrames) {
      this.changeState(STATES.IDLE);
    }
  }

  addGethu(amount) {
    if (this.isGethuOverload) return;
    this.gethu = Math.min(100, this.gethu + amount);
  }

  triggerGethuSpecial() {
    if (this.gethu < 100) return false;
    this.gethu = 0;
    this.isGethuOverload = true;
    this.changeState(STATES.SPECIAL);

    // Gethu Overload lasts 8 seconds
    setTimeout(() => {
      this.isGethuOverload = false;
    }, 8000);
    return true;
  }

  takeDamage(rawDamage, knockbackDir, isLightAttack = false) {
    // Heavyweights resist flinching from light jabs during K,K Super Armor frames
    if (this.superArmorFrames > 0 && isLightAttack) {
      this.hp = Math.max(1, this.hp - rawDamage * 0.5);
      return false;
    }
    const finalDamage = this.isGethuOverload ? rawDamage * 0.5 : rawDamage;
    this.hp = Math.max(0, this.hp - finalDamage);
    this.addGethu(12); // Building Gethu on taking hits

    if (this.hp <= 0) {
      this.changeState(STATES.KO);
    } else {
      this.changeState(STATES.HIT);
      this.velocity.x = knockbackDir * 4;
      setTimeout(() => {
        if (this.state === STATES.HIT) {
          this.velocity.x = 0;
          this.changeState(STATES.IDLE);
        }
      }, 250);
    }
    return true;
  }
}
