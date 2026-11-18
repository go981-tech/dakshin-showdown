import { BoxGeometry, CylinderGeometry, Mesh, MeshStandardMaterial, SphereGeometry, TorusGeometry } from "three";
import { buildCharacterClip } from "./_animBuilder.js";
import { spawnTransientFx } from "./_fxUtils.js";

function makeClips(scene, id) {
  const poses = [
    { time: 0.15, bones: { Hips:{rotation:[0.08,0.22,-0.08]},Spine:{rotation:[-0.12,-0.25,0]},Spine2:{rotation:[-0.16,-0.28,0]},RightArm:{rotation:[-0.75,-0.08,-0.42]},RightForeArm:{rotation:[0,-0.82,0]},LeftArm:{rotation:[0.38,0.12,0.18]},LeftForeArm:{rotation:[0,0.32,0]} } },
    { time: 0.42, bones: { Hips:{rotation:[0.12,0.34,-0.12]},Spine:{rotation:[-0.28,-0.38,0.08]},Spine2:{rotation:[-0.34,-0.42,0]},Neck:{rotation:[0.08,-0.18,0]},RightArm:{rotation:[-1.25,0.18,-0.64]},RightForeArm:{rotation:[0,-1.08,0]},RightHand:{rotation:[0,0,-0.32]},LeftArm:{rotation:[0.62,-0.32,0.28]},LeftUpLeg:{rotation:[-0.22,0,0.06]},LeftLeg:{rotation:[0.48,0,0]} } },
    { time: 0.58, bones: { Hips:{rotation:[0.04,0.12,-0.04]},Spine:{rotation:[-0.12,-0.16,0]},Spine2:{rotation:[-0.18,-0.2,0]},RightArm:{rotation:[-0.58,0.08,-0.24]},RightForeArm:{rotation:[0,-0.48,0]},LeftArm:{rotation:[0.26,-0.12,0.12]} } }
  ];
  return [
    ["special1",0.82,poses],
    ["special2",0.92,poses.map((f,i)=>({time:f.time*(i===0?1:i===1?1.05:1),bones:{...f.bones,Hips:{rotation:[f.bones.Hips.rotation[0],-f.bones.Hips.rotation[1],f.bones.Hips.rotation[2]],position:[0.04,0.03,0]}}}))],
    ["super",1.12,poses.map((f,i)=>({time:f.time*(i===0?.9:i===1?1.08:1),bones:{...f.bones,RightUpLeg:{rotation:[-0.58,0,0]},RightLeg:{rotation:[0.92,0,0]},LeftArm:{rotation:[0.72,-0.22,0.32]},LeftForeArm:{rotation:[0,0.48,0]}}}))]
  ].map(([kind,duration,frames])=>buildCharacterClip(scene,{name:`south_${kind}_${id}`,fighterId:id,kind,duration,frames,fxCleanupAt:[duration*0.48,duration],returnToClean:true}));
}
export function buildClips(scene) { return makeClips(scene,"rahul"); }
export function fx(battle, attacker, target, moveId) {
  const color=0xffd700;
  return spawnTransientFx(battle,560,{attacker,target,create:(root,{dir,ax,ay})=>{
    const mat=new MeshStandardMaterial({color,emissive:color,emissiveIntensity:1,metalness:.7,roughness:.2});
    const mic=new Mesh(new CylinderGeometry(.035,.035,.38,10),mat); mic.rotation.z=Math.PI/2;
    const head=new Mesh(new SphereGeometry(.12,12,10),mat);
    head.position.x=dir*.22; mic.position.x=dir*.08; root.add(mic,head);
    root.position.set(ax+dir*.5,ay+.2,.35);
  }},(root,p,{dir})=>{root.position.x+=(dir*(p*.018));root.rotation.z=p*4*dir;root.scale.setScalar(.85+p*.55);});
}
