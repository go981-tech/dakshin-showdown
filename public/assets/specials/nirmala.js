import { BoxGeometry, Mesh, MeshBasicMaterial, MeshStandardMaterial, SphereGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene,id){
 const gst=(kind,duration,twist)=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,fxCleanupAt:[duration*.42,duration*.56,duration*.72,duration],returnToClean:true,frames:[
  {time:.12,bones:{Hips:{rotation:[.06,.10,-.16]},Spine:{rotation:[-.12,-.14,.12]},Spine2:{rotation:[-.16,-.18,.14]},Neck:{rotation:[.08,.12,-.08]},LeftArm:{rotation:[.46,-.18,.30]},LeftForeArm:{rotation:[0,.54,0]},LeftHand:{rotation:[.08,.08,.24]}},hips:[-.03,.03,0]},
  {time:.30,bones:{Hips:{rotation:[.12,.24,-.28]},Spine:{rotation:[-.24,-.32,.18]},Spine2:{rotation:[-.32,-.40,.22]},Neck:{rotation:[.12,-.18,-.10]},RightArm:{rotation:[-.82,.20,-.54]},RightForeArm:{rotation:[0,-.88,0]},RightHand:{rotation:[.10,.10,-.34]},LeftArm:{rotation:[.68,-.32,.40]},LeftForeArm:{rotation:[0,.72,0]}},hips:[.05,.06,0]},
  {time:duration*.48,bones:{Hips:{rotation:[.16,.38,twist]},Spine:{rotation:[-.34,-.46,.24]},Spine2:{rotation:[-.44,-.54,.28]},Neck:{rotation:[.16,-.24,-.14]},RightArm:{rotation:[-1.40,.30,-.70]},RightForeArm:{rotation:[0,-1.24,0]},RightHand:{rotation:[.16,.14,-.44]},LeftArm:{rotation:[.82,-.40,.48]},LeftForeArm:{rotation:[0,.82,0]},RightUpLeg:{rotation:[-.64,0,-.14]},RightLeg:{rotation:[.96,0,0]}},hips:[.12,.10,0]},
  {time:duration*.74,bones:{Hips:{rotation:[.06,.12,-.06]},Spine:{rotation:[-.12,-.14,.06]},RightArm:{rotation:[-.54,.08,-.20]},RightForeArm:{rotation:[0,-.44,0]},LeftArm:{rotation:[.32,-.12,.16]},RightLeg:{rotation:[.32,0,0]}},hips:[.02,.02,0]}
 ]});
 return [gst("special1",.86,-.14),gst("special2",1.04,.18),gst("super",1.15,.22)];
}
export function buildClips(scene){return makeClips(scene,"nirmala");}
export function fx(battle,attacker,target,moveId){
 const color=0x9900ff;
 return spawnTransientFx(battle,800,{attacker,target,create:(root,{tx,ty})=>{
  const mat=new MeshBasicMaterial({color:0xffc04d,transparent:true,opacity:.92});
  for(let i=0;i<18;i++){const kernel=new Mesh(new SphereGeometry(.035,6,4),mat);const x=((i*37)%100)/100-.5;kernel.position.set(x*1.4,1.2-(i%6)*.22,(i%3)*.08-.08);root.add(kernel);}
  const meter=new Mesh(new BoxGeometry(.7,.06,.04),new MeshStandardMaterial({color,emissive:color,emissiveIntensity:.8}));meter.position.set(0,.95,.28);root.add(meter);root.position.set(tx,ty-.2,.2);
 }},(root,p)=>{root.position.y-=p*.55;root.scale.setScalar(.8+p*.8);});
}
