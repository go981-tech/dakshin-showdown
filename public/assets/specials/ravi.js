import { BoxGeometry, Mesh, MeshBasicMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const punch=(kind,duration)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.44,duration*.68,duration],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.06,-.18,-.08]},Spine:{rotation:[-.1,.24,-.08]},Spine2:{rotation:[-.14,.28,-.1]},LeftArm:{rotation:[.36,-.26,.22]},LeftForeArm:{rotation:[0,.54,0]}},hips:[-.04,.02,0]},
  {time:.30,bones:{Hips:{rotation:[.12,-.34,-.14]},Spine:{rotation:[-.22,.38,-.12]},Spine2:{rotation:[-.28,.44,-.14]},Neck:{rotation:[.08,-.18,.04]},RightArm:{rotation:[-.74,.18,-.48]},RightForeArm:{rotation:[0,-.82,0]},RightHand:{rotation:[.08,.08,-.28]},LeftArm:{rotation:[.58,-.38,.36]},LeftForeArm:{rotation:[0,.66,0]}},hips:[.04,.05,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.16,-.52,-.18]},Spine:{rotation:[-.34,.56,-.16]},Spine2:{rotation:[-.42,.64,-.18]},Neck:{rotation:[.14,-.28,.06]},RightArm:{rotation:[-1.48,.28,-.74]},RightForeArm:{rotation:[0,-1.28,0]},RightHand:{rotation:[.12,.12,-.42]},LeftArm:{rotation:[.72,-.42,.44]},LeftForeArm:{rotation:[0,.76,0]},RightUpLeg:{rotation:[-.72,0,-.14]},RightLeg:{rotation:[1.02,0,0]}},hips:[.12,.10,0]},
  {time:duration*.72,bones:{Hips:{rotation:[.06,-.18,-.06]},Spine:{rotation:[-.12,.22,-.06]},RightArm:{rotation:[-.62,.12,-.24]},RightForeArm:{rotation:[0,-.52,0]},LeftArm:{rotation:[.32,-.18,.18]},RightLeg:{rotation:[.38,0,0]}},hips:[.02,.02,0]}
 ]});
 const kick=buildCharacterClip(scene,{name:`south_special2_${id}`,fighterId:id,kind:"special2",duration:1.04,fxCleanupAt:[.48,.78,1.04],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.08,.18,.08]},Spine:{rotation:[-.12,-.2,.08]},Spine2:{rotation:[-.16,-.24,.1]},LeftArm:{rotation:[.42,.18,.24]},LeftForeArm:{rotation:[0,.52,0]}},hips:[-.02,.02,0]},
  {time:.34,bones:{Hips:{rotation:[.12,.32,.14]},Spine:{rotation:[-.26,-.38,.12]},Spine2:{rotation:[-.34,-.44,.14]},RightArm:{rotation:[-.42,.12,-.28]},RightForeArm:{rotation:[0,-.44,0]},RightUpLeg:{rotation:[-.9,0,-.18]},RightLeg:{rotation:[1.18,0,0]}},hips:[.08,.08,0]},
  {time:.52,bones:{Hips:{rotation:[.18,.44,.18]},Spine:{rotation:[-.38,-.48,.16]},Spine2:{rotation:[-.48,-.56,.18]},Neck:{rotation:[.12,-.24,.05]},RightArm:{rotation:[-.28,.18,-.16]},RightForeArm:{rotation:[0,-.28,0]},RightUpLeg:{rotation:[-1.55,0,-.24]},RightLeg:{rotation:[1.55,0,0]},LeftUpLeg:{rotation:[-.28,0,.08]},LeftLeg:{rotation:[.42,0,0]}},hips:[.14,.12,.06]},
  {time:.78,bones:{Hips:{rotation:[.06,-.12,-.04]},Spine:{rotation:[-.12,.16,-.04]},RightArm:{rotation:[-.48,.08,-.2]},RightForeArm:{rotation:[0,-.42,0]},RightLeg:{rotation:[.42,0,0]}},hips:[.02,.02,0]}
 ]});
 return [punch("special1",.82),kick,buildCharacterClip(scene,{name:`south_super_${id}`,fighterId:id,kind:"super",duration:1.15,fxCleanupAt:[.46,.82,1.15],returnToClean:true,frames:[
  {time:.16,bones:{Hips:{rotation:[.08,-.22,.12]},Spine:{rotation:[-.16,.28,.12]},Spine2:{rotation:[-.22,.34,.14]},LeftArm:{rotation:[.64,-.38,.42]},LeftForeArm:{rotation:[0,.72,0]}},hips:[-.04,.02,0]},
  {time:.52,bones:{Hips:{rotation:[.18,-.58,.24]},Spine:{rotation:[-.42,.68,.18]},Spine2:{rotation:[-.52,.78,.2]},Neck:{rotation:[.16,-.32,.08]},RightArm:{rotation:[-1.62,.32,-.82]},RightForeArm:{rotation:[0,-1.36,0]},RightHand:{rotation:[.18,.16,-.48]},LeftArm:{rotation:[.82,-.46,.48]},LeftForeArm:{rotation:[0,.86,0]},RightUpLeg:{rotation:[-.92,0,-.18]},RightLeg:{rotation:[1.32,0,0]}},hips:[.16,.14,.04]},
  {time:.82,bones:{Hips:{rotation:[.08,-.22,.08]},Spine:{rotation:[-.16,.26,.08]},RightArm:{rotation:[-.72,.14,-.28]},RightForeArm:{rotation:[0,-.58,0]},LeftArm:{rotation:[.36,-.16,.18]},RightLeg:{rotation:[.38,0,0]}},hips:[.04,.04,0]}
 ]})];
}
export function buildClips(scene){return makeClips(scene,"ravi");}
export function fx(battle,attacker,target,moveId){
 const color=0xff0044;
 return spawnTransientFx(battle,650,{attacker,target,create:(root,{dir,tx,ty})=>{
  const mat=new MeshBasicMaterial({color,transparent:true,opacity:.72});
  for(let i=0;i<4;i++){const ring=new Mesh(new TorusGeometry(.35+i*.19,.035,8,24),mat);ring.rotation.x=Math.PI/2;ring.position.y=i*.08;root.add(ring);}
  for(let i=0;i<8;i++){const shard=new Mesh(new BoxGeometry(.12,.04,.04),mat);const a=i*Math.PI/4;shard.position.set(Math.cos(a)*.5,Math.sin(a)*.28,.14);shard.rotation.z=a;root.add(shard);}
  root.position.set(tx,ty-.28,.26);
 }},(root,p)=>{root.scale.setScalar(.7+p*1.9);root.rotation.z+=.22*(moveId==="super"?1.8:1);});
}
