import { BoxGeometry, Mesh, MeshStandardMaterial } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const shoulder=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.44,duration*.68,duration],returnToClean:true,frames:[
  {time:.14,bones:{Hips:{rotation:[.08,-.12,-.16]},Spine:{rotation:[-.12,.18,-.18]},Spine2:{rotation:[-.16,.22,-.22]},Neck:{rotation:[.12,-.18,-.08]},LeftArm:{rotation:[.44,-.12,.28]},LeftForeArm:{rotation:[0,.48,0]}},hips:[-.04,.02,0]},
  {time:.34,bones:{Hips:{rotation:[.14,-.28,-.36]},Spine:{rotation:[-.24,.36,-.28]},Spine2:{rotation:[-.32,.42,-.34]},Neck:{rotation:[.18,-.28,-.12]},RightArm:{rotation:[-.82,-.12,-.64]},RightForeArm:{rotation:[0,-.86,0]},RightHand:{rotation:[.08,.08,-.42]},LeftArm:{rotation:[.64,-.28,.38]},LeftForeArm:{rotation:[0,.58,0]}},hips:[.06,.06,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.18,-.42,twist]},Spine:{rotation:[-.34,.52,-.38]},Spine2:{rotation:[-.44,.58,-.42]},Neck:{rotation:[.22,-.34,-.16]},RightArm:{rotation:[-1.52,.24,-.82]},RightForeArm:{rotation:[0,-1.34,0]},RightHand:{rotation:[.16,.12,-.48]},LeftArm:{rotation:[.78,-.36,.46]},LeftForeArm:{rotation:[0,.74,0]},RightUpLeg:{rotation:[-.68,0,-.12]},RightLeg:{rotation:[1.08,0,0]}},hips:[.14,.10,0]},
  {time:duration*.72,bones:{Hips:{rotation:[.06,-.14,-.08]},Spine:{rotation:[-.12,.18,-.08]},Spine2:{rotation:[-.16,.22,-.1]},RightArm:{rotation:[-.58,.08,-.24]},RightForeArm:{rotation:[0,-.48,0]},RightLeg:{rotation:[.38,0,0]}},hips:[.02,.02,0]}
 ]});
 return [shoulder("special1",.84,-.16),shoulder("special2",1.02,.18),shoulder("super",1.15,.22)];
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
