from pathlib import Path

# Build on v2.0.11 lifecycle/anti-farming hardening.
exec(Path('audit_v211.py').read_text(encoding='utf-8'))

def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Patch anchor missing: {label}')
    return text.replace(old,new,1)

ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')

# 1) Add derived achievements with no XP rewards. They are recomputed from real state,
# so imports cannot fabricate them and repeated actions cannot farm anything.
insert='''\nfunction computeAchievements(){\n const completed=(view.completedWeeks||[]).slice().sort((x,y)=>x-y),sessions=view.sessionLogs||[],tests=state.tests||[];\n const achieved=[];\n const add=(id,title,detail)=>achieved.push({id,title,detail});\n if(sessions.some(s=>Number(s.completion)>=.70))add("first_mission","PRIMERA MISIÓN","Completa tu primera misión válida.");\n if(completed.length>=1)add("first_week","SEMANA CERRADA","Cierra tu primera semana de entrenamiento.");\n if(tests.length>=1)add("first_cycle","PRIMER CICLO","Registra tu primera prueba física de ciclo.");\n if(completed.some(w=>w>=4))add("week_4","BASE FORJADA","Completa las primeras 4 semanas.");\n if(completed.some(w=>w>=12))add("week_12","MITAD DEL ASCENSO","Completa 12 semanas.");\n if(completed.some(w=>w>=24))add("week_24","ASCENSO COMPLETO","Completa las 24 semanas.");\n if(sessions.filter(s=>Number(s.completion)>=.70).length>=50)add("missions_50","50 MISIONES","Completa 50 misiones válidas.");\n state.achievements=achieved;return achieved\n}\nfunction renderAchievements(){\n const list=$("achievementsList");if(!list)return;\n const items=computeAchievements();\n list.innerHTML=items.length?items.map(x=>`<div class="card"><strong>${escapeHTML(x.title)}</strong><div class="muted">${escapeHTML(x.detail)}</div></div>`).join(""):'<div class="muted">Aún no hay logros desbloqueados.</div>'\n}\n'''
anchor='function renderHistory(){'
if anchor not in a: raise SystemExit('achievement insertion anchor missing')
a=a.replace(anchor,insert+'\n'+anchor,1)

# 2) Render achievements during refresh and after meaningful state changes.
a=once(a,'renderHistory();','renderHistory();renderAchievements();','achievement refresh')

# 3) Add achievements panel to Operator view.
ip=Path('www/index.html')
h=ip.read_text(encoding='utf-8')
anchor='<div id="operatorRank"'
pos=h.find(anchor)
if pos<0: raise SystemExit('operator panel anchor missing')
# insert panel before operatorRank parent area conservatively by using data section marker
marker='<section id="data"'
if marker not in h: raise SystemExit('data section anchor missing')
panel='''<section class="card" id="achievementsPanel"><h3>Logros</h3><div id="achievementsList" class="stack"><div class="muted">Aún no hay logros desbloqueados.</div></div></section>\n'''
h=h.replace(marker,panel+marker,1)
ip.write_text(h,encoding='utf-8')

# 4) Store normalization: achievements are never trusted from import; always derived at runtime.
ds=Path('www/data-store.js')
s=ds.read_text(encoding='utf-8')
# replace normalized achievements assignment if present, otherwise force after tests normalize block
if 'achievements:' in s:
    import re
    s=re.sub(r'achievements\s*:\s*Array\.isArray\([^\n]+\)\?[^\n]+,','achievements: [],',s,count=1)
# static fallback: ensure normalized output clears any imported list
anchor='out.tests = out.tests'
if anchor in s and 'out.achievements=[];' not in s:
    s=s.replace(anchor,'out.achievements=[];\n    '+anchor,1)
ds.write_text(s,encoding='utf-8')

# 5) Achievement definitions must not modify XP.
if 'view.xp' in insert or 'progression.xp' in insert: raise SystemExit('achievement XP side effect')

checks=[
 ('achievement engine','function computeAchievements()' in a),
 ('achievement renderer','function renderAchievements()' in a and 'renderHistory();renderAchievements();' in a),
 ('operator panel','id="achievementsList"' in h),
 ('24-week achievement','week_24' in a),
 ('no achievement xp','view.xp' not in insert),
]
for name,ok in checks:
    if not ok: raise SystemExit(f'{name} missing')
print('v2.0.12 achievements hardening PASS')
