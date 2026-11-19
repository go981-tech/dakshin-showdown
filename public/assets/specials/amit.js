import { BoxGeometry, Mesh, MeshBasicMaterial, MeshStandardMaterial } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const file=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.40,duration*.54,duration*.72,duration],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.06,-.12,-.16]},Spine:{rotation:[-.12,.16,-.12]},Spine2:{rotation:[-.16,.20,-.14]},Neck:{rotation:[.08,-.12,.04]},LeftArm:{rotation:[.44,-.18,.28]},LeftForeArm:{rotation:[0,.52,0]},LeftHand:{rotation:[.08,.08,.22]}},hips:[-.03,.03,0]},
  {time:.30,bones:{Hips:{rotation:[.12,-.28,-.26]},Spine:{rotation:[-.24,.32,-.18]},Spine2:{rotation:[-.32,.40,-.20]},Neck:{rotation:[.12,-.18,.06]},RightArm:{rotation:[-.82,.20,-.54]},RightForeArm:{rotation:[0,-.88,0]},RightHand:{rotation:[.10,.10,-.34]},LeftArm:{rotation:[.64,-.30,.38]},LeftForeArm:{rotation:[0,.68,0]}},hips:[.05,.06,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.16,-.42,twist]},Spine:{rotation:[-.34,.48,-.22]},Spine2:{rotation:[-.44,.56,-.26]},Neck:{rotation:[.16,-.24,.08]},RightArm:{rotation:[-1.38,.30,-.68]},RightForeArm:{rotation:[0,-1.24,0]},RightHand:{rotation:[.16,.14,-.42]},LeftArm:{rotation:[.78,-.38,.46]},LeftForeArm:{rotation:[0,.78,0]},RightUpLeg:{rotation:[-.58,0,-.12]},RightLeg:{rotation:[.88,0,0]}},hips:[.12,.10,0]},
  {time:duration*.72,bones:{Hips:{rotation:[.06,-.14,-.06]},Spine:{rotation:[-.12,.16,-.06]},RightArm:{rotation:[-.54,.08,-.20]},RightForeArm:{rotation:[0,-.44,0]},LeftArm:{rotation:[.30,-.12,.14]},RightLeg:{rotation:[.30,0,0]}},hips:[.02,.02,0]}
 ]});
 return [file("special1",.84,-.14),file("special2",1.02,.18),file("super",1.15,.22)];
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
