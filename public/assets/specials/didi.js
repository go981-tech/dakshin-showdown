import { BoxGeometry, Mesh, MeshStandardMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const beat=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.46,duration],returnToClean:true,frames:[
  {time:.14,bones:{Hips:{rotation:[.06,.14,-.05]},Spine:{rotation:[-.12,-.18,0]},Spine2:{rotation:[-.16,-.22,.04]},RightArm:{rotation:[-.82,.18,-.44]},RightForeArm:{rotation:[0,-.72,0]},LeftArm:{rotation:[.42,-.12,.22]},LeftForeArm:{rotation:[0,.38,0]},RightHand:{rotation:[0,0,-.18]}},hips:[-.03,.02,0]},
  {time:duration*.46,bones:{Hips:{rotation:[.1,.32,twist]},Spine:{rotation:[-.26,.38,.12]},Spine2:{rotation:[-.32,.44,.1]},Neck:{rotation:[.1,-.16,0]},RightArm:{rotation:[-1.42,.24,-.58]},RightForeArm:{rotation:[0,-1.18,0]},RightHand:{rotation:[0,0,-.34]},LeftArm:{rotation:[.68,-.28,.34]},LeftForeArm:{rotation:[0,.58,0]},RightUpLeg:{rotation:[-.46,0,-.08]},RightLeg:{rotation:[.72,0,0]}},hips:[.09,.06,0]},
  {time:duration*.68,bones:{Hips:{rotation:[.03,.12,0]},Spine:{rotation:[-.1,.16,0]},Spine2:{rotation:[-.14,.18,0]},RightArm:{rotation:[-.52,.08,-.2]},RightForeArm:{rotation:[0,-.44,0]},LeftArm:{rotation:[.28,-.1,.12]},RightUpLeg:{rotation:[-.16,0,0]},RightLeg:{rotation:[.24,0,0]}},hips:[.02,.02,0]}
 ]});
 return [beat("special1",.84,-.1),beat("special2",1.04,.12),beat("super",1.15,.16)];
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
