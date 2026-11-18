import { BoxGeometry, Mesh, MeshBasicMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const beat=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.46,duration],returnToClean:true,frames:[
  {time:.15,bones:{Hips:{rotation:[.05,.12,-.08]},Spine:{rotation:[-.12,-.18,.08]},Spine2:{rotation:[-.16,-.22,.1]},Neck:{rotation:[.08,.12,0]},RightArm:{rotation:[-.58,.18,-.34]},RightForeArm:{rotation:[0,-.64,0]},LeftArm:{rotation:[.48,-.22,.28]},LeftForeArm:{rotation:[0,.46,0]},RightUpLeg:{rotation:[-.16,0,-.04]},LeftUpLeg:{rotation:[.12,0,.04]}},hips:[-.02,.03,0]},
  {time:duration*.46,bones:{Hips:{rotation:[.12,.36,twist]},Spine:{rotation:[-.28,.44,.14]},Spine2:{rotation:[-.34,.48,.12]},Neck:{rotation:[.12,-.2,.04]},RightArm:{rotation:[-1.28,.24,-.58]},RightForeArm:{rotation:[0,-1.08,0]},RightHand:{rotation:[0,0,-.28]},LeftArm:{rotation:[.74,-.36,.38]},LeftForeArm:{rotation:[0,.66,0]},RightUpLeg:{rotation:[-.58,0,-.12]},RightLeg:{rotation:[.88,0,0]},LeftUpLeg:{rotation:[.16,0,.06]}},hips:[.1,.08,0]},
  {time:duration*.68,bones:{Hips:{rotation:[.04,.12,0]},Spine:{rotation:[-.1,.16,.04]},Spine2:{rotation:[-.14,.18,.04]},RightArm:{rotation:[-.48,.08,-.18]},RightForeArm:{rotation:[0,-.42,0]},LeftArm:{rotation:[.28,-.12,.14]},RightLeg:{rotation:[.28,0,0]}},hips:[.02,.02,0]}
 ]});
 return [beat("special1",.84,-.12),beat("special2",1.02,.14),beat("super",1.15,.18)];
}
export function buildClips(scene){return makeClips(scene,"lalu");}
export function fx(battle,attacker,target,moveId){
 const color=0xffdd00;
 return spawnTransientFx(battle,700,{attacker,target,create:(root,{dir,ax,ay,tx,ty})=>{
  const mat=new MeshBasicMaterial({color,transparent:true,opacity:.82,side:2});
  for(let i=0;i<4;i++){const ring=new Mesh(new TorusGeometry(.28+i*.22,.035,8,24),mat);ring.rotation.y=Math.PI/2;ring.position.x=dir*i*.28;root.add(ring);}root.position.set(ax+dir*.58,ay+.12,.3);
 }},(root,p,{dir})=>{root.position.x+=dir*.012;root.scale.setScalar(.8+p*1.5);});
}
