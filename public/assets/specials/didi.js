import { BoxGeometry, Mesh, MeshStandardMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const amma=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.40,duration*.54,duration*.72,duration],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.05,.14,-.18]},Spine:{rotation:[-.12,-.18,.12]},Spine2:{rotation:[-.16,-.22,.14]},Neck:{rotation:[.08,-.12,.04]},LeftArm:{rotation:[.44,-.18,.28]},LeftForeArm:{rotation:[0,.52,0]},LeftHand:{rotation:[0,0,.28]}},hips:[-.03,.03,0]},
  {time:.28,bones:{Hips:{rotation:[.10,.28,-.28]},Spine:{rotation:[-.24,-.34,.18]},Spine2:{rotation:[-.30,-.40,.20]},Neck:{rotation:[.12,-.18,.06]},RightArm:{rotation:[-.74,.18,-.48]},RightForeArm:{rotation:[0,-.86,0]},RightHand:{rotation:[.08,.08,-.36]}},hips:[.04,.05,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.14,.42,twist]},Spine:{rotation:[-.34,-.48,.22]},Spine2:{rotation:[-.42,-.56,.24]},Neck:{rotation:[.16,-.24,.08]},RightArm:{rotation:[-1.34,.32,-.64]},RightForeArm:{rotation:[0,-1.26,0]},RightHand:{rotation:[.18,.16,-.44]},LeftArm:{rotation:[.72,-.32,.40]},LeftForeArm:{rotation:[0,.68,0]},RightUpLeg:{rotation:[-.46,0,-.10]},RightLeg:{rotation:[.74,0,0]}},hips:[.10,.08,0]},
  {time:duration*.68,bones:{Hips:{rotation:[.06,.18,-.08]},Spine:{rotation:[-.14,-.18,.08]},Spine2:{rotation:[-.18,-.22,.08]},RightArm:{rotation:[-.58,.10,-.22]},RightForeArm:{rotation:[0,-.48,0]},LeftArm:{rotation:[.32,-.12,.16]},RightLeg:{rotation:[.32,0,0]}},hips:[.02,.02,0]}
 ]});
 return [amma("special1",.84,-.12),amma("special2",1.04,.16),amma("super",1.15,.20)];
}
export function buildClips(scene){return makeClips(scene,"didi");}
export function fx(battle,attacker,target,moveId){
 const color=0x00cc44;
 return spawnTransientFx(battle,600,{attacker,target,create:(root,{tx,ty})=>{
  const mat=new MeshStandardMaterial({color,emissive:color,emissiveIntensity:.9,transparent:true,opacity:.9});
  for(let i=0;i<2;i++){const leaf=new Mesh(new BoxGeometry(.32,.06,.62),mat);leaf.rotation.z=(i?-1:1)*.22;leaf.position.set((i?1:-1)*.24,(i?-.02:.14),0);root.add(leaf);}
  const ring=new Mesh(new TorusGeometry(.7,.08,10,32),mat);ring.rotation.x=Math.PI/2;root.add(ring);root.position.set(tx,ty-.82,.24);
 }},(root,p)=>{root.scale.setScalar(.8+p*2.2);root.rotation.z+=.015*(moveId==="super"?2:1);});
}
