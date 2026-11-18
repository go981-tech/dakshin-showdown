import { BoxGeometry, Mesh, MeshBasicMaterial, MeshStandardMaterial } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const beat=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.46,duration],returnToClean:true,frames:[
  {time:.14,bones:{Hips:{rotation:[.05,.18,-.06]},Spine:{rotation:[-.12,-.2,.08]},Spine2:{rotation:[-.16,-.24,.1]},Neck:{rotation:[.08,.14,0]},RightArm:{rotation:[-.62,.16,-.34]},RightForeArm:{rotation:[0,-.58,0]},LeftArm:{rotation:[.44,-.18,.24]},LeftForeArm:{rotation:[0,.42,0]},RightUpLeg:{rotation:[-.16,0,-.04]}},hips:[-.02,.03,0]},
  {time:duration*.46,bones:{Hips:{rotation:[.12,.38,twist]},Spine:{rotation:[-.26,.46,.14]},Spine2:{rotation:[-.34,.52,.14]},Neck:{rotation:[.12,-.22,.04]},RightArm:{rotation:[-1.32,.24,-.62]},RightForeArm:{rotation:[0,-1.08,0]},RightHand:{rotation:[0,0,-.32]},LeftArm:{rotation:[.68,-.32,.34]},LeftForeArm:{rotation:[0,.58,0]},RightUpLeg:{rotation:[-.56,0,-.12]},RightLeg:{rotation:[.86,0,0]},LeftUpLeg:{rotation:[.18,0,.06]}},hips:[.1,.08,0]},
  {time:duration*.68,bones:{Hips:{rotation:[.04,.12,0]},Spine:{rotation:[-.1,.16,.04]},Spine2:{rotation:[-.14,.18,.04]},RightArm:{rotation:[-.48,.08,-.18]},RightForeArm:{rotation:[0,-.42,0]},LeftArm:{rotation:[.28,-.12,.14]},RightLeg:{rotation:[.28,0,0]}},hips:[.02,.02,0]}
 ]});
 return [beat("special1",.82,-.12),beat("special2",1.02,.14),beat("super",1.15,.18)];
}
export function buildClips(scene){return makeClips(scene,"dhruv");}
export function fx(battle,attacker,target,moveId){
 const color=0x00d4ff;
 return spawnTransientFx(battle,620,{attacker,target,create:(root,{dir,tx,ty})=>{
  const mat=new MeshBasicMaterial({color,transparent:true,opacity:.92});
  for(let i=0;i<6;i++){const card=new Mesh(new BoxGeometry(.34,.24,.025),mat);const ang=(i/6)*Math.PI*2;card.position.set(Math.cos(ang)*.48,Math.sin(ang)*.32,0);card.rotation.z=ang;root.add(card);}root.position.set(tx,ty,.28);
 }},(root,p,{dir})=>{root.position.x+=(dir*.008);root.rotation.z+=.12*(moveId==="super"?2:1);root.scale.setScalar(.75+p*1.15);});
}
