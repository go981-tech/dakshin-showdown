import { BoxGeometry, Mesh, MeshBasicMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const signal=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.42,duration*.68,duration],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.06,.14,-.18]},Spine:{rotation:[-.14,-.18,.12]},Spine2:{rotation:[-.18,-.22,.16]},Neck:{rotation:[.08,.12,-.08]},LeftArm:{rotation:[.48,-.18,.32]},LeftForeArm:{rotation:[0,.58,0]},LeftHand:{rotation:[0,0,.28]}},hips:[-.03,.03,0]},
  {time:.30,bones:{Hips:{rotation:[.10,.26,-.28]},Spine:{rotation:[-.24,-.32,.18]},Spine2:{rotation:[-.30,-.38,.22]},Neck:{rotation:[.12,.18,-.12]},RightArm:{rotation:[-.62,.20,-.44]},RightForeArm:{rotation:[0,-.72,0]},RightHand:{rotation:[.08,.08,-.30]},LeftArm:{rotation:[.64,-.28,.44]},LeftForeArm:{rotation:[0,.72,0]}},hips:[.02,.07,.02]},
  {time:duration*.48,bones:{Hips:{rotation:[.16,.42,twist]},Spine:{rotation:[-.34,-.48,.24]},Spine2:{rotation:[-.42,-.56,.28]},Neck:{rotation:[.16,.24,-.16]},RightArm:{rotation:[-1.18,.36,-.68]},RightForeArm:{rotation:[0,-1.14,0]},RightHand:{rotation:[.12,.14,-.38]},LeftArm:{rotation:[.78,-.36,.52]},LeftForeArm:{rotation:[0,.82,0]},RightUpLeg:{rotation:[-.62,0,-.12]},RightLeg:{rotation:[.92,0,0]}},hips:[.12,.10,.04]},
  {time:duration*.72,bones:{Hips:{rotation:[.04,.12,-.04]},Spine:{rotation:[-.10,-.14,.04]},Spine2:{rotation:[-.14,-.18,.06]},RightArm:{rotation:[-.48,.08,-.18]},RightForeArm:{rotation:[0,-.42,0]},LeftArm:{rotation:[.30,-.12,.16]},RightLeg:{rotation:[.30,0,0]}},hips:[.02,.02,0]}
 ]});
 return [signal("special1",.84,-.14),signal("special2",1.02,.16),signal("super",1.15,.20)];
}
export function buildClips(scene){return makeClips(scene,"lalu");}
export function fx(battle,attacker,target,moveId){
 const color=0xffdd00;
 return spawnTransientFx(battle,700,{attacker,target,create:(root,{dir,ax,ay,tx,ty})=>{
  const mat=new MeshBasicMaterial({color,transparent:true,opacity:.82,side:2});
  for(let i=0;i<4;i++){const ring=new Mesh(new TorusGeometry(.28+i*.22,.035,8,24),mat);ring.rotation.y=Math.PI/2;ring.position.x=dir*i*.28;root.add(ring);}root.position.set(ax+dir*.58,ay+.12,.3);
 }},(root,p,{dir})=>{root.position.x+=dir*.012;root.scale.setScalar(.8+p*1.5);});
}
