def apply(ctx):
    # Audio maps & hooks: Dn, kn, Nn, Mn, double_ko, fi, preloadClips, It(), intro & win voice playback
    ctx.replace_exact(
        'dhruv:vn}',
        'dhruv:vn,nirmala:yn,rangaraj:`/assets/rangaraj-super.mp3`}',
        'Dn 13 fighters',
    )
    ctx.replace_exact(
        'kn={ravi:bn,amit:xn},An=Cn,jn=Sn,Mn=1.43,Nn={intro:{url:wn,level:2.2},background:{url:Tn,level:3},battle:{url:En,level:1.242}}',
        'kn={modi:`/assets/memes/modi_2.mp3`,rahul:`/assets/rahulwin.mp3`,didi:`/assets/memes/didi_2.mp3`,trump:`/assets/memes/trump_2.mp3`,yogi:`/assets/memes/yogi_2.mp3`,nitin:`/assets/memes/nitin_2.mp3`,mbapu:Sn,ravi:bn,lalu:`/assets/memes/lalu_2.mp3`,amit:xn,dhruv:`/assets/memes/dhruv_2.mp3`,nirmala:`/assets/memes/nirmala_2.mp3`,rangaraj:`/assets/memes/rangaraj_2.mp3`},An=Cn,jn=Sn,Mn=1.05,Nn={intro:{url:wn,level:.85},background:{url:Tn,level:.78},battle:{url:En,level:.68}}',
        'kn 13 win voices + Mn/Nn mastered levels',
    )
    ctx.replace_exact(
        '"../assets/voice/double_ko.mp3":Xr',
        '"../assets/voice/double_ko.mp3":"/assets/voice/double_ko.mp3"',
        'Dedicated double_ko voice path',
    )
    ctx.replace_exact(
        'Y.preloadClips([X,n].flatMap(e=>Dn[e]??[]))',
        'Y.preloadClips([X,n].flatMap(e=>[Dn[e],kn[e],`/assets/memes/${e}_1.mp3`,`/assets/memes/${e}_2.mp3`].filter(Boolean)))',
        'Preload super, win, and action voice clips',
    )
    ctx.replace_exact(
        'dhruv:[`bed_tariff`,`release_tariff`,`shimmer`,`plop`,`eye_zing`,`bark`,`heartbeat`]}',
        'dhruv:[`bed_tariff`,`release_tariff`,`shimmer`,`plop`,`eye_zing`,`bark`,`heartbeat`],nirmala:[`bed_tariff`,`release_tariff`,`stamp_slam`,`kaching`,`coins`,`poof`],rangaraj:[`release_bulldozer`,`shimmer`,`bell`,`horn_short`,`drumroll`]}',
        'fi 13 fighters',
    )
    ctx.replace_exact(
        'function It(e,t,n){return Mt?Pt[e]?.[t]??n:n}',
        'function It(e,t,n){return n}',
        'Disable It() festival override so introLine/winLine match real audio',
    )
    ctx.replace_span(
        'runPhase(){let{hud:e,audio:t}=this.ctx,[n,r]=this.fighters;switch(this.phase){case`intro`:',
        'case`roundCall`:',
        'runPhase(){let{hud:e,audio:t}=this.ctx,[n,r]=this.fighters;switch(this.phase){case`intro`:{if(!this.isGuest){let i=window.__local2P&&!this.net?this.ctx.input.pollP1():this.ctx.input.poll(),a=window.__local2P&&!this.net?this.ctx.input.pollP2():null;if(i.punch||i.kick||i.super||a?.punch||a?.kick||a?.super){t.stopClip(0),n.forceState(`idle`),r.forceState(`idle`),this.setPhase(`roundCall`);break}}if(this.bossIntro){this.stepBossIntro(),this.phaseTime>this.introLength&&(n.forceState(`idle`),r.forceState(`idle`),this.setPhase(`roundCall`));break}this.cue(`a`,.35,()=>{this._introStage=1,sayLine(this,0,`intro`,{priority:2})}),this._introStage===1&&this.phaseTime>.8&&(!t.clipActive||this.phaseTime>3.6)&&(sayLine(this,1,`intro`,{priority:2}),this._introStage=2,this._p2IntroAt=this.phaseTime),this.cue(`paparazzi`,.3,()=>{(n.char.danceIntro||r.char.danceIntro)&&(this.ctx.arena.paparazzi(10),t.cameraClicks(8))}),!this.isGuest&&this._introStage===2&&this.phaseTime>this._p2IntroAt+.4&&(!t.clipActive||this.phaseTime>7.5)&&(n.forceState(`idle`),r.forceState(`idle`),this.setPhase(`roundCall`));break}case`roundCall`:',
        'Sequence P1 and P2 round intros with skippable clips',
        include_end=True,
    )
    ctx.replace_exact(
        'e?(t.forceState(`intro`),n.forceState(`intro`),this.setPhase(`intro`),this.bossIntro&&this.beginBossIntro()):this.setPhase(`roundCall`)',
        'e?(t.forceState(`intro`),n.forceState(`intro`),this._introStage=0,this._p2IntroAt=0,this.setPhase(`intro`),this.bossIntro&&this.beginBossIntro()):this.setPhase(`roundCall`)',
        'Reset sequential intro pacing state',
    )
    ctx.replace_exact(
        'this.ctx.audio.announce(r.perfect?`perfect`:`wins_${e.char.id}`),this.speech(r.outcome,this.diwali?It(e.char.id,`win`,e.char.winLine):e.char.winLine)',
        'this._lastRoundPerfect=r.perfect,r.perfect&&this.ctx.audio.announce(`perfect`),sayLine(this,r.outcome,`win`,{priority:4})',
        'Route round wins through sayLine',
    )
    ctx.replace_exact(
        'else if(this.match.winner!==null){let e=kn[this.fighters[this.match.winner].char.id];e&&this.cue(`winLine`,1.2,()=>t.playClip(e,Mn))}',
        'else if(this.match.winner!==null){sayLine(this,this.match.winner,`win`,{priority:4})}',
        'Route match-over win line through sayLine',
    )
    ctx.replace_exact(
        '!this.isGuest&&this.phaseTime>3.6&&(this.match.winner===null?(this.match.nextRound(),this.startRound(!1)):this.setPhase(`matchOver`))',
        '!this.isGuest&&this.phaseTime>3.6&&(!t.clipActive||this.phaseTime>6)&&(this.match.winner===null?(this.match.nextRound(),this.startRound(!1)):this.setPhase(`matchOver`))',
        'Round-over waits for no clip active up to 6.0s',
    )
    ctx.replace_exact(
        'startRound(e){e||this.emit',
        'startRound(e){window.__activeBattle=this,e||this.emit',
        'Track active battle for fighter dialogue',
    )
    ctx.replace_exact(
        'startAttack(e){this.attack={def:no[e],frame:0,hasHit:!1},this.enter(`attack`),this.stateFrames=0}',
        'startAttack(e){this.attack={def:no[e],frame:0,hasHit:!1},this.enter(`attack`),this.stateFrames=0,(e===`special1`||e===`special2`)&&window.__activeBattle&&(triggerMemeOnAction(window.__activeBattle,this,e),sayLine(window.__activeBattle,this.side,e,{priority:2}))}',
        'Route special startup through sayLine',
    )
    ctx.replace_exact(
        'this.superCaster=e,this.superMove=kd',
        'this.superCaster=e,window.__activeBattle=this,this.superMove=kd',
        'Track active battle without firing super speech at t0',
    )
    ctx.replace_exact(
        'clipTime:()=>i.clipTime(),popup:(e,t,n)=>{let i=this.ctx.toScreen(t);r.popup(e,i.x,i.y,n)},speech:(t,r)=>this.speech(t===`caster`?e:n.side,r)',
        'clipTime:()=>i.clipTime(),popup:(e,t,n)=>{let i=this.ctx.toScreen(t);r.popup(e,i.x,i.y,n)},battle:this,speech:(t,r)=>t===`target`||t===`defender`||t===`opp`?this.speech(n.side,r,2200):sayLine(this,e,`super`,{priority:4})',
        'Route super speech beats through sayLine',
    )
    ctx.replace_exact(
        'speech:(t,r)=>this.speech(t===`attacker`?e:n.side,r)',
        'battle:this,speech:(t,r)=>sayLine(this,t===`attacker`?e:n.side,`bark1`,{priority:2})',
        'Route grapple speech through sayLine',
    )
    ctx.replace_exact(
        'let l=Dn[t.char.id];l&&i.playClip(l),',
        '',
        'Remove fire-at-t0 super audio',
    )
    ctx.replace_exact(
        'window.setTimeout(()=>i.remove(),2e3)}};function Pf',
        'window.setTimeout(()=>i.remove(),3e3)}};function Pf',
        'Patch speech bubble duration to 3000ms',
    )
    ctx.replace_exact(
        'let e=+(this.playerSide===0);if(this.fighters[e].actionable){let t=Qo(this.fighters[e].char.id,this.rng);this.emit({t:`ev`,e:`speech`,side:e,text:t}),this.speech(e,t)}',
        'let e=+(this.playerSide===0);if(this.fighters[e].actionable){sayLine(this,e,`bark1`,{priority:1})}',
        'Remove random idle taunts and route bark1 through sayLine',
    )
    ctx.replace_exact(
        'speech(e,t){this.rigs[e].headWorld(this.tmp),this.tmp.y+=.45;let n=this.ctx.toScreen(this.tmp);this.ctx.hud.speech(t,n.x,n.y)}',
        'speech(e,t,d=3000){this.rigs[e].headWorld(this.tmp),this.tmp.y+=.45;let n=this.ctx.toScreen(this.tmp);this.ctx.hud.speech(t,n.x,n.y,``,d)}',
        'Pass approved audio duration to battle subtitles',
    )
    ctx.replace_exact(
        'speech(e,t,n,r=``){let i=document.createElement(`div`);',
        'speech(e,t,n,r=``,d=3000){let i=document.createElement(`div`);i.style.setProperty(`--speech-duration`,`${Math.max(300,d)}ms`);',
        'Add HUD subtitle duration parameter',
    )
    ctx.replace_exact(
        'window.setTimeout(()=>i.remove(),3e3)',
        'window.setTimeout(()=>i.remove(),d)',
        'Use actual approved subtitle duration',
    )
    ctx.replace_exact(
        'get clipActive(){return!!this.bufClip||!!this.clip}playClip',
        'get clipActive(){return!!this.bufClip||!!this.clip}get clipEndsAt(){if(this.bufClip&&this.ctx){let e=this.bufClip.startedAt+this.bufClip.duration-this.ctx.currentTime;return e>0?e*1e3:0}let e=this.clip;return e&&!e.paused&&e.duration&&Number.isFinite(e.duration)?Math.max(0,(e.duration-e.currentTime)*1e3):0}playClip',
        'Expose clipEndsAt while preserving clipActive',
    )
