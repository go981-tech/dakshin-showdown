import { BoxGeometry, Mesh, MeshBasicMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const beat=(kind,duration,lean)=>{
  return buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.46,duration],returnToClean:true,frames:[
   {time:.15,bones:{Hips:{rotation:[.04,-.18,.06]},Spine:{rotation:[-.1,.2,0]},Spine2:{rotation:[-.12,.24,0]},RightArm:{rotation:[-.7,.12,-.28]},RightForeArm:{rotation:[0,-.7,0]},LeftArm:{rotation:[.34,-.2,.16]},LeftForeArm:{rotation:[0,.38,0]}},hips:[-.04,.02,0]},
   {time:duration*.48,bones:{Hips:{rotation:[.1,-.42,lean]},Spine:{rotation:[-.24,.42,.1]},Spine2:{rotation:[-.3,.48,.08]},Neck:{rotation:[.06,-.2,0]},RightArm:{rotation:[-1.35,.24,-.52]},RightForeArm:{rotation:[0,-1.12,0]},RightHand:{rotation:[0,0,-.28]},LeftArm:{rotation:[.64,-.32,.28]},LeftForeArm:{rotation:[0,.52,0]},RightUpLeg:{rotation:[-.54,0,-.08]},RightLeg:{rotation:[.86,0,0]}},hips:[.08,.07,0]},
   {time:duration*.68,bones:{Hips:{rotation:[.04,-.16,0]},Spine:{rotation:[-.1,.18,0]},Spine2:{rotation:[-.14,.2,0]},RightArm:{rotation:[-.48,.1,-.18]},RightForeArm:{rotation:[0,-.42,0]},LeftArm:{rotation:[.28,-.12,.12]},RightUpLeg:{rotation:[-.2,0,0]},RightLeg:{rotation:[.32,0,0]}},hips:[.02,.02,0]}
  ]});
 };
 return [beat("special1",.82,-.08),beat("special2",1.02,.12),beat("super",1.15,.16)];
}
export function buildClips(scene){return makeClips(scene,"modi");}
export function fx(battle,attacker,target,moveId){
 const color=0xff2200;
 return spawnTransientFx(battle,650,{attacker,target,create:(root,{dir,ax,ay,tx})=>{
  for(let i=0;i<3;i++){const mat=new MeshBasicMaterial({color,transparent:true,opacity:.8-i*.12});const ring=new Mesh(new TorusGeometry(.42+i*.28,.045,8,28),mat);ring.rotation.x=Math.PI/2;ring.position.set((i-1)*.12,.12+i*.04,.2);root.add(ring);}
 }},(root,p,{tx})=>{root.position.set(tx,.12,.2);root.rotation.z+=.05*(moveId==="super"?2:1);root.scale.setScalar(1+p*1.8);});
}
