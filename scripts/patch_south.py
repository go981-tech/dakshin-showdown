import os
import re

JS_PATH = os.path.join("public", "assets", "main-C7-oASSx.js")
BAK_PATH = JS_PATH + ".bak"

if not os.path.exists(BAK_PATH):
    with open(JS_PATH, "r", encoding="utf-8") as f:
        src = f.read()
    with open(BAK_PATH, "w", encoding="utf-8") as f:
        f.write(src)
else:
    with open(BAK_PATH, "r", encoding="utf-8") as f:
        src = f.read()

def replace_exact(text, old, new, label):
    assert old in text, f"FAILED exact match for [{label}]: {old[:100]!r}"
    return text.replace(old, new, 1)

def replace_span(text, start_anchor, end_anchor, new_block, label, include_end=False):
    i = text.find(start_anchor)
    assert i != -1, f"FAILED start anchor [{label}]: {start_anchor!r}"
    j = text.find(end_anchor, i + len(start_anchor))
    assert j != -1, f"FAILED end anchor [{label}]: {end_anchor!r}"
    if include_end:
        j += len(end_anchor)
    return text[:i] + new_block + text[j:]

# 1. Prepend south-kit and south-supers imports
src = 'import{populateSouthModels,loadSouthCharacter,buildMarinaStage,buildBusStandStage,buildDebateStudioStage,updateSouthStageHazards,upgradeSouthCrowd,updateSouthCrowd,triggerMemeOnAction,spawnOratorSoundwave,triggerKootaniAssist,updateKootaniAssist,updateCensorBossMechanic,onCensorBossGrabBreak,pushFanWarComment,triggerPaalAbhishekam,computeBoxOfficeVerdict,cleanupSouthBattle}from"./south-kit.js?v=20261129";\nimport{createSouthSuper}from"./south-supers.js?v=20261129";\nwindow.__local2P=!1;window.__selectedAssist=window.__selectedAssist||"sumo";window.__censorLock=null;window.__marinaWaveSlip=!1;window.__lastMatchStats=null;\n' + src

# 2. Disable Google Analytics external load in We()
src = replace_span(
    src,
    'function We(){if(!(typeof window>`u`||He)){',
    'He=e.gtag}',
    'function We(){if(!(typeof window>`u`||He)){He=()=>{};',
    'We GA disable',
    include_end=True,
)

# 3. Overhaul 3D Arenas: Marina Beach (Memorials & Lighthouse + 20s Wave), Koyambedu Bus Stand (Green Buses + Corner Auto Bounce), Arangam Debate Studio (Neon Circle + MIC MUTED! LEDs)
src = replace_exact(
    src,
    'qt={sansad:{name:`SANSAD BHAVAN`,subtitle:`Parliament at sunset`},jantar:{name:`JANTAR MANTAR`,subtitle:`Protest ground, New Delhi`},road:{name:`DESI SADAK`,subtitle:`Gali, thela aur traffic`}}',
    'qt={marina:{name:`MARINA BEACH`,subtitle:`Marina Lighthouse, Sundal Carts & 20s Ocean Wave`},jantar:{name:`KOYAMBEDU BUS STAND`,subtitle:`Green Govt Buses & Corner Auto-Rickshaw Bounce`},road:{name:`ARANGAM DEBATE STUDIO`,subtitle:`Neon Circular Floor & Giant MIC MUTED LED Screens`},sansad:{name:`MARINA BEACH`,subtitle:`Marina Lighthouse, Sundal Carts & 20s Ocean Wave`}}',
    'qt stages',
)

src = replace_exact(
    src,
    'Jt={sansad:{skyTop:1780314,skyMid:15232828,skyBottom:16762739,fog:15310950,fogNear:28,fogFar:75,ground:9071178,platformSide:9190174,sunColor:16766624,sunIntensity:2.6,sunPos:[-6,12,9],hemiSky:16769728,hemiGround:5913386,hemiIntensity:1.25,sunDisc:[-30,9,-80],sunDiscColor:16773572,exposure:1.05,floorRoughness:.62},jantar:{skyTop:3108804,skyMid:9683690,skyBottom:15916992,fog:14207922,fogNear:35,fogFar:110,ground:6130234,platformSide:11028282,sunColor:16773592,sunIntensity:2.8,sunPos:[7,16,10],hemiSky:14478335,hemiGround:7033398,hemiIntensity:1.3,sunDisc:[45,38,-90],sunDiscColor:16776168,exposure:.95,floorRoughness:.9},road:{skyTop:8364996,skyMid:14206882,skyBottom:15389606,fog:13481100,fogNear:22,fogFar:70,ground:7233873,platformSide:4144442,sunColor:16769712,sunIntensity:2.5,sunPos:[-8,14,9],hemiSky:15852228,hemiGround:5917240,hemiIntensity:1.3,sunDisc:[-40,30,-90],sunDiscColor:16773320,exposure:1,floorRoughness:.95}}',
    'Jt={sansad:{skyTop:1139386,skyMid:2988248,skyBottom:16756578,fog:14935011,fogNear:32,fogFar:95,ground:15255434,platformSide:12887662,sunColor:16768682,sunIntensity:2.7,sunPos:[8,13,-12],hemiSky:14086143,hemiGround:13414762,hemiIntensity:1.3,sunDisc:[22,10,-85],sunDiscColor:16770452,exposure:1.05,floorRoughness:.82},marina:{skyTop:1139386,skyMid:2988248,skyBottom:16756578,fog:14935011,fogNear:32,fogFar:95,ground:15255434,platformSide:12887662,sunColor:16768682,sunIntensity:2.7,sunPos:[8,13,-12],hemiSky:14086143,hemiGround:13414762,hemiIntensity:1.3,sunDisc:[22,10,-85],sunDiscColor:16770452,exposure:1.05,floorRoughness:.82},jantar:{skyTop:2643854,skyMid:9090264,skyBottom:16114884,fog:13748674,fogNear:34,fogFar:105,ground:5263448,platformSide:3618615,sunColor:16773592,sunIntensity:2.65,sunPos:[6,15,10],hemiSky:14478335,hemiGround:5263440,hemiIntensity:1.3,sunDisc:[40,36,-90],sunDiscColor:16776168,exposure:1,floorRoughness:.9},road:{skyTop:395826,skyMid:922922,skyBottom:2361662,fog:922922,fogNear:24,fogFar:80,ground:526878,platformSide:1118496,sunColor:11197183,sunIntensity:2.3,sunPos:[0,12,10],hemiSky:6920703,hemiGround:1707562,hemiIntensity:1.25,sunDisc:[0,50,-90],sunDiscColor:2282478,exposure:1.08,floorRoughness:.35}}',
    'Jt South Indian arena lighting themes',
)

# Floor $t(): traditional Tamil Pulli Kolam & terracotta Kavi border
new_kolam = '''function $t(){return Yt(1024,1024,e=>{e.fillStyle=`#e4d8be`,e.fillRect(0,0,1024,1024);e.strokeStyle=`#9a2f20`;e.lineWidth=32;e.strokeRect(24,24,976,976);e.strokeStyle=`#f9fafb`;e.lineWidth=6;for(let t=-2;t<=2;t++)for(let n=-2;n<=2;n++){if(Math.abs(t)+Math.abs(n)<=2){e.beginPath(),e.arc(512+t*80,512+n*80,34,0,Math.PI*2),e.stroke();e.beginPath(),e.arc(512+t*80,512+n*80,6,0,Math.PI*2),e.fillStyle=`#fffef5`,e.fill()}}e.strokeStyle=`#ffd23f`;e.lineWidth=8;for(let r of[110,235,340]){e.beginPath(),e.arc(512,512,r,0,Math.PI*2),e.stroke()}})}'''
src = replace_span(src, 'function $t(){', 'function en(){', new_kolam, '$t Tamil kolam floor')

# Arena flags nn(): Crimson/Black/Gold Tamil temple & Rising-Sun festival banner
src = replace_exact(
    src,
    'function nn(){return Yt(192,128,e=>{e.fillStyle=`#ff9933`,e.fillRect(0,0,192,43),e.fillStyle=`#ffffff`,e.fillRect(0,43,192,42),e.fillStyle=`#138808`,e.fillRect(0,85,192,43),Xt(e,96,64,17,`#000080`)})}',
    'function nn(){return Yt(192,128,e=>{e.fillStyle=`#18181b`,e.fillRect(0,0,192,64),e.fillStyle=`#dc2626`,e.fillRect(0,64,192,64),e.fillStyle=`#facc15`,e.beginPath(),e.arc(96,64,22,Math.PI,0),e.fill(),e.strokeStyle=`#facc15`,e.lineWidth=4,e.strokeRect(4,4,184,120)})}',
    'nn South arena flags',
)

# Fort St. George neoclassical white columns + Chennai Central red-brick tower
src = replace_exact(
    src,
    'buildSansad(e){let t=new O({color:14264186,roughness:.85}),n=new O({color:11763287,roughness:.9}),',
    'buildSansad(e){let t=new O({color:15987699,roughness:.82}),n=new O({color:14868962,roughness:.85}),',
    'Fort St. George white sandstone',
)
src = replace_exact(
    src,
    'let p=new O({color:13208674,roughness:.9}),m=new x;m.position.set(24,-.3,-46)',
    'let p=new O({color:11936806,roughness:.88}),m=new x;m.position.set(24,-.3,-46)',
    'Chennai Central red brick tower',
)

# Madurai Meenakshi signboard
src = replace_exact(src, 'e.fillText(`JANTAR MANTAR`,256,62)', 'e.fillText(`MADURAI MEENAKSHI`,256,62)', 'Madurai stage sign title')
src = replace_exact(src, 'e.fillText(`जंतर मंतर · NEW DELHI`,256,120)', 'e.fillText(`மதுரை · TAMIL NADU`,256,120)', 'Madurai stage sign sub')

# Chennai Yellow Auto body in Ot()
src = replace_exact(
    src,
    'function Ot(){let e=new x,t=Ct(3116858,.5,.2),n=Ct(16040960,.6),',
    'function Ot(){let e=new x,t=Ct(16435221,.5,.2),n=Ct(1579035,.6),',
    'Chennai yellow auto',
)

src = replace_exact(
    src,
    'i(this,`themeGroups`,{sansad:new x,jantar:new x,road:new x})',
    'i(this,`themeGroups`,{sansad:new x,jantar:new x,road:new x,marina:new x})',
    'sn themeGroups',
)
src = replace_exact(
    src,
    'this.group.add(this.themeGroups.sansad,this.themeGroups.jantar,this.themeGroups.road)',
    'this.group.add(this.themeGroups.sansad,this.themeGroups.jantar,this.themeGroups.road,this.themeGroups.marina)',
    'sn group add',
)
src = replace_exact(
    src,
    'this.floorTextures={sansad:$t(),jantar:en(),road:wt(Yt)}',
    'this.floorTextures={sansad:en(),jantar:wt(Yt),road:en(),marina:en()}',
    'sn floorTextures',
)
src = replace_exact(
    src,
    'this.buildSansad(this.themeGroups.sansad),this.buildJantarMantar(this.themeGroups.jantar),At(this.themeGroups.road)',
    'buildMarinaStage(this.themeGroups.sansad),buildMarinaStage(this.themeGroups.marina),buildBusStandStage(this.themeGroups.jantar),buildDebateStudioStage(this.themeGroups.road)',
    'sn buildStage South Indian 3D arenas',
)
src = replace_exact(
    src,
    'this.setStage(`sansad`)',
    'this.setStage(`marina`)',
    'sn default stage marina',
)
src = replace_exact(
    src,
    'Gp=`sansad`,Kp=[`sansad`,`jantar`,`road`]',
    'Gp=`marina`,Kp=[`marina`,`jantar`,`road`]',
    'Gp and Kp stages list',
)

# South crowd shirts + South crowd Veshti/Saree/Angavastram/Jasmine layers + brass Kaapi tumblers
src = replace_exact(
    src,
    'let h=[16750899,16777215,1280008,3054591,14688650,16765503,11022898,7031766],g=[9263675,11565650,13210736,7226668];',
    'let h=[16382457,16119285,14423100,1483594,16435252,186898,1579034,12131356],g=[8871746,10514756,12087888,6964522];',
    'South crowd color palette',
)
src = replace_exact(
    src,
    'this.group.add(this.crowd,this.crowdHeads);',
    'this.group.add(this.crowd,this.crowdHeads);upgradeSouthCrowd(this);',
    'Mount South crowd layers',
)
src = replace_exact(
    src,
    'this.crowd.instanceMatrix.needsUpdate=!0,this.crowdHeads.instanceMatrix.needsUpdate=!0,this.updatePlacards(e,t)',
    'this.crowd.instanceMatrix.needsUpdate=!0,this.crowdHeads.instanceMatrix.needsUpdate=!0,updateSouthCrowd(this,this.dummy),this.updatePlacards(e,t)',
    'Animate South crowd layers',
)
src = replace_exact(
    src,
    'this.samosas=new xe(new fe(.07,.11,3),new O({color:14263361,roughness:.7}),t)',
    'this.samosas=new xe(new D(.05,.042,.11,10),new O({color:13677636,roughness:.25,metalness:.7}),t)',
    'Replace samosas with Filter Kaapi tumblers',
)

# Kaapi Master white veshti + ochre shirt (disassociate from Delhi chaiwala silhouette)
src = replace_exact(
    src,
    'o=new O({color:a?16777215:1710620,map:a,roughness:.75}),s=ts(2764602,.85)',
    'o=new O({color:13989126,roughness:.75}),s=ts(16184558,.8)',
    'Kaapi Master white veshti outfit',
)

# 4. Crowd placards (an) — all 13 fighters
new_an = '''an=[{pool:`neutral`,text:`VANAKKAM!`,bg:`#ffffff`,fg:`#c0392b`},{pool:`neutral`,text:`VETRI!`,bg:`#ffd23f`,fg:`#1a237e`},{pool:`neutral`,text:`MASS!`,bg:`#ff9933`,fg:`#ffffff`},{pool:`neutral`,text:`NAARKALI!`,bg:`#138808`,fg:`#ffffff`},{pool:`modi`,text:`SURYA ANNA`,bg:`#e11d48`,fg:`#ffffff`},{pool:`modi`,text:`CYCLE RALLY!`,bg:`#111827`,fg:`#facc15`},{pool:`modi`,text:`RISING SUN`,bg:`#dc2626`,fg:`#fef08a`},{pool:`rahul`,text:`THALAPATHY`,bg:`#b91c1c`,fg:`#fef08a`},{pool:`rahul`,text:`WHISTLE PODU`,bg:`#ffffff`,fg:`#b91c1c`},{pool:`rahul`,text:`1000CR MASS!`,bg:`#7f1d1d`,fg:`#fde047`},{pool:`didi`,text:`IRON AMMA!`,bg:`#15803d`,fg:`#ffffff`},{pool:`didi`,text:`TWO LEAVES`,bg:`#ffffff`,fg:`#15803d`},{pool:`didi`,text:`FORT ST GEORGE`,bg:`#065f46`,fg:`#d1fae5`},{pool:`trump`,text:`THAGGEDHE LE`,bg:`#ea580c`,fg:`#ffffff`},{pool:`trump`,text:`SANDAL RAJU`,bg:`#ffffff`,fg:`#c2410c`},{pool:`trump`,text:`WILDFIRE!`,bg:`#7c2d12`,fg:`#fed7aa`},{pool:`yogi`,text:`LAL CAPTAIN`,bg:`#dc2626`,fg:`#ffffff`},{pool:`yogi`,text:`LAL SALAM!`,bg:`#ffffff`,fg:`#991b1b`},{pool:`yogi`,text:`SILVERLINE`,bg:`#7f1d1d`,fg:`#fecaca`},{pool:`nitin`,text:`BANDE SHIV`,bg:`#0284c7`,fg:`#ffffff`},{pool:`nitin`,text:`5 GUARANTEES`,bg:`#ffffff`,fg:`#0369a1`},{pool:`nitin`,text:`SILK BOARD`,bg:`#0369a1`,fg:`#e0f2fe`},{pool:`ravi`,text:`POWER STAR`,bg:`#dc2626`,fg:`#ffffff`},{pool:`ravi`,text:`OG KATANA!`,bg:`#ffffff`,fg:`#b91c1c`},{pool:`ravi`,text:`FIRE STORM!`,bg:`#1e293b`,fg:`#f87171`},{pool:`lalu`,text:`PULI VOICE`,bg:`#b91c1c`,fg:`#fde047`},{pool:`lalu`,text:`TIGER ROAR`,bg:`#facc15`,fg:`#7f1d1d`},{pool:`lalu`,text:`MIKE SET!`,bg:`#111827`,fg:`#fde047`},{pool:`mbapu`,text:`SELF RESPECT`,bg:`#18181b`,fg:`#facc15`},{pool:`mbapu`,text:`RATIONALISM`,bg:`#facc15`,fg:`#18181b`},{pool:`mbapu`,text:`THATHA REFORM`,bg:`#27272a`,fg:`#ffffff`},{pool:`amit`,text:`FILES IPS!`,bg:`#f97316`,fg:`#ffffff`},{pool:`amit`,text:`PRESS MEET`,bg:`#ffffff`,fg:`#ea580c`},{pool:`amit`,text:`CASE CLOSED!`,bg:`#1e293b`,fg:`#fb923c`},{pool:`dhruv`,text:`SQUAD BRO`,bg:`#06b6d4`,fg:`#082f49`},{pool:`dhruv`,text:`RED ARROWS!`,bg:`#ffffff`,fg:`#0e7490`},{pool:`dhruv`,text:`10M VIEWS!`,bg:`#082f49`,fg:`#22d3ee`},{pool:`nirmala`,text:`TAX MAAMI`,bg:`#9333ea`,fg:`#ffffff`},{pool:`nirmala`,text:`28% GST!`,bg:`#facc15`,fg:`#581c87`},{pool:`rangaraj`,text:`POINT-KU VAA`,bg:`#0284c7`,fg:`#ffffff`},{pool:`rangaraj`,text:`MIC MUTED!`,bg:`#dc2626`,fg:`#fef08a`}]'''
src = replace_span(src, 'an=[', '],on=', new_an[:-1], 'an crowd placards')

# 5. Pan-South 13-Fighter Roster N with 3 Combat Archetypes ('mass', 'orator', 'heavy') + Audio-Matched Intro/Win Dialogues
new_N = '''N={modi:{id:`modi`,style:`heavy`,name:`SURYA ANNA`,fullName:`Surya Anna (Dravidian Cartoon Parody)`,party:`Dravidian Sunset Front`,accent:`#e11d48`,headScale:1,look:{skin:12748377,skinShade:10907206,hair:1842204,hairStyle:`side-part`,beard:1842204,beardStyle:`none`,brows:1842204,stache:!0,topStyle:`veshti`,top:16382457,jacket:14423100,pants:16382457,shoes:2629150,glasses:!0,shoulders:1.06,belly:1.15,scale:1},walkFwd:2.32,walkBack:1.8,jumpV:7.6,jumpVx:2.5,damageMul:1,fightClips:!0,moveNames:{special1:`DRAVIDA PALM!`,special2:`RED-BLACK STRIKE!`,finisher:`CYCLE WHEELIE COMBO!`,sweep:`VESHTI SWEEP!`,uppercut:`FORT UPPERCUT!`,grab:`SUNRISE SLAM!`,roundhouse:`MGR SPIN ROUNDHOUSE!`},superName:`VIDIYAL CYCLE RALLY`,superDesc:`[HEAVYWEIGHT · K,K Super Armor] Rides into battle on his ECR bicycle & slams a Rising Sun cyclone.`,introLine:`Tamilnattu arasin mudhalamaicharaga...`,winLine:`Nermaiyaga seyven endrum urudhi mozhigiren!`,facePhoto:`faces/modi.webp?v=20261126`,dance:{label:`DAPPAANKUTHU!`,colors:[14753096,15790320,16435252]}},rahul:{id:`rahul`,style:`mass`,name:`THALAPATHY`,fullName:`Thalapathy Star (FDFS Hero Parody)`,party:`Thalapathy Welfare Wing`,accent:`#dc2626`,headScale:1,look:{skin:13802352,skinShade:11894874,hair:1841432,hairStyle:`side-part`,beard:5063232,beardStyle:`stubble-grey`,brows:2235162,topStyle:`shawl`,top:16382457,jacket:14423100,pants:4605515,shoes:2960691,shades:!0,glasses:!0,shoulders:1.08,belly:.92,scale:1.04},walkFwd:2.52,walkBack:1.95,jumpV:7.8,jumpVx:2.65,damageMul:.98,fightClips:!0,moveNames:{special1:`AUDIO LAUNCH PUNCH!`,special2:`KUTHU FLYING KICK!`,finisher:`FDFS MASS COMBO!`,sweep:`VERITHANAM SWEEP!`,uppercut:`THALAPATHY UPPERCUT!`,grab:`BOX OFFICE SLAM!`,roundhouse:`WHISTLE ROUNDHOUSE!`},superName:`LEO SLOW-MO & 1000CR`,superDesc:`[MASS HERO · J,J,K Slow-Mo Launch] Drops the Audio Launch golden mic & lands an FDFS slow-mo blitz.`,introLine:`What bro? It's very wrong bro!`,winLine:`Bloody Sweet!`,facePhoto:`faces/rahul.webp?v=20261126`,dance:{label:`VAATHI STEP!`,colors:[14425126,16435252,16777215]}},didi:{id:`didi`,style:`heavy`,name:`IRON AMMA`,fullName:`Puratchi Amma (Two-Leaf Parody)`,party:`Two-Leaf Fortress`,accent:`#16a34a`,headScale:.94,look:{skin:12880482,skinShade:11039052,hair:2762794,hairStyle:`bun`,beard:1907224,beardStyle:`none`,brows:2761760,topStyle:`sari`,top:1600088,jacket:15578672,pants:1600088,shoes:15921906,glasses:!1,shoulders:.94,belly:1.05,scale:.88},walkFwd:2.42,walkBack:1.86,jumpV:7.7,jumpVx:2.55,damageMul:1,fightClips:!0,moveNames:{special1:`AMMA CANTEEN SLAP!`,special2:`PALLU WHIP KICK!`,finisher:`FORTRESS COMBO!`,sweep:`POES GARDEN SWEEP!`,uppercut:`IRON UPPERCUT!`,grab:`CAPE SLAM!`,roundhouse:`MARINA ROUNDHOUSE!`},superName:`POES GARDEN THRONE`,superDesc:`[HEAVYWEIGHT · K,K Super Armor] Ascends on an emerald Lion Throne & drops the Two-Leaf gavel.`,introLine:`Unmaiyana makkal iyakkam!`,winLine:`Naan irukkindra varai, enakkup pinnalum!`,facePhoto:`faces/didi.webp?v=20261126`,modelHeight:.88,dance:{label:`AMMA SWAG!`,colors:[1483594,16777215,15578672]}},trump:{id:`trump`,style:`mass`,name:`SANDAL RAJU`,fullName:`Sandal Raju (Wildfire Syndicate Parody)`,party:`Red Sandal Syndicate`,accent:`#ea580c`,headScale:1,look:{skin:12814194,skinShade:10841432,hair:2169116,hairStyle:`side-part`,beard:2169116,beardStyle:`full`,brows:2169116,stache:!0,topStyle:`kurta-jacket`,top:14838820,jacket:1843760,pants:2434341,shoes:1118481,shades:!0,glasses:!0,shoulders:1.15,belly:1.18,scale:1.03},walkFwd:2.18,walkBack:1.68,jumpV:7.5,jumpVx:2.45,damageMul:1.05,fightClips:!0,moveNames:{special1:`SHOULDER TILT PUNCH!`,special2:`CHITTOOR KICK!`,finisher:`THAGGEDHE LE COMBO!`,sweep:`AXE SWEEP!`,uppercut:`WILDFIRE UPPERCUT!`,grab:`COLLAR GRAB SLAM!`,roundhouse:`PART-2 ROUNDHOUSE!`},superName:`THAGGEDHE LE AXE`,superDesc:`[MASS HERO · J,J,K Slow-Mo Launch] Strikes the chin-tilt pose & lands a Rapa Rapa dropkick!`,introLine:`Pushpa Pushparaj... Thaggedhe Le!`,winLine:`Pushpa ante flower-a? Fireuu!`,facePhoto:`faces/trump.webp?v=20261126`,modelHeight:1.03,dance:{label:`RAPA RAPA!`,colors:[15357964,16777215,1843760]}},yogi:{id:`yogi`,style:`heavy`,name:`LAL CAPTAIN`,fullName:`Lal Captain (Backwater Cadre Parody)`,party:`Malabar Red Cadre`,accent:`#b91c1c`,headScale:1,look:{skin:12618340,skinShade:10513996,hair:14869218,hairStyle:`swept`,beard:14869218,beardStyle:`none`,brows:9868950,stache:!0,topStyle:`veshti`,top:16382457,jacket:13114910,pants:16382457,shoes:1710618,glasses:!1,shoulders:1.08,belly:1.08,scale:.98},walkFwd:2.24,walkBack:1.74,jumpV:7.55,jumpVx:2.45,damageMul:1.03,fightClips:!0,moveNames:{special1:`LAL SALAM PUNCH!`,special2:`SILVERLINE KICK!`,finisher:`CADRE DISCIPLINE!`,sweep:`MUNDU SWEEP!`,uppercut:`KADAKKU UPPERCUT!`,grab:`COMRADE SLAM!`,roundhouse:`BACKWATER ROUNDHOUSE!`},superName:`KADAKKU PURATHU K-RAIL`,superDesc:`[HEAVYWEIGHT · K,K Super Armor] Blasts the SilverLine express with a Red Salute roundhouse!`,introLine:`Mukhyamantri kaserayil aakam!`,winLine:`Entho undakki kalayam ennanaanu vicharikunnathu!`,facePhoto:`faces/yogi.webp?v=20261126`,modelHeight:.97,dance:{label:`MUNDU SWAG!`,colors:[12131356,16777215,16763200]}},nitin:{id:`nitin`,style:`heavy`,name:`BANDE SHIV`,fullName:`Bande Shiv (Ring-Road Granite Parody)`,party:`Bengaluru Flyover Front`,accent:`#0284c7`,headScale:1,look:{skin:13144426,skinShade:11039312,hair:2433312,hairStyle:`side-part`,beard:2433312,beardStyle:`full`,brows:2038295,topStyle:`tshirt`,top:16382457,jacket:186898,pants:15921386,shoes:3811870,shades:!0,glasses:!0,shoulders:1.14,belly:1.22,scale:1.02},walkFwd:2.2,walkBack:1.7,jumpV:7.5,jumpVx:2.45,damageMul:1.04,fightClips:!0,moveNames:{special1:`ORR GRIDLOCK UPPER!`,special2:`TUNNEL ROAD KICK!`,finisher:`5-GUARANTEE COMBO!`,sweep:`POTHOLE SWEEP!`,uppercut:`SILK BOARD UPPERCUT!`,grab:`FLYOVER TAKEDOWN!`,roundhouse:`HEBBAL ROUNDHOUSE!`},superName:`SILK BOARD 999s & BANDE`,superDesc:`[HEAVYWEIGHT · K,K Super Armor] Traps the foe at Silk Board signal & drops a Kanakapura boulder!`,introLine:`One thing I would like to tell you — my birthday...`,winLine:`By profession I'm a businessman!`,facePhoto:`faces/nitin.webp?v=20261126`,dance:{label:`DOLLU BEAT!`,colors:[157895,16435252,14423100]}},ravi:{id:`ravi`,style:`mass`,name:`POWER STAR`,fullName:`Power Star (Storm Katana Parody)`,party:`Janasena Power Wing`,accent:`#dc2626`,headScale:1,look:{skin:12618340,skinShade:10513996,hair:1841689,hairStyle:`side-part`,beard:1841689,beardStyle:`stubble-grey`,brows:1709073,stache:!0,topStyle:`shawl`,top:16382457,jacket:14425126,pants:16184558,shoes:3811870,glasses:!0,shoulders:1.06,belly:1.02,scale:1},modelHeight:.96,walkFwd:2.46,walkBack:1.88,jumpV:7.8,jumpVx:2.6,damageMul:.99,fightClips:!0,danceIntro:!0,moveNames:{jab:`KAKINADA JAB!`,kick:`GABBAR SINGH KICK!`,finisher:`OG TSUNAMI COMBO!`,special1:`PAWAN PUNCH!`,special2:`POWER STAR KICK!`,sweep:`TOLLYWOOD SWEEP!`,uppercut:`TRENDING UPPERCUT!`,roundhouse:`ANDHRA ROUNDHOUSE!`,grab:`SENADHIPATHI SLAM!`},superName:`HUNGRY CHEETAH OG`,superDesc:`[MASS HERO · J,J,K Slow-Mo Launch] Draws the crimson OG Katana & detonates a Fire Storm!`,introLine:`Naaku konchem thikka undhi, kaani daniko lekka undhi!`,winLine:`Janamlo unta! Janam la unta!`,facePhoto:`faces/ravi.webp?v=20261126`,dance:{label:`KAKINADA STEP!`,colors:[14427686,16777215,16435252]}},lalu:{id:`lalu`,style:`orator`,name:`PULI VOICE`,fullName:`Puli Voice (Mike-Set Orator Parody)`,party:`Tiger Voice Brigade`,accent:`#eab308`,headScale:1,look:{skin:11565136,skinShade:9658430,hair:1841689,hairStyle:`swept`,beard:1841689,beardStyle:`none`,brows:1841689,stache:!0,topStyle:`veshti`,top:15219758,jacket:15380008,pants:15921386,shoes:3811870,glasses:!1,shoulders:1.1,belly:1.2,scale:1},modelHeight:.94,walkFwd:2.22,walkBack:1.72,jumpV:7.6,jumpVx:2.5,damageMul:1.02,fightClips:!0,moveNames:{jab:`THAMBI JAB!`,cross:`AAMAI CURRY CROSS!`,kick:`PULI KICK!`,uppercut:`STAGE MIC UPPERCUT!`,roundhouse:`VAIGAI ROUNDHOUSE!`,finisher:`NON-STOP SPEECH COMBO!`,lowJab:`PODIUM JAB!`,sweep:`EGMORE SWEEP!`,special1:`SIGNAL PALM!`,special2:`VAIGAI EXPRESS KICK!`,grab:`MIKE SET SLAM!`},superName:`MIKE SET PULI ROAR`,superDesc:`[ORATOR ZONER · J,J,J Soundwave Rings] Blasts 150dB sonic waves & unleashes the Golden Puli Tiger!`,introLine:`Moondru yaanaigal uyirizhundhirukkindranar!`,winLine:`1500 yaanai irundhuchu... ippa 650 thaan!`,facePhoto:`faces/lalu.webp?v=20261126`,dance:{label:`PARAI ATTAM!`,colors:[15381256,14423100,1118481]}},mbapu:{id:`mbapu`,style:`heavy`,name:`THATHA REFORM`,fullName:`Thatha Reform (Censor Boss Parody)`,party:`Election Censor Board`,accent:`#facc15`,headScale:1,look:{skin:12157018,skinShade:10118726,hair:16119285,hairStyle:`receding`,beard:16119285,beardStyle:`full-white`,brows:14474460,stache:!0,topStyle:`veshti`,top:1579034,jacket:1579034,pants:1579034,shoes:1579034,glasses:!0,shoulders:.98,belly:.95,scale:1},walkFwd:2.36,walkBack:1.85,jumpV:8,jumpVx:2.65,damageMul:1,fightClips:!0,moveNames:{jab:`RATIONAL JAB!`,cross:`LOGIC CROSS!`,kick:`WALKING STICK KICK!`,uppercut:`VAIKOM UPPERCUT!`,roundhouse:`SELF-RESPECT SPIN!`,finisher:`SUYAMARIYADHAI STORM!`,lowJab:`TORCH JAB!`,sweep:`EQUALITY SWEEP!`,special1:`QUESTION EVERYTHING!`,special2:`FLYING THATHA!`,grab:`GREAT REFORM SLAM!`},superName:`VAIKOM TORCH CHAKRA`,superDesc:`[HEAVYWEIGHT · K,K Super Armor] Boss emits a Red Card Aura locking buttons unless broken by Grab [I]!`,introLine:`Kadavul kitta undiyal vekkiringale — adhu Aathigam!`,winLine:`Aathma motcham nadakkum!`,facePhoto:`faces/mbapu.webp?v=20261126`,dance:{label:`THATHA SWAG!`,colors:[16435252,1579034,16777215]}},amit:{id:`amit`,style:`mass`,name:`FILES IPS`,fullName:`Files Inspector (Press-Meet Parody)`,party:`En Man Press Force`,accent:`#f97316`,headScale:1,look:{skin:12618340,skinShade:10513996,hair:1973276,hairStyle:`side-part`,beard:1973276,beardStyle:`full`,brows:1973276,topStyle:`kurta-jacket`,top:1973276,jacket:15895100,pants:2434341,shoes:1118481,shades:!0,glasses:!0,shoulders:1.12,belly:1.12,scale:1},modelHeight:.98,walkFwd:2.26,walkBack:1.74,jumpV:7.6,jumpVx:2.5,damageMul:1.01,fightClips:!0,moveNames:{jab:`BOOTH JAB!`,cross:`FILE THROW!`,kick:`YATRA KICK!`,uppercut:`PRESS MEET UPPER!`,roundhouse:`ARAVAKURICHI SPIN!`,finisher:`COUNTER-QUESTION COMBO!`,lowJab:`WATCH CLIP JAB!`,sweep:`MIC DROP SWEEP!`,special1:`ENNA SIR ITHU!`,special2:`KARNATAKA CADRE KICK!`,grab:`FILE LOCK SLAM!`},superName:`PRESS MEET & SECRET FILES`,superDesc:`[MASS HERO · J,J,K Slow-Mo Launch] Fends off 10 TV mics & drops Confidential Files!`,introLine:`Adhukkellam bayappadathinga! Naalaiku onnume illaina...`,winLine:`Ippo irukkira arasiyal thalaivar... vazha mudiyum?!`,facePhoto:`faces/amit.webp?v=20261126`,dance:{label:`LOTUS STEP!`,colors:[16347926,16777215,1973276]}},dhruv:{id:`dhruv`,style:`orator`,name:`SQUAD BRO`,fullName:`Squad Bro (Explainer Studio Parody)`,party:`Squad Bro YouTube`,accent:`#22d3ee`,headScale:1,look:{skin:13605490,skinShade:11566168,hair:1709330,hairStyle:`quiff`,beard:2761244,beardStyle:`none`,brows:2038295,topStyle:`tshirt`,top:2042436,jacket:2042436,pants:13153418,shoes:15921906,glasses:!1,shoulders:1.05,belly:.9,scale:1.04},modelHeight:1,walkFwd:2.48,walkBack:1.9,jumpV:7.8,jumpVx:2.6,damageMul:.98,fightClips:!0,moveNames:{jab:`HELLO SQUAD JAB!`,cross:`CONTROVERSY CROSS!`,kick:`SPONSORED KICK!`,uppercut:`CLICKBAIT UPPER!`,roundhouse:`ALGORITHM CRESCENT!`,finisher:`RATIO THE NARRATIVE!`,lowJab:`SKIP AD SHOT!`,sweep:`TIMELINE SWEEP!`,special1:`RED ARROW PUNCH!`,special2:`VIRAL SHORTS KICK!`,grab:`COPYRIGHT STRIKE!`},superName:`10M CLICKBAIT HOUNDS`,superDesc:`[ORATOR ZONER · J,J,J Soundwave Rings] Fires red clickbait arrows & Rajapalayam hounds!`,introLine:`Hello everyone, naan Madan Gowri! Hello my dear MG Squad!`,winLine:`Indha video motivational video-va illa inspirational-a...`,facePhoto:`faces/dhruv.webp?v=20261126`,dance:{label:`REEL STEP!`,colors:[2282478,2042436,16777215]}},nirmala:{id:`nirmala`,style:`heavy`,name:`TAX MAAMI`,fullName:`Tax Maami (28% GST Parody)`,party:`Caramel Popcorn Treasury`,accent:`#a855f7`,headScale:.95,look:{skin:12880482,skinShade:11039052,hair:2762794,hairStyle:`bun`,beard:1907224,beardStyle:`none`,brows:2761760,topStyle:`sari`,top:1600088,jacket:15578672,pants:1600088,shoes:15921906,glasses:!0,shoulders:.96,belly:1.05,scale:.93},walkFwd:2.3,walkBack:1.8,jumpV:7.6,jumpVx:2.5,damageMul:1.04,fightClips:!0,moveNames:{special1:`18% POPCORN SLAP!`,special2:`28% CARAMEL KICK!`,finisher:`BAHI-KHATA COMBO!`,sweep:`ONION PRICE SWEEP!`,uppercut:`GST SLAB UPPERCUT!`,grab:`AUDIT SLAM!`,roundhouse:`CESS ROUNDHOUSE!`},superName:`28% CARAMEL GST BLAST`,superDesc:`[HEAVYWEIGHT · K,K Super Armor] Playable full fighter! Drops a giant 28% Caramel Popcorn GST ledger!`,introLine:`Waise parivar se aati hoon jahan onion rakhte hi nahi!`,winLine:`Social media: popcorn ke upar bhi daal rahe hain tax!`,facePhoto:`faces/nirmala.webp?v=20261126`,modelHeight:.93,dance:{label:`GST SWAG!`,colors:[11032055,16435252,16777215]}},rangaraj:{id:`rangaraj`,style:`orator`,name:`RANGARAJ`,fullName:`Rangaraj Studio (Prime Time Host Parody)`,party:`Kelvikku Enna Bathil`,accent:`#38bdf8`,headScale:1,look:{skin:12618340,skinShade:10513996,hair:1973276,hairStyle:`side-part`,beard:1973276,beardStyle:`none`,brows:1973276,topStyle:`kurta-jacket`,top:1973276,jacket:15895100,pants:2434341,shoes:1118481,glasses:!0,shoulders:1.06,belly:1.04,scale:1},modelHeight:1,walkFwd:2.4,walkBack:1.88,jumpV:7.7,jumpVx:2.55,damageMul:1,fightClips:!0,moveNames:{jab:`POINT-KU JAB!`,cross:`KELVI CROSS!`,kick:`STUDIO KICK!`,uppercut:`MIC MUTE UPPER!`,roundhouse:`PRIME TIME SPIN!`,finisher:`DEBATE CHECKMATE!`,lowJab:`PANEL JAB!`,sweep:`TRP SWEEP!`,special1:`ENNA BATHIL?!`,special2:`LIVE BREAK KICK!`,grab:`PANEL LOCK SLAM!`},superName:`KELVIKKU ENNA BATHIL`,superDesc:`[ORATOR ZONER · J,J,J Soundwave Rings] Mutes the opponent's mic & blasts studio sonic rings!`,introLine:`Edhirkatchi thalaivarum pradhanarum pesittu iruppanga!`,winLine:`Irandaavadhu point vandhu — Bharat Pradhanam!`,facePhoto:`faces/rangaraj.webp?v=20261126`,dance:{label:`TRP STEP!`,colors:[3718648,16435252,16777215]}}}'''
src = replace_span(src, 'N={modi:', ',Ei=e=>', new_N, 'N 13-fighter Pan-South roster with styles')

# 6. Async 3D GLB model loaders Kc & Jc + 3D Studio Portraits (Bp) + natural fighting stance
src = replace_span(
    src,
    'async function Kc(t,n){',
    'function qc(e){',
    'async function Kc(t,n){await populateSouthModels(Vc,Oc,kc,N,at,t,n);return(n??e).filter(e=>e in Vc)}function qc(e){',
    'Kc async 3D GLB models',
    include_end=True,
)
src = replace_exact(
    src,
    'async function Jc(e,t,n){if(Vc[e])return n?.(100),!0;',
    'async function Jc(e,t,n){if(Vc[e])return n?.(100),!0;return await loadSouthCharacter(e,Vc,Oc,kc,N,at,t,n)}async function _unusedJc(e,t,n){',
    'Jc per-fighter on-demand character GLB loader',
)
src = replace_exact(
    src,
    'var $c=[{re:/^outfit_(top|bottom)$|^didi_(sari|blouse)$|^yogi_body$|^nitin_body$/,mode:`all`},{re:/^trump_body$/,mode:`blue`}];',
    'var $c=[{re:/^outfit_(top|bottom)$|^didi_(sari|blouse)$|^yogi_body$|^nitin_body$|^TOP|^BOT|^SCARF/,mode:`all`},{re:/^trump_body$/,mode:`blue`}];',
    '$c mirror-match Kit outfit material regex',
)
src = replace_exact(
    src,
    'for(let t of e)Zp[t]||(Zp[t]=`${Yp}faces/${t}.webp${Xp}`);',
    'for(let t of e){try{qc(t)&&(Zp[t]=Bp(t,null,1.02))}catch{}Zp[t]||(Zp[t]=`${Yp}faces/${t}.webp${Xp}`)}',
    'Render 3D studio portraits into Zp',
)
src = replace_exact(
    src,
    'setTransform(e,t,n,r,i=.22){',
    'setTransform(e,t,n,r,i=.28){',
    'dl natural 3D fighting stance angle',
)
src = replace_exact(
    src,
    'setFacePhoto(){}',
    'setFacePhoto(t){}',
    'dl setFacePhoto noop keeping UV head map',
)

# 7. Famous meme dialogues across ALL Sakthis, Grapples, Zo Taunts, GST Maami & Normal Hits
# 7a. Trigger action meme bubble + TTS audio + Mass Hero launch + matchStats inside jf.onHit
src = replace_exact(
    src,
    'onHit(e){e.defender===this.boss&&e.attacker.side===this.playerSide&&!e.blocked&&!this.budgetUsed&&(this.budget=Math.min(1,this.budget+e.damage/40)),',
    'onHit(e){!e.blocked&&!e.armor&&triggerMemeOnAction(this,e.attacker,e.moveId),e.attacker.side===this.playerSide&&!e.blocked&&(this.budget=Math.min(1,this.budget+e.damage/55)),e.attacker.side===this.playerSide&&!e.blocked&&(this.matchStats.maxCombo=Math.max(this.matchStats.maxCombo,e.defender.comboHits),[`kick`,`roundhouse`,`sweep`,`airKick`,`special2`,`finisher`].includes(e.moveId)?this.matchStats.kicks++:[`jab`,`cross`,`lowJab`,`uppercut`,`airPunch`,`special1`].includes(e.moveId)&&this.matchStats.punches++),(!e.blocked&&!e.armor&&e.attacker.char.style===`mass`&&([`finisher`,`special2`].includes(e.moveId)||e.attacker.char.id===`ravi`&&e.moveId===`roundhouse`))&&(this.timeScale=.25,this.slowMoTime=.3,this.massZoomTimer=.45,e.defender.vy=Math.max(e.defender.vy,9.8),e.defender.grounded=!1,(()=>{this.tmp.set(e.x,e.y+.55,.3);let p=this.ctx.toScreen(this.tmp);this.ctx.hud.popup(`🎬 SLOW-MO LAUNCH!`,p.x,p.y,`#facc15`)})()),',
    'onHit triggerMemeOnAction + Mass Hero launch + matchStats',
)

# 7b. Stalin Anna Sakthi (aa) speech + popup
src = replace_exact(
    src,
    '!this.impactDone&&o>=this.IMPACT&&(this.impactDone=!0,this.impactPoint.copy(u.root.position),this.landSuperHit(r.target.hp,c,4.6,8.5)',
    'o>=.35&&o<2.4&&!this._s1&&(this._s1=!0,r.speech(`caster`,`Ungalil Oruvan! Vidiyal Aatchi!`),r.popup(`DRAVIDIAN MODEL!`,this.v2.set(s.x,2.6,.3),`#e11d48`)),!this.impactDone&&o>=this.IMPACT&&(this.impactDone=!0,r.speech(`caster`,`Kalaiyrom, Kizhikkrom! Naadu Namadhe!`),this.impactPoint.copy(u.root.position),this.landSuperHit(r.target.hp,c,4.6,8.5)',
    'aa Stalin Sakthi meme speeches',
)

# 7c. Vijay Sakthi (Nl) speech
src = replace_exact(src, 't.fillText(`ALOO`,130,82)', 't.fillText(`SCRIPT`,125,82)', 'Nl SCRIPT')
src = replace_exact(src, 't.fillText(`SONA`,385,82)', 't.fillText(`1000CR`,382,82)', 'Nl 1000CR')
src = replace_exact(src, 'Ek aisi machine lagaunga...', 'En nenjil kudiyirukkum thozhargale!', 'Vijay Sakthi line 1')
src = replace_exact(src, 'Is side se aloo ghusega...', 'What bro, it\'s very wrong bro!', 'Vijay Sakthi line 2')
src = replace_exact(src, '...us side se SONA niklega!', '...1000CR Bloody Sweet! I am waiting!', 'Vijay Sakthi line 3')

# 7d. Jayalalithaa Sakthi (didi) speech + frog reaction + toss items
src = replace_exact(src, 'r.speech(`caster`,`Jadu hobe!`)', 'r.speech(`caster`,`Naan Ninaithal...!`)', 'Jayalalithaa super start')
src = replace_exact(src, 'r.speech(`caster`,`Jadu hoye gelo!`)', 'r.speech(`caster`,`Makkalal Naan, Makkalukkagave Naan!`)', 'Jayalalithaa super finish')
src = replace_exact(src, 'e.k>.7?`HUMBA HUMBA!`:`HUMBA!`', 'e.k>.7?`IRATTAI ILAI!`:`AMMA AATCHI!`', 'Jayalalithaa chant')
src = replace_exact(src, '[`CHAPPAL!`,Es(1.4)],[`ROSOGOLLA!`,o],[`BALLOT PAPER!`,s]', '[`MIXIE!`,Es(1.4)],[`LADDOO!`,o],[`LAPTOP!`,s]', 'Amma scheme toss items')
src = replace_exact(
    src,
    'f.char.id===`modi`?`Yeh kaun sa jadu hai?!`:f.char.id===`trump`?`Witch hunt! Total witch hunt!`:f.char.id===`yogi`?`Yeh kaisa jadu-tona hai?!`:`Bhai, yeh toh jadu hai!`',
    '{modi:`Idhu enna maayam Amma?!`,rahul:`What bro, frog bro?!`,trump:`Flower illa, thavalai aakittaanga!`,yogi:`Kadakku... ribbit?!`,nitin:`Operation failed!`,ravi:`Thavalai style lo kotteddama?!`,lalu:`Thambi! Frog curry-aa?!`,mbapu:`Science illa, frog magic!`,amit:`Enna sir frog ithu?!`,dhruv:`Hello MG Squad, frog-aayitten!`}[f.char.id]??`Amma magic!`',
    'Jayalalithaa frog reactions',
)

# 7e. Allu Arjun Pushpa Sakthi (trump) + Seized stamp
src = replace_exact(src, 'e.fillText(`EXECUTIVE ORDER`,192,78)', 'e.fillText(`SYNDICATE ORDER`,192,78)', 'mc SYNDICATE ORDER')
src = replace_exact(src, 'e.fillText(`TARIFF`,192,176)', 'e.fillText(`THAGGEDHE`,192,176)', 'mc THAGGEDHE')
src = replace_exact(src, 'e.fillText(`50%`,192,272)', 'e.fillText(`100%`,192,272)', 'mc 100%')
src = replace_exact(src, 'e.fillText(`TARIFFED`,256,132)', 'e.fillText(`SEIZED!`,256,132)', 'hc SEIZED')
src = replace_exact(src, '`TARIFF STAMP!`', '`THAGGEDHE LE!`', 'Pushpa stamp popup')
src = replace_exact(
    src,
    '!_&&g(.15)&&r.speech(`caster`,`Tariff time!`),!_&&g(o-.4)&&r.speech(`caster`,`Beautiful, isn\'t it?`),!_&&g(c+.2)&&r.speech(`caster`,`Fifty percent. Tremendous!`)',
    'g(.15)&&r.speech(`caster`,`Pushpa ante flower anukunnava?!`),g(o-.4)&&r.speech(`caster`,`FIREUUU! Wildfellow!`),g(c+.2)&&r.speech(`caster`,`Thaggedhe Le! Rapa Rapa!`)',
    'Allu Arjun Pushpa Sakthi lines',
)
src = replace_exact(
    src,
    '{modi:`Mitron... yeh kya aa raha hai?!`,rahul:`Bhai, yeh tariff nahi, tsunami hai!`,didi:`Ei! Eta ki tariff?!`,trump:`Fake tariff!`,yogi:`Tariff? Hum swadeshi hain!`,nitin:`Tariff se pehle toll toh bharo!`,mbapu:`Shanti apnao, tariff bhulao!`,ravi:`Tariff? Paisa toh mere peeche aata hai!`,lalu:`Tariff? Railway mein toh concession milta hai!`,amit:`Tariff? Iski bhi chronology hai!`,dhruv:`Tariff? Iska poora explainer banega!`}[m.char.id]',
    '{modi:`Idhu sandalwood tsunami-ya?!`,rahul:`Wrong bro! Pushpa crate bro!`,didi:`Ayyo red sandal storm!`,trump:`Wildfire bidda!`,yogi:`Kerala forest crates?!`,nitin:`Highway toll kattu Pushpa!`,mbapu:`Rationalise this stamp!`,ravi:`Pushpa vs Power Star!`,lalu:`Sandal wood cut pannaadhe!`,amit:`Customs file open aayiduchu!`,dhruv:`Hello MG Squad — crate-a paaru!`}[m.char.id]',
    'Pushpa target reactions',
)
src = replace_exact(src, '[`TARIFF!`,`TARIFF!!`,`50%!`,`HUGE!`,`TARIFF!`,`TREMENDOUS!`]', '[`THAGGEDHE!`,`FIREUU!`,`RAPA RAPA!`,`WILDFIRE!`,`1000 CR!`,`BIDDA!`]', 'Pushpa chants')

# 7f. Pinarayi Vijayan SilverLine Dozer Sakthi (yogi)
src = replace_exact(
    src,
    '!y&&v(.12)&&r.speech(`caster`,`Shaanti…`),v(o)&&r.speech(`caster`,`Site clear karo!`),v(s+.35)&&r.speech(`target`,{modi:`Arre, yeh bulldozer kiska hai?!`,rahul:`Bhai, bulldozer?! Seriously?!`,didi:`Ei! Bulldozer thamao!`,trump:`Is that a... bulldozer?!`,yogi:`Mera hi bulldozer?!`,nitin:`Bulldozer? Mere highway pe?!`,ravi:`Bulldozer? Shooting ka set mat todo!`,lalu:`Bulldozer? Patri pe mat chadhao!`,mbapu:`Bulldozer nahi, shanti chahiye!`,amit:`Bulldozer? Yeh chaal maine nahi chali!`,dhruv:`Bulldozer?! Doston, yeh dekho!`}[g.char.id])',
    'v(.12)&&r.speech(`caster`,`Chillu-nnu iru…`),v(o)&&r.speech(`caster`,`KADAKKU PURATHU!`),v(s+.35)&&r.speech(`target`,{modi:`Metro work-aa Captain?!`,rahul:`Dozer bro, very wrong bro!`,didi:`Stop that SilverLine dozer!`,trump:`Thaggedhe... bulldozer?!`,yogi:`LDF varum!`,nitin:`Naan flyover podren, neenga idikkireenga!`,ravi:`Set damage aithundhi!`,lalu:`Thambi, road-a thondadhe!`,mbapu:`Pagutharivu dozer!`,amit:`Permission vaanguneengala Captain?!`,dhruv:`Vlog break — SilverLine vandhuduchu!`}[g.char.id])',
    'Pinarayi Sakthi lines',
)
src = replace_exact(src, 'r.speech(`caster`,`Kaam chalu hai!`)', 'r.speech(`caster`,`LDF Varum, Ellam Sheri Aakum!`)', 'Pinarayi end line')

# 7g. D. K. Shivakumar Sakthi (nitin)
src = replace_exact(src, 'Gaddha-mukt Bharat... ek minute.', 'Kanakapura Bande... ondu nimisha!', 'DKS super line 1')
src = replace_exact(src, 'Arre arre... yeh gaddha kahan se aaya?!', 'Ayyo Silk Board pothole-aa idhu?!', 'DKS super hole 1')
src = replace_exact(src, 'Arey pothole!!', 'Outer Ring Road pit!!', 'DKS super hole 2')
src = replace_exact(src, 'Quality ka koi compromise nahi!', 'Operation Success — 5 Guarantees!', 'DKS walk away line')

# 7h. Pawan Kalyan Sakthi (ravi)
src = replace_exact(
    src,
    'r.clipTime()===null&&p(.1)&&r.speech(`caster`,`Money follows, brother!`),p(o+.9)&&r.speech(`caster`,`Main nahi bhaagta, yeh mere peeche aata hai!`)',
    'p(.1)&&r.speech(`caster`,`Cheppanu Brother — Seize the Ship!`),p(o+.9)&&r.speech(`caster`,`Naaku konchem thikka undhi, daniko lekka undhi!`)',
    'Pawan Kalyan Sakthi lines',
)
src = replace_exact(src, 'Arre! Main hil kyun nahi pa raha?!', 'Ayyo! Time freeze aayiducha?!', 'PK freeze target')
src = replace_exact(src, '`TIME IS MONEY!`', '`100% STRIKE RATE!`', 'PK dragon banner')

# 7i. Seeman Sakthi (lalu)
src = replace_exact(src, 'e.fillText(`संसद जंक्शन`,256,68)', 'e.fillText(`சென்னை எழும்பூர்`,256,68)', 'tu tamil station')
src = replace_exact(src, 'e.fillText(`SANSAD JN.`,256,148)', 'e.fillText(`EGMORE JN.`,256,148)', 'tu EGMORE JN')
src = replace_exact(src, 'e.fillText(`RAIL RAJA`,256,52)', 'e.fillText(`VAIGAI EXP`,256,52)', 'nu VAIGAI EXP')
src = replace_exact(src, 'Yatrigan kripya dhyan dein!', 'Thambi! Aamai Kari saapittiya?!', 'Seeman train line 1')
src = replace_exact(src, 'Chai garam, gaadi time pe!', 'Idhu Uruttu illa da — Vaigai Superfast Express!', 'Seeman train line 2')
src = replace_exact(src, 'Arre! Gaadi aa rahi hai?!', 'Ayyo! Vaigai Express varuthu!!', 'Seeman target reaction')
src = replace_exact(src, '`RAIL RAJA EXPRESS!`', '`AAMAI KARI EXPRESS!`', 'Seeman train popup 1')
src = replace_exact(src, '`NO WAITING LIST!`', '`ZERO URUTTU!`', 'Seeman train popup 2')

# 7j. Periyar Sakthi (mbapu)
src = replace_exact(src, 'n.speech(`caster`,`Manch khaali karo!`)', 'n.speech(`caster`,`Venkaya! Pagutharivu Thee!`)', 'Periyar super line')
src = replace_exact(src, '`MANCH CHHODO!`', '`PAGUTHARIVU CHAKRA!`', 'Periyar popup 1')
src = replace_exact(src, '`SHANTI CHAKKA!`', '`TORCH WHEEL!`', 'Periyar popup 2')
src = replace_exact(src, '`SHANTI TOOFAN!`', '`SUYAMARIYADHAI!`', 'Periyar popup 3')

# 7k. Annamalai Press Meet Sakthi (amit)
src = replace_exact(src, '$u=[`KYA`,`BAAT`,`KAR`,`RAHE HO`,`AAP?!`]', '$u=[`NAAN`,`SOLREN`,`KEKURINGALA`,`ENNA`,`SIR?!`]', '$u NAAN SOLREN')
src = replace_exact(src, 'n.speech(`caster`,`Shah-maat.`)', 'n.speech(`caster`,`En Mann En Makkal — Checkmate!`)', 'Annamalai checkmate speech')
src = replace_exact(src, 'word:`DHISHUM!`', 'word:`RAFALE!`', 'Annamalai word 1')
src = replace_exact(src, 'word:`THAPPAD!`', 'word:`SECRET FILE!`', 'Annamalai word 2')
src = replace_exact(src, 'word:`GHOONSA!`', 'word:`PRESS MEET!`', 'Annamalai word 3')
src = replace_exact(src, 'word:`DHAPP!`', 'word:`EXPOSED!`', 'Annamalai word 4')
src = replace_exact(src, '`DAL-BADAL!`', '`PRESS MEET!`', 'Annamalai popup 1')
src = replace_exact(src, '`JAAN DE DENGE!`', '`CASE FILED!`', 'Annamalai popup 2')
src = replace_exact(src, '`GHAR MANTRI! GHAR MANTRI!`', '`FILES IPS! FILES IPS!`', 'Annamalai fan chant')
src = replace_exact(src, '`DHAI GHAR KI CHAAL!`', '`WRITE IT DOWN!`', 'Annamalai knight charge')
src = replace_exact(src, '`SHAH-MAAT!`', '`CHECKMATE SIR!`', 'Annamalai checkmate popup')
src = replace_exact(src, 'Dekho, mere supporters aa gaye!', 'Dey! En aalunga varanga!', 'Annamalai target supporters')
src = replace_exact(src, 'Arre! Tum log toh mere the!', 'Dei! Neengellam en katchi da!', 'Annamalai target betrayal')
src = replace_exact(src, 'Arre, utaaro mujhe!', 'Ayyo, keela irakkunga da!', 'Annamalai target hoist')

# 7l. Squad Bro Sakthi (dhruv)
src = replace_exact(src, 'gd=[`KAL`,`PARSO`,`AGLE HAFTE`,`KABHI NAHI`]', 'gd=[`HELLO`,`SQUAD BRO`,`WIKIPEDIA`,`PART 2`]', 'gd Madan Gowri calendar')
src = replace_exact(src, 't.fillText(`TO-DO: LADAI`,128,23)', 't.fillText(`TODAY TOPIC`,128,23)', 'xd Madan Gowri card')
src = replace_exact(src, 't.fillText(`@factbhai`,36,e+890)', 't.fillText(`@squadbro_yt`,36,e+890)', 'Sd @squadbro_yt')
src = replace_exact(src, 't.fillText(`aaj mood nahi... #relax`,36,e+936)', 't.fillText(`wikipedia summary... #squadbro`,36,e+936)', 'Sd #squadbro')
src = replace_exact(src, '`MOOD: OFF`', '`THUMBNAIL: RED`', 'MG thumbnail popup')
src = replace_exact(src, '`KAL DEKHTE HAIN!`', '`HELLO SQUAD BRO!`', 'MG greeting popup')
src = replace_exact(src, '`REELS TIME!`', '`VIDEO TIME!`', 'MG reels popup')
src = replace_exact(src, '`DOOMSCROLLED!`', '`MG ROASTED!`', 'MG slam popup')
src = replace_exact(src, '`GERMAN SHEPHERD REELS!`', '`RAJAPALAYAM REELS!`', 'MG hounds popup')

# 7m. Nirmala GST Maami popup & immediate arrival alert
src = replace_exact(src, '`\"Sabka hissa banta hai, Bapu!\"`', '`\"Popcorn-ukkum 18% GST! Cream Bun-ukkum GST!\"`', 'Ca Nirmala popcorn quote')
src = replace_exact(
    src,
    'm(i)&&r.audio.stampSlam()',
    'm(i)&&(r.audio.stampSlam(),r.popup(`"Popcorn-ukkum 18% GST!"`,this.v1.set(this.nx,2.15,.6),`#facc15`))',
    'Ca Nirmala arrival popcorn popup',
)

# 7n. Zo Idle Taunts & Grapple Dialogues (ec, Ys, Xs, Ws, Ks, qs)
new_zo = 'Zo={modi:[`Morning walk mudinjathu, sandai-ku vaa!`,`Kalaiyrom, Kizhikkrom — ready-aa?`,`Dravidian Model defense paakuriya?`],rahul:[`What bro, still waiting bro! It\'s very wrong bro!`,`En nenjil kudiyirukkum opponent, attack pannu!`,`Kutty story sollalamaa?`],didi:[`Naan ninaithal one punch-la mudichiduven!`,`Fort St. George gate open-aa irukku, vaa!`,`Amma discipline teriyuma?`],trump:[`Flower nu nenachikitiya? Fire da!`,`Thaggedhe Le! Rapa Rapa!`,`Part 3 shooting poguma, illa adippiya?`],yogi:[`Kadakku purathu — step forward!`,`Chillu-nnu iru, aprom fight pannu!`,`Lal Salam! Red flag paathiya?`],nitin:[`Silk Board signal-la maatikitiya?`,`Kanakapura Bande waiting here, banni!`,`5 Guarantees-la punch free! Guarantee!`],ravi:[`Cheppanu brother! Step munde vey!`,`Seize the Ship! Slow-motion vendam!`,`Naaku thikka lesindhi, ready avvu!`],lalu:[`Thambi! Aamai kari saapittiya illaiya?!`,`Vaigai Express miss aagidum, vaa thambi!`,`Idhu uruttu illa, history! Stage-ku vaa!`],amit:[`Naan solren kekuringala?! Chronology paaru!`,`Rafale watch timer odudhu, seekiram vaa!`,`DMK Files open pannatta?`],dhruv:[`Hello Squad Bro! Opponent offline pola!`,`Wikipedia tab open panni wait panren!`,`Like, share, adichu kaattu!`],mbapu:[`Vengayam! அறிவோடு சிந்தி, அப்புறம் அடி!`,`Question blind hype, then throw a punch!`,`Suyamariyadhai never stalls!`]}'
src = replace_span(src, 'Zo={modi:', ';function Qo(', new_zo + ';function Qo(', 'Zo South taunts', include_end=True)

src = replace_exact(src, '`Gale milo, mitron!`', '`Ungalil Oruvan Hug!`', 'Modi hug grapple')
src = replace_exact(src, '`Wrist lock!`', '`Audio Launch Lock!`', 'Wrist lock grapple')
src = replace_exact(src, '`Ei! Shono!`', '`Naan Ninaithal!`', 'Didi slap grapple')
src = replace_exact(src, '[`THAPPAD!`,`CHATAAK!`,`THAPPAD!`]', '[`AMMA SLAP!`,`PADAYATRA!`,`ARAI!`]', 'Didi slap popups')
src = replace_exact(src, '`Great to see you!`', '`Wildfire Handshake!`', 'Allu Arjun handshake')
src = replace_exact(src, 'start:`Great Patki!`,first:`PATKI!`,next:`PHIR SE!`,last:`GREAT PATKI!`', 'start:`Vengayam! Pagutharivu!`,first:`LOGIC!`,next:`EQUALITY!`,last:`REFORM SLAM!`', 'Periyar grapple')
src = replace_exact(src, 'start:`Dhobi pachhad!`,first:`DHOBI PACHHAD!`,next:`DHOBI PACHHAD!`,last:`DHOBI PACHHAD!`', 'start:`Thambi Aamai Kari!`,first:`URUTTU!`,next:`AAMAI KARI!`,last:`MIKE SET SLAM!`', 'Seeman grapple')
src = replace_exact(
    src,
    'ec={rahul:{pair:`shackle`,rate:1.05,release:3.35,end:3.75,start:`Aikido, bhai!`,ouch:`Aah, haath!`,beats:[{at:1.75,word:`TWIST!`,power:.3},{at:2.7,word:`KHATA-KHAT!`,power:.7},{at:3.3,word:`AIKIDO FATAFAT!`,power:1}]},yogi:{pair:`slammer`,rate:1.25,release:6,end:6.3,start:`Bulldozer chalega!`,ouch:`Arre, utaro mujhe!`,beats:[{at:4.6,word:`UTHA!`,power:.3},{at:5.4,word:`PALAT!`,power:.4},{at:5.95,word:`BULLDOZER SLAM!`,power:1}]},nitin:{pair:`takedown`,rate:1,release:1.6,end:2.6,start:`Road roller aa raha hai!`,ouch:`Arre, rukiye!`,beats:[{at:.85,word:`TOLL FREE!`,power:.3},{at:1.55,word:`HIGHWAY TAKEDOWN!`,power:1}]},ravi:{pair:`upper`,rate:.75,release:2,end:2.4,start:`Dekh, hero ki entry!`,ouch:`Nahi, hero nahi!`,beats:[{at:1.3,word:`DHISHOOM!`,power:.7},{at:1.98,word:`FILMY UPPERCUT!`,power:1}]},amit:{pair:`takedown`,rate:1,release:1.6,end:2.6,start:`Ghera daal do!`,ouch:`Arre, yeh kaisa ghera?!`,beats:[{at:.85,word:`GHERA!`,power:.3},{at:1.55,word:`Z-PLUS TAKEDOWN!`,power:1}]},dhruv:{pair:`shackle`,rate:1.05,release:3.35,end:3.75,start:`Ruko, pehle source batao!`,ouch:`Aah, mera haath!`,beats:[{at:1.75,word:`SOURCE?!`,power:.3},{at:2.7,word:`FACT #1!`,power:.7},{at:3.3,word:`FACT-CHECK LOCK!`,power:1}]}}',
    'ec={rahul:{pair:`shackle`,rate:1.05,release:3.35,end:3.75,start:`What bro! Very wrong bro!`,ouch:`Ayyo Thalapathy!`,beats:[{at:1.75,word:`VERITHANAM!`,power:.3},{at:2.7,word:`BLOODY SWEET!`,power:.7},{at:3.3,word:`BOX OFFICE SLAM!`,power:1}]},yogi:{pair:`slammer`,rate:1.25,release:6,end:6.3,start:`Kadakku purathu!`,ouch:`Ayyo Captain!`,beats:[{at:4.6,word:`LAL SALAM!`,power:.3},{at:5.4,word:`SILVERLINE!`,power:.4},{at:5.95,word:`COMRADE SLAM!`,power:1}]},nitin:{pair:`takedown`,rate:1,release:1.6,end:2.6,start:`Resort bus-ge hattu!`,ouch:`Ayyo Silk Board!`,beats:[{at:.85,word:`BANDE!`,power:.3},{at:1.55,word:`FLYOVER TAKEDOWN!`,power:1}]},ravi:{pair:`upper`,rate:.75,release:2,end:2.4,start:`Seize the Ship!`,ouch:`Ayyo Power Star!`,beats:[{at:1.3,word:`CHEPPANU BRO!`,power:.7},{at:1.98,word:`OG UPPERCUT!`,power:1}]},amit:{pair:`takedown`,rate:1,release:1.6,end:2.6,start:`Naan solren kekuringala?!`,ouch:`Enna sir file-a?!`,beats:[{at:.85,word:`FILE #1!`,power:.3},{at:1.55,word:`PRESS MEET LOCK!`,power:1}]},dhruv:{pair:`shackle`,rate:1.05,release:3.35,end:3.75,start:`Hello MG Squad! Source idho!`,ouch:`Aah thumbnail!`,beats:[{at:1.75,word:`WIKIPEDIA!`,power:.3},{at:2.7,word:`10M VIEWS!`,power:.7},{at:3.3,word:`COPYRIGHT STRIKE!`,power:1}]},nirmala:{pair:`takedown`,rate:1,release:1.6,end:2.6,start:`18% Popcorn Audit!`,ouch:`Ayyo tax slab!`,beats:[{at:.85,word:`18% GST!`,power:.3},{at:1.55,word:`28% CARAMEL SLAM!`,power:1}]},rangaraj:{pair:`shackle`,rate:1.05,release:3.35,end:3.75,start:`Kelvikku enna bathil?!`,ouch:`Mic muted!`,beats:[{at:1.75,word:`POINT-KU VAA!`,power:.3},{at:2.7,word:`MIC MUTED!`,power:.7},{at:3.3,word:`DEBATE LOCK!`,power:1}]}}',
    'ec grapples (13 fighters)',
)

# 7o. Initial ticker line in Ff
src = replace_exact(
    src,
    'this.pushTicker(`SATIRE LIVE: Sansad Showdown — the fight nobody demanded`)',
    'this.pushTicker(`ROHINI FDFS LIVE: Dakshin Showdown — First Day First Show!`)',
    'Ff initial ticker',
)

# 8. NewsDesk & Newspaper & Taunts & Tea Kadai Vendor (13 characters)
new_news = '''Ao={godi:{name:`RANGARAJ STUDIO`,channel:`SUDU SORU TV`},troll:{name:`ADMIN PULLINGO`,channel:`MEME FACTORY`}};function jo(e,t){return e===`modi`||t===`rahul`?{godi:e,troll:t}:t===`modi`||e===`rahul`?{godi:t,troll:e}:{godi:e,troll:t}}var Mo={godi:`modi`,troll:`rahul`};function No(e,t){return Mo=jo(e,t),Mo}var Po={modi:`SURYA ANNA`,rahul:`THALAPATHY`,didi:`IRON AMMA`,trump:`SANDAL RAJU`,yogi:`LAL CAPTAIN`,nitin:`BANDE SHIV`,mbapu:`THATHA REFORM`,ravi:`POWER STAR`,lalu:`PULI VOICE`,amit:`FILES IPS`,dhruv:`SQUAD BRO`,nirmala:`TAX MAAMI`,rangaraj:`RANGARAJ`},Fo={modi:`Surya Anna`,rahul:`Thalapathy`,didi:`Iron Amma`,trump:`Sandal Raju`,yogi:`Lal Captain`,nitin:`Bande Shiv`,mbapu:`Thatha`,ravi:`Power Star`,lalu:`Puli Voice`,amit:`Files IPS`,dhruv:`Squad Bro`,nirmala:`Tax Maami`,rangaraj:`Rangaraj`},Io=(e,t)=>e[Math.min(e.length-1,Math.floor(t()*e.length))],Lo=(e,t)=>e.replace(/\\{(\\w+)\\}/g,(e,n)=>t[n]??``),Ro=e=>Mo.godi===e?`godi`:`troll`,zo=e=>e===`godi`?`troll`:`godi`,Bo=e=>Mo.godi===e?Mo.troll:Mo.godi;function Vo(e,t,n,r,i){let a={ticker:r,priority:i};return a[e]=t,a[zo(e)]=n,a}var Ho={godi:[`PRIME TIME SPECIAL! {M} — history created!`,`Breaking studio! {AN} strikes with {M}!`,`Panel agrees: greatest {M} in South arena!`,`Opposition stunned silent!`,`Marina crowd is ROARING!`,`Full force! {D} has zero answers!`],troll:[`#{M} trending No. 1 across TN, KL, KA, AP!`,`Direct FDFS theater celebration impact!`,`{AN} dropped a verified meme hit!`,`Clip that! Reel going 10M views!`,`{D} got ratio'd in 4K Ultra HD!`,`Bro unloaded a mass {M} fr fr!`] },Uo={godi:[`Fake narrative! Imported editing!`,`{DN} was only checking studio mic!`,`Slow-mo replay clearly shows zero touch!`,`Sudu Soru TV demands judicial probe on {M}!`,`Strategic tactical pause. Watch till 9 PM!`,`Chronology check... {DN} planned that dodge!`],troll:[`Paid PR clip! {DN} barely felt it!`,`Admin Pullingo confirms: recycled cinema stunt!`,`Audio launch hype exceeded actual damage!`,`{DN} was just stretching for Bajji break!`,`Fact-check pending in pinned comment!`,`Bro replied with a WhatsApp status 💀`] },Wo=[`FLASH: {A}'s {M} lands — box office analysts stunned!`,`SENATE INDEX {DIR} {N} pts after {A}'s {M}`,`{D} calls urgent all-party Filter Kaapi meeting`,`Walkout staged at Valluvar Kottam over {M}`,`South Film Twitter splits into 4 factions over {M}`,`7 anchors shouting simultaneously over {M}`,`Official clarification coming after interval block.`],Go=[`Weather: 100% humidity & sudden Kuthu storms on Marina Beach`,`Silk Board traffic remains paused to watch this match`,`Cricket fans chanting from Napier Bridge arches`,`Free Mysore Pak distributed near Valluvar Kottam`,`Exit polls give 110% vote share to both fighters`,`Tea Kadai master reports record Filter Kaapi sales`,`Temple cow enters Fort St. George — traffic police salute`,`Breaking: Nothing happened yet, stay tuned after ads`,`WhatsApp forwards graduate with Honours in Fight Analysis`,`Reminder: Pan-South fictional cartoon satire. All in good fun!`];function Ko(e){let t=35+Math.floor(e()*40),n=35+Math.floor(e()*40),r=Math.floor(e()*30);return`EXIT POLL: ${Po[Mo.godi]} ${t}% · ${Po[Mo.troll]} ${n}% · OTHERS ${r}% · TOTAL ${t+n+r}% · Error margin: ±100%`}function qo(e,t=Math.random){switch(e.kind){case`roundStart`:return{godi:e.final?`FINAL ROUND! Four states watching live!`:`Round ${e.round}! ${Fo[Mo.godi]} steps to the podium!`,troll:e.final?`Final round macha! Popcorn & Bajji ready!`:`Round ${e.round}! ${Fo[Mo.troll]} ratio check!`,ticker:Ko(t),priority:!0};case`hit`:{let n={A:Po[e.attacker],D:Po[Bo(e.attacker)],AN:Fo[e.attacker],DN:Fo[Bo(e.attacker)],M:e.move.replace(/!$/,``),DIR:t()<.5?`surges`:`drops`,N:String(100+Math.floor(t()*900))},r=Ro(e.attacker),i=e.knockdown||t()<.35?Lo(Io(Wo,t),n):void 0;return Vo(r,Lo(Io(Ho[r],t),n),Lo(Io(Uo[zo(r)],t),n),i,e.knockdown)}case`block`:return Vo(Ro(Bo(e.attacker)),Io([`BLOCKED! Granite Kanchipuram wall!`,`Soundproof studio glass block!`,`Not today macha — BLOCKED!`],t),void 0,void 0,!1);case`super`:{let t=Ro(e.caster),n=Jo[e.caster]??Jo.modi;return Vo(t,n.hype,n.spin,`BREAKING: ${e.superName} unleashed! ${n.ticker}`,!0)}case`ko`:{if(e.timeUp||!e.winner)return{godi:`Time up! ${Fo[Mo.godi]} claims moral mandate!`,troll:`Time up! Comments section declares draw!`,ticker:`TIME UP: Both sides celebrate with Mysore Pak & laddoos`,priority:!0};let t=Ro(e.winner);return Vo(t,{godi:`SOZHI MUDINJATHU! Clean sweep!`,troll:`K.O.! Pack up the flex banners!`}[t],{godi:`EVMs & lights blamed! Recount now!`,troll:`Scripted referee! Part 2 coming!`}[zo(t)],`BREAKING: ${Po[e.winner]} wins by K.O.! Emergency press meet called!`,!0)}case`roundWin`:return{ticker:e.perfect?`PERFECT ROUND for ${Po[e.winner]}! Zero HP lost!`:`${Po[e.winner]} wins the round! Filter Kaapi poured outside!`,priority:!0};case`cow`:return{godi:`Temple cow on stage! Match paused with respect!`,troll:`Cow has better footwork than half the roster ngl`,ticker:`BREAKING: Sacred cow strolls across Marina ring!`,priority:!0};case`cowGone`:return{godi:`Cow leaves the stage! Debate resumes!`,troll:`Cow exited left. Back to sandai!`,priority:!0};case`chai`:return Vo(Ro(e.kicker),`Kaapi tumbler kicked! GST added to replacement!`,`${Po[e.kicker]} owes the Tea Master ₹10!`,void 0,!1);case`bored`:return{godi:`Standoff at Marina! Speak into the mic!`,troll:`Zero action for 5 seconds — audience scrolling reels`,ticker:void 0,priority:!1};case`comeback`:{let t=Ro(e.leader);return Vo(t,{godi:`Comeback! ${Po[e.leader]} wave sweeps the arena!`,troll:`Comeback arc loading... ${Fo[e.leader]} mass interval block!`}[t],void 0,void 0,!1)}}}var Jo={modi:{hype:`VIDIYAL CYCLE RALLY! Sunburst over Marina!`,spin:`Rode an ECR morning cycle straight into a ring KO 💀`,ticker:`Rohini FDFS fans go wild`},rahul:{hype:`LEO SLOW-MO & 1000CR! Box office record shattered!`,spin:`Froze time with coffee cups and audio-launch hype 💀`,ticker:`Pan-India trade trackers revise FDFS numbers`},didi:{hype:`POES GARDEN THRONE! Lion Chair drop!`,spin:`Rained tiffins, laptops and two-leaf justice!! 💀`,ticker:`Emerald Lion Throne spotted at Marina Arena`},trump:{hype:`THAGGEDHE LE AXE! Red Sandal storm unleashed!`,spin:`Stamped THAGGEDHE LE across the opponent's ribs 💀`,ticker:`Seshachalam timber rates spike 100%`},yogi:{hype:`KADAKKU PURATHU K-RAIL! SilverLine blitz!`,spin:`Parked an express K-Rail train straight on stage 💀`,ticker:`SilverLine route detours right through the ring`},nitin:{hype:`SILK BOARD 999s & BANDE! 5 guarantees ignited!`,spin:`Dropped a Resort Volvo and Kanakapura granite boulder 💀`,ticker:`Outer Ring Road commuters cheer from gridlock`},ravi:{hype:`HUNGRY CHEETAH OG! Crimson Katana Fire Storm!`,spin:`Pulled an anime katana slash in bullet-time 💀`,ticker:`Kakinada fans burst crackers outside studio`},lalu:{hype:`MIKE SET PULI ROAR! Golden Tiger unleashed!`,spin:`Horn speakers shattered the sound barrier 💀`,ticker:`Special Express mic setup installed on stage`},amit:{hype:`PRESS MEET & SECRET FILES! ENNA SIR CHECKMATE!`,spin:`Tough questions turned into flying dossier stacks 💀`,ticker:`Journalists dodge flying classified folders`},dhruv:{hype:`10M CLICKBAIT HOUNDS! 1M likes in 3 seconds!`,spin:`Outsourced combat to glowing red arrows & hounds 💀`,ticker:`Thumbnail with 3 red arrows breaks server`},mbapu:{hype:`VAIKOM TORCH CHAKRA! Rationalist gale!`,spin:`Shattered dogma chains right inside the ring 💀`,ticker:`Rationalism Index hits all-time peak`},nirmala:{hype:`28% CARAMEL GST BLAST! Bahi-Khata vasool!`,spin:`Taxed popcorn, cream buns, and the opponent's Gethu 💀`,ticker:`GST Council raises combo tax to 28%`},rangaraj:{hype:`KELVIKKU ENNA BATHIL! Prime time stun-lock!`,spin:`Muted opponent's studio mic live on air 💀`,ticker:`Arangam TRP hits 99.9%`}},Yo={modi:[`"Wait for the next 5-year manifesto." — Sunset Camp`,`"Cinema guild conspired with lighting crew." — Sunset Camp`,`"We demand a Marina Beach recount!" — Sunset Camp`],rahul:[`"Censor board cut my third act punch!" — Welfare Wing`,`"Waiting for pan-India OTT verdict." — Welfare Wing`,`"Audio launch crowd would've been louder." — Welfare Wing`],didi:[`"Fort gate was locked from inside." — Two-Leaf Camp`,`"Unfair! Ring bell rang early." — Two-Leaf Camp`,`"Next budget gives two extra paddles!" — Two-Leaf Camp`],trump:[`"Flower nu nenachikitiya? Wait for Part 3!" — Syndicate Camp`,`"Sandalwood customs delayed my crate!" — Syndicate Camp`,`"Ref wasn't even following dialogue!" — Syndicate Camp`],yogi:[`"This was a tactical harthal!" — Red Cadre`,`"SilverLine DPR still under review." — Red Cadre`,`"We boycott the scoreboard!" — Red Cadre`],nitin:[`"Stuck at Silk Board signal for 4 hours." — Flyover Camp`,`"White-topping work started mid-match!" — Flyover Camp`,`"Fifth guarantee covers rematch fees." — Flyover Camp`],ravi:[`"Interval block — second half coming!" — Power Wing`,`"Dubbing artist arrived late." — Power Wing`,`"Next dialogue will clear the boundary." — Power Wing`],lalu:[`"They changed the mic frequency mid-speech!" — Tiger Brigade`,`"Historical evidence in next 4-hour rally!" — Tiger Brigade`,`"Platform signal was amber!" — Tiger Brigade`],amit:[`"Enna sir, out-of-syllabus punches!" — Press Force`,`"White paper will be released on Tuesday." — Press Force`,`"Next press meet settles this!" — Press Force`],dhruv:[`"Algorithm demonetized my uppercut!" — Squad Camp`,`"Wait for Part 2 Expose tomorrow!" — Squad Camp`,`"Thumbnail CTR betrayed us!" — Squad Camp`],mbapu:[`"Censor Red Card expired too soon!" — Election Board`,`"Study the syllabus and return next round!" — Self-Respect Camp`,`"Model Code of Conduct applies next match." — Election Board`],nirmala:[`"Caramel popcorn tax slab was miscalculated!" — Treasury Camp`,`"Onion prices not included in this combo!" — Treasury Camp`,`"18% GST surcharge pending!" — Treasury Camp`],rangaraj:[`"They muted my mic during rebuttal!" — Studio Panel`,`"Answer my question first — Point-ku vaanga!" — Studio Panel`,`"Break after this!" — Studio Panel`]};function Xo(e,t,n,r=Math.random){let i=Math.max(...n),a=Math.min(...n),o=i-a>=2;return{masthead:Io([`ROHINI FDFS BOX OFFICE RECEIPT`,`TEA KADAI BLOCKBUSTER POSTER`,`TASMAC FLEX BANNER TRACKER`,`SOUTH CINEMA 1000CR LEDGER`],r),headline:o?{modi:`SURYA ANNA SMASHES BOX OFFICE RECORD!`,rahul:`THALAPATHY HITS ₹1000 CRORE CLUB!`,didi:`IRON AMMA STORMS ROHINI SCREEN 1!`,trump:`SANDAL RAJU RULES ALL INDIA FDFS!`,yogi:`LAL CAPTAIN SHATTERS OVERSEAS RECORDS!`,nitin:`BANDE SHIV PAVED OVER BOX OFFICE!`,mbapu:`CENSOR BOARD THATHA CLEARS ALL CUTS!`,ravi:`POWER STAR UNLEASHES DAY-1 TSUNAMI!`,lalu:`PULI VOICE ROARS HOUSEFULL SHOWS!`,amit:`FILES IPS CLOSES EVERY CASE DAY 1!`,dhruv:`SQUAD BRO TRENDS #1 WORLDWIDE!`,nirmala:`TAX MAAMI COLLECTS 28% GST RECORD!`,rangaraj:`RANGARAJ STUDIO TOPS TRP CHARTS!`}[e]:{modi:`SURYA ANNA CLINCHES CLIMAX SHOW!`,rahul:`THALAPATHY WINS LAST-REEL BLOCKBUSTER!`,didi:`IRON AMMA HOLDS HOUSEFULL FORTRESS!`,trump:`SANDAL RAJU REFUSES TO BOW!`,yogi:`LAL CAPTAIN EDGES PHOTO FINISH!`,nitin:`BANDE SHIV CLEARS SILK BOARD IN CLIMAX!`,mbapu:`THATHA REFORM PREVAILS BY RED CARD!`,ravi:`POWER STAR STEALS FINAL REEL!`,lalu:`PULI VOICE WINS CLIMAX SPEECH!`,amit:`FILES IPS WINS BY ONE PRESS QUESTION!`,dhruv:`SQUAD BRO EXPLAINS THE WIN IN 10 MINS!`,nirmala:`TAX MAAMI AUDITS THE FINAL ROUND!`,rangaraj:`RANGARAJ WINS IN PRIME TIME FINALE!`}[e],sub:o?`SUPER HIT ${i}–${a} · Flex banners printed`:`NAIL-BITER ${i}–${a} · Recount at Tea Kadai`,excuse:Io(Yo[t]??Yo.modi,r)}}'''

src = replace_span(src, 'Ao={godi:', 'var Zo={modi:', new_news + 'var Zo={modi:', 'Ao..Xo news & box office headlines', include_end=True)
src = replace_exact(src, '$o=[`Chai! Chai!`,`Garam chai!`,`Cutting chai, ₹10!`,`Chai le lo, chai!`]', '$o=[`Filter Kaapi!`,`Degree Kaapi!`,`Suda Bajji, ₹10!`,`Kaapi! Kaapi!`]', '$o vendor lines')
src = replace_exact(src, 'es=[`Arre! Mera cup!`,`Oye! Chai gira di!`,`Paise kaun dega?!`]', 'es=[`Ayyo! En Kaapi!`,`Yov! Glass pochu!`,`Kaasu yaaru kuduppa?!`]', 'es vendor break lines')
src = replace_exact(src, '`+10 SOAN PAPDI!`', '`+10 MYSORE PAK!`', 'pickup mysore pak')
src = replace_exact(src, 't.fillText(`SOAN PAPDI`,128,66)', 't.fillText(`MYSORE PAK`,128,66)', 'qa MYSORE PAK box texture')
src = replace_exact(src, 'this.ctx.hud.speech(`Lo ji, soan papdi! 🪔`,r.x,r.y,`small`)', 'this.ctx.hud.speech(`Suda Suda Mysore Pak! 🌾`,r.x,r.y,`small`)', 'vendor Mysore Pak drop speech')
src = replace_exact(src, 'Maza aaya? 🪔 Mithai khilao', 'Mass-aa irundhucha? ☕ Buy Filter Kaapi', 'La result button')
src = replace_exact(src, 'DOUBLE GHEE KHATAM!', 'DOUBLE SOZHI MUDINJATHU!', 'double KO banner')
src = replace_exact(src, '`GHEE KHATAM!`', '`SOZHI MUDINJATHU!`', 'KO banner')
src = replace_exact(src, 'i.meterLabel.textContent=c?`SHAKTI READY!`:`SHAKTI`', 'i.meterLabel.textContent=c?`GETHU READY!`:`GETHU`', 'GETHU meter')
src = replace_exact(src, '`📕 BUDGET PESH HAI!<small>Ab lagega tax</small>`', '`📕 TAX MAAMI ARRIVES!<small>18% Slab + Cess!</small>`', 'GST Maami announce')

# 9. Pongal Flex Card + Filter Kaapi UPI tip modal + Pongal/Tamil festive lines
new_pt = 'Pt={modi:{intro:`Vanakkam! Iniya Pongal!`,win:`Pongal vetri namadhe!`},rahul:{intro:`Pongal greetings to all fans!`,win:`Sweet Pongal, mass victory!`},didi:{intro:`Thai Piranthaal Vazhi Pirakkum!`,win:`Amma fortress celebrates Pongal!`},trump:{intro:`Fire Star Pongal! Zero filter!`,win:`Thaggedhe Le Pongal special!`},yogi:{intro:`Lal Salam & Pongal Vaazhthukkal!`,win:`Red Star victory celebration!`},nitin:{intro:`Pongal rush at Silk Board cleared!`,win:`Expressway sweet Pongal win!`},ravi:{intro:`Sankranti & Pongal Blockbuster!`,win:`Box office Pongal hit!`},lalu:{intro:`Vaigai Express Pongal special!`,win:`Thambi Pongal feast begins!`},mbapu:{intro:`Self-Respect Thai Pongal to all!`,win:`Rational light shines bright!`},amit:{intro:`Pongal press meet begins!`,win:`All files signed for Pongal!`},dhruv:{intro:`Pongal Vlog live now guys!`,win:`Like, share, Pongal special!`}}'
src = replace_span(src, 'Pt={', ';function Ft(', new_pt + ';function Ft(', 'Pt Pongal lines', include_end=True)
src = replace_exact(
    src,
    'function It(e,t,n){return Mt?Pt[e]?.[t]??n:n}',
    'function It(e,t,n){return n}',
    'Disable It() festival override so introLine/winLine match real audio',
)
src = replace_exact(
    src,
    'this.cue(`a`,.5,()=>this.speech(0,this.diwali?It(n.char.id,`intro`,n.char.introLine):n.char.introLine)),this.cue(`b`,this.introLength/2+.1,()=>this.speech(1,this.diwali?It(r.char.id,`intro`,r.char.introLine):r.char.introLine))',
    'this.cue(`a`,.5,()=>{this.speech(0,n.char.introLine),t.playClip(`/assets/memes/${n.char.id}_1.mp3`,.95)}),this.cue(`b`,this.introLength/2+.1,()=>{this.speech(1,r.char.introLine),t.playClip(`/assets/memes/${r.char.id}_1.mp3`,.95)})',
    'Play matching _1.mp3 audio on intro speech bubbles',
)
src = replace_exact(
    src,
    'this.ctx.audio.announce(r.perfect?`perfect`:`wins_${e.char.id}`),this.speech(r.outcome,this.diwali?It(e.char.id,`win`,e.char.winLine):e.char.winLine)',
    'this._lastRoundPerfect=r.perfect,(r.perfect?this.ctx.audio.announce(`perfect`):(()=>{let wc=kn[e.char.id];wc&&this.ctx.audio.playClip(wc,Mn)})()),this.speech(r.outcome,e.char.winLine)',
    'Play matching kn win voice on every round win',
)
src = replace_exact(
    src,
    'else if(this.match.winner!==null){let e=kn[this.fighters[this.match.winner].char.id];e&&this.cue(`winLine`,1.2,()=>t.playClip(e,Mn))}',
    'else if(this._lastRoundPerfect&&this.match.winner!==null){let e=kn[this.fighters[this.match.winner].char.id];e&&this.cue(`winLine`,1.2,()=>t.playClip(e,Mn))}',
    'Avoid double-playing kn on non-perfect matchOver',
)
src = replace_exact(src, 'Lt=[`Mithai le lo! Kaju katli!`,`Ladoo garam garam!`,`Diwali special: chai + mithai!`,`Soan papdi bhi hai!`]', 'Lt=[`Suda Suda Bajji!`,`Mysore Pak ready!`,`Filter Kaapi + Vada!`,`Jigarthanda special!`]', 'Lt festive kaapi lines')
src = replace_exact(src, 'Ea=[[21,`Ek laddoo`],[51,`Kaju katli box`],[101,`Diwali mithai thali`]]', 'Ea=[[21,`Filter Kaapi`],[51,`Medu Vada + Kaapi`],[101,`Banana Leaf Meals`]]', 'UPI tips')
src = src.replace('Diwali card bhejo', 'Pongal Flex Bhejo')
src = src.replace('Diwali pe mithai khilao?', 'Buy us a Filter Kaapi?')
src = src.replace('Diwali pe mithai khilao', 'Buy Filter Kaapi ☕')
src = src.replace('Game free hai, koi ad nahi. Aapki mithai se servers chalte hain aur Chapter 2 jaldi aata hai.', 'Game is free with zero ads. Your Filter Kaapi keeps servers running & funds more Tamil Nadu stages!')
src = src.replace('Diwali Special Edition 🪔', 'Rohini FDFS Edition 🎬')
src = replace_exact(
    src,
    'function Ka(e,t){return Mt?{date:e.replace(`Satire Edition`,`Rohini FDFS Edition 🎬`),excuse:Math.random()<.5?`Breaking: Sansad mein sirf green patakhe allowed.`:t}:{date:e,excuse:t}}',
    'function Ka(e,t){return{date:e.replace(`Satire Edition`,`Rohini FDFS Edition 🎬`),excuse:t}}',
    'Ka keep character Box Office excuse',
)
src = src.replace('Breaking: Sansad mein sirf green patakhe allowed.', 'Breaking: Housefull Rohini FDFS crowd tears flex banners!')
src = re.sub(r'`[^`\n]{1,6} WINNER`', '`🏆 WINNER`', src)
src = src.replace('ðŸ™ ', '🙏')
src = src.replace('Shukriya, Sansad Supporter!', 'Nandri, Dakshin Supporter!')
src = src.replace('Aapki ₹${t} ki mithai se game free rehta hai aur Chapter 2 paas aata hai.', 'Your ₹${t} Filter Kaapi fuels free matches & South Arena updates!')
src = src.replace('SHUBH DEEPAVALI', 'PONGAL VAALTHUKKAL')
src = src.replace('SANSAD SHOWDOWN', 'DAKSHIN SHOWDOWN')
src = replace_exact(src, 'Shubh Deepavali! 🪔 Iss Diwali ${t} ke saath Sansad Showdown khelo', 'Iniya Pongal! 🪔 Play Dakshin Showdown with ${t}', 'Share text')
src = src.replace('celebrates outside the Sansad. (Cartoon, not a real photo)', 'celebrates outside Fort St. George. (Satire cartoon)')
src = src.replace('rules the Sansad!', 'rules the Dakshin Arena!')

# 10. Kootani VIP Cameo / Assist (KeyB / #budget-meter) in ALL 1P matches, recharging every 15s
src = replace_exact(src, 'this.boss&&!this.net&&ga()', '!this.net&&!window.__local2P&&ga()', 'budget preload 1P')
src = replace_exact(
    src,
    'i(this,`budget`,0),i(this,`budgetUsed`,!1)',
    'i(this,`budget`,1),i(this,`budgetUsed`,!1),i(this,`massZoomTimer`,0),i(this,`matchStats`,{kicks:0,punches:0,supers:0,grabs:0,maxCombo:0})',
    'jf budget, massZoomTimer, matchStats fields',
)
src = replace_exact(
    src,
    'this.budget=0,this.budgetUsed=!1',
    'this.budget=1,this.budgetUsed=!1',
    'startRound budget ready at start',
)
src = replace_exact(
    src,
    'this.boss&&!this.net?this.ctx.hud.setBudget(this.budgetUsed?0:this.budget,this.phase===`fight`&&!this.budgetUsed):this.ctx.hud.setBudget(0,!1)',
    '!this.net&&!window.__local2P?this.ctx.hud.setBudget(this._kootaniHazard?0:this.budget,this.phase===`fight`&&!this._kootaniHazard):this.ctx.hud.setBudget(0,!1)',
    'budget hud bar 1P',
)
src = replace_exact(
    src,
    'this.boss&&!this.budgetUsed&&!this.net&&(this.budget=Math.min(1,this.budget+qe/(this.hardBoss?lo.budgetSeconds:10)))',
    '!window.__local2P&&!this._kootaniHazard&&!this.net&&(this.budget=Math.min(1,this.budget+qe/15))',
    'budget charge timer 15s cooldown',
)
src = replace_span(
    src,
    'get budgetReady(){',
    'skipCinema(){',
    'get budgetReady(){let e=this.fighters[this.playerSide],o=this.fighters[+(this.playerSide===0)];return!window.__local2P&&!this.net&&!this._kootaniHazard&&this.budget>=1&&this.phase===`fight`&&this.hitStop===0&&e.actionable&&e.hp>0&&o.hp>1}callBudget(){if(!this.budgetReady)return!1;return this.budget=0,k(`budget_called`,{player:this.fighters[this.playerSide].char.id,assist:window.__selectedAssist||`random`}),triggerKootaniAssist(this,this.playerSide)}',
    'budgetReady & callBudget Kootani 3D Stage Hazard',
    include_end=False,
)
src = replace_exact(
    src,
    'this.diwali&&!this.net&&!this.boss&&this.stepMithai()',
    '!this.net&&!this.boss&&this.stepMithai()',
    'enable Mysore Pak drops',
)

# 10b. 13-Fighter additions to Dn, kn, Nn, Mn, double_ko, fi, Ba, so, co, bo, Tc, Ec, Zp, Zo, Pt
src = replace_exact(src, 'dhruv:vn}', 'dhruv:vn,nirmala:yn,rangaraj:`/assets/rangaraj-super.mp3`}', 'Dn 13 fighters')
src = replace_exact(
    src,
    'kn={ravi:bn,amit:xn},An=Cn,jn=Sn,Mn=1.43,Nn={intro:{url:wn,level:2.2},background:{url:Tn,level:3},battle:{url:En,level:1.242}}',
    'kn={modi:`/assets/memes/modi_2.mp3`,rahul:`/assets/rahulwin.mp3`,didi:`/assets/memes/didi_2.mp3`,trump:`/assets/memes/trump_2.mp3`,yogi:`/assets/memes/yogi_2.mp3`,nitin:`/assets/memes/nitin_2.mp3`,mbapu:Sn,ravi:bn,lalu:`/assets/memes/lalu_2.mp3`,amit:xn,dhruv:`/assets/memes/dhruv_2.mp3`,nirmala:`/assets/memes/nirmala_2.mp3`,rangaraj:`/assets/memes/rangaraj_2.mp3`},An=Cn,jn=Sn,Mn=1.05,Nn={intro:{url:wn,level:.85},background:{url:Tn,level:.78},battle:{url:En,level:.68}}',
    'kn 13 win voices + Mn/Nn mastered levels',
)
src = replace_exact(
    src,
    '"../assets/voice/double_ko.mp3":Xr',
    '"../assets/voice/double_ko.mp3":"/assets/voice/double_ko.mp3"',
    'Dedicated double_ko voice path',
)
src = replace_exact(
    src,
    'Y.preloadClips([X,n].flatMap(e=>Dn[e]??[]))',
    'Y.preloadClips([X,n].flatMap(e=>[Dn[e],kn[e],`/assets/memes/${e}_1.mp3`,`/assets/memes/${e}_2.mp3`].filter(Boolean)))',
    'Preload super, win, and action voice clips',
)
src = replace_exact(src, 'dhruv:[`bed_tariff`,`release_tariff`,`shimmer`,`plop`,`eye_zing`,`bark`,`heartbeat`]}', 'dhruv:[`bed_tariff`,`release_tariff`,`shimmer`,`plop`,`eye_zing`,`bark`,`heartbeat`],nirmala:[`bed_tariff`,`release_tariff`,`stamp_slam`,`kaching`,`coins`,`poof`],rangaraj:[`release_bulldozer`,`shimmer`,`bell`,`horn_short`,`drumroll`]}', 'fi 13 fighters')
src = replace_exact(src, 'dhruv:`Happy Diwali, doston! Khushiyan share karna!`}', 'dhruv:`Happy Diwali, doston! Khushiyan share karna!`,nirmala:`Iniya Pongal! 18% GST Free on Filter Kaapi!`,rangaraj:`Pongal special debate — Point-ku vaanga!`}', 'Ba 13 fighters')
src = replace_exact(
    src,
    'inputs:`↓J, J`}]}}',
    'inputs:`↓J, J`}]}`},nirmala:{stance:`stance`,pace:1.25,getup:oo,strikes:{jab:U(`palm_m`,1),cross:U(`palm`,1),kick:U(`snapkick2`),uppercut:U(`uppercut`,1),roundhouse:U(`roundhouse_m`),finisher:U(`thaiknee`),lowJab:U(`lowjab`,1),sweep:U(`stomp`),special1:U(`elbowhead`),special2:U(`kick_m`),airPunch:U(`cross_m`,1),airKick:U(`kick_m`),grab:U(`palm_m`,1)},chains:{cross:{punch:`special1`,kick:`finisher`},lowJab:{punch:`special1`,kick:`sweep`}},combos:[{name:`18% Popcorn Slab`,inputs:`J, J, J  or  ↓J, J`},{name:`28% Caramel Vasool`,inputs:`J, J, K`},{name:`Onion Price Stomp`,inputs:`↓J, K`}]},rangaraj:{stance:`rhguard`,pace:.95,getup:oo,strikes:{jab:U(`jab`),cross:U(`elbowhead`),kick:U(`pushkick`),uppercut:U(`elbowupper`),roundhouse:U(`roundhouse`),finisher:U(`spinkick`),lowJab:U(`sbupper`),sweep:U(`sweep360`),special1:U(`sbcombo`),special2:U(`sidekick`),airPunch:U(`cross`),airKick:U(`sidekick`),grab:U(`palm`,1)},chains:{cross:{kick:`special2`},lowJab:{punch:`special1`}},combos:[{name:`Kelvikku Enna Bathil`,inputs:`J, J, J`},{name:`Point-ku Vaanga Kick`,inputs:`J, J, K`},{name:`Mic Mute Lock`,inputs:`↓J, J`}]}}',
    'so 13 fighters',
)
src = replace_exact(
    src,
    'inputs:`↓J, J`}]}`},nirmala:',
    'inputs:`↓J, J`}]},nirmala:',
    'fix so syntax',
)
src = replace_exact(
    src,
    'airKick:[1.02,1.6,.69]}}',
    'airKick:[1.02,1.6,.69]},nirmala:{jab:[.58,1.37,1.77],cross:[.61,1.32,1.41],kick:[.75,.83,.67],uppercut:[.57,1.11,.46],roundhouse:[.79,1.15,1.07],finisher:[.33,1,.84],lowJab:[.38,.83,.82],sweep:[.5,.1,.71],special1:[.49,1.1,.74],special2:[.75,1.13,.62],airPunch:[.55,1.14,.34],airKick:[.75,1.13,.62]},rangaraj:{jab:[.8,1.25,.57],cross:[.63,1.21,.74],kick:[.91,.9,1.27],uppercut:[.69,1.34,.62],roundhouse:[1,.98,.97],finisher:[.98,.8,.89],lowJab:[.66,1.06,.19],sweep:[1.04,.64,1.34],special1:[.83,1.24,.46],special2:[.91,1.21,.71],airPunch:[.82,1.13,.34],airKick:[.91,1.21,.71]}}',
    'co 13 fighters',
)
src = replace_exact(
    src,
    'bo=[`modi`,`rahul`,`didi`,`trump`,`yogi`,`nitin`,`ravi`,`lalu`,`amit`,`dhruv`]',
    'bo=[`modi`,`rahul`,`didi`,`trump`,`yogi`,`nitin`,`ravi`,`lalu`,`amit`,`dhruv`,`nirmala`,`rangaraj`]',
    'bo 13 fighters',
)
src = replace_exact(
    src,
    'dhruv:`${xc}dhruv.glb${wc}`}',
    'dhruv:`${xc}dhruv.glb${wc}`,nirmala:`${xc}didi.glb${Cc}`,rangaraj:`${xc}amit.glb${wc}`}',
    'Tc 13 fighters',
)
src = replace_exact(
    src,
    'dhruv:`/models/dhruv.glb${wc}`}',
    'dhruv:`/models/dhruv.glb${wc}`,nirmala:`/models/didi.glb${Cc}`,rangaraj:`/models/amit.glb${wc}`}',
    'Ec 13 fighters',
)
src = replace_exact(
    src,
    'dhruv:`${Yp}faces/dhruv.webp?v=20261107_real`}',
    'dhruv:`${Yp}faces/dhruv.webp?v=20261107_real`,nirmala:`${Yp}faces/nirmala.webp?v=20261126`,rangaraj:`${Yp}faces/rangaraj.webp?v=20261126`}',
    'Zp 13 fighters',
)
src = replace_exact(
    src,
    'Suyamariyadhai never stalls!`]}',
    'Suyamariyadhai never stalls!`],nirmala:[`Popcorn-ukkum 18% GST!`,`Cream bun-ukkum GST!`,`Audit ready-aa?`],rangaraj:[`Point-ku vaanga!`,`Kelvikku enna bathil?!`,`Mic mute pannidatta?!`]}',
    'Zo 13 fighters',
)
src = replace_exact(
    src,
    'Like, share, Pongal special!`}}',
    'Like, share, Pongal special!`},nirmala:{intro:`Pongal special 0% GST!`,win:`Sweet Pongal Vasool!`},rangaraj:{intro:`Pongal Special Debate live!`,win:`Debate closed on Pongal!`}}',
    'Pt 13 fighters',
)

# 11. Upgrade 3: Local 2-Player Same-Keyboard Mode (#local2p-btn, Wf.pollP1 / pollP2, jf.step) + Censor Board Boss button lock
censor_guard = 'let _cl=window.__censorLock;if(_cl&&_cl.remaining>0){if(_cl.key===`kick`&&e.kick){e.kick=!1;window.__onCensorBlocked?.(`kick`)}if(_cl.key===`super`&&e.super){e.super=!1;window.__onCensorBlocked?.(`super`)}}'
src = replace_exact(
    src,
    'poll(){let e=n(),t=this.any(If,this.held)||this.touchHeld.has(`left`);return e.moveX=t===(this.any(Lf,this.held)||this.touchHeld.has(`right`))?0:t?-1:1,e.up=this.any(Rf,this.held)||this.touchHeld.has(`up`),e.down=this.any(zf,this.held)||this.touchHeld.has(`down`),e.punch=this.any(Bf,this.pressed)||this.touchPressed.has(`punch`),e.kick=this.any(Vf,this.pressed)||this.touchPressed.has(`kick`),e.super=this.any(Hf,this.pressed)||this.touchPressed.has(`super`),e.grab=this.any(Uf,this.pressed)||this.touchPressed.has(`grab`)||e.punch&&e.kick,e.grab&&(e.punch=!1,e.kick=!1),this.pressed.clear(),this.touchPressed.clear(),e}',
    'poll(){let e=n(),t=this.any(If,this.held)||this.touchHeld.has(`left`);e.moveX=t===(this.any(Lf,this.held)||this.touchHeld.has(`right`))?0:t?-1:1,e.up=this.any(Rf,this.held)||this.touchHeld.has(`up`),e.down=this.any(zf,this.held)||this.touchHeld.has(`down`),e.punch=this.any(Bf,this.pressed)||this.touchPressed.has(`punch`),e.kick=this.any(Vf,this.pressed)||this.touchPressed.has(`kick`),e.super=this.any(Hf,this.pressed)||this.touchPressed.has(`super`),e.grab=this.any(Uf,this.pressed)||this.touchPressed.has(`grab`)||e.punch&&e.kick,e.grab&&(e.punch=!1,e.kick=!1);' + censor_guard + 'this.pressed.clear(),this.touchPressed.clear();return e}pollP1(){let e=n(),l=this.held.has(`KeyA`)||this.touchHeld.has(`left`),r=this.held.has(`KeyD`)||this.touchHeld.has(`right`);e.moveX=l===r?0:l?-1:1,e.up=this.held.has(`KeyW`)||this.touchHeld.has(`up`),e.down=this.held.has(`KeyS`)||this.touchHeld.has(`down`),e.punch=this.any([`KeyJ`,`KeyZ`],this.pressed)||this.touchPressed.has(`punch`),e.kick=this.any([`KeyK`,`KeyX`],this.pressed)||this.touchPressed.has(`kick`),e.super=this.any([`KeyL`,`Space`,`KeyC`],this.pressed)||this.touchPressed.has(`super`),e.grab=this.any([`KeyI`,`KeyV`],this.pressed)||this.touchPressed.has(`grab`)||e.punch&&e.kick,e.grab&&(e.punch=!1,e.kick=!1);' + censor_guard + 'for(let k of[`KeyJ`,`KeyZ`,`KeyK`,`KeyX`,`KeyL`,`Space`,`KeyC`,`KeyI`,`KeyV`])this.pressed.delete(k);return this.touchPressed.clear(),e}pollP2(){let e=n(),l=this.held.has(`ArrowLeft`),r=this.held.has(`ArrowRight`);e.moveX=l===r?0:l?-1:1,e.up=this.held.has(`ArrowUp`),e.down=this.held.has(`ArrowDown`),e.punch=this.any([`KeyU`,`Numpad1`],this.pressed),e.kick=this.any([`KeyO`,`Numpad2`],this.pressed),e.super=this.any([`Enter`,`NumpadEnter`,`Numpad0`,`Slash`],this.pressed),e.grab=this.any([`KeyP`,`Numpad3`],this.pressed)||e.punch&&e.kick,e.grab&&(e.punch=!1,e.kick=!1);for(let k of[`KeyU`,`Numpad1`,`KeyO`,`Numpad2`,`Enter`,`NumpadEnter`,`Numpad0`,`Slash`,`KeyP`,`Numpad3`])this.pressed.delete(k);return e}',
    'Wf poll (censor lock) + pollP1 & pollP2',
)

src = replace_exact(
    src,
    'let i=this.ctx.input.poll(),a=this.net?this.hostDelay.pass(i):i,o=+(this.playerSide===0),s=r??this.bot.think(this.fighters[o],this.fighters[this.playerSide],.016666666666666666),c=r?s:this.dodgeBomb(this.fighters[o],s)',
    'window.__onCensorBlocked=(k)=>{let p=this.fighters[this.playerSide],sc=this.ctx.toScreen(this.tmp.set(p.x,2.2,.3));this.ctx.hud.popup(`✂️ ${k.toUpperCase()} CENSORED! GRAB [I]!`,sc.x,sc.y,`#ef4444`)};let i=window.__local2P&&!this.net?this.ctx.input.pollP1():this.ctx.input.poll(),a=this.net?this.hostDelay.pass(i):i,o=+(this.playerSide===0),s=r??(window.__local2P&&!this.net?this.ctx.input.pollP2():this.bot.think(this.fighters[o],this.fighters[this.playerSide],.016666666666666666)),c=r||window.__local2P&&!this.net?s:this.dodgeBomb(this.fighters[o],s)',
    'jf.step local2P + censor blocked feedback',
)

# Update P2 labels & wire #local2p-btn & [data-assist] picker
src = replace_exact(
    src,
    'let t=Q?`2P · FRIEND${$.friendReady?` · READY ✓`:``}`:e===`mbapu`?`FINAL BOSS · OPPONENT`:`CPU`;Em(q(`#plate-p1`)',
    'let t=Q?`2P · FRIEND${$.friendReady?` · READY ✓`:``}`:window.__local2P?`2P · LOCAL KEYBOARD`:e===`mbapu`?`FINAL BOSS · OPPONENT`:`CPU`;Em(q(`#plate-p1`)',
    'Dm plate-p2 label',
)
src = replace_exact(
    src,
    'q(`#vs-line`).textContent=`${N[X].name} (YOU) vs ${e?N[e].name:`…`} (${Q?`FRIEND`:e===`mbapu`?`BOSS`:`CPU`})`',
    'q(`#vs-line`).textContent=`${N[X].name} (YOU) vs ${e?N[e].name:`…`} (${Q?`FRIEND`:window.__local2P?`2P LOCAL`:e===`mbapu`?`BOSS`:`CPU`})`',
    'Dm vs-line local2P',
)
src = replace_exact(
    src,
    'document.querySelector(`#fight-btn`).addEventListener(`click`,Nm),',
    'document.querySelectorAll(`[data-assist]`).forEach(el=>el.addEventListener(`click`,()=>{window.__selectedAssist=el.dataset.assist;document.querySelectorAll(`[data-assist]`).forEach(x=>x.classList.toggle(`selected`,x===el));let lbl=document.querySelector(`#budget-meter .label`);if(lbl)lbl.textContent={sumo:`FLYING SUMO`,squad:`FLYING SQUAD`,light:`STUDIO LIGHT`,random:`RANDOM KOOTANI`}[window.__selectedAssist]||`KOOTANI CAMEO`;Y.uiSelect()})),document.querySelector(`#local2p-btn`)?.addEventListener(`click`,()=>{window.__local2P=!window.__local2P;let b=document.querySelector(`#local2p-btn`);b.classList.toggle(`active`,window.__local2P);b.textContent=window.__local2P?`⚔️ 2P LOCAL: ON`:`⚔️ 2P LOCAL: OFF`;Y.uiSelect(),Dm()}),document.querySelector(`#fight-btn`).addEventListener(`click`,Nm),',
    'bind #local2p-btn + [data-assist]',
)

# Also update HUD opponent label when local 2P is active
src = replace_exact(
    src,
    'this.playerSide,this.net?`FRIEND`:`CPU`,this.bossSide',
    'this.playerSide,this.net?`FRIEND`:window.__local2P?`2P`:`CPU`,this.bossSide',
    'jf setup HUD 2P label',
)

# 12. Sutli Bomb -> SIVAKASI 1000-WALA VEDI (crimson/gold cracker, gold blast ring, festive confetti)
src = replace_exact(src, 'let r=Za(9071162,0,.95),a=new v(new E(.2,18,14),r);this.bomb.add(a);',
    'let r=Za(14423100,2621440,.5),a=new v(new E(.2,18,14),r);a.scale.set(1,1.18,1);this.bomb.add(a);', 'Vedi crimson body')
src = replace_exact(src, 'new v(new Oe(.2,.012,6,24),Za(5914658,0,.9));e.rotation.set(Math.random()*Math.PI,Math.random()*Math.PI,0)',
    'new v(new Oe(.2,.016,6,24),Za(16435252,3801088,.35));e.rotation.set(Math.PI/2+(Math.random()-.5)*.5,0,(Math.random()-.5)*.5),e.position.y=(Math.random()-.5)*.28', 'Vedi gold kasavu bands')
src = replace_exact(src, 'new v(new D(.205,.205,.09,18),Za(14034984,3801088,.7))', 'new v(new D(.21,.21,.1,18),Za(1483594,0,.6))', 'Vedi green label band')
src = replace_exact(src, 'this.ring=new v(new oe(1.34,eo,72),new S({color:16722458,', 'this.ring=new v(new oe(1.34,eo,72),new S({color:16435252,', 'Vedi gold danger ring')
src = replace_exact(src, 'new v(new Re(1.34,72),new S({color:16722458,', 'new v(new Re(1.34,72),new S({color:16435252,', 'Vedi gold danger disc')
src = replace_exact(src, 'let u=[14034984,16765803,16777215,2792778];', 'let u=[16435252,14423100,2282478,16777215,1483594];', 'Vedi festive confetti')
src, n_bomb = re.subn(r'`[^`]{0,8}SUTLI BOMB<small>Ring se bahar bhaago!</small>`', '`🧨 SIVAKASI VEDI!<small>Odu macha! 1000-Wala vedikkudhu!</small>`', src)
assert n_bomb == 1, 'Vedi announce'
src, n_hiss = re.subn(r't\.speech\(`SSSS[^`]*`', 't.speech(`Chata-pata! Sivakasi vedi! 🧨`', src)
assert n_hiss == 1, 'Vedi hiss'

# 13. GST Maami cinematic: book cover, slab popups, collection banner
src = replace_exact(src, 'e.fillText(`BUDGET`,96,110)', 'e.fillText(`GST BILL`,96,110)', 'GST book title')
src = replace_exact(src, 'e.fillText(`2026`,96,160)', 'e.fillText(`18% + CESS`,96,160)', 'GST book subtitle')
src = replace_exact(src, 'r.popup(`GST ${e.rate}!`,', 'r.popup([`KAAPI 5%!`,`CREAM BUN 12%!`,`POPCORN 18%!`,`CESS 28%!`][t]??`GST ${e.rate}!`,', 'GST slab popups')
src = replace_exact(src, 'r.popup(`TAX COLLECTED!`,', 'r.popup(`GST VASOOL!`,', 'GST collected banner')

# 14. Bespoke Iconic South Movie & Incident Special Move Animations per Character
src = replace_span(
    src,
    'function kd(e){',
    'var Ad=class{',
    'function kd(e){return createSouthSuper(e,{P,B,V,F,R,L})}var Ad=class{',
    'kd bespoke South Super animations',
    include_end=True,
)

# 15. Rendering & Animation Smoothness: native unlocked vsync, MSAA + balanced DPR/1024 shadows, sub-frame visual interpolation, smooth clip-to-idle tracking
src = replace_exact(
    src,
    'J=new Ie({canvas:ip,antialias:!1,powerPreference:`high-performance`});J.setPixelRatio(Math.min(window.devicePixelRatio,M?1.5:2))',
    'J=new Ie({canvas:ip,antialias:!M,powerPreference:`high-performance`});J.setPixelRatio(Math.min(window.devicePixelRatio,M?1.35:1.5))',
    'WebGL antialias + balanced DPR',
)
src = replace_exact(
    src,
    'Ph=Math.min(window.devicePixelRatio,M?1.5:2)',
    'Ph=Math.min(window.devicePixelRatio,M?1.35:1.5)',
    'Ph balanced DPR',
)
src = replace_exact(
    src,
    'let n=M?1024:2048;this.sun.shadow.mapSize.set(n,n)',
    'let n=1024;this.sun.shadow.mapSize.set(n,n)',
    '1024 shadow map for 60/120fps stability',
)
src = replace_exact(
    src,
    'let t=Hp===`battle`||Hp===`result`&&!!Z||!!xp&&!M,n=Z?.paused?100:t?1e3/60:1e3/30;if(e<jh-1||(jh=Math.max(jh+n,e-n),Sp.active))return;',
    'let n=Z?.paused?80:0;if(n>0&&e<jh+n)return;if(Sp.active)return;jh=e;',
    'Unlocked native monitor vsync loop',
)
src = replace_exact(
    src,
    '!l&&!u&&(c.stopDance?.(),c.stopClip?.(),c.blendTo(o,s,t)),u||c.setMirror?.(!1);let d=this.phase===`grapple`?this.grapple:null,f=this.phase===`super`&&i!==this.superCaster?this.superMove:null,p=d?i===this.grappleSide?d.attTf:d.defTf:f?.targetTf??null;if(p)c.setFree(p.x,p.y,p.z,p.yaw,p.roll);else{let n=this.smooth[i],r=Math.exp(-e*14);n.x*=r,n.y*=r;let o=a.x+n.x,s=Math.max(0,a.y+n.y);',
    'u&&F(c.current,o,Math.min(1,t*10),c.current),!l&&!u&&(c.stopDance?.(),c.stopClip?.(),c.blendTo(o,Math.max(s,16),t)),u||c.setMirror?.(!1);let d=this.phase===`grapple`?this.grapple:null,f=this.phase===`super`&&i!==this.superCaster?this.superMove:null,p=d?i===this.grappleSide?d.attTf:d.defTf:f?.targetTf??null;if(p)c.setFree(p.x,p.y,p.z,p.yaw,p.roll);else{let n=this.smooth[i],r=Math.exp(-e*14);n.x*=r,n.y*=r;let g=this.phase===`fight`?Math.min(qe,this.acc):0,o=Math.max(-A,Math.min(A,a.x+a.vx*g+n.x)),s=Math.max(0,a.y+(a.grounded?0:a.vy*g)+n.y);',
    'Sub-frame movement interpolation + smooth clip exit',
)
src = replace_exact(
    src,
    'setTransform(e,t,n,r,i=.28){',
    'setTransform(e,t,n,r,i=.36){',
    'Smooth default idle yaw angle',
)
src = replace_exact(
    src,
    'function Ah(t){Dh+=t,e.forEach((e,n)=>{let r=lm[e];if(!r||!r.root.visible)return;let i=Hp===`select`&&e===X;r.blendTo(i?Wi(Dh,e):$i(Dh+n*1.9,e),6,t)});let n=Math.sin(Dh*.25)*(Hp===`select`?.12:.3),r=4.1*Math.max(1,1.5/lp.camera.aspect);Oh.set(0,1.15,0),kh.set(0+Math.sin(n)*r,1.45,Math.cos(n)*r),lp.set(kh,Oh,2.5,40)',
    'function Ah(t){Dh+=t,e.forEach((e,n)=>{let r=lm[e];if(!r||!r.root.visible)return;let i=Hp===`select`&&e===X;r.blendTo(i?Wi(Dh,e):$i(Dh+n*1.9,e),9,t)});let n=Math.sin(Dh*.25)*(Hp===`select`?.12:.3),r=4.1*Math.max(1,1.5/lp.camera.aspect);Oh.set(0,1.15,0),kh.set(0+Math.sin(n)*r,1.45,Math.cos(n)*r),lp.set(kh,Oh,4.5,40)',
    'Menu camera & pose smooth damping',
)

# 16. Bugless Gameplay + Modified Combat Mechanics (Fighter3D DEFAULT_FRAMES, Gethu Overload 1.3x Speed / 50% Armor, +18/+12 Gethu, Double-Tap Dash, Just-Frame Mass Parry, Hit-Confirm Super Cancel, Extended Chains)
src = replace_exact(
    src,
    'i(this,`downFrames`,0),i(this,`grounded`,!0),this.side=e',
    'i(this,`downFrames`,0),i(this,`grounded`,!0),i(this,`dashFrames`,0),i(this,`dashDir`,0),i(this,`tapDir`,0),i(this,`tapAge`,0),i(this,`prevMoveX`,0),i(this,`blockFrames`,0),i(this,`overloadFrames`,0),this.side=e',
    'ko constructor dash, parry & overloadFrames fields',
)
src = replace_exact(
    src,
    'this.comboHits=0,this.downFrames=0,this.grounded=!0,this.enter(`idle`)}',
    'this.comboHits=0,this.downFrames=0,this.grounded=!0,this.wantsSuper=!1,this.dashFrames=0,this.dashDir=0,this.tapDir=0,this.tapAge=0,this.prevMoveX=0,this.blockFrames=0,this.overloadFrames=0,this.enter(`idle`)}get isGethuOverload(){return this.overloadFrames>0}',
    'ko reset dash, parry & isGethuOverload getter',
)
src = replace_exact(
    src,
    'jab:{id:`jab`,startup:5,active:3,recovery:10,damage:5,height:`high`,hitstun:16,blockstun:10,knockdown:!1,launch:0,push:1.6,lunge:1.6,chains:{punch:`cross`,kick:`kick`}},cross:{id:`cross`,startup:6,active:3,recovery:12,damage:6,height:`high`,hitstun:18,blockstun:11,knockdown:!1,launch:0,push:1.8,lunge:2,chains:{punch:`uppercut`,kick:`finisher`}},kick:{id:`kick`,startup:9,active:4,recovery:15,damage:9,height:`mid`,hitstun:22,blockstun:13,knockdown:!1,launch:0,push:2,lunge:1.4,chains:{kick:`roundhouse`}},uppercut:{id:`uppercut`,startup:9,active:4,recovery:20,damage:11,height:`mid`,hitstun:24,blockstun:15,knockdown:!0,launch:8,push:1.4,lunge:1.8},',
    'jab:{id:`jab`,startup:4,active:4,recovery:8,damage:8,height:`high`,hitstun:18,blockstun:10,knockdown:!1,launch:0,push:.85,lunge:1.6,chains:{punch:`cross`,kick:`kick`}},cross:{id:`cross`,startup:5,active:4,recovery:10,damage:8,height:`high`,hitstun:20,blockstun:11,knockdown:!1,launch:0,push:.9,lunge:1.8,chains:{punch:`uppercut`,kick:`finisher`}},kick:{id:`kick`,startup:7,active:5,recovery:12,damage:13,height:`mid`,hitstun:22,blockstun:13,knockdown:!1,launch:0,push:1.2,lunge:1.5,chains:{kick:`roundhouse`}},uppercut:{id:`uppercut`,startup:8,active:4,recovery:14,damage:11,height:`mid`,hitstun:28,blockstun:15,knockdown:!1,launch:0,push:.75,lunge:1.4,chains:{kick:`finisher`,punch:`special1`}},',
    'DEFAULT_FRAMES Punch/Kick/Uppercut frame data & 5-hit chains',
)
src = replace_exact(
    src,
    'special1:{id:`special1`,startup:13,active:4,recovery:19,damage:13,height:`mid`,hitstun:26,blockstun:16,knockdown:!0,launch:7.5,push:2.2,lunge:3},special2:{id:`special2`,startup:15,active:5,recovery:20,damage:14,height:`mid`,hitstun:26,blockstun:16,knockdown:!0,launch:4.5,push:5.2,lunge:2.6},',
    'special1:{id:`special1`,startup:10,active:6,recovery:15,damage:14,height:`mid`,hitstun:28,blockstun:16,knockdown:!1,launch:0,push:.75,lunge:1.6,chains:{kick:`special2`,punch:`uppercut`}},special2:{id:`special2`,startup:11,active:6,recovery:18,damage:18,height:`mid`,hitstun:28,blockstun:16,knockdown:!0,launch:5.5,push:4.8,lunge:2.6},',
    'DEFAULT_FRAMES Special frame data (5-hit extenders)',
)
src = replace_exact(
    src,
    'landing:{id:`landing`,startup:0,active:0,recovery:14,',
    'landing:{id:`landing`,startup:0,active:0,recovery:8,',
    'snappier jump landing recovery',
)
src = replace_exact(
    src,
    'update(e,t){if(this.wantsSuper=!1,this.stateFrames++,e.grab||e.punch||e.kick?this.buffer={button:e.grab?`grab`:e.kick?`kick`:`punch`,frames:9}:this.buffer&&(this.buffer.frames--,this.buffer.frames<=0&&(this.buffer=null)),e.super?this.superBuffer=Eo:this.superBuffer>0&&this.superBuffer--,Do.has(this.state))return;let n=t>=this.x?1:-1;switch(this.state){case`idle`:case`walk`:case`crouch`:this.comboHits=0,this.updateActionable(e,n);break;',
    'update(e,t){if(this.wantsSuper=!1,this.stateFrames++,this.overloadFrames>0&&this.overloadFrames--,this.tapAge>0&&this.tapAge--,e.grab||e.punch||e.kick?this.buffer={button:e.grab?`grab`:e.kick?`kick`:`punch`,frames:24}:this.buffer&&(this.buffer.frames--,this.buffer.frames<=0&&(this.buffer=null)),e.super?this.superBuffer=Eo:this.superBuffer>0&&this.superBuffer--,Do.has(this.state)){if(this.state===`getup`&&this.stateFrames===1){this.facing=t>=this.x?1:-1}return}let n=t>=this.x?1:-1;e.moveX!==0&&this.prevMoveX===0&&(this.tapDir===e.moveX&&this.tapAge>0&&this.actionable&&!e.down?(this.dashFrames=10,this.dashDir=e.moveX,this.tapAge=0):(this.tapDir=e.moveX,this.tapAge=14)),this.prevMoveX=e.moveX,this.actionable&&e.moveX*n<0?this.blockFrames=Math.min(60,this.blockFrames+1):this.state!==`blockstun`&&(this.blockFrames=0);switch(this.state){case`idle`:case`walk`:case`crouch`:this.comboHits=0,this.updateActionable(e,n);break;',
    'ko update dash, parry timing, overloadFrames, facing fix, 24f buffer',
)
src = replace_exact(
    src,
    'updateActionable(e,t){this.facing=t;let n=e.moveX*this.facing;if(this.moveRel=n,this.holdingBack=n<0,this.superBuffer>0&&this.meter>=100){this.superBuffer=0,this.wantsSuper=!0,this.vx=0;return}if(e.up&&!e.down){this.startJump(n);return}this.crouching=e.down;let r=this.consumeBuffer();r?this.startAttack(ro(r,this.crouching,n>0)):this.crouching?(this.enter(`crouch`),this.vx=0):n===0?(this.enter(`idle`),this.vx=0):(this.enter(`walk`),this.vx=n>0?this.char.walkFwd*this.facing:-this.char.walkBack*this.facing)}',
    'updateActionable(e,t){this.facing=t;let n=e.moveX*this.facing,ov=this.overloadFrames>0?1.3:1;if(this.moveRel=n,this.holdingBack=n<0,this.superBuffer>0&&this.meter>=100){this.superBuffer=0,this.wantsSuper=!0,this.vx=0;return}if(e.up&&!e.down){this.dashFrames=0,this.startJump(n);return}this.crouching=e.down;let r=this.consumeBuffer();if(r){this.dashFrames=0,this.startAttack(ro(r,this.crouching,n>0));return}if(this.dashFrames>0){this.dashFrames--,this.vx=this.dashDir*(this.dashDir===this.facing?7.2:6)*ov,this.moveRel=this.dashDir*this.facing,this.enter(`walk`);return}this.crouching?(this.enter(`crouch`),this.vx=0):n===0?(this.enter(`idle`),this.vx=0):(this.enter(`walk`),this.vx=(n>0?this.char.walkFwd*this.facing:-this.char.walkBack*this.facing)*ov)}',
    'ko updateActionable burst dash step + 1.3x Gethu Overload speed',
)
src = replace_exact(
    src,
    'updateAttack(){let e=this.attack;if(!e){this.enter(`idle`);return}e.frame++;let t=e.def;if(e.frame<=t.startup+t.active?this.vx=(t.lunge+(e.frame<=t.startup+1?To(this,t.id):0))*this.facing:this.vx*=.75,t.chains&&e.hasHit&&this.buffer&&e.frame>=t.startup+t.active){let e=po(this.char.id,t,this.buffer.button);if(e){this.buffer=null,this.startAttack(e);return}}e.frame>=io(t)&&(this.attack=null,this.crouching=!!t.crouching,this.enter(t.crouching?`crouch`:`idle`))}integrate()',
    'updateAttack(){let e=this.attack;if(!e){this.enter(`idle`);return}e.frame+=this.overloadFrames>0&&e.frame%3===0?2:1;let t=e.def;if(e.frame<=t.startup+t.active){let lg=this.char.style===`orator`&&[`jab`,`cross`,`uppercut`].includes(t.id)?t.lunge*.2:t.lunge;this.vx=(lg+(e.frame<=t.startup+1?To(this,t.id):0))*this.facing}else this.vx*=.75;if(e.hasHit&&!e.blocked&&this.superBuffer>0&&this.meter>=100&&e.frame>=t.startup){this.superBuffer=0,this.attack=null,this.wantsSuper=!0,this.vx=0,this.enter(`idle`);return}if(t.chains&&e.hasHit&&this.buffer&&e.frame>=t.startup+t.active){let e=po(this.char.id,t,this.buffer.button);if(e){this.buffer=null,this.startAttack(e);return}}e.frame>=io(t)&&(this.attack=null,this.crouching=!!t.crouching,this.enter(t.crouching?`crouch`:`idle`))}integrate()',
    'ko updateAttack Hit-Confirm Super Cancel + Orator zoner lunge + 1.3x Gethu Overload',
)
src = replace_exact(
    src,
    'this.x+=this.vx*qe,this.y+=this.vy*qe,this.state===`walk`&&(this.walkDistance+=Math.abs(this.vx)*qe),this.x=Math.max(-A,Math.min(A,this.x))',
    'this.x+=this.vx*qe*(this.grounded&&window.__marinaWaveSlip?1.45:1),this.y+=this.vy*qe,this.state===`walk`&&(this.walkDistance+=Math.abs(this.vx)*qe),this.x=Math.max(-A,Math.min(A,this.x))',
    'ko integrate Marina wave reduced friction slide',
)
src = replace_exact(
    src,
    'function So(e,t){return Math.max(co[e][t]?.[0]??0,Qe)}',
    'function So(e,t){return Math.max(co[e][t]?.[0]??0,Qe)+(N[e]?.style===`orator`&&[`jab`,`cross`,`uppercut`].includes(t)?1.35:0)}',
    'Orator mid-range soundwave zoner reach',
)
src = replace_exact(
    src,
    'if(a){n.blocked=!0;let r=Math.min(Math.round(n.def.damage*e.char.damageMul*$e),Math.ceil(t.hp)-1);return r>0&&(t.hp-=r),t.applyBlock(n.def,i),e.addMeter(2),t.addMeter(3),af(e,t,n.def.push*.6),{attacker:e,defender:t,moveId:n.def.id,blocked:!0,damage:Math.max(0,r),knockdown:!1,ko:!1,x:o,y:s}}let c=t.attackPhase===`startup`,l=tf(e,t,n.def.damage*(c?et:1));return t.applyHit(n.def,l,i),e.addMeter(l*.9+2),t.addMeter(l*.6),af(e,t,n.def.push*.8),{attacker:e,defender:t,moveId:n.def.id,blocked:!1,damage:l,knockdown:t.state===`knockdown`,ko:t.state===`ko`,counter:c,x:o,y:s}}',
    'if(a){n.blocked=!0;let p=t.blockFrames>0&&t.blockFrames<=7;if(p)return t.blockFrames=99,t.attack=null,t.stun=0,t.vx=0,t.enter(t.crouching?`crouch`:`idle`),t.addMeter(18),af(e,t,n.def.push*.9),{attacker:e,defender:t,moveId:n.def.id,blocked:!0,parry:!0,damage:0,knockdown:!1,ko:!1,x:o,y:s};let r=Math.min(Math.round(n.def.damage*e.char.damageMul*$e),Math.ceil(t.hp)-1);return r>0&&(t.hp-=r),t.applyBlock(n.def,i),e.addMeter(2),t.addMeter(3),af(e,t,n.def.push*.6),{attacker:e,defender:t,moveId:n.def.id,blocked:!0,parry:!1,damage:Math.max(0,r),knockdown:!1,ko:!1,x:o,y:s}}if(t.char.style===`heavy`&&t.state===`attack`&&[`kick`,`roundhouse`].includes(t.attack?.def?.id)&&[`jab`,`cross`,`lowJab`,`airPunch`].includes(n.def.id)){let l0=tf(e,t,n.def.damage),l=Math.max(1,Math.round(l0*.5));return t.hp=Math.max(1,t.hp-l),e.addMeter(4),t.addMeter(8),{attacker:e,defender:t,moveId:n.def.id,blocked:!1,armor:!0,damage:l,knockdown:!1,ko:!1,x:o,y:s}}let c=t.attackPhase===`startup`,l0=tf(e,t,n.def.damage*(c?et:1)),l=t.overloadFrames>0?Math.max(1,Math.round(l0*.5)):l0;return t.applyHit(n.def,l,i),e.addMeter(e.overloadFrames>0?8:Math.max(18,l*.9+2)),t.addMeter(Math.max(12,l*.6)),af(e,t,n.def.push*.8),{attacker:e,defender:t,moveId:n.def.id,blocked:!1,damage:l,knockdown:t.state===`knockdown`,ko:t.state===`ko`,counter:c,x:o,y:s}}',
    'nf Just-Frame Mass Parry + Heavyweight K,K Super Armor + Gethu Overload',
)
src = replace_exact(
    src,
    't.meter=0,t.attack=null,t.vx=0,t.forceState(`super`)',
    't.meter=0,t.overloadFrames=480,t.attack=null,t.vx=0,t.forceState(`super`);e===this.playerSide&&(this.matchStats.supers++)',
    'startSuper triggers 8-second (480f) Gethu Overload + matchStats',
)
src = replace_exact(
    src,
    'if(e.blocked){this.ctx.news.event({kind:`block`,attacker:e.attacker.char.id}),n.block(),this.hitStop=3,r.shake(.03,.12);return}',
    'if(e.blocked){if(e.parry){this.tmp.set(e.x,e.y+.45,.3);let p2=this.ctx.toScreen(this.tmp);a.popup(`MASS PARRY!`,p2.x,p2.y,`#facc15`),t.hitSpark(this.tmp,1.35,!1,e.attacker.facing),t.shockwave(this.tmp,16435252,.35,1.25,!0),n.hit(.9),this.hitStop=7,r.shake(.12,.16);return}this.ctx.news.event({kind:`block`,attacker:e.attacker.char.id}),n.block(),this.hitStop=3,r.shake(.03,.12);return}if(e.armor){this.tmp.set(e.x,e.y+.5,.3);let p2=this.ctx.toScreen(this.tmp);a.popup(`🛡️ SUPER ARMOR!`,p2.x,p2.y,`#38bdf8`),t.hitSpark(this.tmp,1.1,!1,e.attacker.facing),n.block(),this.hitStop=2;return}',
    'onHit Just-Frame Mass Parry + Heavyweight Super Armor FX',
)
src = replace_exact(
    src,
    'function af(e,t,n){Math.abs(t.x)>=6.45&&(e.vx=-e.facing*n)}',
    'function af(e,t,n){Math.abs(t.x)>=5.95&&(e.vx=-e.facing*n)}',
    'Corner pushback escape distance balance',
)

# 17. Hook Paal Abhishekam (5+ hits), Fan War Feed, Stage Hazards, Kootani Assist Step, Censor Boss, Mass Hero Camera Zoom, Box Office Receipt
src = replace_exact(
    src,
    'combo(e,t){if(t<2)return;let n=this.sides[e];n.combo.innerHTML=`<b>${t}</b> HITS`,n.combo.classList.remove(`show`),n.combo.offsetWidth,n.combo.classList.add(`show`),this.comboTimers[e]=1.4}',
    'combo(e,t){if(t<2)return;let n=this.sides[e];n.combo.innerHTML=`<b>${t}</b> HITS`,n.combo.classList.remove(`show`),n.combo.offsetWidth,n.combo.classList.add(`show`),this.comboTimers[e]=1.4,t>=5&&triggerPaalAbhishekam(e,t)}',
    'HUD 5+ combo Paal Abhishekam splash',
)
src = replace_exact(
    src,
    'this.ctx.news.event({kind:`hit`,attacker:e.attacker.char.id,move:s??Df[e.moveId],damage:e.damage,knockdown:e.knockdown})',
    'this.ctx.news.event({kind:`hit`,attacker:e.attacker.char.id,move:s??Df[e.moveId],damage:e.damage,knockdown:e.knockdown,combo:e.defender.comboHits})',
    'pass combo count to news/fanwar feed',
)
src = replace_exact(
    src,
    'event(e){let t=qo(e,this.rng);',
    'event(e){pushFanWarComment({kind:e.kind,attacker:e.attacker,combo:e.combo,knockdown:e.knockdown});let t=qo(e,this.rng);',
    'Ff.event -> Fan War live comment feed',
)
src = replace_exact(
    src,
    't.frame===t.def.startup+1&&Ef.has(t.def.id)&&this.checkChai(e)',
    't.frame===t.def.startup+1&&e.char.style===`orator`&&[`jab`,`cross`,`uppercut`].includes(t.def.id)&&spawnOratorSoundwave(this,e,t.def.id),t.frame===t.def.startup+1&&Ef.has(t.def.id)&&this.checkChai(e)',
    'jf.step Orator 3D soundwave rings on J,J,J',
)
src = replace_exact(
    src,
    'this.checkBoredom(),!this.net&&!this.boss&&this.stepMithai()',
    'updateSouthStageHazards(this.ctx.arena,this,this.time,qe),updateKootaniAssist(this,qe),updateCensorBossMechanic(this,qe),this.checkBoredom(),!this.net&&!this.boss&&this.stepMithai()',
    'jf.step stage hazards + Kootani assist + Censor boss',
)
src = replace_exact(
    src,
    'n.frameFight(o.x,s.x,o.y,s.y)',
    '(n.frameFight(o.x,s.x,o.y,s.y),this.massZoomTimer>0&&(this.massZoomTimer=Math.max(0,this.massZoomTimer-e),n.targetPos.z=Math.max(3,n.targetPos.z-2.5),n.rate=16))',
    'Mass Hero slow-mo camera zoom z - 2.5',
)
src = replace_exact(
    src,
    'trackBoss(e){this.bossSeconds+=qe,e.hp<this.bossHpSeen?(this.roundDamage+=this.bossHpSeen-e.hp,this.bossCalm=0):this.bossCalm+=qe,this.hardBoss&&this.bossCalm>=lo.regenDelay&&e.hp>0&&(e.hp=Math.min(e.maxHp,e.hp+lo.regen*qe)),this.bossHpSeen=e.hp,this.bestDamage=Math.max(this.bestDamage,this.roundDamage)}',
    'trackBoss(e){this.bossSeconds+=qe,e.hp<this.bossHpSeen?(this.roundDamage+=this.bossHpSeen-e.hp,this.bossCalm=0):this.bossCalm+=qe,this.bossHpSeen=e.hp,this.bestDamage=Math.max(this.bestDamage,this.roundDamage)}',
    'Remove Shanti boss passive regen (replaced by Censor Red Card aura)',
)
src = replace_exact(
    src,
    't.cinemaTitle(`AB ASLI PARIKSHA`,`MBAPU · ANTIM YODDHA`)',
    't.cinemaTitle(`MODEL CODE OF CONDUCT`,`CENSOR BOARD · ELECTION BOSS`)',
    'Censor Boss intro title',
)
src = replace_exact(
    src,
    'this.grappleSide=e,this.grapple=tc(',
    'e===this.playerSide&&(this.matchStats.grabs++),onCensorBossGrabBreak(this,t,n),this.grappleSide=e,this.grapple=tc(',
    'Grab breaks Censor Boss lock + stats',
)
src = replace_exact(
    src,
    'this.ctx.hud.clearSay()}',
    'this.ctx.hud.clearSay(),cleanupSouthBattle(this)}',
    'jf.dispose cleanupSouthBattle',
)
src = replace_exact(
    src,
    'this.onMatchEnd?.(e,{',
    'window.__lastMatchStats={...this.matchStats};this.onMatchEnd?.(e,{',
    'jf.endMatch store matchStats',
)
src = replace_exact(
    src,
    'a(`#paper-date`).textContent=o.date,a(`#paper-headline`).textContent=i.headline,a(`#paper-sub`).textContent=i.sub,a(`#paper-excuse`).textContent=o.excuse,a(`#paper-photo`).setAttribute(`src`,Zp[t.winner]),a(`#paper-caption`).textContent=`${N[t.winner].fullName} celebrates outside Fort St. George. (Satire cartoon)`',
    'a(`#paper-date`).textContent=o.date;let bo=computeBoxOfficeVerdict(t.winner,r,t.wins,window.__lastMatchStats||{});a(`#boxoffice-crores`)&&(a(`#boxoffice-crores`).textContent=bo.clubText);a(`#tanglish-roast`)&&(a(`#tanglish-roast`).textContent=`🔥 TANGLISH ROAST: ${bo.roast}`);a(`#receipt-lines`)&&(a(`#receipt-lines`).textContent=`ROHINI FDFS · KICKS: ${(window.__lastMatchStats?.kicks)||0} · PUNCHES: ${(window.__lastMatchStats?.punches)||0} · BLUE SHIRT REVIEW: ${bo.reviewScore}`);a(`#paper-headline`).textContent=i.headline,a(`#paper-sub`).textContent=i.sub,a(`#paper-excuse`).textContent=o.excuse,a(`#paper-photo`).setAttribute(`src`,Zp[t.winner]),a(`#paper-caption`).textContent=`${N[t.winner].fullName} — Rohini FDFS Box Office Poster!`',
    'Box Office Crore Club & Dynamic Tanglish Roast receipt',
)

# Clean any stray Sansad strings in title/result/select
src = src.replace('PICK YOUR NETA', 'PICK YOUR THALAIVAR')
src = src.replace('FIGHT!', 'PODU SANDAI!')
for old_v in ('?v=20261101_smooth', '?v=20261104_face', '?v=20261107_real', '?v=20261104', '?v=20261117', '?v=20261118', '?v=20261119', '?v=20261120', '?v=20261125'):
    src = src.replace(old_v, '?v=20261126')

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(src)

print(f"Successfully patched {JS_PATH} ({len(src)} chars)")
