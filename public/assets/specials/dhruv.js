import { BoxGeometry, Mesh, MeshBasicMaterial, MeshStandardMaterial } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const click=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.38,duration*.48,duration*.68,duration],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.06,.16,-.16]},Spine:{rotation:[-.12,-.20,.12]},Spine2:{rotation:[-.16,-.24,.14]},Neck:{rotation:[.08,.14,-.08]},RightArm:{rotation:[-.66,.16,-.38]},RightForeArm:{rotation:[0,-.62,0]},RightHand:{rotation:[.08,.08,-.24]},LeftArm:{rotation:[.44,-.16,.28]},LeftForeArm:{rotation:[0,.48,0]}},hips:[-.03,.03,0]},
  {time:.28,bones:{Hips:{rotation:[.12,.32,-.26]},Spine:{rotation:[-.24,-.36,.18]},Spine2:{rotation:[-.32,-.44,.20]},Neck:{rotation:[.12,-.20,-.10]},RightArm:{rotation:[-.94,.22,-.58]},RightForeArm:{rotation:[0,-1.02,0]},RightHand:{rotation:[.12,.12,-.36]},LeftArm:{rotation:[.68,-.28,.38]},LeftForeArm:{rotation:[0,.68,0]}},hips:[.05,.06,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.16,.46,twist]},Spine:{rotation:[-.34,-.52,.24]},Spine2:{rotation:[-.44,-.60,.28]},Neck:{rotation:[.16,-.26,-.14]},RightArm:{rotation:[-1.38,.32,-.72]},RightForeArm:{rotation:[0,-1.22,0]},RightHand:{rotation:[.18,.16,-.46]},LeftArm:{rotation:[.82,-.38,.48]},LeftForeArm:{rotation:[0,.82,0]},RightUpLeg:{rotation:[-.58,0,-.12]},RightLeg:{rotation:[.88,0,0]}},hips:[.12,.10,0]},
  {time:duration*.72,bones:{Hips:{rotation:[.06,.16,-.06]},Spine:{rotation:[-.12,-.16,.06]},RightArm:{rotation:[-.54,.08,-.20]},RightForeArm:{rotation:[0,-.44,0]},LeftArm:{rotation:[.30,-.12,.14]},RightLeg:{rotation:[.30,0,0]}},hips:[.02,.02,0]}
 ]});
 return [click("special1",.82,-.14),click("special2",1.02,.18),click("super",1.15,.22)];
}
export function buildClips(scene){return makeClips(scene,"dhruv");}
export function fx(battle,attacker,target,moveId){
 const color=0x00d4ff;
 return spawnTransientFx(battle,620,{attacker,target,create:(root,{dir,tx,ty})=>{
  const mat=new MeshBasicMaterial({color,transparent:true,opacity:.92});
  for(let i=0;i<6;i++){const card=new Mesh(new BoxGeometry(.34,.24,.025),mat);const ang=(i/6)*Math.PI*2;card.position.set(Math.cos(ang)*.48,Math.sin(ang)*.32,0);card.rotation.z=ang;root.add(card);}root.position.set(tx,ty,.28);
 }},(root,p,{dir})=>{root.position.x+=(dir*.008);root.rotation.z+=.12*(moveId==="super"?2:1);root.scale.setScalar(.75+p*1.15);});
}
