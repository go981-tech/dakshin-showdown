def apply(ctx):
    # 7o. Initial ticker line in Ff
    ctx.replace_exact(
        'this.pushTicker(`SATIRE LIVE: Sansad Showdown — the fight nobody demanded`)',
        'this.pushTicker(`ROHINI FDFS LIVE: Dakshin Showdown — First Day First Show!`)',
        'Ff initial ticker',
    )

    # 8. NewsDesk & Newspaper & Taunts & Tea Kadai Vendor (13 characters)
    new_news = '''Ao={godi:{name:`RANGARAJ STUDIO`,channel:`SUDU SORU TV`},troll:{name:`ADMIN PULLINGO`,channel:`MEME FACTORY`}};function jo(e,t){return e===`modi`||t===`rahul`?{godi:e,troll:t}:t===`modi`||e===`rahul`?{godi:t,troll:e}:{godi:e,troll:t}}var Mo={godi:`modi`,troll:`rahul`};function No(e,t){return Mo=jo(e,t),Mo}var Po={modi:`SURYA ANNA`,rahul:`THALAPATHY`,didi:`IRON AMMA`,trump:`SANDAL RAJU`,yogi:`LAL CAPTAIN`,nitin:`BANDE SHIV`,mbapu:`THATHA REFORM`,ravi:`POWER STAR`,lalu:`PULI VOICE`,amit:`FILES IPS`,dhruv:`SQUAD BRO`,nirmala:`TAX MAAMI`,rangaraj:`RANGARAJ`},Fo={modi:`Surya Anna`,rahul:`Thalapathy`,didi:`Iron Amma`,trump:`Sandal Raju`,yogi:`Lal Captain`,nitin:`Bande Shiv`,mbapu:`Thatha`,ravi:`Power Star`,lalu:`Puli Voice`,amit:`Files IPS`,dhruv:`Squad Bro`,nirmala:`Tax Maami`,rangaraj:`Rangaraj`},Io=(e,t)=>e[Math.min(e.length-1,Math.floor(t()*e.length))],Lo=(e,t)=>e.replace(/\\{(\\w+)\\}/g,(e,n)=>t[n]??``),Ro=e=>Mo.godi===e?`godi`:`troll`,zo=e=>e===`godi`?`troll`:`godi`,Bo=e=>Mo.godi===e?Mo.troll:Mo.godi;function Vo(e,t,n,r,i){let a={ticker:r,priority:i};return a[e]=t,a[zo(e)]=n,a}var Ho={godi:[`PRIME TIME SPECIAL! {M} — history created!`,`Breaking studio! {AN} strikes with {M}!`,`Panel agrees: greatest {M} in South arena!`,`Opposition stunned silent!`,`Marina crowd is ROARING!`,`Full force! {D} has zero answers!`],troll:[`#{M} trending No. 1 across TN, KL, KA, AP!`,`Direct FDFS theater celebration impact!`,`{AN} dropped a verified meme hit!`,`Clip that! Reel going 10M views!`,`{D} got ratio'd in 4K Ultra HD!`,`Bro unloaded a mass {M} fr fr!`] },Uo={godi:[`Fake narrative! Imported editing!`,`{DN} was only checking studio mic!`,`Slow-mo replay clearly shows zero touch!`,`Sudu Soru TV demands judicial probe on {M}!`,`Strategic tactical pause. Watch till 9 PM!`,`Chronology check... {DN} planned that dodge!`],troll:[`Paid PR clip! {DN} barely felt it!`,`Admin Pullingo confirms: recycled cinema stunt!`,`Audio launch hype exceeded actual damage!`,`{DN} was just stretching for Bajji break!`,`Fact-check pending in pinned comment!`,`Bro replied with a WhatsApp status 💀`] },Wo=[`FLASH: {A}'s {M} lands — box office analysts stunned!`,`SENATE INDEX {DIR} {N} pts after {A}'s {M}`,`{D} calls urgent all-party Filter Kaapi meeting`,`Walkout staged at Valluvar Kottam over {M}`,`South Film Twitter splits into 4 factions over {M}`,`7 anchors shouting simultaneously over {M}`,`Official clarification coming after interval block.`],Go=[`Weather: 100% humidity & sudden Kuthu storms on Marina Beach`,`Silk Board traffic remains paused to watch this match`,`Cricket fans chanting from Napier Bridge arches`,`Free Mysore Pak distributed near Valluvar Kottam`,`Exit polls give 110% vote share to both fighters`,`Tea Kadai master reports record Filter Kaapi sales`,`Temple cow enters Fort St. George — traffic police salute`,`Breaking: Nothing happened yet, stay tuned after ads`,`WhatsApp forwards graduate with Honours in Fight Analysis`,`Reminder: Pan-South fictional cartoon satire. All in good fun!`];function Ko(e){let t=35+Math.floor(e()*40),n=35+Math.floor(e()*40),r=Math.floor(e()*30);return`EXIT POLL: ${Po[Mo.godi]} ${t}% · ${Po[Mo.troll]} ${n}% · OTHERS ${r}% · TOTAL ${t+n+r}% · Error margin: ±100%`}function qo(e,t=Math.random){switch(e.kind){case`roundStart`:return{godi:e.final?`FINAL ROUND! Four states watching live!`:`Round ${e.round}! ${Fo[Mo.godi]} steps to the podium!`,troll:e.final?`Final round macha! Popcorn & Bajji ready!`:`Round ${e.round}! ${Fo[Mo.troll]} ratio check!`,ticker:Ko(t),priority:!0};case`hit`:{let n={A:Po[e.attacker],D:Po[Bo(e.attacker)],AN:Fo[e.attacker],DN:Fo[Bo(e.attacker)],M:e.move.replace(/!$/,``),DIR:t()<.5?`surges`:`drops`,N:String(100+Math.floor(t()*900))},r=Ro(e.attacker),i=e.knockdown||t()<.35?Lo(Io(Wo,t),n):void 0;return Vo(r,Lo(Io(Ho[r],t),n),Lo(Io(Uo[zo(r)],t),n),i,e.knockdown)}case`block`:return Vo(Ro(Bo(e.attacker)),Io([`BLOCKED! Granite Kanchipuram wall!`,`Soundproof studio glass block!`,`Not today macha — BLOCKED!`],t),void 0,void 0,!1);case`super`:{let t=Ro(e.caster),n=Jo[e.caster]??Jo.modi;return Vo(t,n.hype,n.spin,`BREAKING: ${e.superName} unleashed! ${n.ticker}`,!0)}case`ko`:{if(e.timeUp||!e.winner)return{godi:`Time up! ${Fo[Mo.godi]} claims moral mandate!`,troll:`Time up! Comments section declares draw!`,ticker:`TIME UP: Both sides celebrate with Mysore Pak & laddoos`,priority:!0};let t=Ro(e.winner);return Vo(t,{godi:`SOZHI MUDINJATHU! Clean sweep!`,troll:`K.O.! Pack up the flex banners!`}[t],{godi:`EVMs & lights blamed! Recount now!`,troll:`Scripted referee! Part 2 coming!`}[zo(t)],`BREAKING: ${Po[e.winner]} wins by K.O.! Emergency press meet called!`,!0)}case`roundWin`:return{ticker:e.perfect?`PERFECT ROUND for ${Po[e.winner]}! Zero HP lost!`:`${Po[e.winner]} wins the round! Filter Kaapi poured outside!`,priority:!0};case`cow`:return{godi:`Temple cow on stage! Match paused with respect!`,troll:`Cow has better footwork than half the roster ngl`,ticker:`BREAKING: Sacred cow strolls across Marina ring!`,priority:!0};case`cowGone`:return{godi:`Cow leaves the stage! Debate resumes!`,troll:`Cow exited left. Back to sandai!`,priority:!0};case`chai`:return Vo(Ro(e.kicker),`Kaapi tumbler kicked! GST added to replacement!`,`${Po[e.kicker]} owes the Tea Master ₹10!`,void 0,!1);case`bored`:return{godi:`Standoff at Marina! Speak into the mic!`,troll:`Zero action for 5 seconds — audience scrolling reels`,ticker:void 0,priority:!1};case`comeback`:{let t=Ro(e.leader);return Vo(t,{godi:`Comeback! ${Po[e.leader]} wave sweeps the arena!`,troll:`Comeback arc loading... ${Fo[e.leader]} mass interval block!`}[t],void 0,void 0,!1)}}}var Jo={modi:{hype:`VIDIYAL CYCLE RALLY! Sunburst over Marina!`,spin:`Rode an ECR morning cycle straight into a ring KO 💀`,ticker:`Rohini FDFS fans go wild`},rahul:{hype:`LEO SLOW-MO & 1000CR! Box office record shattered!`,spin:`Froze time with coffee cups and audio-launch hype 💀`,ticker:`Pan-India trade trackers revise FDFS numbers`},didi:{hype:`POES GARDEN THRONE! Lion Chair drop!`,spin:`Rained tiffins, laptops and two-leaf justice!! 💀`,ticker:`Emerald Lion Throne spotted at Marina Arena`},trump:{hype:`THAGGEDHE LE AXE! Red Sandal storm unleashed!`,spin:`Stamped THAGGEDHE LE across the opponent's ribs 💀`,ticker:`Seshachalam timber rates spike 100%`},yogi:{hype:`KADAKKU PURATHU K-RAIL! SilverLine blitz!`,spin:`Parked an express K-Rail train straight on stage 💀`,ticker:`SilverLine route detours right through the ring`},nitin:{hype:`SILK BOARD 999s & BANDE! 5 guarantees ignited!`,spin:`Dropped a Resort Volvo and Kanakapura granite boulder 💀`,ticker:`Outer Ring Road commuters cheer from gridlock`},ravi:{hype:`HUNGRY CHEETAH OG! Crimson Katana Fire Storm!`,spin:`Pulled an anime katana slash in bullet-time 💀`,ticker:`Kakinada fans burst crackers outside studio`},lalu:{hype:`MIKE SET PULI ROAR! Golden Tiger unleashed!`,spin:`Horn speakers shattered the sound barrier 💀`,ticker:`Special Express mic setup installed on stage`},amit:{hype:`PRESS MEET & SECRET FILES! ENNA SIR CHECKMATE!`,spin:`Tough questions turned into flying dossier stacks 💀`,ticker:`Journalists dodge flying classified folders`},dhruv:{hype:`10M CLICKBAIT HOUNDS! 1M likes in 3 seconds!`,spin:`Outsourced combat to glowing red arrows & hounds 💀`,ticker:`Thumbnail with 3 red arrows breaks server`},mbapu:{hype:`VAIKOM TORCH CHAKRA! Rationalist gale!`,spin:`Shattered dogma chains right inside the ring 💀`,ticker:`Rationalism Index hits all-time peak`},nirmala:{hype:`28% CARAMEL GST BLAST! Bahi-Khata vasool!`,spin:`Taxed popcorn, cream buns, and the opponent's Gethu 💀`,ticker:`GST Council raises combo tax to 28%`},rangaraj:{hype:`KELVIKKU ENNA BATHIL! Prime time stun-lock!`,spin:`Muted opponent's studio mic live on air 💀`,ticker:`Arangam TRP hits 99.9%`}},Yo={modi:[`"Wait for the next 5-year manifesto." — Sunset Camp`,`"Cinema guild conspired with lighting crew." — Sunset Camp`,`"We demand a Marina Beach recount!" — Sunset Camp`],rahul:[`"Censor board cut my third act punch!" — Welfare Wing`,`"Waiting for pan-India OTT verdict." — Welfare Wing`,`"Audio launch crowd would've been louder." — Welfare Wing`],didi:[`"Fort gate was locked from inside." — Two-Leaf Camp`,`"Unfair! Ring bell rang early." — Two-Leaf Camp`,`"Next budget gives two extra paddles!" — Two-Leaf Camp`],trump:[`"Flower nu nenachikitiya? Wait for Part 3!" — Syndicate Camp`,`"Sandalwood customs delayed my crate!" — Syndicate Camp`,`"Ref wasn't even following dialogue!" — Syndicate Camp`],yogi:[`"This was a tactical harthal!" — Red Cadre`,`"SilverLine DPR still under review." — Red Cadre`,`"We boycott the scoreboard!" — Red Cadre`],nitin:[`"Stuck at Silk Board signal for 4 hours." — Flyover Camp`,`"White-topping work started mid-match!" — Flyover Camp`,`"Fifth guarantee covers rematch fees." — Flyover Camp`],ravi:[`"Interval block — second half coming!" — Power Wing`,`"Dubbing artist arrived late." — Power Wing`,`"Next dialogue will clear the boundary." — Power Wing`],lalu:[`"They changed the mic frequency mid-speech!" — Tiger Brigade`,`"Historical evidence in next 4-hour rally!" — Tiger Brigade`,`"Platform signal was amber!" — Tiger Brigade`],amit:[`"Enna sir, out-of-syllabus punches!" — Press Force`,`"White paper will be released on Tuesday." — Press Force`,`"Next press meet settles this!" — Press Force`],dhruv:[`"Algorithm demonetized my uppercut!" — Squad Camp`,`"Wait for Part 2 Expose tomorrow!" — Squad Camp`,`"Thumbnail CTR betrayed us!" — Squad Camp`],mbapu:[`"Censor Red Card expired too soon!" — Election Board`,`"Study the syllabus and return next round!" — Self-Respect Camp`,`"Model Code of Conduct applies next match." — Election Board`],nirmala:[`"Caramel popcorn tax slab was miscalculated!" — Treasury Camp`,`"Onion prices not included in this combo!" — Treasury Camp`,`"18% GST surcharge pending!" — Treasury Camp`],rangaraj:[`"They muted my mic during rebuttal!" — Studio Panel`,`"Answer my question first — Point-ku vaanga!" — Studio Panel`,`"Break after this!" — Studio Panel`]};function Xo(e,t,n,r=Math.random){let i=Math.max(...n),a=Math.min(...n),o=i-a>=2;return{masthead:Io([`ROHINI FDFS BOX OFFICE RECEIPT`,`TEA KADAI BLOCKBUSTER POSTER`,`TASMAC FLEX BANNER TRACKER`,`SOUTH CINEMA 1000CR LEDGER`],r),headline:o?{modi:`SURYA ANNA SMASHES BOX OFFICE RECORD!`,rahul:`THALAPATHY HITS ₹1000 CRORE CLUB!`,didi:`IRON AMMA STORMS ROHINI SCREEN 1!`,trump:`SANDAL RAJU RULES ALL INDIA FDFS!`,yogi:`LAL CAPTAIN SHATTERS OVERSEAS RECORDS!`,nitin:`BANDE SHIV PAVED OVER BOX OFFICE!`,mbapu:`CENSOR BOARD THATHA CLEARS ALL CUTS!`,ravi:`POWER STAR UNLEASHES DAY-1 TSUNAMI!`,lalu:`PULI VOICE ROARS HOUSEFULL SHOWS!`,amit:`FILES IPS CLOSES EVERY CASE DAY 1!`,dhruv:`SQUAD BRO TRENDS #1 WORLDWIDE!`,nirmala:`TAX MAAMI COLLECTS 28% GST RECORD!`,rangaraj:`RANGARAJ STUDIO TOPS TRP CHARTS!`}[e]:{modi:`SURYA ANNA CLINCHES CLIMAX SHOW!`,rahul:`THALAPATHY WINS LAST-REEL BLOCKBUSTER!`,didi:`IRON AMMA HOLDS HOUSEFULL FORTRESS!`,trump:`SANDAL RAJU REFUSES TO BOW!`,yogi:`LAL CAPTAIN EDGES PHOTO FINISH!`,nitin:`BANDE SHIV CLEARS SILK BOARD IN CLIMAX!`,mbapu:`THATHA REFORM PREVAILS BY RED CARD!`,ravi:`POWER STAR STEALS FINAL REEL!`,lalu:`PULI VOICE WINS CLIMAX SPEECH!`,amit:`FILES IPS WINS BY ONE PRESS QUESTION!`,dhruv:`SQUAD BRO EXPLAINS THE WIN IN 10 MINS!`,nirmala:`TAX MAAMI AUDITS THE FINAL ROUND!`,rangaraj:`RANGARAJ WINS IN PRIME TIME FINALE!`}[e],sub:o?`SUPER HIT ${i}–${a} · Flex banners printed`:`NAIL-BITER ${i}–${a} · Recount at Tea Kadai`,excuse:Io(Yo[t]??Yo.modi,r)}}'''
    ctx.replace_span('Ao={godi:', 'var Zo={modi:', new_news + 'var Zo={modi:', 'Ao..Xo news & box office headlines', include_end=True)

    ctx.replace_exact('$o=[`Chai! Chai!`,`Garam chai!`,`Cutting chai, ₹10!`,`Chai le lo, chai!`]', '$o=[`Filter Kaapi!`,`Degree Kaapi!`,`Suda Bajji, ₹10!`,`Kaapi! Kaapi!`]', '$o vendor lines')
    ctx.replace_exact('es=[`Arre! Mera cup!`,`Oye! Chai gira di!`,`Paise kaun dega?!`]', 'es=[`Ayyo! En Kaapi!`,`Yov! Glass pochu!`,`Kaasu yaaru kuduppa?!`]', 'es vendor break lines')
    ctx.replace_exact('`+10 SOAN PAPDI!`', '`+10 MYSORE PAK!`', 'pickup mysore pak')
    ctx.replace_exact('t.fillText(`SOAN PAPDI`,128,66)', 't.fillText(`MYSORE PAK`,128,66)', 'qa MYSORE PAK box texture')
    ctx.replace_exact('this.ctx.hud.speech(`Lo ji, soan papdi! 🪔`,r.x,r.y,`small`)', 'this.ctx.hud.speech(`Suda Suda Mysore Pak! 🌾`,r.x,r.y,`small`)', 'vendor Mysore Pak drop speech')
    ctx.replace_exact('Maza aaya? 🪔 Mithai khilao', 'Mass-aa irundhucha? ☕ Buy Filter Kaapi', 'La result button')
    ctx.replace_exact('DOUBLE GHEE KHATAM!', 'DOUBLE SOZHI MUDINJATHU!', 'double KO banner')
    ctx.replace_exact('`GHEE KHATAM!`', '`SOZHI MUDINJATHU!`', 'KO banner')
    ctx.replace_exact('i.meterLabel.textContent=c?`SHAKTI READY!`:`SHAKTI`', 'i.meterLabel.textContent=c?`GETHU READY!`:`GETHU`', 'GETHU meter')

    # 9. UI/Result strings & Kaapi tip modal
    ctx.replace_exact('Lt=[`Mithai le lo! Kaju katli!`,`Ladoo garam garam!`,`Diwali special: chai + mithai!`,`Soan papdi bhi hai!`]', 'Lt=[`Suda Suda Bajji!`,`Mysore Pak ready!`,`Filter Kaapi + Vada!`,`Jigarthanda special!`]', 'Lt festive kaapi lines')
    ctx.replace_exact('Ea=[[21,`Ek laddoo`],[51,`Kaju katli box`],[101,`Diwali mithai thali`]]', 'Ea=[[21,`Filter Kaapi`],[51,`Medu Vada + Kaapi`],[101,`Banana Leaf Meals`]]', 'UPI tips')
    ctx.replace_all('Diwali card bhejo', 'Pongal Flex Bhejo', 'Pongal Flex Bhejo')
    ctx.replace_all('Diwali pe mithai khilao?', 'Buy us a Filter Kaapi?', 'Buy us a Filter Kaapi?')
    ctx.replace_all('Diwali pe mithai khilao', 'Buy Filter Kaapi ☕', 'Buy Filter Kaapi')
    ctx.replace_all('Game free hai, koi ad nahi. Aapki mithai se servers chalte hain aur Chapter 2 jaldi aata hai.', 'Game is free with zero ads. Your Filter Kaapi keeps servers running & funds more Tamil Nadu stages!', 'Filter Kaapi CTA copy')
    ctx.replace_all('Diwali Special Edition 🪔', 'Rohini FDFS Edition 🎬', 'Rohini FDFS Edition')
    ctx.replace_exact(
        'function Ka(e,t){return Mt?{date:e.replace(`Satire Edition`,`Rohini FDFS Edition 🎬`),excuse:Math.random()<.5?`Breaking: Sansad mein sirf green patakhe allowed.`:t}:{date:e,excuse:t}}',
        'function Ka(e,t){return{date:e.replace(`Satire Edition`,`Rohini FDFS Edition 🎬`),excuse:t}}',
        'Ka keep character Box Office excuse',
    )
    ctx.replace_all('Breaking: Sansad mein sirf green patakhe allowed.', 'Breaking: Housefull Rohini FDFS crowd tears flex banners!', 'Breaking Rohini headline')
    ctx.sub_regex(r'`[^`\n]{1,6} WINNER`', '`🏆 WINNER`', 'winner label trophy')
    ctx.replace_all('ðŸ™ ', '🙏', 'fix pray emoji mojibake')
    ctx.replace_all('Shukriya, Sansad Supporter!', 'Nandri, Dakshin Supporter!', 'Dakshin Supporter')
    ctx.replace_all('Aapki ₹${t} ki mithai se game free rehta hai aur Chapter 2 paas aata hai.', 'Your ₹${t} Filter Kaapi fuels free matches & South Arena updates!', 'Filter Kaapi receipt copy')
    ctx.replace_all('SHUBH DEEPAVALI', 'PONGAL VAALTHUKKAL', 'PONGAL VAALTHUKKAL')
    ctx.replace_all('SANSAD SHOWDOWN', 'DAKSHIN SHOWDOWN', 'DAKSHIN SHOWDOWN')
    ctx.replace_exact('Shubh Deepavali! 🪔 Iss Diwali ${t} ke saath Sansad Showdown khelo', 'Iniya Pongal! 🪔 Play Dakshin Showdown with ${t}', 'Share text')
    ctx.replace_all('celebrates outside the Sansad. (Cartoon, not a real photo)', 'celebrates outside Fort St. George. (Satire cartoon)', 'Fort St George caption')
    ctx.replace_all('rules the Sansad!', 'rules the Dakshin Arena!', 'Dakshin Arena headline')

    # 11b. Select screen P2 labels & #local2p-btn + [data-assist] picker
    ctx.replace_exact(
        'let t=Q?`2P · FRIEND${$.friendReady?` · READY ✓`:``}`:e===`mbapu`?`FINAL BOSS · OPPONENT`:`CPU`;Em(q(`#plate-p1`)',
        'let t=Q?`2P · FRIEND${$.friendReady?` · READY ✓`:``}`:window.__local2P?`2P · LOCAL KEYBOARD`:e===`mbapu`?`FINAL BOSS · OPPONENT`:`CPU`;Em(q(`#plate-p1`)',
        'Dm plate-p2 label',
    )
    ctx.replace_exact(
        'q(`#vs-line`).textContent=`${N[X].name} (YOU) vs ${e?N[e].name:`…`} (${Q?`FRIEND`:e===`mbapu`?`BOSS`:`CPU`})`',
        'q(`#vs-line`).textContent=`${N[X].name} (YOU) vs ${e?N[e].name:`…`} (${Q?`FRIEND`:window.__local2P?`2P LOCAL`:e===`mbapu`?`BOSS`:`CPU`})`',
        'Dm vs-line local2P',
    )
    ctx.replace_exact(
        'document.querySelector(`#fight-btn`).addEventListener(`click`,Nm),',
        'document.querySelectorAll(`[data-assist]`).forEach(el=>el.addEventListener(`click`,()=>{window.__selectedAssist=el.dataset.assist;document.querySelectorAll(`[data-assist]`).forEach(x=>x.classList.toggle(`selected`,x===el));let lbl=document.querySelector(`#budget-meter .label`);if(lbl)lbl.textContent={sumo:`FLYING SUMO`,squad:`FLYING SQUAD`,light:`STUDIO LIGHT`,random:`RANDOM KOOTANI`}[window.__selectedAssist]||`KOOTANI CAMEO`;Y.uiSelect()})),document.querySelector(`#local2p-btn`)?.addEventListener(`click`,()=>{window.__local2P=!window.__local2P;let b=document.querySelector(`#local2p-btn`);b.classList.toggle(`active`,window.__local2P);b.textContent=window.__local2P?`⚔️ 2P LOCAL: ON`:`⚔️ 2P LOCAL: OFF`;Y.uiSelect(),Dm()}),document.querySelector(`#fight-btn`).addEventListener(`click`,Nm),',
        'bind #local2p-btn + [data-assist]',
    )
    ctx.replace_exact('this.playerSide,this.net?`FRIEND`:`CPU`,this.bossSide', 'this.playerSide,this.net?`FRIEND`:window.__local2P?`2P`:`CPU`,this.bossSide', 'jf setup HUD 2P label')

    # 15. Rendering & Animation Smoothness
    ctx.replace_exact(
        'J=new Ie({canvas:ip,antialias:!1,powerPreference:`high-performance`});J.setPixelRatio(Math.min(window.devicePixelRatio,M?1.5:2))',
        'J=new Ie({canvas:ip,antialias:!M,powerPreference:`high-performance`});J.setPixelRatio(Math.min(window.devicePixelRatio,M?1.35:1.5))',
        'WebGL antialias + balanced DPR',
    )
    ctx.replace_exact('Ph=Math.min(window.devicePixelRatio,M?1.5:2)', 'Ph=Math.min(window.devicePixelRatio,M?1.35:1.5)', 'Ph balanced DPR')
    ctx.replace_exact('let n=M?1024:2048;this.sun.shadow.mapSize.set(n,n)', 'let n=1024;this.sun.shadow.mapSize.set(n,n)', '1024 shadow map for 60/120fps stability')
    ctx.replace_exact(
        'let t=Hp===`battle`||Hp===`result`&&!!Z||!!xp&&!M,n=Z?.paused?100:t?1e3/60:1e3/30;if(e<jh-1||(jh=Math.max(jh+n,e-n),Sp.active))return;',
        'let n=Z?.paused?80:0;if(n>0&&e<jh+n)return;if(Sp.active)return;jh=e;',
        'Unlocked native monitor vsync loop',
    )
    ctx.replace_exact(
        '!l&&!u&&(c.stopDance?.(),c.stopClip?.(),c.blendTo(o,s,t)),u||c.setMirror?.(!1);let d=this.phase===`grapple`?this.grapple:null,f=this.phase===`super`&&i!==this.superCaster?this.superMove:null,p=d?i===this.grappleSide?d.attTf:d.defTf:f?.targetTf??null;if(p)c.setFree(p.x,p.y,p.z,p.yaw,p.roll);else{let n=this.smooth[i],r=Math.exp(-e*14);n.x*=r,n.y*=r;let o=a.x+n.x,s=Math.max(0,a.y+n.y);',
        'u&&F(c.current,o,Math.min(1,t*10),c.current),!l&&!u&&(c.stopDance?.(),c.stopClip?.(),c.blendTo(o,Math.max(s,16),t)),u||c.setMirror?.(!1);let d=this.phase===`grapple`?this.grapple:null,f=this.phase===`super`&&i!==this.superCaster?this.superMove:null,p=d?i===this.grappleSide?d.attTf:d.defTf:f?.targetTf??null;if(p)c.setFree(p.x,p.y,p.z,p.yaw,p.roll);else{let n=this.smooth[i],r=Math.exp(-e*14);n.x*=r,n.y*=r;let g=this.phase===`fight`?Math.min(qe,this.acc):0,o=Math.max(-A,Math.min(A,a.x+a.vx*g+n.x)),s=Math.max(0,a.y+(a.grounded?0:a.vy*g)+n.y);',
        'Sub-frame movement interpolation + smooth clip exit',
    )
    ctx.replace_exact('setTransform(e,t,n,r,i=.28){', 'setTransform(e,t,n,r,i=.36){', 'Smooth default idle yaw angle')
    ctx.replace_exact(
        'function Ah(t){Dh+=t,e.forEach((e,n)=>{let r=lm[e];if(!r||!r.root.visible)return;let i=Hp===`select`&&e===X;r.blendTo(i?Wi(Dh,e):$i(Dh+n*1.9,e),6,t)});let n=Math.sin(Dh*.25)*(Hp===`select`?.12:.3),r=4.1*Math.max(1,1.5/lp.camera.aspect);Oh.set(0,1.15,0),kh.set(0+Math.sin(n)*r,1.45,Math.cos(n)*r),lp.set(kh,Oh,2.5,40)',
        'function Ah(t){Dh+=t,e.forEach((e,n)=>{let r=lm[e];if(!r||!r.root.visible)return;let i=Hp===`select`&&e===X;r.blendTo(i?Wi(Dh,e):$i(Dh+n*1.9,e),9,t)});let n=Math.sin(Dh*.25)*(Hp===`select`?.12:.3),r=4.1*Math.max(1,1.5/lp.camera.aspect);Oh.set(0,1.15,0),kh.set(0+Math.sin(n)*r,1.45,Math.cos(n)*r),lp.set(kh,Oh,4.5,40)',
        'Menu camera & pose smooth damping',
    )

    # 17. Paal Abhishekam (5+ hits), Fan War Feed, Stage Hazards, Kootani Assist Step, Censor Boss, Mass Hero Camera Zoom, Box Office Receipt
    ctx.replace_exact(
        'combo(e,t){if(t<2)return;let n=this.sides[e];n.combo.innerHTML=`<b>${t}</b> HITS`,n.combo.classList.remove(`show`),n.combo.offsetWidth,n.combo.classList.add(`show`),this.comboTimers[e]=1.4}',
        'combo(e,t){if(t<2)return;let n=this.sides[e];n.combo.innerHTML=`<b>${t}</b> HITS`,n.combo.classList.remove(`show`),n.combo.offsetWidth,n.combo.classList.add(`show`),this.comboTimers[e]=1.4,t>=5&&triggerPaalAbhishekam(e,t)}',
        'HUD 5+ combo Paal Abhishekam splash',
    )
    ctx.replace_exact(
        'this.ctx.news.event({kind:`hit`,attacker:e.attacker.char.id,move:s??Df[e.moveId],damage:e.damage,knockdown:e.knockdown})',
        'this.ctx.news.event({kind:`hit`,attacker:e.attacker.char.id,move:s??Df[e.moveId],damage:e.damage,knockdown:e.knockdown,combo:e.defender.comboHits})',
        'pass combo count to news/fanwar feed',
    )
    ctx.replace_exact(
        'event(e){let t=qo(e,this.rng);',
        'event(e){pushFanWarComment({kind:e.kind,attacker:e.attacker,combo:e.combo,knockdown:e.knockdown});let t=qo(e,this.rng);',
        'Ff.event -> Fan War live comment feed',
    )
    ctx.replace_exact(
        't.frame===t.def.startup+1&&Ef.has(t.def.id)&&this.checkChai(e)',
        't.frame===t.def.startup+1&&e.char.style===`orator`&&[`jab`,`cross`,`uppercut`].includes(t.def.id)&&spawnOratorSoundwave(this,e,t.def.id),t.frame===t.def.startup+1&&Ef.has(t.def.id)&&this.checkChai(e)',
        'jf.step Orator 3D soundwave rings on J,J,J',
    )
    ctx.replace_exact(
        'this.checkBoredom(),!this.net&&!this.boss&&this.stepMithai()',
        'updateSouthStageHazards(this.ctx.arena,this,this.time,qe),updateKootaniAssist(this,qe),updateCensorBossMechanic(this,qe),this.checkBoredom(),!this.net&&!this.boss&&this.stepMithai()',
        'jf.step stage hazards + Kootani assist + Censor boss',
    )
    ctx.replace_exact(
        'n.frameFight(o.x,s.x,o.y,s.y)',
        '(n.frameFight(o.x,s.x,o.y,s.y),this.massZoomTimer>0&&(this.massZoomTimer=Math.max(0,this.massZoomTimer-e),n.targetPos.z=Math.max(3,n.targetPos.z-2.5),n.rate=16))',
        'Mass Hero slow-mo camera zoom z - 2.5',
    )
    ctx.replace_exact(
        'trackBoss(e){this.bossSeconds+=qe,e.hp<this.bossHpSeen?(this.roundDamage+=this.bossHpSeen-e.hp,this.bossCalm=0):this.bossCalm+=qe,this.hardBoss&&this.bossCalm>=lo.regenDelay&&e.hp>0&&(e.hp=Math.min(e.maxHp,e.hp+lo.regen*qe)),this.bossHpSeen=e.hp,this.bestDamage=Math.max(this.bestDamage,this.roundDamage)}',
        'trackBoss(e){this.bossSeconds+=qe,e.hp<this.bossHpSeen?(this.roundDamage+=this.bossHpSeen-e.hp,this.bossCalm=0):this.bossCalm+=qe,this.bossHpSeen=e.hp,this.bestDamage=Math.max(this.bestDamage,this.roundDamage)}',
        'Remove Shanti boss passive regen (replaced by Censor Red Card aura)',
    )
    ctx.replace_exact('t.cinemaTitle(`AB ASLI PARIKSHA`,`MBAPU · ANTIM YODDHA`)', 't.cinemaTitle(`MODEL CODE OF CONDUCT`,`CENSOR BOARD · ELECTION BOSS`)', 'Censor Boss intro title')
    ctx.replace_exact('this.grappleSide=e,this.grapple=tc(', 'e===this.playerSide&&(this.matchStats.grabs++),onCensorBossGrabBreak(this,t,n),this.grappleSide=e,this.grapple=tc(', 'Grab breaks Censor Boss lock + stats')
    ctx.replace_exact('this.ctx.hud.clearSay()}', 'this.ctx.hud.clearSay(),cleanupSouthBattle(this)}', 'jf.dispose cleanupSouthBattle')
    ctx.replace_exact('this.onMatchEnd?.(e,{', 'window.__lastMatchStats={...this.matchStats};this.onMatchEnd?.(e,{', 'jf.endMatch store matchStats')
    ctx.replace_exact(
        'a(`#paper-date`).textContent=o.date,a(`#paper-headline`).textContent=i.headline,a(`#paper-sub`).textContent=i.sub,a(`#paper-excuse`).textContent=o.excuse,a(`#paper-photo`).setAttribute(`src`,Zp[t.winner]),a(`#paper-caption`).textContent=`${N[t.winner].fullName} celebrates outside Fort St. George. (Satire cartoon)`',
        'a(`#paper-date`).textContent=o.date;let bo=computeBoxOfficeVerdict(t.winner,r,t.wins,window.__lastMatchStats||{});a(`#boxoffice-crores`)&&(a(`#boxoffice-crores`).textContent=bo.clubText);a(`#tanglish-roast`)&&(a(`#tanglish-roast`).textContent=`🔥 TANGLISH ROAST: ${bo.roast}`);a(`#receipt-lines`)&&(a(`#receipt-lines`).textContent=`ROHINI FDFS · KICKS: ${(window.__lastMatchStats?.kicks)||0} · PUNCHES: ${(window.__lastMatchStats?.punches)||0} · BLUE SHIRT REVIEW: ${bo.reviewScore}`);a(`#paper-headline`).textContent=i.headline,a(`#paper-sub`).textContent=i.sub,a(`#paper-excuse`).textContent=o.excuse,a(`#paper-photo`).setAttribute(`src`,Zp[t.winner]),a(`#paper-caption`).textContent=`${N[t.winner].fullName} — Rohini FDFS Box Office Poster!`',
        'Box Office Crore Club & Dynamic Tanglish Roast receipt',
    )

    # Clean stray Sansad/version strings in title/result/select
    ctx.replace_all('PICK YOUR NETA', 'PICK YOUR THALAIVAR', 'PICK YOUR THALAIVAR')
    ctx.replace_all('FIGHT!', 'PODU SANDAI!', 'PODU SANDAI!')
    for old_v in ('?v=20261101_smooth', '?v=20261104_face', '?v=20261107_real', '?v=20261104', '?v=20261117', '?v=20261118', '?v=20261119', '?v=20261120', '?v=20261125'):
        ctx.replace_all(old_v, '?v=20261126', f'cache-buster {old_v}')
