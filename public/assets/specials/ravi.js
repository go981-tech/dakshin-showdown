import { BoxGeometry, Mesh, MeshBasicMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const beat=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.46,duration],returnToClean:true,frames:[
  {time:.14,bones:{Hips:{rotation:[.06,-.18,-.12]},Spine:{rotation:[-.12,.24,-.12]},Spine2:{rotation:[-.16,.28,-.14]},RightArm:{rotation:[-.72,.12,-.44]},RightForeArm:{rotation:[0,-.68,0]},LeftArm:{rotation:[.42,-.18,.26]},LeftForeArm:{rotation:[0,.38,0]},Neck:{rotation:[.08,-.16,0]},RightUpLeg:{rotation:[-.22,0,-.08]}},hips:[-.04,.03,0]},
  {time:duration*.46,bones:{Hips:{rotation:[.14,-.48,twist]},Spine:{rotation:[-.28,.5,-.16]},Spine2:{rotation:[-.36,.56,-.18]},Neck:{rotation:[.12,-.26,.04]},RightArm:{rotation:[-1.42,.24,-.68]},RightForeArm:{rotation:[0,-1.16,0]},RightHand:{rotation:[0,0,-.34]},LeftArm:{rotation:[.68,-.36,.34]},LeftForeArm:{rotation:[0,.58,0]},RightUpLeg:{rotation:[-.82,0,-.16]},RightLeg:{rotation:[1.12,0,0]},LeftUpLeg:{rotation:[.24,0,.08]}},hips:[.1,.09,0]},
  {time:duration*.68,bones:{Hips:{rotation:[.04,-.14,-.04]},Spine:{rotation:[-.1,.18,-.06]},Spine2:{rotation:[-.14,.22,-.08]},RightArm:{rotation:[-.54,.08,-.22]},RightForeArm:{rotation:[0,-.46,0]},LeftArm:{rotation:[.28,-.12,.14]},RightLeg:{rotation:[.42,0,0]}},hips:[.02,.02,0]}
 ]});
 return [beat("special1",.82,-.14),beat("special2",1.04,.16),beat("super",1.15,.18)];
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
