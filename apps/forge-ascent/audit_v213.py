from pathlib import Path

# Build on v2.0.12 achievements hardening.
exec(Path('audit_v212.py').read_text(encoding='utf-8'))

def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Patch anchor missing: {label}')
    return text.replace(old,new,1)

ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')

# 1) Distinguish completed (4/5) from perfect (5/5) weeks in derived achievements.
a=once(a,
' const completed=(view.completedWeeks||[]).slice().sort((x,y)=>x-y),sessions=view.sessionLogs||[],tests=state.tests||[];\n const achieved=[];',
' const completed=(view.completedWeeks||[]).slice().sort((x,y)=>x-y),sessions=view.sessionLogs||[],tests=state.tests||[];\n const perfect=completed.filter(w=>(view.weekProgress[String(w)]||[]).length>=5);\n const achieved=[];',
'perfect week derivation')
a=once(a,
' if(completed.some(w=>w>=24))add("week_24","ASCENSO COMPLETO","Completa las 24 semanas.");\n if(sessions.filter(s=>Number(s.completion)>=.70).length>=50)add("missions_50","50 MISIONES","Completa 50 misiones válidas.");',
' if(completed.some(w=>w>=24))add("week_24","ASCENSO COMPLETO","Completa las 24 semanas.");\n if(perfect.length>=1)add("perfect_1","SEMANA PERFECTA","Completa las 5 misiones de una misma semana.");\n if(perfect.length>=6)add("perfect_6","DISCIPLINA TOTAL","Completa 6 semanas perfectas.");\n if(sessions.filter(s=>Number(s.completion)>=.70).length>=50)add("missions_50","50 MISIONES","Completa 50 misiones válidas.");',
'perfect achievements')

# 2) Explicit derived program-complete state on the main dashboard.
a=once(a,
'function refresh(){const session=ENGINE.buildSession(activeDay,view.activeWeek,state,DATA);',
'function programComplete(){return view.completedWeeks.includes(24)}\nfunction refresh(){const done=programComplete(),session=ENGINE.buildSession(activeDay,view.activeWeek,state,DATA);',
'program complete helper')
a=once(a,
'$("week").textContent=`${view.activeWeek}/24`;$('+'"sessions"'+')',
'$("week").textContent=done?"24/24 · COMPLETADO":`${view.activeWeek}/24`;$('+'"sessions"'+')',
'week dashboard completed state')
a=once(a,
'$("mission").textContent=`Semana ${view.activeWeek} · ${session.name}`;if($("heroMission"))$("heroMission").textContent=`Semana ${view.activeWeek} · ${session.name}`;if($("heroStatus"))$("heroStatus").textContent=`${modeLabel(session.decision.mode)} · ${session.items.length} bloques`;',
'$("mission").textContent=done?"ASCENSO COMPLETO":`Semana ${view.activeWeek} · ${session.name}`;if($("heroMission"))$("heroMission").textContent=done?"ASCENSO COMPLETO":`Semana ${view.activeWeek} · ${session.name}`;if($("heroStatus"))$("heroStatus").textContent=done?"PROGRAMA CERRADO":`${modeLabel(session.decision.mode)} · ${session.items.length} bloques`;',
'completed dashboard messaging')

# 3) Week-close feedback distinguishes 4/5, 5/5, and final program close; XP remains unchanged.
a=once(a,
'view.completedWeeks.push(w);view.xp+=150;if(w===view.activeWeek&&w<24){view.activeWeek=w+1;view.selectedWeek=view.activeWeek}save();$("calendarMsg").textContent="Semana completada. +150 EXP.";refresh()});',
'const perfectWeek=daysFor(w).length>=5;view.completedWeeks.push(w);view.xp+=150;if(w===view.activeWeek&&w<24){view.activeWeek=w+1;view.selectedWeek=view.activeWeek}save();$("calendarMsg").textContent=w===24?"ASCENSO COMPLETO · Programa de 24 semanas cerrado. +150 EXP.":perfectWeek?"Semana perfecta 5/5. +150 EXP.":"Semana completada 4/5. +150 EXP.";refresh()});',
'week close messaging')

ap.write_text(a,encoding='utf-8')

checks=[
 ('program complete helper','function programComplete()' in a),
 ('program complete UI','ASCENSO COMPLETO' in a and 'PROGRAMA CERRADO' in a),
 ('perfect derivation','const perfect=completed.filter' in a),
 ('perfect achievements','perfect_1' in a and 'perfect_6' in a),
 ('4/5 messaging','Semana completada 4/5' in a),
 ('5/5 messaging','Semana perfecta 5/5' in a),
]
for name,ok in checks:
    if not ok: raise SystemExit(f'{name} missing')
print('v2.0.13 completion/perfect-week hardening PASS')
