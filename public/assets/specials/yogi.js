import { BoxGeometry, CylinderGeometry, Mesh, MeshBasicMaterial, MeshStandardMaterial } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const beat=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.48,duration],returnToClean:true,frames:[
  {time:.15,bones:{Hips:{rotation:[.05,.12,-.06]},Spine:{rotation:[-.14,-.18,.06]},Spine2:{rotation:[-.18,-.22,.08]},RightArm:{rotation:[-.68,.16,-.38]},RightForeArm:{rotation:[0,-.62,0]},LeftArm:{rotation:[.48,-.22,.32]},LeftForeArm:{rotation:[0,.44,0]},Neck:{rotation:[.08,.14,0]},RightUpLeg:{rotation:[-.16,0,-.04]}},hips:[-.02,.02,0]},
  {time:duration*.46,bones:{Hips:{rotation:[.12,.28,twist]},Spine:{rotation:[-.26,.36,.14]},Spine2:{rotation:[-.34,.42,.12]},Neck:{rotation:[.12,-.18,.04]},RightArm:{rotation:[-1.32,.22,-.62]},RightForeArm:{rotation:[0,-1.08,0]},RightHand:{rotation:[0,0,-.32]},LeftArm:{rotation:[.72,-.34,.38]},LeftForeArm:{rotation:[0,.68,0]},RightUpLeg:{rotation:[-.48,0,-.1]},RightLeg:{rotation:[.82,0,0]},LeftUpLeg:{rotation:[.16,0,.06]}},hips:[.08,.07,0]},
  {time:duration*.7,bones:{Hips:{rotation:[.04,.1,0]},Spine:{rotation:[-.1,.16,.04]},Spine2:{rotation:[-.14,.18,.04]},RightArm:{rotation:[-.48,.08,-.22]},RightForeArm:{rotation:[0,-.42,0]},LeftArm:{rotation:[.32,-.12,.16]},RightLeg:{rotation:[.28,0,0]}},hips:[.02,.02,0]}
 ]});
 return [beat("special1",.82,-.12),beat("special2",1.02,.12),beat("super",1.15,.16)];
}
export function buildClips(scene){return makeClips(scene,"yogi");}
export function fx(battle,attacker,target,moveId){
 const color=0xd90000;
 return spawnTransientFx(battle,700,{attacker,target,create:(root,{dir,ax,ay})=>{
  const mat=new MeshStandardMaterial({color,emissive:color,emissiveIntensity:1,transparent:true,opacity:.72,roughness:.25});
  const shield=new Mesh(new CylinderGeometry(.68,.68,.08,8),mat);shield.rotation.x=Math.PI/2;root.add(shield);root.position.set(ax+dir*.68,ay,.35);
 }},(root,p)=>{root.scale.setScalar(.75+p*1.35);root.rotation.z+=.04*(moveId==="super"?2:1);});
}
