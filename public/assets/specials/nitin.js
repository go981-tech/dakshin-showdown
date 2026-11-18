import { Mesh, MeshStandardMaterial, SphereGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const beat=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.48,duration],returnToClean:true,frames:[
  {time:.15,bones:{Hips:{rotation:[.06,.12,-.06]},Spine:{rotation:[-.12,-.16,.04]},Spine2:{rotation:[-.16,-.2,.06]},RightArm:{rotation:[-.78,.14,-.42]},RightForeArm:{rotation:[0,-.68,0]},LeftArm:{rotation:[.44,-.18,.24]},LeftForeArm:{rotation:[0,.4,0]},Neck:{rotation:[.06,.12,0]},RightUpLeg:{rotation:[-.18,0,-.04]}},hips:[-.03,.03,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.12,.32,twist]},Spine:{rotation:[-.28,.42,.12]},Spine2:{rotation:[-.34,.48,.12]},Neck:{rotation:[.12,-.16,0]},RightArm:{rotation:[-1.38,.28,-.66]},RightForeArm:{rotation:[0,-1.16,0]},RightHand:{rotation:[0,0,-.36]},LeftArm:{rotation:[.72,-.36,.36]},LeftForeArm:{rotation:[0,.64,0]},RightUpLeg:{rotation:[-.64,0,-.12]},RightLeg:{rotation:[.96,0,0]},LeftUpLeg:{rotation:[.18,0,.06]}},hips:[.12,.08,0]},
  {time:duration*.68,bones:{Hips:{rotation:[.04,.12,0]},Spine:{rotation:[-.1,.16,.04]},Spine2:{rotation:[-.14,.18,.04]},RightArm:{rotation:[-.52,.08,-.22]},RightForeArm:{rotation:[0,-.44,0]},LeftArm:{rotation:[.3,-.12,.14]},RightLeg:{rotation:[.32,0,0]}},hips:[.02,.02,0]}
 ]});
 return [beat("special1",.86,-.12),beat("special2",1.04,.14),beat("super",1.15,.18)];
}
export function buildClips(scene){return makeClips(scene,"nitin");}
export function fx(battle,attacker,target,moveId){
 const color=0xffaa00;
 return spawnTransientFx(battle,620,{attacker,target,create:(root,{dir,ax,ay,tx})=>{
  const mat=new MeshStandardMaterial({color,emissive:0x553300,emissiveIntensity:.55,roughness:.72});
  for(let i=0;i<5;i++){const rock=new Mesh(new SphereGeometry(.12+i*.025,8,6),mat);rock.position.set(dir*(.2+i*.18),(i%2)*.08+(i%3)*.04,.16);root.add(rock);}root.position.set((ax+tx)*.5,ay-.7,.18);
 }},(root,p,{dir})=>{root.position.x+=dir*.012;root.rotation.z=p*.12*dir;root.scale.setScalar(1+p*1.4);});
}
