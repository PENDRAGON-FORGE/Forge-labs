from pathlib import Path

# Build on v2.0.13 completion/perfect-week hardening.
exec(Path('audit_v213.py').read_text(encoding='utf-8'))

def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Patch anchor missing: {label}')
    return text.replace(old,new,1)

ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')

# 1) Long-term adherence metrics are derived only from CLOSED weeks.
# This prevents an in-progress week from depressing adherence prematurely.
insert='''\nfunction adherenceStats(){\n const completed=(view.completedWeeks||[]).slice().sort((x,y)=>x-y);\n const closedMissions=completed.reduce((sum,w)=>sum+(view.weekProgress[String(w)]||[]).length,0);\n const planned=completed.length*5;\n const adherence=planned?Math.round((closedMissions/planned)*100):null;\n const perfect=completed.filter(w=>(view.weekProgress[String(w)]||[]).length>=5).length;\n return {completedWeeks:completed.length,closedMissions,planned,adherence,perfect,programComplete:completed.includes(24)}\n}\nfunction ensureProgramStatusPanel(){\n let box=$("programStatusPanel");if(box)return box;\n const achievements=$("achievementsPanel"),data=$("data"),parent=achievements?.parentNode||data?.parentNode;if(!parent)return null;\n box=document.createElement("section");box.className="card";box.id="programStatusPanel";\n if(achievements)parent.insertBefore(box,achievements);else parent.insertBefore(box,data);return box\n}\nfunction renderProgramStatus(){\n const box=ensureProgramStatusPanel();if(!box)return;const m=adherenceStats();\n const adherence=m.adherence==null?"—":`${m.adherence}%`;\n const status=m.programComplete?"PROGRAMA CERRADO":`Semana activa ${view.activeWeek}/24`;\n box.innerHTML=`<h3>Estado del programa</h3><div class="grid"><div><strong>${status}</strong><div class="muted">${m.completedWeeks}/24 semanas cerradas</div></div><div><strong>${adherence}</strong><div class="muted">Adherencia en semanas cerradas</div></div><div><strong>${m.closedMissions}/${m.planned||0}</strong><div class="muted">Misiones válidas / planificadas cerradas</div></div><div><strong>${m.perfect}</strong><div class="muted">Semanas perfectas 5/5</div></div></div>`\n}\n'''
anchor='function programComplete(){return view.completedWeeks.includes(24)}'
if anchor not in a: raise SystemExit('program complete insertion anchor missing')
a=a.replace(anchor,insert+'\n'+anchor,1)

# 2) Render long-term status with the standard refresh path.
a=once(a,'renderHistory();renderAchievements();','renderHistory();renderAchievements();renderProgramStatus();','program status refresh')

# 3) Once 24/24 is closed, the program is read-only for mission logging.
a=once(a,
' const checks=[...document.querySelectorAll(".check")],done=checks.filter(x=>x.checked).length,current=daysFor(),session=ENGINE.buildSession(activeDay,view.activeWeek,state,DATA);',
' if(programComplete()){$("workoutMsg").textContent="ASCENSO COMPLETO · El programa está cerrado. Tus registros permanecen disponibles en Progreso y Operador.";return}\n const checks=[...document.querySelectorAll(".check")],done=checks.filter(x=>x.checked).length,current=daysFor(),session=ENGINE.buildSession(activeDay,view.activeWeek,state,DATA);',
'manual post-program guard')

a=once(a,
' const current=view.weekProgress[String(view.activeWeek)]||[];\n if(current.includes(activeDay)){ $("closeoutMsg").textContent="Esta misión ya está registrada para hoy."; return; }',
' if(programComplete()){ $("closeoutMsg").textContent="ASCENSO COMPLETO · El programa está cerrado."; return; }\n const current=view.weekProgress[String(view.activeWeek)]||[];\n if(current.includes(activeDay)){ $("closeoutMsg").textContent="Esta misión ya está registrada para hoy."; return; }',
'guided post-program guard')

# 4) A completed 24-week program cannot be reactivated into an older week.
a=once(a,
'$("activateWeek").addEventListener("click",()=>{if(view.selectedWeek>view.activeWeek){$("calendarMsg").textContent=`Cierra primero la semana ${view.activeWeek} antes de avanzar.`;return}',
'$("activateWeek").addEventListener("click",()=>{if(programComplete()){$("calendarMsg").textContent="ASCENSO COMPLETO · El programa de 24 semanas ya está cerrado.";return}if(view.selectedWeek>view.activeWeek){$("calendarMsg").textContent=`Cierra primero la semana ${view.activeWeek} antes de avanzar.`;return}',
'post-program week activation guard')

ap.write_text(a,encoding='utf-8')

# 5) Store invariants for long-term use: completed weeks unique/sorted and weekProgress slots unique.
ds=Path('www/data-store.js')
s=ds.read_text(encoding='utf-8')
anchor='    out.progression.completedWeeks = out.progression.completedWeeks.filter(w=>(out.progression.weekProgress[String(w)]||[]).length>=4);'
replace='''    for(const wk of Object.keys(out.progression.weekProgress)){\n      out.progression.weekProgress[wk]=[...new Set((out.progression.weekProgress[wk]||[]).map(Number).filter(d=>Number.isInteger(d)&&d>=0&&d<=4))].sort((a,b)=>a-b);\n    }\n    out.progression.completedWeeks=[...new Set(out.progression.completedWeeks.map(Number).filter(w=>Number.isInteger(w)&&w>=1&&w<=24))].sort((a,b)=>a-b);\n    out.progression.completedWeeks = out.progression.completedWeeks.filter(w=>(out.progression.weekProgress[String(w)]||[]).length>=4);'''
s=once(s,anchor,replace,'long-term progression normalization')
ds.write_text(s,encoding='utf-8')

checks=[
 ('adherence engine','function adherenceStats()' in a and 'closedMissions' in a),
 ('dynamic status panel','function ensureProgramStatusPanel()' in a and 'programStatusPanel' in a),
 ('status renderer','function renderProgramStatus()' in a and 'renderProgramStatus();' in a),
 ('manual post-program guard','programa está cerrado. Tus registros permanecen disponibles' in a),
 ('guided post-program guard','ASCENSO COMPLETO · El programa está cerrado.' in a),
 ('activation post-program guard','El programa de 24 semanas ya está cerrado.' in a),
 ('week progress dedupe','new Set((out.progression.weekProgress[wk]' in s),
 ('completed week dedupe','new Set(out.progression.completedWeeks.map(Number)' in s),
]
for name,ok in checks:
    if not ok: raise SystemExit(f'{name} missing')
print('v2.0.14 long-term/adherence hardening PASS')
