from pathlib import Path

# Build on v2.0.10 analytics/rank/progression hardening.
exec(Path('audit_v210.py').read_text(encoding='utf-8'))

def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Patch anchor missing: {label}')
    return text.replace(old,new,1)

ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')

# 1) Do not allow activating a future week before the current active week is closed.
a=once(a,
'$("activateWeek").addEventListener("click",()=>{view.activeWeek=view.selectedWeek;if(!view.weekProgress[String(view.activeWeek)])view.weekProgress[String(view.activeWeek)]=[];save();$("calendarMsg").textContent=`Semana ${view.activeWeek} activada sin borrar su progreso.`;refresh()});',
'$("activateWeek").addEventListener("click",()=>{if(view.selectedWeek>view.activeWeek){$("calendarMsg").textContent=`Cierra primero la semana ${view.activeWeek} antes de avanzar.`;return}view.activeWeek=view.selectedWeek;if(!view.weekProgress[String(view.activeWeek)])view.weekProgress[String(view.activeWeek)]=[];save();$("calendarMsg").textContent=`Semana ${view.activeWeek} activada sin borrar su progreso.`;refresh()});',
'future week activation guard')

# 2) Partial-session retries may improve a slot, but only the incremental completion earns XP.
old=''' const checks=[...document.querySelectorAll(".check")],done=checks.filter(x=>x.checked).length,current=daysFor(),session=ENGINE.buildSession(activeDay,view.activeWeek,state,DATA);\n if(current.includes(activeDay)){$("workoutMsg").textContent="Misión ya contabilizada para esta semana.";return}'''
new=''' const checks=[...document.querySelectorAll(".check")],done=checks.filter(x=>x.checked).length,current=daysFor(),session=ENGINE.buildSession(activeDay,view.activeWeek,state,DATA);\n const priorBest=Math.max(0,...view.sessionLogs.filter(x=>Number(x.week)===view.activeWeek&&Number(x.day)===activeDay+1).map(x=>Number(x.completion)||0));\n if(current.includes(activeDay)){$("workoutMsg").textContent="Misión ya contabilizada para esta semana.";return}'''
a=once(a,old,new,'manual prior completion')
old=''' view.sessionLogs.push(log);if(completion>=.70)view.weekProgress[String(view.activeWeek)]=[...current,activeDay];view.sessions++;view.xp+=Math.round(session.xp*completion);\n save();$("workoutMsg").textContent=completion>=.70?`Sesión guardada · ${duration} min · +${Math.round(session.xp*completion)} EXP.`:`Sesión parcial guardada (${Math.round(completion*100)}%) · +${Math.round(session.xp*completion)} EXP. No cuenta aún como misión semanal.`;resetSessionForm();refresh();'''
new=''' const priorCredit=Math.round(session.xp*Math.min(1,priorBest)),newCredit=Math.round(session.xp*Math.min(1,completion)),xpEarned=Math.max(0,newCredit-priorCredit);\n view.sessionLogs.push(log);if(completion>=.70)view.weekProgress[String(view.activeWeek)]=[...current,activeDay];view.sessions++;view.xp+=xpEarned;\n save();$("workoutMsg").textContent=completion>=.70?`Sesión guardada · ${duration} min · +${xpEarned} EXP.`:`Sesión parcial guardada (${Math.round(completion*100)}%) · +${xpEarned} EXP incremental. No cuenta aún como misión semanal.`;resetSessionForm();refresh();'''
a=once(a,old,new,'manual incremental XP')

# Guided completion after a partial manual attempt only earns the remaining slot XP.
old=''' const current=view.weekProgress[String(view.activeWeek)]||[];\n if(current.includes(activeDay)){ $("closeoutMsg").textContent="Esta misión ya está registrada para hoy."; return; }\n const now=new Date(), end=now.toTimeString().slice(0,5);'''
new=''' const current=view.weekProgress[String(view.activeWeek)]||[];\n if(current.includes(activeDay)){ $("closeoutMsg").textContent="Esta misión ya está registrada para hoy."; return; }\n const priorBest=Math.max(0,...view.sessionLogs.filter(x=>Number(x.week)===view.activeWeek&&Number(x.day)===activeDay+1).map(x=>Number(x.completion)||0));\n const now=new Date(), end=now.toTimeString().slice(0,5);'''
a=once(a,old,new,'guided prior completion')
old=''' view.sessionLogs.push(log);view.weekProgress[String(view.activeWeek)]=[...current,activeDay];view.sessions++;view.xp+=Math.round(s.xp||0);\n STORE.save(state);\n $("missionCloseout").classList.add("hidden");$("missionComplete").classList.remove("hidden");\n $("completeXp").textContent=`+${s.xp||0} EXP`;'''
new=''' const fullCredit=Math.round(s.xp||0),priorCredit=Math.round(fullCredit*Math.min(1,priorBest)),xpEarned=Math.max(0,fullCredit-priorCredit);\n view.sessionLogs.push(log);view.weekProgress[String(view.activeWeek)]=[...current,activeDay];view.sessions++;view.xp+=xpEarned;\n STORE.save(state);\n $("missionCloseout").classList.add("hidden");$("missionComplete").classList.remove("hidden");\n $("completeXp").textContent=`+${xpEarned} EXP`;'''
a=once(a,old,new,'guided incremental XP')

# 3) Physical tests: one rewarded record per 4-week cycle; future cycles stay locked.
old='''  if(!t.date||Object.values(t).some(v=>typeof v==="number"&&!Number.isFinite(v))){$("testMsg").textContent="Revisa los campos de la prueba.";return}\n  if(t.pain>=5){$("testMsg").textContent="Prueba no guardada como válida: dolor demasiado alto.";return}\n  const i=state.tests.findIndex(x=>x.id===t.id);if(i>=0)state.tests[i]=t;else{state.tests.push(t);view.xp+=100}'''
new='''  if(!t.date||Object.values(t).some(v=>typeof v==="number"&&!Number.isFinite(v))){$("testMsg").textContent="Revisa los campos de la prueba.";return}\n  if(t.pain>=5){$("testMsg").textContent="Prueba no guardada como válida: dolor demasiado alto.";return}\n  if(t.cycle*4>view.activeWeek){$("testMsg").textContent=`El ciclo ${t.cycle} se habilita al llegar a la semana ${t.cycle*4}.`;return}\n  t.id=`cycle-${t.cycle}`;const i=state.tests.findIndex(x=>Number(x.cycle)===t.cycle);if(i>=0)state.tests[i]=t;else{state.tests.push(t);view.xp+=100}'''
a=once(a,old,new,'test cycle reward lock')

ap.write_text(a,encoding='utf-8')

# 4) Sanitize completedWeeks against real weekly progress on save/import, and keep activeWeek consistent.
ds=Path('www/data-store.js')
s=ds.read_text(encoding='utf-8')
anchor='''    out.progression.sessions = Math.max(out.progression.sessions, out.sessionLogs.length);\n    out.reviews.sort((a,b)=>a.date.localeCompare(b.date));'''
replacement='''    out.progression.completedWeeks = out.progression.completedWeeks.filter(w=>(out.progression.weekProgress[String(w)]||[]).length>=4);\n    if(out.progression.completedWeeks.length){const next=Math.min(24,Math.max(...out.progression.completedWeeks)+1);out.progression.activeWeek=Math.max(out.progression.activeWeek,next);out.progression.selectedWeek=Math.max(out.progression.selectedWeek,out.progression.activeWeek)}\n    out.progression.sessions = Math.max(out.progression.sessions, out.sessionLogs.length);\n    out.reviews.sort((a,b)=>a.date.localeCompare(b.date));'''
s=once(s,anchor,replacement,'completed week reconciliation')
ds.write_text(s,encoding='utf-8')

# Static guarantees.
checks=[
 ('future activation guard','Cierra primero la semana ${view.activeWeek}' in a),
 ('manual incremental XP','xpEarned=Math.max(0,newCredit-priorCredit)' in a),
 ('guided incremental XP','xpEarned=Math.max(0,fullCredit-priorCredit)' in a),
 ('cycle test lock','t.id=`cycle-${t.cycle}`' in a and 't.cycle*4>view.activeWeek' in a),
 ('completed week reconciliation','out.progression.completedWeeks = out.progression.completedWeeks.filter' in s),
]
for name,ok in checks:
    if not ok: raise SystemExit(f'{name} missing')
print('v2.0.11 lifecycle/XP hardening PASS')
