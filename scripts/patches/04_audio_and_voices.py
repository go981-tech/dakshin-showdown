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
        'this.cue(`a`,.5,()=>{this.speech(0,n.char.introLine),t.playClip(`/assets/memes/${n.char.id}_1.mp3`,.95)}),this.cue(`b`,this.introLength/2+.1,()=>{this.speech(1,r.char.introLine),t.playClip(`/assets/memes/${r.char.id}_1.mp3`,.95)})',
        'Play matching _1.mp3 audio on intro speech bubbles',
    )
    ctx.replace_exact(
        'this.ctx.audio.announce(r.perfect?`perfect`:`wins_${e.char.id}`),this.speech(r.outcome,this.diwali?It(e.char.id,`win`,e.char.winLine):e.char.winLine)',
        'this._lastRoundPerfect=r.perfect,(r.perfect?this.ctx.audio.announce(`perfect`):(()=>{let wc=kn[e.char.id];wc&&this.ctx.audio.playClip(wc,Mn)})()),this.speech(r.outcome,e.char.winLine)',
        'Play matching kn win voice on every round win',
    )
    ctx.replace_exact(
        'else if(this.match.winner!==null){let e=kn[this.fighters[this.match.winner].char.id];e&&this.cue(`winLine`,1.2,()=>t.playClip(e,Mn))}',
        'else if(this._lastRoundPerfect&&this.match.winner!==null){let e=kn[this.fighters[this.match.winner].char.id];e&&this.cue(`winLine`,1.2,()=>t.playClip(e,Mn))}',
        'Avoid double-playing kn on non-perfect matchOver',
    )
