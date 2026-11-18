def apply(ctx):
    # 7b. Stalin Anna Sakthi (aa) speech + popup
    ctx.replace_exact(
        '!this.impactDone&&o>=this.IMPACT&&(this.impactDone=!0,this.impactPoint.copy(u.root.position),this.landSuperHit(r.target.hp,c,4.6,8.5)',
        'o>=.35&&o<2.4&&!this._s1&&(this._s1=!0,r.speech(`caster`,`Ungalil Oruvan! Vidiyal Aatchi!`),r.popup(`DRAVIDIAN MODEL!`,this.v2.set(s.x,2.6,.3),`#e11d48`)),!this.impactDone&&o>=this.IMPACT&&(this.impactDone=!0,r.speech(`caster`,`Kalaiyrom, Kizhikkrom! Naadu Namadhe!`),this.impactPoint.copy(u.root.position),this.landSuperHit(r.target.hp,c,4.6,8.5)',
        'aa Stalin Sakthi meme speeches',
    )

    # 7c. Vijay Sakthi (Nl) speech
    ctx.replace_exact('t.fillText(`ALOO`,130,82)', 't.fillText(`SCRIPT`,125,82)', 'Nl SCRIPT')
    ctx.replace_exact('t.fillText(`SONA`,385,82)', 't.fillText(`1000CR`,382,82)', 'Nl 1000CR')
    ctx.replace_exact('Ek aisi machine lagaunga...', 'En nenjil kudiyirukkum thozhargale!', 'Vijay Sakthi line 1')
    ctx.replace_exact('Is side se aloo ghusega...', 'What bro, it\'s very wrong bro!', 'Vijay Sakthi line 2')
    ctx.replace_exact('...us side se SONA niklega!', '...1000CR Bloody Sweet! I am waiting!', 'Vijay Sakthi line 3')

    # 7d. Jayalalithaa Sakthi (didi) speech + frog reaction + toss items
    ctx.replace_exact('r.speech(`caster`,`Jadu hobe!`)', 'r.speech(`caster`,`Naan Ninaithal...!`)', 'Jayalalithaa super start')
    ctx.replace_exact('r.speech(`caster`,`Jadu hoye gelo!`)', 'r.speech(`caster`,`Makkalal Naan, Makkalukkagave Naan!`)', 'Jayalalithaa super finish')
    ctx.replace_exact('e.k>.7?`HUMBA HUMBA!`:`HUMBA!`', 'e.k>.7?`IRATTAI ILAI!`:`AMMA AATCHI!`', 'Jayalalithaa chant')
    ctx.replace_exact('[`CHAPPAL!`,Es(1.4)],[`ROSOGOLLA!`,o],[`BALLOT PAPER!`,s]', '[`MIXIE!`,Es(1.4)],[`LADDOO!`,o],[`LAPTOP!`,s]', 'Amma scheme toss items')
    ctx.replace_exact(
        'f.char.id===`modi`?`Yeh kaun sa jadu hai?!`:f.char.id===`trump`?`Witch hunt! Total witch hunt!`:f.char.id===`yogi`?`Yeh kaisa jadu-tona hai?!`:`Bhai, yeh toh jadu hai!`',
        '{modi:`Idhu enna maayam Amma?!`,rahul:`What bro, frog bro?!`,trump:`Flower illa, thavalai aakittaanga!`,yogi:`Kadakku... ribbit?!`,nitin:`Operation failed!`,ravi:`Thavalai style lo kotteddama?!`,lalu:`Thambi! Frog curry-aa?!`,mbapu:`Science illa, frog magic!`,amit:`Enna sir frog ithu?!`,dhruv:`Hello MG Squad, frog-aayitten!`}[f.char.id]??`Amma magic!`',
        'Jayalalithaa frog reactions',
    )

    # 7e. Allu Arjun Pushpa Sakthi (trump) + Seized stamp
    ctx.replace_exact('e.fillText(`EXECUTIVE ORDER`,192,78)', 'e.fillText(`SYNDICATE ORDER`,192,78)', 'mc SYNDICATE ORDER')
    ctx.replace_exact('e.fillText(`TARIFF`,192,176)', 'e.fillText(`THAGGEDHE`,192,176)', 'mc THAGGEDHE')
    ctx.replace_exact('e.fillText(`50%`,192,272)', 'e.fillText(`100%`,192,272)', 'mc 100%')
    ctx.replace_exact('e.fillText(`TARIFFED`,256,132)', 'e.fillText(`SEIZED!`,256,132)', 'hc SEIZED')
    ctx.replace_exact('`TARIFF STAMP!`', '`THAGGEDHE LE!`', 'Pushpa stamp popup')
    ctx.replace_exact(
        '!_&&g(.15)&&r.speech(`caster`,`Tariff time!`),!_&&g(o-.4)&&r.speech(`caster`,`Beautiful, isn\'t it?`),!_&&g(c+.2)&&r.speech(`caster`,`Fifty percent. Tremendous!`)',
        'g(.15)&&r.speech(`caster`,`Pushpa ante flower anukunnava?!`),g(o-.4)&&r.speech(`caster`,`FIREUUU! Wildfellow!`),g(c+.2)&&r.speech(`caster`,`Thaggedhe Le! Rapa Rapa!`)',
        'Allu Arjun Pushpa Sakthi lines',
    )
    ctx.replace_exact(
        '{modi:`Mitron... yeh kya aa raha hai?!`,rahul:`Bhai, yeh tariff nahi, tsunami hai!`,didi:`Ei! Eta ki tariff?!`,trump:`Fake tariff!`,yogi:`Tariff? Hum swadeshi hain!`,nitin:`Tariff se pehle toll toh bharo!`,mbapu:`Shanti apnao, tariff bhulao!`,ravi:`Tariff? Paisa toh mere peeche aata hai!`,lalu:`Tariff? Railway mein toh concession milta hai!`,amit:`Tariff? Iski bhi chronology hai!`,dhruv:`Tariff? Iska poora explainer banega!`}[m.char.id]',
        '{modi:`Idhu sandalwood tsunami-ya?!`,rahul:`Wrong bro! Pushpa crate bro!`,didi:`Ayyo red sandal storm!`,trump:`Wildfire bidda!`,yogi:`Kerala forest crates?!`,nitin:`Highway toll kattu Pushpa!`,mbapu:`Rationalise this stamp!`,ravi:`Pushpa vs Power Star!`,lalu:`Sandal wood cut pannaadhe!`,amit:`Customs file open aayiduchu!`,dhruv:`Hello MG Squad — crate-a paaru!`}[m.char.id]',
        'Pushpa target reactions',
    )
    ctx.replace_exact('[`TARIFF!`,`TARIFF!!`,`50%!`,`HUGE!`,`TARIFF!`,`TREMENDOUS!`]', '[`THAGGEDHE!`,`FIREUU!`,`RAPA RAPA!`,`WILDFIRE!`,`1000 CR!`,`BIDDA!`]', 'Pushpa chants')

    # 7f. Pinarayi Vijayan SilverLine Dozer Sakthi (yogi)
    ctx.replace_exact(
        '!y&&v(.12)&&r.speech(`caster`,`Shaanti…`),v(o)&&r.speech(`caster`,`Site clear karo!`),v(s+.35)&&r.speech(`target`,{modi:`Arre, yeh bulldozer kiska hai?!`,rahul:`Bhai, bulldozer?! Seriously?!`,didi:`Ei! Bulldozer thamao!`,trump:`Is that a... bulldozer?!`,yogi:`Mera hi bulldozer?!`,nitin:`Bulldozer? Mere highway pe?!`,ravi:`Bulldozer? Shooting ka set mat todo!`,lalu:`Bulldozer? Patri pe mat chadhao!`,mbapu:`Bulldozer nahi, shanti chahiye!`,amit:`Bulldozer? Yeh chaal maine nahi chali!`,dhruv:`Bulldozer?! Doston, yeh dekho!`}[g.char.id])',
        'v(.12)&&r.speech(`caster`,`Chillu-nnu iru…`),v(o)&&r.speech(`caster`,`KADAKKU PURATHU!`),v(s+.35)&&r.speech(`target`,{modi:`Metro work-aa Captain?!`,rahul:`Dozer bro, very wrong bro!`,didi:`Stop that SilverLine dozer!`,trump:`Thaggedhe... bulldozer?!`,yogi:`LDF varum!`,nitin:`Naan flyover podren, neenga idikkireenga!`,ravi:`Set damage aithundhi!`,lalu:`Thambi, road-a thondadhe!`,mbapu:`Pagutharivu dozer!`,amit:`Permission vaanguneengala Captain?!`,dhruv:`Vlog break — SilverLine vandhuduchu!`}[g.char.id])',
        'Pinarayi Sakthi lines',
    )
    ctx.replace_exact('r.speech(`caster`,`Kaam chalu hai!`)', 'r.speech(`caster`,`LDF Varum, Ellam Sheri Aakum!`)', 'Pinarayi end line')

    # 7g. D. K. Shivakumar Sakthi (nitin)
    ctx.replace_exact('Gaddha-mukt Bharat... ek minute.', 'Kanakapura Bande... ondu nimisha!', 'DKS super line 1')
    ctx.replace_exact('Arre arre... yeh gaddha kahan se aaya?!', 'Ayyo Silk Board pothole-aa idhu?!', 'DKS super hole 1')
    ctx.replace_exact('Arey pothole!!', 'Outer Ring Road pit!!', 'DKS super hole 2')
    ctx.replace_exact('Quality ka koi compromise nahi!', 'Operation Success — 5 Guarantees!', 'DKS walk away line')

    # 7h. Pawan Kalyan Sakthi (ravi)
    ctx.replace_exact(
        'r.clipTime()===null&&p(.1)&&r.speech(`caster`,`Money follows, brother!`),p(o+.9)&&r.speech(`caster`,`Main nahi bhaagta, yeh mere peeche aata hai!`)',
        'p(.1)&&r.speech(`caster`,`Cheppanu Brother — Seize the Ship!`),p(o+.9)&&r.speech(`caster`,`Naaku konchem thikka undhi, daniko lekka undhi!`)',
        'Pawan Kalyan Sakthi lines',
    )
    ctx.replace_exact('Arre! Main hil kyun nahi pa raha?!', 'Ayyo! Time freeze aayiducha?!', 'PK freeze target')
    ctx.replace_exact('`TIME IS MONEY!`', '`100% STRIKE RATE!`', 'PK dragon banner')

    # 7i. Seeman Sakthi (lalu)
    ctx.replace_exact('e.fillText(`संसद जंक्शन`,256,68)', 'e.fillText(`சென்னை எழும்பூர்`,256,68)', 'tu tamil station')
    ctx.replace_exact('e.fillText(`SANSAD JN.`,256,148)', 'e.fillText(`EGMORE JN.`,256,148)', 'tu EGMORE JN')
    ctx.replace_exact('e.fillText(`RAIL RAJA`,256,52)', 'e.fillText(`VAIGAI EXP`,256,52)', 'nu VAIGAI EXP')
    ctx.replace_exact('Yatrigan kripya dhyan dein!', 'Thambi! Aamai Kari saapittiya?!', 'Seeman train line 1')
    ctx.replace_exact('Chai garam, gaadi time pe!', 'Idhu Uruttu illa da — Vaigai Superfast Express!', 'Seeman train line 2')
    ctx.replace_exact('Arre! Gaadi aa rahi hai?!', 'Ayyo! Vaigai Express varuthu!!', 'Seeman target reaction')
    ctx.replace_exact('`RAIL RAJA EXPRESS!`', '`AAMAI KARI EXPRESS!`', 'Seeman train popup 1')
    ctx.replace_exact('`NO WAITING LIST!`', '`ZERO URUTTU!`', 'Seeman train popup 2')

    # 7j. Periyar Sakthi (mbapu)
    ctx.replace_exact('n.speech(`caster`,`Manch khaali karo!`)', 'n.speech(`caster`,`Venkaya! Pagutharivu Thee!`)', 'Periyar super line')
    ctx.replace_exact('`MANCH CHHODO!`', '`PAGUTHARIVU CHAKRA!`', 'Periyar popup 1')
    ctx.replace_exact('`SHANTI CHAKKA!`', '`TORCH WHEEL!`', 'Periyar popup 2')
    ctx.replace_exact('`SHANTI TOOFAN!`', '`SUYAMARIYADHAI!`', 'Periyar popup 3')

    # 7k. Annamalai Press Meet Sakthi (amit)
    ctx.replace_exact('$u=[`KYA`,`BAAT`,`KAR`,`RAHE HO`,`AAP?!`]', '$u=[`NAAN`,`SOLREN`,`KEKURINGALA`,`ENNA`,`SIR?!`]', '$u NAAN SOLREN')
    ctx.replace_exact('n.speech(`caster`,`Shah-maat.`)', 'n.speech(`caster`,`En Mann En Makkal — Checkmate!`)', 'Annamalai checkmate speech')
    ctx.replace_exact('word:`DHISHUM!`', 'word:`RAFALE!`', 'Annamalai word 1')
    ctx.replace_exact('word:`THAPPAD!`', 'word:`SECRET FILE!`', 'Annamalai word 2')
    ctx.replace_exact('word:`GHOONSA!`', 'word:`PRESS MEET!`', 'Annamalai word 3')
    ctx.replace_exact('word:`DHAPP!`', 'word:`EXPOSED!`', 'Annamalai word 4')
    ctx.replace_exact('`DAL-BADAL!`', '`PRESS MEET!`', 'Annamalai popup 1')
    ctx.replace_exact('`JAAN DE DENGE!`', '`CASE FILED!`', 'Annamalai popup 2')
    ctx.replace_exact('`GHAR MANTRI! GHAR MANTRI!`', '`FILES IPS! FILES IPS!`', 'Annamalai fan chant')
    ctx.replace_exact('`DHAI GHAR KI CHAAL!`', '`WRITE IT DOWN!`', 'Annamalai knight charge')
    ctx.replace_exact('`SHAH-MAAT!`', '`CHECKMATE SIR!`', 'Annamalai checkmate popup')
    ctx.replace_exact('Dekho, mere supporters aa gaye!', 'Dey! En aalunga varanga!', 'Annamalai target supporters')
    ctx.replace_exact('Arre! Tum log toh mere the!', 'Dei! Neengellam en katchi da!', 'Annamalai target betrayal')
    ctx.replace_exact('Arre, utaaro mujhe!', 'Ayyo, keela irakkunga da!', 'Annamalai target hoist')

    # 7l. Squad Bro Sakthi (dhruv)
    ctx.replace_exact('gd=[`KAL`,`PARSO`,`AGLE HAFTE`,`KABHI NAHI`]', 'gd=[`HELLO`,`SQUAD BRO`,`WIKIPEDIA`,`PART 2`]', 'gd Madan Gowri calendar')
    ctx.replace_exact('t.fillText(`TO-DO: LADAI`,128,23)', 't.fillText(`TODAY TOPIC`,128,23)', 'xd Madan Gowri card')
    ctx.replace_exact('t.fillText(`@factbhai`,36,e+890)', 't.fillText(`@squadbro_yt`,36,e+890)', 'Sd @squadbro_yt')
    ctx.replace_exact('t.fillText(`aaj mood nahi... #relax`,36,e+936)', 't.fillText(`wikipedia summary... #squadbro`,36,e+936)', 'Sd #squadbro')
    ctx.replace_exact('`MOOD: OFF`', '`THUMBNAIL: RED`', 'MG thumbnail popup')
    ctx.replace_exact('`KAL DEKHTE HAIN!`', '`HELLO SQUAD BRO!`', 'MG greeting popup')
    ctx.replace_exact('`REELS TIME!`', '`VIDEO TIME!`', 'MG reels popup')
    ctx.replace_exact('`DOOMSCROLLED!`', '`MG ROASTED!`', 'MG slam popup')
    ctx.replace_exact('`GERMAN SHEPHERD REELS!`', '`RAJAPALAYAM REELS!`', 'MG hounds popup')

    # 7m. Nirmala GST Maami popup & immediate arrival alert
    ctx.replace_exact('`"Sabka hissa banta hai, Bapu!"`', '`"Popcorn-ukkum 18% GST! Cream Bun-ukkum GST!"`', 'Ca Nirmala popcorn quote')
    ctx.replace_exact(
        'm(i)&&r.audio.stampSlam()',
        'm(i)&&(r.audio.stampSlam(),r.popup(`"Popcorn-ukkum 18% GST!"`,this.v1.set(this.nx,2.15,.6),`#facc15`))',
        'Ca Nirmala arrival popcorn popup',
    )

    # 7n. Zo Idle Taunts & Grapple Dialogues (13 fighters)
    new_zo = 'Zo={modi:[`Morning walk mudinjathu, sandai-ku vaa!`,`Kalaiyrom, Kizhikkrom — ready-aa?`,`Dravidian Model defense paakuriya?`],rahul:[`What bro, still waiting bro! It\'s very wrong bro!`,`En nenjil kudiyirukkum opponent, attack pannu!`,`Kutty story sollalamaa?`],didi:[`Naan ninaithal one punch-la mudichiduven!`,`Fort St. George gate open-aa irukku, vaa!`,`Amma discipline teriyuma?`],trump:[`Flower nu nenachikitiya? Fire da!`,`Thaggedhe Le! Rapa Rapa!`,`Part 3 shooting poguma, illa adippiya?`],yogi:[`Kadakku purathu — step forward!`,`Chillu-nnu iru, aprom fight pannu!`,`Lal Salam! Red flag paathiya?`],nitin:[`Silk Board signal-la maatikitiya?`,`Kanakapura Bande waiting here, banni!`,`5 Guarantees-la punch free! Guarantee!`],ravi:[`Cheppanu brother! Step munde vey!`,`Seize the Ship! Slow-motion vendam!`,`Naaku thikka lesindhi, ready avvu!`],lalu:[`Thambi! Aamai kari saapittiya illaiya?!`,`Vaigai Express miss aagidum, vaa thambi!`,`Idhu uruttu illa, history! Stage-ku vaa!`],amit:[`Naan solren kekuringala?! Chronology paaru!`,`Rafale watch timer odudhu, seekiram vaa!`,`DMK Files open pannatta?`],dhruv:[`Hello Squad Bro! Opponent offline pola!`,`Wikipedia tab open panni wait panren!`,`Like, share, adichu kaattu!`],mbapu:[`Vengayam! அறிவோடு சிந்தி, அப்புறம் அடி!`,`Question blind hype, then throw a punch!`,`Suyamariyadhai never stalls!`]}'
    ctx.replace_span('Zo={modi:', ';function Qo(', new_zo + ';function Qo(', 'Zo South taunts', include_end=True)
    ctx.replace_exact('Suyamariyadhai never stalls!`]}', 'Suyamariyadhai never stalls!`],nirmala:[`Popcorn-ukkum 18% GST!`,`Cream bun-ukkum GST!`,`Audit ready-aa?`],rangaraj:[`Point-ku vaanga!`,`Kelvikku enna bathil?!`,`Mic mute pannidatta?!`]}', 'Zo 13 fighters')

    ctx.replace_exact('`Gale milo, mitron!`', '`Ungalil Oruvan Hug!`', 'Modi hug grapple')
    ctx.replace_exact('`Wrist lock!`', '`Audio Launch Lock!`', 'Wrist lock grapple')
    ctx.replace_exact('`Ei! Shono!`', '`Naan Ninaithal!`', 'Didi slap grapple')
    ctx.replace_exact('[`THAPPAD!`,`CHATAAK!`,`THAPPAD!`]', '[`AMMA SLAP!`,`PADAYATRA!`,`ARAI!`]', 'Didi slap popups')
    ctx.replace_exact('`Great to see you!`', '`Wildfire Handshake!`', 'Allu Arjun handshake')
    ctx.replace_exact('start:`Great Patki!`,first:`PATKI!`,next:`PHIR SE!`,last:`GREAT PATKI!`', 'start:`Vengayam! Pagutharivu!`,first:`LOGIC!`,next:`EQUALITY!`,last:`REFORM SLAM!`', 'Periyar grapple')
    ctx.replace_exact('start:`Dhobi pachhad!`,first:`DHOBI PACHHAD!`,next:`DHOBI PACHHAD!`,last:`DHOBI PACHHAD!`', 'start:`Thambi Aamai Kari!`,first:`URUTTU!`,next:`AAMAI KARI!`,last:`MIKE SET SLAM!`', 'Seeman grapple')
    ctx.replace_exact(
        'ec={rahul:{pair:`shackle`,rate:1.05,release:3.35,end:3.75,start:`Aikido, bhai!`,ouch:`Aah, haath!`,beats:[{at:1.75,word:`TWIST!`,power:.3},{at:2.7,word:`KHATA-KHAT!`,power:.7},{at:3.3,word:`AIKIDO FATAFAT!`,power:1}]},yogi:{pair:`slammer`,rate:1.25,release:6,end:6.3,start:`Bulldozer chalega!`,ouch:`Arre, utaro mujhe!`,beats:[{at:4.6,word:`UTHA!`,power:.3},{at:5.4,word:`PALAT!`,power:.4},{at:5.95,word:`BULLDOZER SLAM!`,power:1}]},nitin:{pair:`takedown`,rate:1,release:1.6,end:2.6,start:`Road roller aa raha hai!`,ouch:`Arre, rukiye!`,beats:[{at:.85,word:`TOLL FREE!`,power:.3},{at:1.55,word:`HIGHWAY TAKEDOWN!`,power:1}]},ravi:{pair:`upper`,rate:.75,release:2,end:2.4,start:`Dekh, hero ki entry!`,ouch:`Nahi, hero nahi!`,beats:[{at:1.3,word:`DHISHOOM!`,power:.7},{at:1.98,word:`FILMY UPPERCUT!`,power:1}]},amit:{pair:`takedown`,rate:1,release:1.6,end:2.6,start:`Ghera daal do!`,ouch:`Arre, yeh kaisa ghera?!`,beats:[{at:.85,word:`GHERA!`,power:.3},{at:1.55,word:`Z-PLUS TAKEDOWN!`,power:1}]},dhruv:{pair:`shackle`,rate:1.05,release:3.35,end:3.75,start:`Ruko, pehle source batao!`,ouch:`Aah, mera haath!`,beats:[{at:1.75,word:`SOURCE?!`,power:.3},{at:2.7,word:`FACT #1!`,power:.7},{at:3.3,word:`FACT-CHECK LOCK!`,power:1}]}}',
        'ec={rahul:{pair:`shackle`,rate:1.05,release:3.35,end:3.75,start:`What bro! Very wrong bro!`,ouch:`Ayyo Thalapathy!`,beats:[{at:1.75,word:`VERITHANAM!`,power:.3},{at:2.7,word:`BLOODY SWEET!`,power:.7},{at:3.3,word:`BOX OFFICE SLAM!`,power:1}]},yogi:{pair:`slammer`,rate:1.25,release:6,end:6.3,start:`Kadakku purathu!`,ouch:`Ayyo Captain!`,beats:[{at:4.6,word:`LAL SALAM!`,power:.3},{at:5.4,word:`SILVERLINE!`,power:.4},{at:5.95,word:`COMRADE SLAM!`,power:1}]},nitin:{pair:`takedown`,rate:1,release:1.6,end:2.6,start:`Resort bus-ge hattu!`,ouch:`Ayyo Silk Board!`,beats:[{at:.85,word:`BANDE!`,power:.3},{at:1.55,word:`FLYOVER TAKEDOWN!`,power:1}]},ravi:{pair:`upper`,rate:.75,release:2,end:2.4,start:`Seize the Ship!`,ouch:`Ayyo Power Star!`,beats:[{at:1.3,word:`CHEPPANU BRO!`,power:.7},{at:1.98,word:`OG UPPERCUT!`,power:1}]},amit:{pair:`takedown`,rate:1,release:1.6,end:2.6,start:`Naan solren kekuringala?!`,ouch:`Enna sir file-a?!`,beats:[{at:.85,word:`FILE #1!`,power:.3},{at:1.55,word:`PRESS MEET LOCK!`,power:1}]},dhruv:{pair:`shackle`,rate:1.05,release:3.35,end:3.75,start:`Hello MG Squad! Source idho!`,ouch:`Aah thumbnail!`,beats:[{at:1.75,word:`WIKIPEDIA!`,power:.3},{at:2.7,word:`10M VIEWS!`,power:.7},{at:3.3,word:`COPYRIGHT STRIKE!`,power:1}]},nirmala:{pair:`takedown`,rate:1,release:1.6,end:2.6,start:`18% Popcorn Audit!`,ouch:`Ayyo tax slab!`,beats:[{at:.85,word:`18% GST!`,power:.3},{at:1.55,word:`28% CARAMEL SLAM!`,power:1}]},rangaraj:{pair:`shackle`,rate:1.05,release:3.35,end:3.75,start:`Kelvikku enna bathil?!`,ouch:`Mic muted!`,beats:[{at:1.75,word:`POINT-KU VAA!`,power:.3},{at:2.7,word:`MIC MUTED!`,power:.7},{at:3.3,word:`DEBATE LOCK!`,power:1}]}}',
        'ec grapples (13 fighters)',
    )

    # 13. GST Maami cinematic
    ctx.replace_exact('e.fillText(`BUDGET`,96,110)', 'e.fillText(`GST BILL`,96,110)', 'GST book title')
    ctx.replace_exact('e.fillText(`2026`,96,160)', 'e.fillText(`18% + CESS`,96,160)', 'GST book subtitle')
    ctx.replace_exact('r.popup(`GST ${e.rate}!`,', 'r.popup([`KAAPI 5%!`,`CREAM BUN 12%!`,`POPCORN 18%!`,`CESS 28%!`][t]??`GST ${e.rate}!`,', 'GST slab popups')
    ctx.replace_exact('r.popup(`TAX COLLECTED!`,', 'r.popup(`GST VASOOL!`,', 'GST collected banner')

    # 14. Bespoke Iconic South Movie & Incident Special Move Animations per Character
    ctx.replace_span(
        'function kd(e){',
        'var Ad=class{',
        'function kd(e){return createSouthSuper(e,{P,B,V,F,R,L})}var Ad=class{',
        'kd bespoke South Super animations',
        include_end=True,
    )
