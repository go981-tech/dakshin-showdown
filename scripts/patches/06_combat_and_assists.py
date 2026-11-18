def apply(ctx):
    # 7a. Mass Hero launch + matchStats inside jf.onHit; startup VFX is triggered by startAttack
    ctx.replace_exact(
        'onHit(e){e.defender===this.boss&&e.attacker.side===this.playerSide&&!e.blocked&&!this.budgetUsed&&(this.budget=Math.min(1,this.budget+e.damage/40)),',
        'onHit(e){e.attacker.side===this.playerSide&&!e.blocked&&(this.budget=Math.min(1,this.budget+e.damage/55)),e.attacker.side===this.playerSide&&!e.blocked&&(this.matchStats.maxCombo=Math.max(this.matchStats.maxCombo,e.defender.comboHits),[`kick`,`roundhouse`,`sweep`,`airKick`,`special2`,`finisher`].includes(e.moveId)?this.matchStats.kicks++:[`jab`,`cross`,`lowJab`,`uppercut`,`airPunch`,`special1`].includes(e.moveId)&&this.matchStats.punches++),(!e.blocked&&!e.armor&&e.attacker.char.style===`mass`&&([`finisher`,`special2`].includes(e.moveId)||e.attacker.char.id===`ravi`&&e.moveId===`roundhouse`))&&(this.timeScale=.25,this.slowMoTime=.3,this.massZoomTimer=.45,e.defender.vy=Math.max(e.defender.vy,9.8),e.defender.grounded=!1,(()=>{this.tmp.set(e.x,e.y+.55,.3);let p=this.ctx.toScreen(this.tmp);this.ctx.hud.popup(`🎬 SLOW-MO LAUNCH!`,p.x,p.y,`#facc15`)})()),',
        'onHit triggerMemeOnAction + Mass Hero launch + matchStats',
    )

    # 10. Kootani VIP Cameo / Assist (KeyB / #budget-meter) in ALL 1P matches, recharging every 15s
    ctx.replace_exact('this.boss&&!this.net&&ga()', '!this.net&&!window.__local2P&&ga()', 'budget preload 1P')
    ctx.replace_exact(
        'i(this,`budget`,0),i(this,`budgetUsed`,!1)',
        'i(this,`budget`,1),i(this,`budgetUsed`,!1),i(this,`massZoomTimer`,0),i(this,`matchStats`,{kicks:0,punches:0,supers:0,grabs:0,maxCombo:0})',
        'jf budget, massZoomTimer, matchStats fields',
    )
    ctx.replace_exact('this.budget=0,this.budgetUsed=!1', 'this.budget=1,this.budgetUsed=!1', 'startRound budget ready at start')
    ctx.replace_exact(
        'this.boss&&!this.net?this.ctx.hud.setBudget(this.budgetUsed?0:this.budget,this.phase===`fight`&&!this.budgetUsed):this.ctx.hud.setBudget(0,!1)',
        '!this.net&&!window.__local2P?this.ctx.hud.setBudget(this._kootaniHazard?0:this.budget,this.phase===`fight`&&!this._kootaniHazard):this.ctx.hud.setBudget(0,!1)',
        'budget hud bar 1P',
    )
    ctx.replace_exact(
        'this.boss&&!this.budgetUsed&&!this.net&&(this.budget=Math.min(1,this.budget+qe/(this.hardBoss?lo.budgetSeconds:10)))',
        '!window.__local2P&&!this._kootaniHazard&&!this.net&&(this.budget=Math.min(1,this.budget+qe/15))',
        'budget charge timer 15s cooldown',
    )
    ctx.replace_span(
        'get budgetReady(){',
        'skipCinema(){',
        'get budgetReady(){let e=this.fighters[this.playerSide],o=this.fighters[+(this.playerSide===0)];return!window.__local2P&&!this.net&&!this._kootaniHazard&&this.budget>=1&&this.phase===`fight`&&this.hitStop===0&&e.actionable&&e.hp>0&&o.hp>1}callBudget(){if(!this.budgetReady)return!1;return this.budget=0,k(`budget_called`,{player:this.fighters[this.playerSide].char.id,assist:window.__selectedAssist||`random`}),triggerKootaniAssist(this,this.playerSide)}',
        'budgetReady & callBudget Kootani 3D Stage Hazard',
        include_end=False,
    )
    ctx.replace_exact('this.diwali&&!this.net&&!this.boss&&this.stepMithai()', '!this.net&&!this.boss&&this.stepMithai()', 'enable Mysore Pak drops')

    # 11. Local 2-Player Same-Keyboard Mode (#local2p-btn, Wf.pollP1 / pollP2, jf.step) + Censor Board Boss button lock
    censor_guard = 'let _cl=window.__censorLock;if(_cl&&_cl.remaining>0){if(_cl.key===`kick`&&e.kick){e.kick=!1;window.__onCensorBlocked?.(`kick`)}if(_cl.key===`super`&&e.super){e.super=!1;window.__onCensorBlocked?.(`super`)}}'
    ctx.replace_exact(
        'poll(){let e=n(),t=this.any(If,this.held)||this.touchHeld.has(`left`);return e.moveX=t===(this.any(Lf,this.held)||this.touchHeld.has(`right`))?0:t?-1:1,e.up=this.any(Rf,this.held)||this.touchHeld.has(`up`),e.down=this.any(zf,this.held)||this.touchHeld.has(`down`),e.punch=this.any(Bf,this.pressed)||this.touchPressed.has(`punch`),e.kick=this.any(Vf,this.pressed)||this.touchPressed.has(`kick`),e.super=this.any(Hf,this.pressed)||this.touchPressed.has(`super`),e.grab=this.any(Uf,this.pressed)||this.touchPressed.has(`grab`)||e.punch&&e.kick,e.grab&&(e.punch=!1,e.kick=!1),this.pressed.clear(),this.touchPressed.clear(),e}',
        'poll(){let e=n(),t=this.any(If,this.held)||this.touchHeld.has(`left`);e.moveX=t===(this.any(Lf,this.held)||this.touchHeld.has(`right`))?0:t?-1:1,e.up=this.any(Rf,this.held)||this.touchHeld.has(`up`),e.down=this.any(zf,this.held)||this.touchHeld.has(`down`),e.punch=this.any(Bf,this.pressed)||this.touchPressed.has(`punch`),e.kick=this.any(Vf,this.pressed)||this.touchPressed.has(`kick`),e.super=this.any(Hf,this.pressed)||this.touchPressed.has(`super`),e.grab=this.any(Uf,this.pressed)||this.touchPressed.has(`grab`)||e.punch&&e.kick,e.grab&&(e.punch=!1,e.kick=!1);' + censor_guard + 'this.pressed.clear(),this.touchPressed.clear();return e}pollP1(){let e=n(),l=this.held.has(`KeyA`)||this.touchHeld.has(`left`),r=this.held.has(`KeyD`)||this.touchHeld.has(`right`);e.moveX=l===r?0:l?-1:1,e.up=this.held.has(`KeyW`)||this.touchHeld.has(`up`),e.down=this.held.has(`KeyS`)||this.touchHeld.has(`down`),e.punch=this.any([`KeyJ`,`KeyZ`],this.pressed)||this.touchPressed.has(`punch`),e.kick=this.any([`KeyK`,`KeyX`],this.pressed)||this.touchPressed.has(`kick`),e.super=this.any([`KeyL`,`Space`,`KeyC`],this.pressed)||this.touchPressed.has(`super`),e.grab=this.any([`KeyI`,`KeyV`],this.pressed)||this.touchPressed.has(`grab`)||e.punch&&e.kick,e.grab&&(e.punch=!1,e.kick=!1);' + censor_guard + 'for(let k of[`KeyJ`,`KeyZ`,`KeyK`,`KeyX`,`KeyL`,`Space`,`KeyC`,`KeyI`,`KeyV`])this.pressed.delete(k);return this.touchPressed.clear(),e}pollP2(){let e=n(),l=this.held.has(`ArrowLeft`),r=this.held.has(`ArrowRight`);e.moveX=l===r?0:l?-1:1,e.up=this.held.has(`ArrowUp`),e.down=this.held.has(`ArrowDown`),e.punch=this.any([`KeyU`,`Numpad1`],this.pressed),e.kick=this.any([`KeyO`,`Numpad2`],this.pressed),e.super=this.any([`Enter`,`NumpadEnter`,`Numpad0`,`Slash`],this.pressed),e.grab=this.any([`KeyP`,`Numpad3`],this.pressed)||e.punch&&e.kick,e.grab&&(e.punch=!1,e.kick=!1);for(let k of[`KeyU`,`Numpad1`,`KeyO`,`Numpad2`,`Enter`,`NumpadEnter`,`Numpad0`,`Slash`,`KeyP`,`Numpad3`])this.pressed.delete(k);return e}',
        'Wf poll (censor lock) + pollP1 & pollP2',
    )
    ctx.replace_exact(
        'let i=this.ctx.input.poll(),a=this.net?this.hostDelay.pass(i):i,o=+(this.playerSide===0),s=r??this.bot.think(this.fighters[o],this.fighters[this.playerSide],.016666666666666666),c=r?s:this.dodgeBomb(this.fighters[o],s)',
        'window.__onCensorBlocked=(k)=>{let p=this.fighters[this.playerSide],sc=this.ctx.toScreen(this.tmp.set(p.x,2.2,.3));this.ctx.hud.popup(`✂️ ${k.toUpperCase()} CENSORED! GRAB [I]!`,sc.x,sc.y,`#ef4444`)};let i=window.__local2P&&!this.net?this.ctx.input.pollP1():this.ctx.input.poll(),a=this.net?this.hostDelay.pass(i):i,o=+(this.playerSide===0),s=r??(window.__local2P&&!this.net?this.ctx.input.pollP2():this.bot.think(this.fighters[o],this.fighters[this.playerSide],.016666666666666666)),c=r||window.__local2P&&!this.net?s:this.dodgeBomb(this.fighters[o],s)',
        'jf.step local2P + censor blocked feedback',
    )

    # 16. Combat Mechanics: frame data, Gethu Overload 1.3x Speed / 50% Armor, Dash, Just-Frame Parry, Super Armor, Wave slip
    ctx.replace_exact(
        'i(this,`downFrames`,0),i(this,`grounded`,!0),this.side=e',
        'i(this,`downFrames`,0),i(this,`grounded`,!0),i(this,`dashFrames`,0),i(this,`dashDir`,0),i(this,`tapDir`,0),i(this,`tapAge`,0),i(this,`prevMoveX`,0),i(this,`blockFrames`,0),i(this,`overloadFrames`,0),this.side=e',
        'ko constructor dash, parry & overloadFrames fields',
    )
    ctx.replace_exact(
        'this.comboHits=0,this.downFrames=0,this.grounded=!0,this.enter(`idle`)}',
        'this.comboHits=0,this.downFrames=0,this.grounded=!0,this.wantsSuper=!1,this.dashFrames=0,this.dashDir=0,this.tapDir=0,this.tapAge=0,this.prevMoveX=0,this.blockFrames=0,this.overloadFrames=0,this.enter(`idle`)}get isGethuOverload(){return this.overloadFrames>0}',
        'ko reset dash, parry & isGethuOverload getter',
    )
    ctx.replace_exact(
        'jab:{id:`jab`,startup:5,active:3,recovery:10,damage:5,height:`high`,hitstun:16,blockstun:10,knockdown:!1,launch:0,push:1.6,lunge:1.6,chains:{punch:`cross`,kick:`kick`}},cross:{id:`cross`,startup:6,active:3,recovery:12,damage:6,height:`high`,hitstun:18,blockstun:11,knockdown:!1,launch:0,push:1.8,lunge:2,chains:{punch:`uppercut`,kick:`finisher`}},kick:{id:`kick`,startup:9,active:4,recovery:15,damage:9,height:`mid`,hitstun:22,blockstun:13,knockdown:!1,launch:0,push:2,lunge:1.4,chains:{kick:`roundhouse`}},uppercut:{id:`uppercut`,startup:9,active:4,recovery:20,damage:11,height:`mid`,hitstun:24,blockstun:15,knockdown:!0,launch:8,push:1.4,lunge:1.8},',
        'jab:{id:`jab`,startup:4,active:4,recovery:8,damage:8,height:`high`,hitstun:18,blockstun:10,knockdown:!1,launch:0,push:.85,lunge:1.6,chains:{punch:`cross`,kick:`kick`}},cross:{id:`cross`,startup:5,active:4,recovery:10,damage:8,height:`high`,hitstun:20,blockstun:11,knockdown:!1,launch:0,push:.9,lunge:1.8,chains:{punch:`uppercut`,kick:`finisher`}},kick:{id:`kick`,startup:7,active:5,recovery:12,damage:13,height:`mid`,hitstun:22,blockstun:13,knockdown:!1,launch:0,push:1.2,lunge:1.5,chains:{kick:`roundhouse`}},uppercut:{id:`uppercut`,startup:8,active:4,recovery:14,damage:11,height:`mid`,hitstun:28,blockstun:15,knockdown:!1,launch:0,push:.75,lunge:1.4,chains:{kick:`finisher`,punch:`special1`}},',
        'DEFAULT_FRAMES Punch/Kick/Uppercut frame data & 5-hit chains',
    )
    ctx.replace_exact(
        'special1:{id:`special1`,startup:13,active:4,recovery:19,damage:13,height:`mid`,hitstun:26,blockstun:16,knockdown:!0,launch:7.5,push:2.2,lunge:3},special2:{id:`special2`,startup:15,active:5,recovery:20,damage:14,height:`mid`,hitstun:26,blockstun:16,knockdown:!0,launch:4.5,push:5.2,lunge:2.6},',
        'special1:{id:`special1`,startup:10,active:6,recovery:15,damage:14,height:`mid`,hitstun:28,blockstun:16,knockdown:!1,launch:0,push:.75,lunge:1.6,chains:{kick:`special2`,punch:`uppercut`}},special2:{id:`special2`,startup:11,active:6,recovery:18,damage:18,height:`mid`,hitstun:28,blockstun:16,knockdown:!0,launch:5.5,push:4.8,lunge:2.6},',
        'DEFAULT_FRAMES Special frame data (5-hit extenders)',
    )
    ctx.replace_exact('landing:{id:`landing`,startup:0,active:0,recovery:14,', 'landing:{id:`landing`,startup:0,active:0,recovery:8,', 'snappier jump landing recovery')
    ctx.replace_exact(
        'update(e,t){if(this.wantsSuper=!1,this.stateFrames++,e.grab||e.punch||e.kick?this.buffer={button:e.grab?`grab`:e.kick?`kick`:`punch`,frames:9}:this.buffer&&(this.buffer.frames--,this.buffer.frames<=0&&(this.buffer=null)),e.super?this.superBuffer=Eo:this.superBuffer>0&&this.superBuffer--,Do.has(this.state))return;let n=t>=this.x?1:-1;switch(this.state){case`idle`:case`walk`:case`crouch`:this.comboHits=0,this.updateActionable(e,n);break;',
        'update(e,t){if(this.wantsSuper=!1,this.stateFrames++,this.overloadFrames>0&&this.overloadFrames--,this.tapAge>0&&this.tapAge--,e.grab||e.punch||e.kick?this.buffer={button:e.grab?`grab`:e.kick?`kick`:`punch`,frames:24}:this.buffer&&(this.buffer.frames--,this.buffer.frames<=0&&(this.buffer=null)),e.super?this.superBuffer=Eo:this.superBuffer>0&&this.superBuffer--,Do.has(this.state)){if(this.state===`getup`&&this.stateFrames===1){this.facing=t>=this.x?1:-1}return}let n=t>=this.x?1:-1;e.moveX!==0&&this.prevMoveX===0&&(this.tapDir===e.moveX&&this.tapAge>0&&this.actionable&&!e.down?(this.dashFrames=10,this.dashDir=e.moveX,this.tapAge=0):(this.tapDir=e.moveX,this.tapAge=14)),this.prevMoveX=e.moveX,this.actionable&&e.moveX*n<0?this.blockFrames=Math.min(60,this.blockFrames+1):this.state!==`blockstun`&&(this.blockFrames=0);switch(this.state){case`idle`:case`walk`:case`crouch`:this.comboHits=0,this.updateActionable(e,n);break;',
        'ko update dash, parry timing, overloadFrames, facing fix, 24f buffer',
    )
    ctx.replace_exact(
        'updateActionable(e,t){this.facing=t;let n=e.moveX*this.facing;if(this.moveRel=n,this.holdingBack=n<0,this.superBuffer>0&&this.meter>=100){this.superBuffer=0,this.wantsSuper=!0,this.vx=0;return}if(e.up&&!e.down){this.startJump(n);return}this.crouching=e.down;let r=this.consumeBuffer();r?this.startAttack(ro(r,this.crouching,n>0)):this.crouching?(this.enter(`crouch`),this.vx=0):n===0?(this.enter(`idle`),this.vx=0):(this.enter(`walk`),this.vx=n>0?this.char.walkFwd*this.facing:-this.char.walkBack*this.facing)}',
        'updateActionable(e,t){this.facing=t;let n=e.moveX*this.facing,ov=this.overloadFrames>0?1.3:1;if(this.moveRel=n,this.holdingBack=n<0,this.superBuffer>0&&this.meter>=100){this.superBuffer=0,this.wantsSuper=!0,this.vx=0;return}if(e.up&&!e.down){this.dashFrames=0,this.startJump(n);return}this.crouching=e.down;let r=this.consumeBuffer();if(r){this.dashFrames=0,this.startAttack(ro(r,this.crouching,n>0));return}if(this.dashFrames>0){this.dashFrames--,this.vx=this.dashDir*(this.dashDir===this.facing?7.2:6)*ov,this.moveRel=this.dashDir*this.facing,this.enter(`walk`);return}this.crouching?(this.enter(`crouch`),this.vx=0):n===0?(this.enter(`idle`),this.vx=0):(this.enter(`walk`),this.vx=(n>0?this.char.walkFwd*this.facing:-this.char.walkBack*this.facing)*ov)}',
        'ko updateActionable burst dash step + 1.3x Gethu Overload speed',
    )
    ctx.replace_exact(
        'updateAttack(){let e=this.attack;if(!e){this.enter(`idle`);return}e.frame++;let t=e.def;if(e.frame<=t.startup+t.active?this.vx=(t.lunge+(e.frame<=t.startup+1?To(this,t.id):0))*this.facing:this.vx*=.75,t.chains&&e.hasHit&&this.buffer&&e.frame>=t.startup+t.active){let e=po(this.char.id,t,this.buffer.button);if(e){this.buffer=null,this.startAttack(e);return}}e.frame>=io(t)&&(this.attack=null,this.crouching=!!t.crouching,this.enter(t.crouching?`crouch`:`idle`))}integrate()',
        'updateAttack(){let e=this.attack;if(!e){this.enter(`idle`);return}e.frame+=this.overloadFrames>0&&e.frame%3===0?2:1;let t=e.def;if(e.frame<=t.startup+t.active){let lg=this.char.style===`orator`&&[`jab`,`cross`,`uppercut`].includes(t.id)?t.lunge*.2:t.lunge;this.vx=(lg+(e.frame<=t.startup+1?To(this,t.id):0))*this.facing}else this.vx*=.75;if(e.hasHit&&!e.blocked&&this.superBuffer>0&&this.meter>=100&&e.frame>=t.startup){this.superBuffer=0,this.attack=null,this.wantsSuper=!0,this.vx=0,this.enter(`idle`);return}if(t.chains&&e.hasHit&&this.buffer&&e.frame>=t.startup+t.active){let e=po(this.char.id,t,this.buffer.button);if(e){this.buffer=null,this.startAttack(e);return}}e.frame>=io(t)&&(this.attack=null,this.crouching=!!t.crouching,this.enter(t.crouching?`crouch`:`idle`))}integrate()',
        'ko updateAttack Hit-Confirm Super Cancel + Orator zoner lunge + 1.3x Gethu Overload',
    )
    ctx.replace_exact(
        'this.x+=this.vx*qe,this.y+=this.vy*qe,this.state===`walk`&&(this.walkDistance+=Math.abs(this.vx)*qe),this.x=Math.max(-A,Math.min(A,this.x))',
        'this.x+=this.vx*qe*(this.grounded&&window.__marinaWaveSlip?1.45:1),this.y+=this.vy*qe,this.state===`walk`&&(this.walkDistance+=Math.abs(this.vx)*qe),this.x=Math.max(-A,Math.min(A,this.x))',
        'ko integrate Marina wave reduced friction slide',
    )
    ctx.replace_exact(
        'function So(e,t){return Math.max(co[e][t]?.[0]??0,Qe)}',
        'function So(e,t){return Math.max(co[e][t]?.[0]??0,Qe)+(N[e]?.style===`orator`&&[`jab`,`cross`,`uppercut`].includes(t)?1.35:0)}',
        'Orator mid-range soundwave zoner reach',
    )
    ctx.replace_exact(
        'if(a){n.blocked=!0;let r=Math.min(Math.round(n.def.damage*e.char.damageMul*$e),Math.ceil(t.hp)-1);return r>0&&(t.hp-=r),t.applyBlock(n.def,i),e.addMeter(2),t.addMeter(3),af(e,t,n.def.push*.6),{attacker:e,defender:t,moveId:n.def.id,blocked:!0,damage:Math.max(0,r),knockdown:!1,ko:!1,x:o,y:s}}let c=t.attackPhase===`startup`,l=tf(e,t,n.def.damage*(c?et:1));return t.applyHit(n.def,l,i),e.addMeter(l*.9+2),t.addMeter(l*.6),af(e,t,n.def.push*.8),{attacker:e,defender:t,moveId:n.def.id,blocked:!1,damage:l,knockdown:t.state===`knockdown`,ko:t.state===`ko`,counter:c,x:o,y:s}}',
        'if(a){n.blocked=!0;let p=t.blockFrames>0&&t.blockFrames<=7;if(p)return t.blockFrames=99,t.attack=null,t.stun=0,t.vx=0,t.enter(t.crouching?`crouch`:`idle`),t.addMeter(18),af(e,t,n.def.push*.9),{attacker:e,defender:t,moveId:n.def.id,blocked:!0,parry:!0,damage:0,knockdown:!1,ko:!1,x:o,y:s};let r=Math.min(Math.round(n.def.damage*e.char.damageMul*$e),Math.ceil(t.hp)-1);return r>0&&(t.hp-=r),t.applyBlock(n.def,i),e.addMeter(2),t.addMeter(3),af(e,t,n.def.push*.6),{attacker:e,defender:t,moveId:n.def.id,blocked:!0,parry:!1,damage:Math.max(0,r),knockdown:!1,ko:!1,x:o,y:s}}if(t.char.style===`heavy`&&t.state===`attack`&&[`kick`,`roundhouse`].includes(t.attack?.def?.id)&&[`jab`,`cross`,`lowJab`,`airPunch`].includes(n.def.id)){let l0=tf(e,t,n.def.damage),l=Math.max(1,Math.round(l0*.5));return t.hp=Math.max(1,t.hp-l),e.addMeter(4),t.addMeter(8),{attacker:e,defender:t,moveId:n.def.id,blocked:!1,armor:!0,damage:l,knockdown:!1,ko:!1,x:o,y:s}}let c=t.attackPhase===`startup`,l0=tf(e,t,n.def.damage*(c?et:1)),l=t.overloadFrames>0?Math.max(1,Math.round(l0*.5)):l0;return t.applyHit(n.def,l,i),e.addMeter(e.overloadFrames>0?8:Math.max(18,l*.9+2)),t.addMeter(Math.max(12,l*.6)),af(e,t,n.def.push*.8),{attacker:e,defender:t,moveId:n.def.id,blocked:!1,damage:l,knockdown:t.state===`knockdown`,ko:t.state===`ko`,counter:c,x:o,y:s}}',
        'nf Just-Frame Mass Parry + Heavyweight K,K Super Armor + Gethu Overload',
    )
    ctx.replace_exact(
        't.meter=0,t.attack=null,t.vx=0,t.forceState(`super`)',
        't.meter=0,t.overloadFrames=480,t.attack=null,t.vx=0,t.forceState(`super`);e===this.playerSide&&(this.matchStats.supers++)',
        'startSuper triggers 8-second (480f) Gethu Overload + matchStats',
    )
    ctx.replace_exact(
        'if(e.blocked){this.ctx.news.event({kind:`block`,attacker:e.attacker.char.id}),n.block(),this.hitStop=3,r.shake(.03,.12);return}',
        'if(e.blocked){if(e.parry){this.tmp.set(e.x,e.y+.45,.3);let p2=this.ctx.toScreen(this.tmp);a.popup(`MASS PARRY!`,p2.x,p2.y,`#facc15`),t.hitSpark(this.tmp,1.35,!1,e.attacker.facing),t.shockwave(this.tmp,16435252,.35,1.25,!0),n.hit(.9),this.hitStop=7,r.shake(.12,.16);return}this.ctx.news.event({kind:`block`,attacker:e.attacker.char.id}),n.block(),this.hitStop=3,r.shake(.03,.12);return}if(e.armor){this.tmp.set(e.x,e.y+.5,.3);let p2=this.ctx.toScreen(this.tmp);a.popup(`🛡️ SUPER ARMOR!`,p2.x,p2.y,`#38bdf8`),t.hitSpark(this.tmp,1.1,!1,e.attacker.facing),n.block(),this.hitStop=2;return}',
        'onHit Just-Frame Mass Parry + Heavyweight Super Armor FX',
    )
    ctx.replace_exact(
        'function af(e,t,n){Math.abs(t.x)>=6.45&&(e.vx=-e.facing*n)}',
        'function af(e,t,n){Math.abs(t.x)>=5.95&&(e.vx=-e.facing*n)}',
        'Corner pushback escape distance balance',
    )
