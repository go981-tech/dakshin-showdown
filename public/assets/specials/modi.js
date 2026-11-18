import { BoxGeometry, Mesh, MeshBasicMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const cycle=(kind,duration,lean)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.44,duration*.68,duration],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.06,-.16,-.12]},Spine:{rotation:[-.12,.20,-.10]},Spine2:{rotation:[-.16,.24,-.12]},Neck:{rotation:[.08,-.14,.02]},LeftArm:{rotation:[.42,-.20,.28]},LeftForeArm:{rotation:[0,.48,0]}},hips:[-.04,.02,0]},
  {time:.32,bones:{Hips:{rotation:[.12,-.34,-.18]},Spine:{rotation:[-.26,.42,-.14]},Spine2:{rotation:[-.34,.50,-.16]},Neck:{rotation:[.12,-.22,.04]},RightArm:{rotation:[-.88,.22,-.54]},RightForeArm:{rotation:[0,-.92,0]},RightHand:{rotation:[.08,.08,-.32]},LeftArm:{rotation:[.68,-.34,.36]},LeftForeArm:{rotation:[0,.68,0]}},hips:[.06,.06,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.16,-.48,lean]},Spine:{rotation:[-.38,.58,-.18]},Spine2:{rotation:[-.48,.66,-.20]},Neck:{rotation:[.16,-.28,.06]},RightArm:{rotation:[-1.48,.30,-.72]},RightForeArm:{rotation:[0,-1.32,0]},RightHand:{rotation:[.14,.12,-.42]},LeftArm:{rotation:[.82,-.42,.48]},LeftForeArm:{rotation:[0,.82,0]},RightUpLeg:{rotation:[-.78,0,-.16]},RightLeg:{rotation:[1.14,0,0]}},hips:[.14,.12,.04]},
  {time:duration*.72,bones:{Hips:{rotation:[.06,-.16,-.06]},Spine:{rotation:[-.12,.18,-.06]},RightArm:{rotation:[-.58,.10,-.22]},RightForeArm:{rotation:[0,-.48,0]},LeftArm:{rotation:[.30,-.12,.14]},RightLeg:{rotation:[.36,0,0]}},hips:[.02,.02,0]}
 ]});
 return [cycle("special1",.82,-.10),cycle("special2",1.02,.16),cycle("super",1.15,.20)];
}
export function buildClips(scene){return makeClips(scene,"modi");}
export function fx(battle,attacker,target,moveId){
 const color=0xff2200;
 return spawnTransientFx(battle,650,{attacker,target,create:(root,{dir,ax,ay,tx})=>{
  for(let i=0;i<3;i++){const mat=new MeshBasicMaterial({color,transparent:true,opacity:.8-i*.12});const ring=new Mesh(new TorusGeometry(.42+i*.28,.045,8,28),mat);ring.rotation.x=Math.PI/2;ring.position.set((i-1)*.12,.12+i*.04,.2);root.add(ring);}
 }},(root,p,{tx})=>{root.position.set(tx,.12,.2);root.rotation.z+=.05*(moveId==="super"?2:1);root.scale.setScalar(1+p*1.8);});
}
