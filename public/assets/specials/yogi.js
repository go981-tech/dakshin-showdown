import { BoxGeometry, CylinderGeometry, Mesh, MeshBasicMaterial, MeshStandardMaterial } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const redSalute=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.42,duration*.68,duration],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.08,.10,-.18]},Spine:{rotation:[-.16,-.12,.12]},Spine2:{rotation:[-.20,-.16,.14]},Neck:{rotation:[.10,.12,-.10]},LeftArm:{rotation:[.56,-.22,.38]},LeftForeArm:{rotation:[0,.68,0]},LeftHand:{rotation:[.12,.10,.36]}},hips:[-.03,.02,0]},
  {time:.30,bones:{Hips:{rotation:[.14,.22,-.28]},Spine:{rotation:[-.28,-.32,.18]},Spine2:{rotation:[-.36,-.40,.22]},Neck:{rotation:[.14,.18,-.14]},RightArm:{rotation:[-.82,.18,-.52]},RightForeArm:{rotation:[0,-.96,0]},RightHand:{rotation:[.10,.10,-.38]},LeftArm:{rotation:[.74,-.34,.46]},LeftForeArm:{rotation:[0,.78,0]}},hips:[.03,.06,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.18,.36,twist]},Spine:{rotation:[-.38,-.44,.24]},Spine2:{rotation:[-.48,-.52,.28]},Neck:{rotation:[.18,.24,-.18]},RightArm:{rotation:[-1.42,.32,-.72]},RightForeArm:{rotation:[0,-1.32,0]},RightHand:{rotation:[.16,.14,-.46]},LeftArm:{rotation:[.88,-.42,.54]},LeftForeArm:{rotation:[0,.88,0]},RightUpLeg:{rotation:[-.68,0,-.14]},RightLeg:{rotation:[1.02,0,0]}},hips:[.12,.10,.04]},
  {time:duration*.72,bones:{Hips:{rotation:[.06,.12,-.06]},Spine:{rotation:[-.12,-.14,.06]},Spine2:{rotation:[-.16,-.18,.08]},RightArm:{rotation:[-.56,.08,-.20]},RightForeArm:{rotation:[0,-.48,0]},LeftArm:{rotation:[.34,-.12,.16]},RightLeg:{rotation:[.34,0,0]}},hips:[.02,.02,0]}
 ]});
 return [redSalute("special1",.82,-.12),redSalute("special2",1.02,.16),redSalute("super",1.15,.20)];
}
export function buildClips(scene){return makeClips(scene,"yogi");}
export function fx(battle,attacker,target,moveId){
 const color=0xd90000;
 return spawnTransientFx(battle,700,{attacker,target,create:(root,{dir,ax,ay})=>{
  const mat=new MeshStandardMaterial({color,emissive:color,emissiveIntensity:1,transparent:true,opacity:.72,roughness:.25});
  const shield=new Mesh(new CylinderGeometry(.68,.68,.08,8),mat);shield.rotation.x=Math.PI/2;root.add(shield);root.position.set(ax+dir*.68,ay,.35);
 }},(root,p)=>{root.scale.setScalar(.75+p*1.35);root.rotation.z+=.04*(moveId==="super"?2:1);});
}
