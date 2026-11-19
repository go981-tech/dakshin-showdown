import { BoxGeometry, CylinderGeometry, Mesh, MeshStandardMaterial, SphereGeometry, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene, id) {
  const audioLaunch = (kind,duration,twist) => buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.44,duration*.68,duration],returnToClean:true,frames:[
    {time:.12,bones:{Hips:{rotation:[.08,.18,-.12]},Spine:{rotation:[-.14,-.20,.10]},Spine2:{rotation:[-.18,-.24,.12]},Neck:{rotation:[.08,-.14,.04]},LeftArm:{rotation:[.42,.18,.24]},LeftForeArm:{rotation:[0,.48,0]},LeftHand:{rotation:[.08,.08,.22]}},hips:[-.04,.02,0]},
    {time:.30,bones:{Hips:{rotation:[.12,.32,-.16]},Spine:{rotation:[-.24,-.36,.14]},Spine2:{rotation:[-.32,-.42,.16]},Neck:{rotation:[.12,-.20,.06]},RightArm:{rotation:[-.88,.22,-.52]},RightForeArm:{rotation:[0,-.92,0]},RightHand:{rotation:[.10,.10,-.32]},LeftArm:{rotation:[.62,-.28,.34]},LeftForeArm:{rotation:[0,.64,0]}},hips:[.04,.05,0]},
    {time:duration*.48,bones:{Hips:{rotation:[.16,.46,twist]},Spine:{rotation:[-.36,-.52,.18]},Spine2:{rotation:[-.46,-.60,.22]},Neck:{rotation:[.16,-.28,.08]},RightArm:{rotation:[-1.44,.32,-.68]},RightForeArm:{rotation:[0,-1.24,0]},RightHand:{rotation:[.16,.14,-.42]},LeftArm:{rotation:[.78,-.38,.44]},LeftForeArm:{rotation:[0,.78,0]},RightUpLeg:{rotation:[-.62,0,-.12]},RightLeg:{rotation:[.92,0,0]}},hips:[.12,.10,0]},
    {time:duration*.72,bones:{Hips:{rotation:[.06,.16,-.05]},Spine:{rotation:[-.12,-.18,.06]},Spine2:{rotation:[-.16,-.22,.08]},RightArm:{rotation:[-.54,.08,-.20]},RightForeArm:{rotation:[0,-.44,0]},LeftArm:{rotation:[.30,-.12,.14]},RightLeg:{rotation:[.32,0,0]}},hips:[.02,.02,0]}
  ]});
  return [
    audioLaunch("special1",.82,-.12),
    audioLaunch("special2",1.04,.18),
    buildCharacterClip(scene,{name:`south_super_${id}`,fighterId:id,kind:"super",duration:1.15,fxCleanupAt:[.46,.82,1.15],returnToClean:true,frames:[
      {time:.14,bones:{Hips:{rotation:[.08,.18,-.12]},Spine:{rotation:[-.14,-.20,.10]},Spine2:{rotation:[-.18,-.24,.12]},LeftArm:{rotation:[.58,-.26,.36]},LeftForeArm:{rotation:[0,.68,0]}},hips:[-.04,.02,0]},
      {time:.52,bones:{Hips:{rotation:[.18,.56,.24]},Spine:{rotation:[-.42,-.62,.22]},Spine2:{rotation:[-.52,-.72,.26]},Neck:{rotation:[.16,-.30,.08]},RightArm:{rotation:[-1.58,.34,-.76]},RightForeArm:{rotation:[0,-1.36,0]},RightHand:{rotation:[.16,.16,-.48]},LeftArm:{rotation:[.82,-.42,.48]},LeftForeArm:{rotation:[0,.86,0]},RightUpLeg:{rotation:[-.86,0,-.18]},RightLeg:{rotation:[1.28,0,0]}},hips:[.16,.14,.04]},
      {time:.82,bones:{Hips:{rotation:[.08,.18,-.08]},Spine:{rotation:[-.16,-.22,.08]},RightArm:{rotation:[-.68,.12,-.26]},RightForeArm:{rotation:[0,-.58,0]},LeftArm:{rotation:[.36,-.14,.18]},RightLeg:{rotation:[.38,0,0]}},hips:[.04,.04,0]}
    ]})
  ];
}
export function buildClips(scene) { return makeClips(scene,"rahul"); }
export function fx(battle, attacker, target, moveId) {
  const color=0xffd700;
  return spawnTransientFx(battle,560,{attacker,target,create:(root,{dir,ax,ay})=>{
    const mat=new MeshStandardMaterial({color,emissive:color,emissiveIntensity:1,metalness:.7,roughness:.2});
    const mic=new Mesh(new CylinderGeometry(.035,.035,.38,10),mat); mic.rotation.z=Math.PI/2;
    const head=new Mesh(new SphereGeometry(.12,12,10),mat);
    head.position.x=dir*.22; mic.position.x=dir*.08; root.add(mic,head);
    root.position.set(ax+dir*.5,ay+.2,.35);
  }},(root,p,{dir})=>{root.position.x+=(dir*(p*.018));root.rotation.z=p*4*dir;root.scale.setScalar(.85+p*.55);});
}
