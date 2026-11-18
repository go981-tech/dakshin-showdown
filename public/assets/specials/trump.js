import { BoxGeometry, Mesh, MeshStandardMaterial } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const beat=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.46,duration],returnToClean:true,frames:[
  {time:.14,bones:{Hips:{rotation:[.08,-.16,-.08]},Spine:{rotation:[-.08,.22,-.12]},Spine2:{rotation:[-.12,.28,-.12]},RightArm:{rotation:[-.92,-.12,-.5]},RightForeArm:{rotation:[0,-.82,0]},LeftArm:{rotation:[.38,.16,.18]},LeftForeArm:{rotation:[0,.42,0]},Neck:{rotation:[.08,-.18,0]}},hips:[-.04,.03,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.14,-.38,twist]},Spine:{rotation:[-.24,.46,-.16]},Spine2:{rotation:[-.34,.52,-.18]},Neck:{rotation:[.14,-.24,.04]},RightArm:{rotation:[-1.48,.28,-.72]},RightForeArm:{rotation:[0,-1.22,0]},RightHand:{rotation:[0,0,-.38]},LeftArm:{rotation:[.72,-.34,.32]},LeftForeArm:{rotation:[0,.62,0]},RightUpLeg:{rotation:[-.62,0,-.12]},RightLeg:{rotation:[.98,0,0]},LeftUpLeg:{rotation:[.18,0,.06]}},hips:[.12,.08,0]},
  {time:duration*.68,bones:{Hips:{rotation:[.04,-.14,-.04]},Spine:{rotation:[-.1,.18,-.06]},Spine2:{rotation:[-.16,.22,-.08]},RightArm:{rotation:[-.56,.1,-.24]},RightForeArm:{rotation:[0,-.48,0]},LeftArm:{rotation:[.32,-.12,.14]},RightLeg:{rotation:[.38,0,0]}},hips:[.02,.02,0]}
 ]});
 return [beat("special1",.84,-.12),beat("special2",1.02,.14),beat("super",1.15,.18)];
}
export function buildClips(scene){return makeClips(scene,"trump");}
export function fx(battle,attacker,target,moveId){
 const color=0xcc3300;
 return spawnTransientFx(battle,600,{attacker,target,create:(root,{dir,ax,ay,tx,ty})=>{
  const mat=new MeshStandardMaterial({color,emissive:color,emissiveIntensity:.8,roughness:.35,metalness:.55});
  const axe=new Mesh(new BoxGeometry(.9,.14,.18),mat);axe.position.set(0,0,.32);axe.rotation.z=dir*.55;
  const blade=new Mesh(new BoxGeometry(.28,.38,.12),mat);blade.position.set(dir*.48,-.08,0);axe.add(blade);root.add(axe);root.position.set(0,0,0);
 }},(root,p,{dir,tx,ty})=>{root.position.set(tx-dir*(1-p)*.9,ty,0);root.rotation.z=p*1.8*dir;root.scale.setScalar(.75+p*.7);});
}
