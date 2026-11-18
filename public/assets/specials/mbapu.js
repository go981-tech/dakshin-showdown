import { BoxGeometry, Mesh, MeshStandardMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const beat=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.48,duration],returnToClean:true,frames:[
  {time:.16,bones:{Hips:{rotation:[.06,.12,-.06]},Spine:{rotation:[-.14,-.16,.08]},Spine2:{rotation:[-.18,-.2,.1]},Neck:{rotation:[.08,.12,0]},RightArm:{rotation:[-.68,.16,-.38]},RightForeArm:{rotation:[0,-.64,0]},LeftArm:{rotation:[.46,-.18,.26]},LeftForeArm:{rotation:[0,.42,0]},RightUpLeg:{rotation:[-.18,0,-.05]},LeftUpLeg:{rotation:[.12,0,.04]}},hips:[-.02,.02,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.14,.34,twist]},Spine:{rotation:[-.28,.44,.14]},Spine2:{rotation:[-.36,.48,.14]},Neck:{rotation:[.12,-.18,.04]},RightArm:{rotation:[-1.38,.28,-.64]},RightForeArm:{rotation:[0,-1.12,0]},RightHand:{rotation:[0,0,-.34]},LeftArm:{rotation:[.72,-.34,.36]},LeftForeArm:{rotation:[0,.62,0]},RightUpLeg:{rotation:[-.6,0,-.12]},RightLeg:{rotation:[.92,0,0]},LeftUpLeg:{rotation:[.18,0,.06]}},hips:[.1,.08,0]},
  {time:duration*.68,bones:{Hips:{rotation:[.04,.12,0]},Spine:{rotation:[-.1,.16,.04]},Spine2:{rotation:[-.14,.18,.04]},RightArm:{rotation:[-.52,.08,-.2]},RightForeArm:{rotation:[0,-.44,0]},LeftArm:{rotation:[.28,-.12,.14]},RightLeg:{rotation:[.32,0,0]}},hips:[.02,.02,0]}
 ]});
 return [beat("special1",.88,-.12),beat("special2",1.04,.14),beat("super",1.15,.18)];
}
export function buildClips(scene){return makeClips(scene,"mbapu");}
export function fx(battle,attacker,target,moveId){
 const color=0x222222;
 return spawnTransientFx(battle,700,{attacker,target,create:(root,{tx,ty})=>{
  const mat=new MeshStandardMaterial({color,emissive:0x111111,emissiveIntensity:.4,roughness:.9,metalness:.15});
  const ring=new Mesh(new TorusGeometry(.8,.09,10,34),mat);ring.rotation.x=Math.PI/2;root.add(ring);
  for(let i=0;i<6;i++){const a=i*Math.PI/3;const crack=new Mesh(new BoxGeometry(.58,.035,.018),mat);crack.position.set(Math.cos(a)*.48,Math.sin(a)*.1,.04);crack.rotation.z=a;root.add(crack);}root.position.set(tx,ty-.9,.18);
 }},(root,p)=>{root.scale.setScalar(.8+p*2.4);});
}
