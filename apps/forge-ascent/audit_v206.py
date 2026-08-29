from pathlib import Path
import json, re


def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"Patch anchor missing: {label}")
    return text.replace(old, new, 1)


ds = Path("www/data-store.js")
s = ds.read_text(encoding="utf-8")
s = once(s, '    schemaVersion: SCHEMA_VERSION,\n    profile: {', '    schemaVersion: SCHEMA_VERSION,\n    ui: { onboardingComplete: false },\n    profile: {', 'ui defaults')
s = once(s, '      heightCm: 185,', '      heightCm: 185,\n      objective: "Bajar grasa y ganar músculo",', 'objective default')
s = once(s, '    } else {\n      Object.assign(d.profile, source.profile||{});', '    } else {\n      Object.assign(d.ui, source.ui||{});\n      Object.assign(d.profile, source.profile||{});', 'ui migrate')
s = once(s, '      schemaVersion:SCHEMA_VERSION,\n      profile:{...d.profile,...(s.profile||{})},', '      schemaVersion:SCHEMA_VERSION,\n      ui:{...d.ui,...(s.ui||{})},\n      profile:{...d.profile,...(s.profile||{})},', 'ui normalize')
s = once(s, '    out.profile.age = Math.floor(number(out.profile.age,13,100,33));', '    out.ui.onboardingComplete = Boolean(out.ui.onboardingComplete);\n    out.profile.objective = String((s.profile && (s.profile.objective || s.profile.goal)) || out.profile.objective || "Bajar grasa y ganar músculo");\n    out.profile.age = Math.floor(number(out.profile.age,13,100,33));', 'objective normalize')
s = once(s, '      weight:number(r.weight,40,300,110),', '      weight:r.weight==null?null:number(r.weight,40,300,null),', 'review weight null')
s = once(s, '      pushups:number(r.pushups,0,300,0),', '      pushups:r.pushups==null?null:number(r.pushups,0,300,null),', 'review pushups null')
s = once(s, '      plank:number(r.plank,0,1800,0),', '      plank:r.plank==null?null:number(r.plank,0,1800,null),', 'review plank null')
s = once(s, '      decision: String(s.decision || "maintain")\n    };', '      decision: String(s.decision || "maintain"),\n      substitutions:Array.isArray(s.substitutions)?s.substitutions:[],\n      exerciseIds:Array.isArray(s.exerciseIds)?s.exerciseIds.map(String):[],\n      guided:Boolean(s.guided)\n    };', 'session metadata')
s = once(s, '    out.reviews.sort((a,b)=>a.date.localeCompare(b.date));', '    out.progression.sessions = Math.max(out.progression.sessions, out.sessionLogs.length);\n    out.reviews.sort((a,b)=>a.date.localeCompare(b.date));', 'session reconciliation')
ds.write_text(s, encoding="utf-8")

hp = Path("www/index.html")
h = hp.read_text(encoding="utf-8")
h = once(h, '<label>Peso objetivo (kg)</label><input id="pgoal" type="number" min="40" max="300" step="0.1">', '<label>Objetivo principal</label><select id="pobjective"><option>Bajar grasa y ganar músculo</option><option>Mejorar condición</option><option>Ganar fuerza</option></select>\n   <label>Peso objetivo (kg)</label><input id="pgoal" type="number" min="40" max="300" step="0.1">', 'profile objective control')
hp.write_text(h, encoding="utf-8")

ap = Path("www/app.js")
a = ap.read_text(encoding="utf-8")
a = once(a, 'function cleanNumber(v,min,max,fallback){const n=Number(v);return Number.isFinite(n)&&n>=min&&n<=max?n:fallback}', 'function cleanNumber(v,min,max,fallback){const n=Number(v);return Number.isFinite(n)&&n>=min&&n<=max?n:fallback}\nfunction localDateISO(d=new Date()){const y=d.getFullYear(),m=String(d.getMonth()+1).padStart(2,"0"),day=String(d.getDate()).padStart(2,"0");return `${y}-${m}-${day}`}', 'local date helper')
a = a.replace('new Date().toISOString().slice(0,10)', 'localDateISO()')
a = a.replace('now.toISOString().slice(0,10)', 'localDateISO(now)')
a = once(a, 'function patternAsset(id){return `assets/exercises/${id}.svg`}', 'function exerciseAsset(id){return `./assets/exercises/${id}.svg`}', 'duplicate asset function')
a = once(a, '$("guidedImage").src=patternAsset(id);', '$("guidedImage").src=exerciseAsset(id);', 'guided exercise asset')
a = once(a, 'function guidedRender(){', 'function exerciseLinesForSession(s){return (s?.items||[]).filter(x=>!x.startsWith("Semana de descarga")&&!x.startsWith("Circuito ·"))}\nfunction guidedRender(){', 'exercise lines helper')
a = once(a, 'const id=s.exerciseIds[guidedState.index],ex=window.FORGE_EXERCISES?.byId(id),line=s.items.find(x=>ex&&x.includes(ex.name))||s.items[guidedState.index]||ex?.name||id;', 'const id=s.exerciseIds[guidedState.index],ex=window.FORGE_EXERCISES?.byId(id),line=exerciseLinesForSession(s)[guidedState.index]||ex?.name||id;', 'guided line mapping')
a = once(a, 'function completeCurrentExercise(){const s=guidedState.session,id=s.exerciseIds[guidedState.index],ex=window.FORGE_EXERCISES?.byId(id),line=s.items.find(x=>ex&&x.includes(ex.name))||"",count=seriesCount(line);', 'function completeCurrentExercise(){const s=guidedState.session,id=s.exerciseIds[guidedState.index],ex=window.FORGE_EXERCISES?.byId(id),line=exerciseLinesForSession(s)[guidedState.index]||"",count=seriesCount(line);', 'guided completion mapping')
a = once(a, 'session.items.map((x,i)=>{const ex=session.exerciseIds?.[i]?EXLIB.byId(session.exerciseIds[i]):null', 'exerciseLinesForSession(session).map((x,i)=>{const ex=session.exerciseIds?.[i]?EXLIB.byId(session.exerciseIds[i]):null', 'manual lines')
a = once(a, 'const omitted=checks.map((c,i)=>c.checked?null:session.items[i]).filter(Boolean),completion=done/checks.length;', 'const planned=exerciseLinesForSession(session),omitted=checks.map((c,i)=>c.checked?null:planned[i]).filter(Boolean),completion=done/checks.length;', 'manual omitted')
a = once(a, 'planned:session.items,completed:checks.map((c,i)=>c.checked?session.items[i]:null).filter(Boolean),omitted,', 'planned,completed:checks.map((c,i)=>c.checked?planned[i]:null).filter(Boolean),omitted,', 'manual completed')
a = once(a, 'let mins=(eh*60+em)-(sh*60+sm);if(mins<=0)mins+=1440;return mins;', 'let mins=(eh*60+em)-(sh*60+sm);if(mins===0)return 0;if(mins<0)mins+=1440;return mins;', 'duration math')
a = once(a, 'if(!start||!end||!Number.isFinite(duration)||duration<=0){', 'if(!start||!end||!Number.isFinite(duration)||duration<=0||duration>240){', 'manual duration guard')
a = once(a, '!Number.isFinite(duration)||duration<1){', '!Number.isFinite(duration)||duration<1||duration>180){', 'guided duration guard')
a = once(a, 'a.download="forge-ascent-v1-3-backup.json";', 'a.download="forge-ascent-v2-backup.json";', 'backup filename')
a = once(a, 'function firstValid(arr,key){for(const x of arr){const v=Number(x?.[key]);if(Number.isFinite(v))return v}return null}', 'function firstValid(arr,key){for(const x of arr){const raw=x?.[key];if(raw==null||raw==="")continue;const v=Number(raw);if(Number.isFinite(v))return v}return null}', 'analytics first null')
a = once(a, 'function lastValid(arr,key){for(let i=arr.length-1;i>=0;i--){const v=Number(arr[i]?.[key]);if(Number.isFinite(v))return v}return null}', 'function lastValid(arr,key){for(let i=arr.length-1;i>=0;i--){const raw=arr[i]?.[key];if(raw==null||raw==="")continue;const v=Number(raw);if(Number.isFinite(v))return v}return null}', 'analytics last null')
a = once(a, 'function trendLabel(values,lowerIsBetter=false){const c=values.map(Number).filter(Number.isFinite);', 'function trendLabel(values,lowerIsBetter=false){const c=values.filter(v=>v!=null&&v!=="").map(Number).filter(Number.isFinite);', 'analytics trend null')
a = once(a, '$("pname").value=p.name;$("page").value=p.age;$("pheight").value=p.heightCm;$("pgoal").value=p.goalWeightKg;', '$("pname").value=p.name;$("page").value=p.age;$("pheight").value=p.heightCm;$("pobjective").value=p.objective||"Bajar grasa y ganar músculo";$("pgoal").value=p.goalWeightKg;', 'profile objective fill')
a = once(a, 'const p={name:$("pname").value.trim()||"Operador",age:', 'const p={name:$("pname").value.trim()||"Operador",objective:$("pobjective").value,age:', 'profile objective save')
a = once(a, 'state.profile.goal=$("onboardGoal").value;view.reviews.push({date:localDateISO(),pain:Number($("onboardPain").value||0),energy:Number($("onboardEnergy").value||6),sleep:8});', 'state.profile.objective=$("onboardGoal").value;view.reviews.push({date:localDateISO(),weight:null,waist:null,pushups:null,plank:null,pain:Number($("onboardPain").value||0),energy:Number($("onboardEnergy").value||6),sleep:8,notes:"Check-in inicial"});', 'onboarding data')
a = once(a, 'function startRest(){if(guidedState.restTimer)clearInterval(guidedState.restTimer);guidedState.restTimer=setInterval(()=>{', 'function startRest(){if(guidedState.restSeconds<=0)guidedState.restSeconds=30;if(guidedState.restTimer)clearInterval(guidedState.restTimer);guidedState.restTimer=setInterval(()=>{', 'rest restart')

a += '''

// FORGE ASCENT v2.0.6 — audited late bindings.
window.setView=function(target){
 const targetView=document.getElementById(target);if(!targetView||!targetView.classList.contains('view'))return false;
 document.querySelectorAll('.view').forEach(v=>v.classList.toggle('active',v===targetView));
 const direct=document.querySelector(`nav button[data-view="${target}"]`);
 document.querySelectorAll('nav button').forEach(b=>b.classList.toggle('active',direct?b===direct:b.dataset.view==='operator'));
 try{refresh()}catch(e){console.error('FORGE ASCENT view refresh failed',e)}window.scrollTo({top:0,left:0,behavior:'auto'});return true;
};
(function bindLateUi(){
 function button(id,fn){const el=document.getElementById(id);if(!el)return;el.type='button';el.onclick=fn}
 function bind(){
  const step=()=>Number(document.querySelector('.onboarding-step:not(.hidden)')?.dataset.step||0);
  document.querySelectorAll('.onboarding-next').forEach(b=>{b.type='button';b.onclick=()=>showOnboardingStep(step()+1)});
  document.querySelectorAll('.onboarding-prev').forEach(b=>{b.type='button';b.onclick=()=>showOnboardingStep(step()-1)});
  button('onboardingFinish',finishOnboarding);
  document.querySelectorAll('[data-open-view]').forEach(b=>{b.type='button';b.onclick=()=>window.setView(b.dataset.openView)});
  button('closeGuided',guidedClose);button('guidedPrev',()=>{guidedState.index--;guidedRender()});button('guidedNext',()=>{guidedState.index++;guidedRender()});button('guidedComplete',completeCurrentExercise);
  button('restStart',startRest);button('restSkip',()=>{if(guidedState.restTimer){clearInterval(guidedState.restTimer);guidedState.restTimer=null}guidedState.restSeconds=30;updateRest()});button('restAdd',()=>{guidedState.restSeconds+=15;updateRest()});
  button('completeClose',()=>{document.getElementById('missionComplete').classList.add('hidden');renderTraining()});button('closeoutBack',()=>{document.getElementById('missionCloseout').classList.add('hidden');document.getElementById('guidedSession').classList.remove('hidden');guidedRender()});button('closeoutSave',saveGuidedMission);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});else bind();
})();
'''

ap.write_text(a, encoding="utf-8")

# Static gates.
h = Path("www/index.html").read_text(encoding="utf-8")
ids = set(re.findall(r'id="([^"]+)"', h))
refs = set(re.findall(r'\$\("([^"]+)"\)', a))
if refs - ids:
    raise SystemExit(f"Missing DOM IDs: {sorted(refs-ids)}")
if len(re.findall(r'\bfunction\s+patternAsset\s*\(', a)) != 1:
    raise SystemExit("patternAsset duplicate remains")
if 'toISOString().slice(0,10)' in a:
    raise SystemExit("UTC date conversion remains")
targets = set(re.findall(r'data-open-view="([^"]+)"', h))
view_ids = set(re.findall(r'<section[^>]+id="([^"]+)"[^>]+class="[^"]*\bview\b', h))
if targets != {'profile','review','body','tests','library','data'} or targets-view_ids:
    raise SystemExit("Operator navigation mismatch")
lib = json.loads(Path("www/exercise-library.json").read_text(encoding="utf-8"))
exercise_ids = {x['id'] for x in lib['exercises']}
asset_ids = {p.stem for p in Path("www/assets/exercises").glob("*.svg")}
if exercise_ids != asset_ids or len(exercise_ids) != 18:
    raise SystemExit("Exercise visual mismatch")
print("runtime/static audit PASS")
