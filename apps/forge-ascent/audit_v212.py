from pathlib import Path

# Build on v2.0.11 lifecycle/anti-farming hardening.
exec(Path('audit_v211.py').read_text(encoding='utf-8'))

def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Patch anchor missing: {label}')
    return text.replace(old,new,1)

ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')

# 1) Derived achievements: no XP rewards, always recomputed from real state.
insert='''\nfunction computeAchievements(){\n const completed=(view.completedWeeks||[]).slice().sort((x,y)=>x-y),sessions=view.sessionLogs||[],tests=state.tests||[];\n const achieved=[];\n const add=(id,title,detail)=>achieved.push({id,title,detail});\n if(sessions.some(s=>Number(s.completion)>=.70))add("first_mission","PRIMERA MISIÓN","Completa tu primera misión válida.");\n if(completed.length>=1)add("first_week","SEMANA CERRADA","Cierra tu primera semana de entrenamiento.");\n if(tests.length>=1)add("first_cycle","PRIMER CICLO","Registra tu primera prueba física de ciclo.");\n if(completed.some(w=>w>=4))add("week_4","BASE FORJADA","Completa las primeras 4 semanas.");\n if(completed.some(w=>w>=12))add("week_12","MITAD DEL ASCENSO","Completa 12 semanas.");\n if(completed.some(w=>w>=24))add("week_24","ASCENSO COMPLETO","Completa las 24 semanas.");\n if(sessions.filter(s=>Number(s.completion)>=.70).length>=50)add("missions_50","50 MISIONES","Completa 50 misiones válidas.");\n state.achievements=achieved;return achieved\n}\nfunction ensureAchievementsPanel(){\n let list=$("achievementsList");if(list)return list;\n const data=$("data");if(!data||!data.parentNode)return null;\n const panel=document.createElement("section");panel.className="card";panel.id="achievementsPanel";\n panel.innerHTML='<h3>Logros</h3><div id="achievementsList" class="stack"><div class="muted">Aún no hay logros desbloqueados.</div></div>';\n data.parentNode.insertBefore(panel,data);return $("achievementsList")\n}\nfunction renderAchievements(){\n const list=ensureAchievementsPanel();if(!list)return;\n const items=computeAchievements();\n list.innerHTML=items.length?items.map(x=>`<div class="card"><strong>${escapeHTML(x.title)}</strong><div class="muted">${escapeHTML(x.detail)}</div></div>`).join(""):'<div class="muted">Aún no hay logros desbloqueados.</div>'\n}\n'''
anchor='function renderHistory(){'
if anchor not in a: raise SystemExit('achievement insertion anchor missing')
a=a.replace(anchor,insert+'\n'+anchor,1)

# 2) Render achievements with the normal refresh path.
a=once(a,'renderHistory();','renderHistory();renderAchievements();','achievement refresh')
ap.write_text(a,encoding='utf-8')

# 3) Store normalization: imported achievements are never trusted.
ds=Path('www/data-store.js')
s=ds.read_text(encoding='utf-8')
if 'achievements:' in s:
    import re
    s=re.sub(r'achievements\s*:\s*Array\.isArray\([^\n]+\)\?[^\n]+,','achievements: [],',s,count=1)
anchor='out.tests = out.tests'
if anchor in s and 'out.achievements=[];' not in s:
    s=s.replace(anchor,'out.achievements=[];\n    '+anchor,1)
ds.write_text(s,encoding='utf-8')

# 4) Achievement definitions must never modify XP.
if 'view.xp' in insert or 'progression.xp' in insert: raise SystemExit('achievement XP side effect')

checks=[
 ('achievement engine','function computeAchievements()' in a),
 ('dynamic achievement panel','function ensureAchievementsPanel()' in a and 'achievementsList' in a),
 ('achievement renderer','function renderAchievements()' in a and 'renderHistory();renderAchievements();' in a),
 ('24-week achievement','week_24' in a),
 ('50-mission achievement','missions_50' in a),
 ('no achievement xp','view.xp' not in insert),
]
for name,ok in checks:
    if not ok: raise SystemExit(f'{name} missing')
print('v2.0.12 achievements hardening PASS')
