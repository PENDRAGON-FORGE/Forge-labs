from pathlib import Path
import json

# Build on v2.0.8 safety and integrity hardening.
exec(Path('audit_v208.py').read_text(encoding='utf-8'))

def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Patch anchor missing: {label}')
    return text.replace(old,new,1)

# 1) Manual partial sessions should be logged and earn proportional XP, but should not
# count as a completed weekly mission until at least 70% of planned exercises are done.
ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')
old='''view.sessionLogs.push(log);view.weekProgress[String(view.activeWeek)]=[...current,activeDay];view.sessions++;view.xp+=Math.round(session.xp*completion);\n save();$("workoutMsg").textContent=`Sesión guardada · ${duration} min · +${Math.round(session.xp*completion)} EXP.`;resetSessionForm();refresh();'''
new='''view.sessionLogs.push(log);if(completion>=.70)view.weekProgress[String(view.activeWeek)]=[...current,activeDay];view.sessions++;view.xp+=Math.round(session.xp*completion);\n save();$("workoutMsg").textContent=completion>=.70?`Sesión guardada · ${duration} min · +${Math.round(session.xp*completion)} EXP.`:`Sesión parcial guardada (${Math.round(completion*100)}%) · +${Math.round(session.xp*completion)} EXP. No cuenta aún como misión semanal.`;resetSessionForm();refresh();'''
a=once(a,old,new,'manual completion threshold')

# Guided session log should use the actual exercise list as planned, not informational banners.
a=once(a,'planned:s.items,completed,omitted:[],','planned:exerciseLinesForSession(s),completed,omitted:[],','guided planned list')
ap.write_text(a,encoding='utf-8')

# 2) Backup reconstruction must follow the same 70% mission-credit rule.
ds=Path('www/data-store.js')
s=ds.read_text(encoding='utf-8')
s=once(s,'    for(const log of out.sessionLogs){\n      const wk=String(log.week),day=Math.max(0,Math.min(4,Number(log.day)-1));','    for(const log of out.sessionLogs){\n      if(Number(log.completion)<0.70) continue;\n      const wk=String(log.week),day=Math.max(0,Math.min(4,Number(log.day)-1));','week credit threshold')
ds.write_text(s,encoding='utf-8')

# 3) Expose and enforce difficulty filtering on primary progression candidates, not only fallbacks.
elp=Path('www/exercise-library.js')
el=elp.read_text(encoding='utf-8')
el=once(el,'return{load,all,byId,byPattern,select,replacementFor,riskAllowed,equipmentMatches,score,resolveId};','return{load,all,byId,byPattern,select,replacementFor,riskAllowed,difficultyAllowed,equipmentMatches,score,resolveId};','expose difficultyAllowed')
elp.write_text(el,encoding='utf-8')

ae=Path('www/adaptive-engine.js')
e=ae.read_text(encoding='utf-8')
e=once(e,'if(ex&&X.riskAllowed(ex,ctx)&&X.equipmentMatches(ex,ctx.equipment))return{id,reason:null}','if(ex&&X.riskAllowed(ex,ctx)&&X.equipmentMatches(ex,ctx.equipment)&&(!X.difficultyAllowed||X.difficultyAllowed(ex,ctx)))return{id,reason:null}','candidate difficulty filter')
ae.write_text(e,encoding='utf-8')

# 4) Add an equipment-free cardio fallback so zero-equipment users keep complete sessions.
tp=Path('www/training-data.js')
t=tp.read_text(encoding='utf-8')
t=once(t,'cardio:{1:["treadmill_walk"],2:["treadmill_brisk","treadmill_walk"],3:["treadmill_brisk","treadmill_walk"]},','cardio:{1:["treadmill_walk","march_in_place"],2:["treadmill_brisk","treadmill_walk","march_in_place"],3:["treadmill_brisk","treadmill_walk","march_in_place"]},','cardio fallback progression')
t=once(t,'treadmill_walk:{name:"Caminata en caminadora",base:15,unit:"min",pattern:"cardio"},','treadmill_walk:{name:"Caminata en caminadora",base:15,unit:"min",pattern:"cardio"},\n    march_in_place:{name:"Marcha activa sin equipo",base:15,unit:"min",pattern:"cardio"},','cardio fallback template')
tp.write_text(t,encoding='utf-8')

jp=Path('www/exercise-library.json')
lib=json.loads(jp.read_text(encoding='utf-8'))
if not any(x.get('id')=='march_in_place' for x in lib['exercises']):
    lib['exercises'].append({
      'id':'march_in_place','name':'Marcha activa sin equipo','pattern':'cardio','difficulty':1,
      'equipment':[],'fatigue':2,'lumbarStress':1,'jointStress':1,'technicalComplexity':1,
      'primaryMuscles':['piernas'],'secondaryMuscles':[],'regression':None,
      'progression':'treadmill_walk','replacementTags':['bajo_impacto','sin_equipo','principiante']
    })
jp.write_text(json.dumps(lib,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')

# Reuse the existing cardio form-guide artwork but relabel it accurately for the no-equipment variant.
svgp=Path('www/assets/exercises/march_in_place.svg')
base=Path('www/assets/exercises/treadmill_walk.svg').read_text(encoding='utf-8')
base=base.replace('Caminata en caminadora','Marcha activa sin equipo')
base=base.replace('Paso cómodo, postura alta y respiración estable.','Marcha controlada, postura alta y respiración estable; sin caminadora.')
svgp.write_text(base,encoding='utf-8')

# Static gates.
if 'completion>=.70' not in a: raise SystemExit('manual mission-credit threshold missing')
if 'Number(log.completion)<0.70' not in s: raise SystemExit('backup mission-credit threshold missing')
if 'difficultyAllowed(ex,ctx)' not in e: raise SystemExit('difficulty filter missing')
if 'march_in_place' not in t: raise SystemExit('no-equipment cardio template missing')
if not svgp.exists(): raise SystemExit('no-equipment cardio visual missing')
print('v2.0.9 progression/equipment hardening PASS')
