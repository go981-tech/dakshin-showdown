def apply(ctx):
    ctx.prepend(
        'import{populateSouthModels,loadSouthCharacter,buildMarinaStage,buildBusStandStage,buildDebateStudioStage,updateSouthStageHazards,upgradeSouthCrowd,updateSouthCrowd,triggerMemeOnAction,sayLine,spawnOratorSoundwave,triggerKootaniAssist,updateKootaniAssist,updateCensorBossMechanic,onCensorBossGrabBreak,pushFanWarComment,triggerPaalAbhishekam,computeBoxOfficeVerdict,cleanupSouthBattle}from"./south-kit.js?v=20261129";\n'
        'import{createSouthSuper}from"./south-supers.js?v=20261129";\n'
        'window.__local2P=!1;window.__selectedAssist=window.__selectedAssist||"sumo";window.__censorLock=null;window.__marinaWaveSlip=!1;window.__lastMatchStats=null;\n',
        "prepend south-kit & south-supers imports",
    )
    ctx.prepend(
        'import"./debug-dialogue.js?v=20261129";\n',
        "prepend live debug dialogue tools",
    )

    ctx.replace_span(
        'function We(){if(!(typeof window>`u`||He)){',
        'He=e.gtag}',
        'function We(){if(!(typeof window>`u`||He)){He=()=>{};',
        "We GA disable",
        include_end=True,
    )
