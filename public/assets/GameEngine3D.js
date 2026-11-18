import * as THREE from 'three';
import { Fighter3D, STATES } from './Fighter3D.js';
import { TAMIL_ROSTER_3D, DEFAULT_FRAMES, DEFAULT_FRAME_DATA, ROSTER_3D_BY_ENGINE_ID } from './RosterConfig3D.js';

export { Fighter3D, STATES, TAMIL_ROSTER_3D, DEFAULT_FRAMES, DEFAULT_FRAME_DATA, ROSTER_3D_BY_ENGINE_ID };

export class FightKaroTamil3D {
  constructor(canvasContainer) {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0f0f1a);
    this.scene.fog = new THREE.FogExp2(0x0f0f1a, 0.035);

    // Dynamic 2.5D Fighting Camera
    this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
    this.camera.position.set(0, 2.5, 11);

    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.shadowMap.enabled = true;
    canvasContainer.appendChild(this.renderer.domElement);

    this.clock = new THREE.Clock();
    this.timeScale = 1.0;
    this.slowMoTimer = 0;
    this.camZoomOffset = 0;
    this.stageType = 'marina';
    this.elapsedTime = 0;
    this.micMutedUntil = 0;
    this.setupLightingAndStage();

    // Instantiate P1 vs P2
    this.p1 = new Fighter3D(this.scene, TAMIL_ROSTER_3D[0], true);
    this.p2 = new Fighter3D(this.scene, TAMIL_ROSTER_3D[7], false);
    this.initFighters();
  }

  setupLightingAndStage() {
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
    hemiLight.position.set(0, 20, 0);
    this.scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xffddaa, 2.0);
    dirLight.position.set(5, 12, 8);
    dirLight.castShadow = true;
    this.scene.add(dirLight);

    // 3D Stage Floor
    const floorGeo = new THREE.PlaneGeometry(30, 12);
    const floorMat = new THREE.MeshStandardMaterial({ color: 0x222230, roughness: 0.7 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    this.scene.add(floor);
  }

  async initFighters() {
    await Promise.all([
      this.p1.loadModel(TAMIL_ROSTER_3D[0].modelPath),
      this.p2.loadModel(TAMIL_ROSTER_3D[7].modelPath)
    ]);
    this.animate();
  }

  check3DCollisions() {
    // Auto-face each other along X-axis
    if (this.p1.position.x < this.p2.position.x) {
      this.p1.facing = 1;
      this.p2.facing = -1;
    } else {
      this.p1.facing = -1;
      this.p2.facing = 1;
    }

    // P1 3D Hitbox -> P2 3D Hurtbox
    if (this.p1.isHitboxActive && !this.p1.hitRegistered) {
      if (this.p1.hitbox.intersectsBox(this.p2.hurtbox)) {
        this.p1.hitRegistered = true;
        const dmg = this.p1.frameData[this.p1.state].damage * this.p1.stats.power;
        const stunned = this.p2.takeDamage(dmg, this.p1.facing, this.p1.state === STATES.PUNCH);
        this.p1.addGethu(18);
        if (stunned) this.onFighterStunned(this.p1, this.p2);
      }
    }

    // P2 3D Hitbox -> P1 3D Hurtbox
    if (this.p2.isHitboxActive && !this.p2.hitRegistered) {
      if (this.p2.hitbox.intersectsBox(this.p1.hurtbox)) {
        this.p2.hitRegistered = true;
        const dmg = this.p2.frameData[this.p2.state].damage * this.p2.stats.power;
        const stunned = this.p1.takeDamage(dmg, this.p2.facing, this.p2.state === STATES.PUNCH);
        this.p2.addGethu(18);
        if (stunned) this.onFighterStunned(this.p2, this.p1);
      }
    }
  }

  onFighterStunned(attacker, defender) {
    // Mass Hero Slow-Mo Gravity Launch on final hit of J,J,K
    if (attacker.style === 'mass' && attacker.state === STATES.KICK && attacker.comboString.join('') === 'JJK') {
      this.timeScale = 0.25;
      this.slowMoTimer = 0.3;
      this.camZoomOffset = -2.5;
      defender.velocity.y = 11.5;
      defender.isGrounded = false;
    }
    if (this.stageType === 'studio') {
      this.micMutedUntil = this.elapsedTime + 1.2;
    }
  }

  updateCamera() {
    // Track midpoint between both 3D fighters and zoom dynamically based on distance
    const midX = (this.p1.position.x + this.p2.position.x) / 2;
    const dist = Math.abs(this.p1.position.x - this.p2.position.x);
    const targetZ = THREE.MathUtils.clamp(dist * 1.15 + 6 + this.camZoomOffset, 5.5, 15);

    this.camera.position.x = THREE.MathUtils.lerp(this.camera.position.x, midX, 0.1);
    this.camera.position.z = THREE.MathUtils.lerp(this.camera.position.z, targetZ, 0.15);
    this.camera.lookAt(midX, 1.4, 0);
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    const rawDelta = Math.min(this.clock.getDelta(), 0.1);
    this.elapsedTime += rawDelta;
    if (this.slowMoTimer > 0) {
      this.slowMoTimer -= rawDelta;
      if (this.slowMoTimer <= 0) {
        this.timeScale = 1.0;
        this.camZoomOffset = 0;
      }
    }
    const delta = rawDelta * this.timeScale;
    const stageOptions = {
      waveSlipActive: this.stageType === 'marina' && (this.elapsedTime % 20) < 4.5,
      busStandBounce: this.stageType === 'busstand'
    };

    this.p1.update(delta, -28, stageOptions);
    this.p2.update(delta, -28, stageOptions);
    this.check3DCollisions();
    this.updateCamera();

    this.renderer.render(this.scene, this.camera);
  }
}

if (typeof window !== 'undefined') {
  window.FightKaroTamil3D = {
    Fighter3D,
    STATES,
    TAMIL_ROSTER_3D,
    DEFAULT_FRAMES,
    DEFAULT_FRAME_DATA,
    ROSTER_3D_BY_ENGINE_ID,
    FightKaroTamil3D
  };
}
