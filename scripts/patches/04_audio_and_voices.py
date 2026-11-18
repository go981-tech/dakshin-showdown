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
    ctx.replace_exact(
        'this.cue(`a`,.5,()=>this.speech(0,this.diwali?It(n.char.id,`intro`,n.char.introLine):n.char.introLine)),this.cue(`b`,this.introLength/2+.1,()=>this.speech(1,this.diwali?It(r.char.id,`intro`,r.char.introLine):r.char.introLine))',
        'this.cue(`a`,.5,()=>sayLine(this,0,`intro`,{priority:2})),this.cue(`b`,this.introLength/2+.1,()=>sayLine(this,1,`intro`,{priority:2}))',
        'Route round intros through sayLine',
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
        'startRound(e){e||this.emit',
        'startRound(e){window.__activeBattle=this,e||this.emit',
        'Track active battle for fighter dialogue',
    )
    ctx.replace_exact(
        'startAttack(e){this.attack={def:no[e],frame:0,hasHit:!1},this.enter(`attack`),this.stateFrames=0}',
        'startAttack(e){this.attack={def:no[e],frame:0,hasHit:!1},this.enter(`attack`),this.stateFrames=0,(e===`special1`||e===`special2`)&&sayLine(window.__activeBattle,this.side,e,{priority:2})}',
        'Route special startup through sayLine',
    )
    ctx.replace_exact(
        'this.superCaster=e,this.superMove=kd',
        'this.superCaster=e,window.__activeBattle=this,sayLine(this,e,`super`,{priority:4}),this.superMove=kd',
        'Route super start through sayLine',
    )
    ctx.replace_exact(
        'speech:(t,r)=>this.speech(t===`caster`?e:n.side,r)',
        'battle:this,speech:(t,r)=>sayLine(this,t===`caster`?e:n.side,`super`,{priority:4})',
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
