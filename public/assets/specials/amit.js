import { BoxGeometry, Mesh, MeshBasicMaterial, MeshStandardMaterial } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const beat=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.46,duration],returnToClean:true,frames:[
  {time:.14,bones:{Hips:{rotation:[.06,-.14,-.06]},Spine:{rotation:[-.12,.18,-.08]},Spine2:{rotation:[-.16,.22,-.1]},Neck:{rotation:[.08,-.12,0]},RightArm:{rotation:[-.72,.14,-.38]},RightForeArm:{rotation:[0,-.68,0]},LeftArm:{rotation:[.42,-.18,.24]},LeftForeArm:{rotation:[0,.38,0]},RightUpLeg:{rotation:[-.16,0,-.04]}},hips:[-.03,.02,0]},
  {time:duration*.46,bones:{Hips:{rotation:[.12,-.36,twist]},Spine:{rotation:[-.28,.44,-.14]},Spine2:{rotation:[-.34,.48,-.16]},Neck:{rotation:[.12,-.22,.04]},RightArm:{rotation:[-1.42,.26,-.68]},RightForeArm:{rotation:[0,-1.18,0]},RightHand:{rotation:[0,0,-.36]},LeftArm:{rotation:[.68,-.34,.34]},LeftForeArm:{rotation:[0,.58,0]},RightUpLeg:{rotation:[-.58,0,-.12]},RightLeg:{rotation:[.88,0,0]},LeftUpLeg:{rotation:[.16,0,.06]}},hips:[.1,.08,0]},
  {time:duration*.68,bones:{Hips:{rotation:[.04,-.12,0]},Spine:{rotation:[-.1,.16,-.04]},Spine2:{rotation:[-.14,.18,-.04]},RightArm:{rotation:[-.52,.08,-.2]},RightForeArm:{rotation:[0,-.44,0]},LeftArm:{rotation:[.28,-.12,.14]},RightLeg:{rotation:[.28,0,0]}},hips:[.02,.02,0]}
 ]});
 return [beat("special1",.84,-.12),beat("special2",1.02,.14),beat("super",1.15,.18)];
}
export function buildClips(scene){return makeClips(scene,"amit");}
export function fx(battle,attacker,target,moveId){
 const color=0xff6600;
 return spawnTransientFx(battle,700,{attacker,target,create:(root,{tx,ty})=>{
  const mat=new MeshStandardMaterial({color:0xf4e7c4,roughness:.6,metalness:.08});
  for(let i=0;i<5;i++){const page=new Mesh(new BoxGeometry(.48,.05,.62),mat);page.position.set((i%2-.5)*.12,i*.07-(i===4?.03:0),0);page.rotation.z=(i%2-.5)*.08;root.add(page);}
  const stamp=new Mesh(new BoxGeometry(.38,.12,.04),new MeshBasicMaterial({color:0xcc0000,transparent:true,opacity:.9}));stamp.position.set(.08,.82,.38);stamp.rotation.z=-.18;root.add(stamp);root.position.set(tx,ty+.9,.32);
 }},(root,p)=>{root.position.y-=p*.016;root.rotation.z=p*.15*(moveId==="super"?2:1);root.scale.setScalar(.72+p*.62);});
}
