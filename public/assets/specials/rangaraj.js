import { BoxGeometry, Mesh, MeshBasicMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const debate=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.40,duration*.54,duration*.72,duration],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.06,.16,-.16]},Spine:{rotation:[-.12,-.20,.12]},Spine2:{rotation:[-.16,-.24,.14]},Neck:{rotation:[.08,.14,-.08]},LeftArm:{rotation:[.44,-.18,.28]},LeftForeArm:{rotation:[0,.52,0]},LeftHand:{rotation:[.08,.08,.24]}},hips:[-.03,.03,0]},
  {time:.30,bones:{Hips:{rotation:[.12,.32,-.26]},Spine:{rotation:[-.24,-.36,.18]},Spine2:{rotation:[-.32,-.44,.20]},Neck:{rotation:[.12,-.20,-.10]},RightArm:{rotation:[-.82,.20,-.54]},RightForeArm:{rotation:[0,-.88,0]},RightHand:{rotation:[.10,.10,-.34]},LeftArm:{rotation:[.64,-.28,.38]},LeftForeArm:{rotation:[0,.68,0]}},hips:[.05,.06,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.16,.46,twist]},Spine:{rotation:[-.34,-.52,.24]},Spine2:{rotation:[-.44,-.60,.28]},Neck:{rotation:[.16,-.26,-.14]},RightArm:{rotation:[-1.38,.32,-.68]},RightForeArm:{rotation:[0,-1.22,0]},RightHand:{rotation:[.16,.14,-.42]},LeftArm:{rotation:[.78,-.38,.46]},LeftForeArm:{rotation:[0,.78,0]},RightUpLeg:{rotation:[-.58,0,-.12]},RightLeg:{rotation:[.88,0,0]}},hips:[.12,.10,0]},
  {time:duration*.72,bones:{Hips:{rotation:[.06,.16,-.06]},Spine:{rotation:[-.12,-.16,.06]},RightArm:{rotation:[-.54,.08,-.20]},RightForeArm:{rotation:[0,-.44,0]},LeftArm:{rotation:[.30,-.12,.14]},RightLeg:{rotation:[.30,0,0]}},hips:[.02,.02,0]}
 ]});
 return [debate("special1",.82,-.14),debate("special2",1.02,.18),debate("super",1.15,.22)];
}
export function buildClips(scene){return makeClips(scene,"rangaraj");}
export function fx(battle,attacker,target,moveId){
 const color=0x38bdf8;
 return spawnTransientFx(battle,800,{attacker,target,create:(root,{tx,ty})=>{
  const mat=new MeshBasicMaterial({color,transparent:true,opacity:.88});
  const ring=new Mesh(new TorusGeometry(.72,.055,8,36),mat);ring.rotation.x=Math.PI/2;root.add(ring);
  for(let i=0;i<5;i++){const ticker=new Mesh(new BoxGeometry(.32,.12,.035),mat);ticker.position.set((i-2)*.18,.28,0);ticker.rotation.z=i*.12;root.add(ticker);}root.position.set(tx,ty-.42,.28);
 }},(root,p)=>{root.rotation.z+=.22*(moveId==="super"?2:1);root.scale.setScalar(.7+p*1.25);});
}
