def apply(ctx):
    # 3. Overhaul 3D Arenas: Marina Beach, Koyambedu Bus Stand, Arangam Debate Studio
    ctx.replace_exact(
        'qt={sansad:{name:`SANSAD BHAVAN`,subtitle:`Parliament at sunset`},jantar:{name:`JANTAR MANTAR`,subtitle:`Protest ground, New Delhi`},road:{name:`DESI SADAK`,subtitle:`Gali, thela aur traffic`}}',
        'qt={marina:{name:`MARINA BEACH`,subtitle:`Marina Lighthouse, Sundal Carts & 20s Ocean Wave`},jantar:{name:`KOYAMBEDU BUS STAND`,subtitle:`Green Govt Buses & Corner Auto-Rickshaw Bounce`},road:{name:`ARANGAM DEBATE STUDIO`,subtitle:`Neon Circular Floor & Giant MIC MUTED LED Screens`},sansad:{name:`MARINA BEACH`,subtitle:`Marina Lighthouse, Sundal Carts & 20s Ocean Wave`}}',
        'qt stages',
    )

    ctx.replace_exact(
        'Jt={sansad:{skyTop:1780314,skyMid:15232828,skyBottom:16762739,fog:15310950,fogNear:28,fogFar:75,ground:9071178,platformSide:9190174,sunColor:16766624,sunIntensity:2.6,sunPos:[-6,12,9],hemiSky:16769728,hemiGround:5913386,hemiIntensity:1.25,sunDisc:[-30,9,-80],sunDiscColor:16773572,exposure:1.05,floorRoughness:.62},jantar:{skyTop:3108804,skyMid:9683690,skyBottom:15916992,fog:14207922,fogNear:35,fogFar:110,ground:6130234,platformSide:11028282,sunColor:16773592,sunIntensity:2.8,sunPos:[7,16,10],hemiSky:14478335,hemiGround:7033398,hemiIntensity:1.3,sunDisc:[45,38,-90],sunDiscColor:16776168,exposure:.95,floorRoughness:.9},road:{skyTop:8364996,skyMid:14206882,skyBottom:15389606,fog:13481100,fogNear:22,fogFar:70,ground:7233873,platformSide:4144442,sunColor:16769712,sunIntensity:2.5,sunPos:[-8,14,9],hemiSky:15852228,hemiGround:5917240,hemiIntensity:1.3,sunDisc:[-40,30,-90],sunDiscColor:16773320,exposure:1,floorRoughness:.95}}',
        'Jt={sansad:{skyTop:1139386,skyMid:2988248,skyBottom:16756578,fog:14935011,fogNear:32,fogFar:95,ground:15255434,platformSide:12887662,sunColor:16768682,sunIntensity:2.7,sunPos:[8,13,-12],hemiSky:14086143,hemiGround:13414762,hemiIntensity:1.3,sunDisc:[22,10,-85],sunDiscColor:16770452,exposure:1.05,floorRoughness:.82},marina:{skyTop:1139386,skyMid:2988248,skyBottom:16756578,fog:14935011,fogNear:32,fogFar:95,ground:15255434,platformSide:12887662,sunColor:16768682,sunIntensity:2.7,sunPos:[8,13,-12],hemiSky:14086143,hemiGround:13414762,hemiIntensity:1.3,sunDisc:[22,10,-85],sunDiscColor:16770452,exposure:1.05,floorRoughness:.82},jantar:{skyTop:2643854,skyMid:9090264,skyBottom:16114884,fog:13748674,fogNear:34,fogFar:105,ground:5263448,platformSide:3618615,sunColor:16773592,sunIntensity:2.65,sunPos:[6,15,10],hemiSky:14478335,hemiGround:5263440,hemiIntensity:1.3,sunDisc:[40,36,-90],sunDiscColor:16776168,exposure:1,floorRoughness:.9},road:{skyTop:395826,skyMid:922922,skyBottom:2361662,fog:922922,fogNear:24,fogFar:80,ground:526878,platformSide:1118496,sunColor:11197183,sunIntensity:2.3,sunPos:[0,12,10],hemiSky:6920703,hemiGround:1707562,hemiIntensity:1.25,sunDisc:[0,50,-90],sunDiscColor:2282478,exposure:1.08,floorRoughness:.35}}',
        'Jt South Indian arena lighting themes',
    )

    new_kolam = '''function $t(){return Yt(1024,1024,e=>{e.fillStyle=`#e4d8be`,e.fillRect(0,0,1024,1024);e.strokeStyle=`#9a2f20`;e.lineWidth=32;e.strokeRect(24,24,976,976);e.strokeStyle=`#f9fafb`;e.lineWidth=6;for(let t=-2;t<=2;t++)for(let n=-2;n<=2;n++){if(Math.abs(t)+Math.abs(n)<=2){e.beginPath(),e.arc(512+t*80,512+n*80,34,0,Math.PI*2),e.stroke();e.beginPath(),e.arc(512+t*80,512+n*80,6,0,Math.PI*2),e.fillStyle=`#fffef5`,e.fill()}}e.strokeStyle=`#ffd23f`;e.lineWidth=8;for(let r of[110,235,340]){e.beginPath(),e.arc(512,512,r,0,Math.PI*2),e.stroke()}})}'''
    ctx.replace_span('function $t(){', 'function en(){', new_kolam, '$t Tamil kolam floor')

    ctx.replace_exact(
        'function nn(){return Yt(192,128,e=>{e.fillStyle=`#ff9933`,e.fillRect(0,0,192,43),e.fillStyle=`#ffffff`,e.fillRect(0,43,192,42),e.fillStyle=`#138808`,e.fillRect(0,85,192,43),Xt(e,96,64,17,`#000080`)})}',
        'function nn(){return Yt(192,128,e=>{e.fillStyle=`#18181b`,e.fillRect(0,0,192,64),e.fillStyle=`#dc2626`,e.fillRect(0,64,192,64),e.fillStyle=`#facc15`,e.beginPath(),e.arc(96,64,22,Math.PI,0),e.fill(),e.strokeStyle=`#facc15`,e.lineWidth=4,e.strokeRect(4,4,184,120)})}',
        'nn South arena flags',
    )

    ctx.replace_exact(
        'buildSansad(e){let t=new O({color:14264186,roughness:.85}),n=new O({color:11763287,roughness:.9}),',
        'buildSansad(e){let t=new O({color:15987699,roughness:.82}),n=new O({color:14868962,roughness:.85}),',
        'Fort St. George white sandstone',
    )
    ctx.replace_exact(
        'let p=new O({color:13208674,roughness:.9}),m=new x;m.position.set(24,-.3,-46)',
        'let p=new O({color:11936806,roughness:.88}),m=new x;m.position.set(24,-.3,-46)',
        'Chennai Central red brick tower',
    )
    ctx.replace_exact('e.fillText(`JANTAR MANTAR`,256,62)', 'e.fillText(`MADURAI MEENAKSHI`,256,62)', 'Madurai stage sign title')
    ctx.replace_exact('e.fillText(`जंतर मंतर · NEW DELHI`,256,120)', 'e.fillText(`மதுரை · TAMIL NADU`,256,120)', 'Madurai stage sign sub')
    ctx.replace_exact(
        'function Ot(){let e=new x,t=Ct(3116858,.5,.2),n=Ct(16040960,.6),',
        'function Ot(){let e=new x,t=Ct(16435221,.5,.2),n=Ct(1579035,.6),',
        'Chennai yellow auto',
    )

    ctx.replace_exact(
        'i(this,`themeGroups`,{sansad:new x,jantar:new x,road:new x})',
        'i(this,`themeGroups`,{sansad:new x,jantar:new x,road:new x,marina:new x})',
        'sn themeGroups',
    )
    ctx.replace_exact(
        'this.group.add(this.themeGroups.sansad,this.themeGroups.jantar,this.themeGroups.road)',
        'this.group.add(this.themeGroups.sansad,this.themeGroups.jantar,this.themeGroups.road,this.themeGroups.marina)',
        'sn group add',
    )
    ctx.replace_exact(
        'this.floorTextures={sansad:$t(),jantar:en(),road:wt(Yt)}',
        'this.floorTextures={sansad:en(),jantar:wt(Yt),road:en(),marina:en()}',
        'sn floorTextures',
    )
    ctx.replace_exact(
        'this.buildSansad(this.themeGroups.sansad),this.buildJantarMantar(this.themeGroups.jantar),At(this.themeGroups.road)',
        'buildMarinaStage(this.themeGroups.sansad),buildMarinaStage(this.themeGroups.marina),buildBusStandStage(this.themeGroups.jantar),buildDebateStudioStage(this.themeGroups.road)',
        'sn buildStage South Indian 3D arenas',
    )
    ctx.replace_exact('this.setStage(`sansad`)', 'this.setStage(`marina`)', 'sn default stage marina')
    ctx.replace_exact('Gp=`sansad`,Kp=[`sansad`,`jantar`,`road`]', 'Gp=`marina`,Kp=[`marina`,`jantar`,`road`]', 'Gp and Kp stages list')

    ctx.replace_exact(
        'let h=[16750899,16777215,1280008,3054591,14688650,16765503,11022898,7031766],g=[9263675,11565650,13210736,7226668];',
        'let h=[16382457,16119285,14423100,1483594,16435252,186898,1579034,12131356],g=[8871746,10514756,12087888,6964522];',
        'South crowd color palette',
    )
    ctx.replace_exact(
        'this.group.add(this.crowd,this.crowdHeads);',
        'this.group.add(this.crowd,this.crowdHeads);upgradeSouthCrowd(this);',
        'Mount South crowd layers',
    )
    ctx.replace_exact(
        'this.crowd.instanceMatrix.needsUpdate=!0,this.crowdHeads.instanceMatrix.needsUpdate=!0,this.updatePlacards(e,t)',
        'this.crowd.instanceMatrix.needsUpdate=!0,this.crowdHeads.instanceMatrix.needsUpdate=!0,updateSouthCrowd(this,this.dummy),this.updatePlacards(e,t)',
        'Animate South crowd layers',
    )
    ctx.replace_exact(
        'this.samosas=new xe(new fe(.07,.11,3),new O({color:14263361,roughness:.7}),t)',
        'this.samosas=new xe(new D(.05,.042,.11,10),new O({color:13677636,roughness:.25,metalness:.7}),t)',
        'Replace samosas with Filter Kaapi tumblers',
    )
    ctx.replace_exact(
        'o=new O({color:a?16777215:1710620,map:a,roughness:.75}),s=ts(2764602,.85)',
        'o=new O({color:13989126,roughness:.75}),s=ts(16184558,.8)',
        'Kaapi Master white veshti outfit',
    )

    # 4. Crowd placards (an)
    new_an = '''an=[{pool:`neutral`,text:`VANAKKAM!`,bg:`#ffffff`,fg:`#c0392b`},{pool:`neutral`,text:`VETRI!`,bg:`#ffd23f`,fg:`#1a237e`},{pool:`neutral`,text:`MASS!`,bg:`#ff9933`,fg:`#ffffff`},{pool:`neutral`,text:`NAARKALI!`,bg:`#138808`,fg:`#ffffff`},{pool:`modi`,text:`SURYA ANNA`,bg:`#e11d48`,fg:`#ffffff`},{pool:`modi`,text:`CYCLE RALLY!`,bg:`#111827`,fg:`#facc15`},{pool:`modi`,text:`RISING SUN`,bg:`#dc2626`,fg:`#fef08a`},{pool:`rahul`,text:`THALAPATHY`,bg:`#b91c1c`,fg:`#fef08a`},{pool:`rahul`,text:`WHISTLE PODU`,bg:`#ffffff`,fg:`#b91c1c`},{pool:`rahul`,text:`1000CR MASS!`,bg:`#7f1d1d`,fg:`#fde047`},{pool:`didi`,text:`IRON AMMA!`,bg:`#15803d`,fg:`#ffffff`},{pool:`didi`,text:`TWO LEAVES`,bg:`#ffffff`,fg:`#15803d`},{pool:`didi`,text:`FORT ST GEORGE`,bg:`#065f46`,fg:`#d1fae5`},{pool:`trump`,text:`THAGGEDHE LE`,bg:`#ea580c`,fg:`#ffffff`},{pool:`trump`,text:`SANDAL RAJU`,bg:`#ffffff`,fg:`#c2410c`},{pool:`trump`,text:`WILDFIRE!`,bg:`#7c2d12`,fg:`#fed7aa`},{pool:`yogi`,text:`LAL CAPTAIN`,bg:`#dc2626`,fg:`#ffffff`},{pool:`yogi`,text:`LAL SALAM!`,bg:`#ffffff`,fg:`#991b1b`},{pool:`yogi`,text:`SILVERLINE`,bg:`#7f1d1d`,fg:`#fecaca`},{pool:`nitin`,text:`BANDE SHIV`,bg:`#0284c7`,fg:`#ffffff`},{pool:`nitin`,text:`5 GUARANTEES`,bg:`#ffffff`,fg:`#0369a1`},{pool:`nitin`,text:`SILK BOARD`,bg:`#0369a1`,fg:`#e0f2fe`},{pool:`ravi`,text:`POWER STAR`,bg:`#dc2626`,fg:`#ffffff`},{pool:`ravi`,text:`OG KATANA!`,bg:`#ffffff`,fg:`#b91c1c`},{pool:`ravi`,text:`FIRE STORM!`,bg:`#1e293b`,fg:`#f87171`},{pool:`lalu`,text:`PULI VOICE`,bg:`#b91c1c`,fg:`#fde047`},{pool:`lalu`,text:`TIGER ROAR`,bg:`#facc15`,fg:`#7f1d1d`},{pool:`lalu`,text:`MIKE SET!`,bg:`#111827`,fg:`#fde047`},{pool:`mbapu`,text:`SELF RESPECT`,bg:`#18181b`,fg:`#facc15`},{pool:`mbapu`,text:`RATIONALISM`,bg:`#facc15`,fg:`#18181b`},{pool:`mbapu`,text:`THATHA REFORM`,bg:`#27272a`,fg:`#ffffff`},{pool:`amit`,text:`FILES IPS!`,bg:`#f97316`,fg:`#ffffff`},{pool:`amit`,text:`PRESS MEET`,bg:`#ffffff`,fg:`#ea580c`},{pool:`amit`,text:`CASE CLOSED!`,bg:`#1e293b`,fg:`#fb923c`},{pool:`dhruv`,text:`SQUAD BRO`,bg:`#06b6d4`,fg:`#082f49`},{pool:`dhruv`,text:`RED ARROWS!`,bg:`#ffffff`,fg:`#0e7490`},{pool:`dhruv`,text:`10M VIEWS!`,bg:`#082f49`,fg:`#22d3ee`},{pool:`nirmala`,text:`TAX MAAMI`,bg:`#9333ea`,fg:`#ffffff`},{pool:`nirmala`,text:`28% GST!`,bg:`#facc15`,fg:`#581c87`},{pool:`rangaraj`,text:`POINT-KU VAA`,bg:`#0284c7`,fg:`#ffffff`},{pool:`rangaraj`,text:`MIC MUTED!`,bg:`#dc2626`,fg:`#fef08a`}]'''
    ctx.replace_span('an=[', '],on=', new_an[:-1], 'an crowd placards')

    # 12. Sutli Bomb -> SIVAKASI 1000-WALA VEDI
    ctx.replace_exact('let r=Za(9071162,0,.95),a=new v(new E(.2,18,14),r);this.bomb.add(a);', 'let r=Za(14423100,2621440,.5),a=new v(new E(.2,18,14),r);a.scale.set(1,1.18,1);this.bomb.add(a);', 'Vedi crimson body')
    ctx.replace_exact('new v(new Oe(.2,.012,6,24),Za(5914658,0,.9));e.rotation.set(Math.random()*Math.PI,Math.random()*Math.PI,0)', 'new v(new Oe(.2,.016,6,24),Za(16435252,3801088,.35));e.rotation.set(Math.PI/2+(Math.random()-.5)*.5,0,(Math.random()-.5)*.5),e.position.y=(Math.random()-.5)*.28', 'Vedi gold kasavu bands')
    ctx.replace_exact('new v(new D(.205,.205,.09,18),Za(14034984,3801088,.7))', 'new v(new D(.21,.21,.1,18),Za(1483594,0,.6))', 'Vedi green label band')
    ctx.replace_exact('this.ring=new v(new oe(1.34,eo,72),new S({color:16722458,', 'this.ring=new v(new oe(1.34,eo,72),new S({color:16435252,', 'Vedi gold danger ring')
    ctx.replace_exact('new v(new Re(1.34,72),new S({color:16722458,', 'new v(new Re(1.34,72),new S({color:16435252,', 'Vedi gold danger disc')
    ctx.replace_exact('let u=[14034984,16765803,16777215,2792778];', 'let u=[16435252,14423100,2282478,16777215,1483594];', 'Vedi festive confetti')
    ctx.sub_regex(r'`[^`]{0,8}SUTLI BOMB<small>Ring se bahar bhaago!</small>`', '`🧨 SIVAKASI VEDI!<small>Odu macha! 1000-Wala vedikkudhu!</small>`', 'Vedi announce', expected_count=1)
    ctx.sub_regex(r't\.speech\(`SSSS[^`]*`', 't.speech(`Chata-pata! Sivakasi vedi! 🧨`', 'Vedi hiss', expected_count=1)
