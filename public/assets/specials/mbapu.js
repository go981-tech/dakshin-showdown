import { BoxGeometry, Mesh, MeshStandardMaterial, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const reform=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.46,duration*.70,duration],returnToClean:true,frames:[
  {time:.14,bones:{Hips:{rotation:[.05,.10,-.12]},Spine:{rotation:[-.12,-.12,.10]},Spine2:{rotation:[-.16,-.16,.12]},Neck:{rotation:[.10,.12,-.06]},LeftArm:{rotation:[.48,-.22,.32]},LeftForeArm:{rotation:[0,.58,0]}},hips:[-.02,.03,0]},
  {time:.32,bones:{Hips:{rotation:[.10,.22,-.24]},Spine:{rotation:[-.22,-.28,.16]},Spine2:{rotation:[-.28,-.34,.18]},Neck:{rotation:[.12,.18,-.10]},RightArm:{rotation:[-.58,.20,-.52]},RightForeArm:{rotation:[0,-.72,0]},RightHand:{rotation:[.08,.08,-.36]},LeftArm:{rotation:[.68,-.34,.42]},LeftForeArm:{rotation:[0,.72,0]}},hips:[.02,.06,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.16,.38,twist]},Spine:{rotation:[-.32,-.44,.22]},Spine2:{rotation:[-.40,-.52,.26]},Neck:{rotation:[.16,.22,-.14]},RightArm:{rotation:[-1.28,.34,-.72]},RightForeArm:{rotation:[0,-1.18,0]},RightHand:{rotation:[.16,.14,-.44]},LeftArm:{rotation:[.82,-.40,.48]},LeftForeArm:{rotation:[0,.82,0]},RightUpLeg:{rotation:[-.48,0,-.10]},RightLeg:{rotation:[.78,0,0]}},hips:[.10,.09,0]},
  {time:duration*.74,bones:{Hips:{rotation:[.04,.12,-.04]},Spine:{rotation:[-.10,-.14,.04]},RightArm:{rotation:[-.48,.08,-.18]},RightForeArm:{rotation:[0,-.42,0]},LeftArm:{rotation:[.30,-.12,.14]},RightLeg:{rotation:[.28,0,0]}},hips:[.02,.02,0]}
 ]});
 return [reform("special1",.88,-.14),reform("special2",1.04,.16),reform("super",1.15,.20)];
}
export function buildClips(scene){return makeClips(scene,"mbapu");}
export function fx(battle,attacker,target,moveId){
 const color=0x222222;
 return spawnTransientFx(battle,700,{attacker,target,create:(root,{tx,ty})=>{
  const mat=new MeshStandardMaterial({color,emissive:0x111111,emissiveIntensity:.4,roughness:.9,metalness:.15});
  const ring=new Mesh(new TorusGeometry(.8,.09,10,34),mat);ring.rotation.x=Math.PI/2;root.add(ring);
  for(let i=0;i<6;i++){const a=i*Math.PI/3;const crack=new Mesh(new BoxGeometry(.58,.035,.018),mat);crack.position.set(Math.cos(a)*.48,Math.sin(a)*.1,.04);crack.rotation.z=a;root.add(crack);}root.position.set(tx,ty-.9,.18);
 }},(root,p)=>{root.scale.setScalar(.8+p*2.4);});
}
