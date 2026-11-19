import { Mesh, MeshStandardMaterial, SphereGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const grid=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.42,duration*.68,duration],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.06,.12,-.18]},Spine:{rotation:[-.14,-.16,.12]},Spine2:{rotation:[-.18,-.20,.14]},Neck:{rotation:[.08,.12,-.08]},LeftArm:{rotation:[.44,-.16,.30]},LeftForeArm:{rotation:[0,.52,0]}},hips:[-.03,.02,0]},
  {time:.32,bones:{Hips:{rotation:[.12,.26,-.28]},Spine:{rotation:[-.26,-.32,.18]},Spine2:{rotation:[-.34,-.38,.20]},Neck:{rotation:[.12,-.18,-.10]},RightArm:{rotation:[-.82,.18,-.56]},RightForeArm:{rotation:[0,-.88,0]},RightHand:{rotation:[.08,.08,-.36]},LeftArm:{rotation:[.68,-.30,.40]},LeftForeArm:{rotation:[0,.68,0]}},hips:[.06,.06,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.16,.40,twist]},Spine:{rotation:[-.36,-.46,.24]},Spine2:{rotation:[-.46,-.54,.28]},Neck:{rotation:[.16,-.24,-.14]},RightArm:{rotation:[-1.42,.28,-.72]},RightForeArm:{rotation:[0,-1.28,0]},RightHand:{rotation:[.16,.14,-.46]},LeftArm:{rotation:[.82,-.38,.48]},LeftForeArm:{rotation:[0,.82,0]},RightUpLeg:{rotation:[-.72,0,-.16]},RightLeg:{rotation:[1.08,0,0]}},hips:[.14,.12,.04]},
  {time:duration*.72,bones:{Hips:{rotation:[.06,.12,-.06]},Spine:{rotation:[-.12,-.14,.06]},RightArm:{rotation:[-.58,.08,-.22]},RightForeArm:{rotation:[0,-.48,0]},LeftArm:{rotation:[.32,-.12,.16]},RightLeg:{rotation:[.36,0,0]}},hips:[.02,.02,0]}
 ]});
 return [grid("special1",.86,-.14),grid("special2",1.04,.18),grid("super",1.15,.22)];
}
export function buildClips(scene){return makeClips(scene,"nitin");}
export function fx(battle,attacker,target,moveId){
 const color=0xffaa00;
 return spawnTransientFx(battle,620,{attacker,target,create:(root,{dir,ax,ay,tx})=>{
  const mat=new MeshStandardMaterial({color,emissive:0x553300,emissiveIntensity:.55,roughness:.72});
  for(let i=0;i<5;i++){const rock=new Mesh(new SphereGeometry(.12+i*.025,8,6),mat);rock.position.set(dir*(.2+i*.18),(i%2)*.08+(i%3)*.04,.16);root.add(rock);}root.position.set((ax+tx)*.5,ay-.7,.18);
 }},(root,p,{dir})=>{root.position.x+=dir*.012;root.rotation.z=p*.12*dir;root.scale.setScalar(1+p*1.4);});
}
