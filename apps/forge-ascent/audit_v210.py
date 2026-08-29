from pathlib import Path

# Build on all v2.0.9 progression/equipment hardening.
exec(Path('audit_v209.py').read_text(encoding='utf-8'))

def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Patch anchor missing: {label}')
    return text.replace(old,new,1)

ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')

# 1) Extend rank progression so the gamified identity keeps evolving across the 24-week plan.
a=once(a,
'function rank(){return ["RECLUTA","CADETE","SOLDADO","VETERANO","OPERADOR","SOMBRA"][Math.min(5,level()-1)]}',
'function rank(){const l=level();if(l>=36)return"FORJADO";if(l>=33)return"ÉLITE";if(l>=29)return"ASCENDENTE";if(l>=25)return"VANGUARDIA";if(l>=21)return"CENTINELA";if(l>=17)return"SOMBRA";if(l>=13)return"OPERADOR";if(l>=9)return"VETERANO";if(l>=6)return"SOLDADO";if(l>=3)return"CADETE";return"RECLUTA"}',
'rank progression')
a=once(a,
'$("coreLevelBadge").textContent=`LV ${lv}`;$("operatorRank").textContent=`Operador · Nivel ${lv}`',
'$("coreLevelBadge").textContent=`LV ${lv}`;$("operatorRank").textContent=`${rank()} · Nivel ${lv}`',
'operator rank display')

# 2) Stop fabricating fitness baselines when the user has not entered measurements yet.
a=once(a,
'const startWeight=firstValid(bodySeries,"weightKg")??110,currentWeight=lastValid(bodySeries,"weightKg")??view.weight;',
'const startWeight=firstValid(bodySeries,"weightKg"),currentWeight=lastValid(bodySeries,"weightKg");',
'weight analytics baseline')
a=once(a,
'const startPush=firstValid(reviews,"pushups")??6,currentPush=lastValid(reviews,"pushups")??6;',
'const startPush=firstValid(reviews,"pushups"),currentPush=lastValid(reviews,"pushups");',
'pushup analytics baseline')
a=once(a,
'const startPlank=firstValid(reviews,"plank")??30,currentPlank=lastValid(reviews,"plank")??30;',
'const startPlank=firstValid(reviews,"plank"),currentPlank=lastValid(reviews,"plank");',
'plank analytics baseline')

old='''$("anWeight").textContent=`${d.currentWeight.toFixed(1)} kg`;$("anWeightDelta").textContent=`Desde inicio: ${fmtDelta(d.currentWeight-d.startWeight," kg")}`;
 $("anWaist").textContent=d.currentWaist==null?"—":`${d.currentWaist.toFixed(1)} cm`;$("anWaistDelta").textContent=d.currentWaist==null||d.startWaist==null?"Sin comparación":`Desde inicio: ${fmtDelta(d.currentWaist-d.startWaist," cm")}`;
 $("anPushups").textContent=d.currentPush;$("anPushupsDelta").textContent=`Desde inicio: ${fmtDelta(d.currentPush-d.startPush)}`;
 $("anPlank").textContent=`${d.currentPlank} s`;$("anPlankDelta").textContent=`Desde inicio: ${fmtDelta(d.currentPlank-d.startPlank," s")}`;'''
new='''$("anWeight").textContent=d.currentWeight==null?"—":`${d.currentWeight.toFixed(1)} kg`;$("anWeightDelta").textContent=d.currentWeight==null||d.startWeight==null?"Sin comparación":`Desde inicio: ${fmtDelta(d.currentWeight-d.startWeight," kg")}`;
 $("anWaist").textContent=d.currentWaist==null?"—":`${d.currentWaist.toFixed(1)} cm`;$("anWaistDelta").textContent=d.currentWaist==null||d.startWaist==null?"Sin comparación":`Desde inicio: ${fmtDelta(d.currentWaist-d.startWaist," cm")}`;
 $("anPushups").textContent=d.currentPush==null?"—":d.currentPush;$("anPushupsDelta").textContent=d.currentPush==null||d.startPush==null?"Sin comparación":`Desde inicio: ${fmtDelta(d.currentPush-d.startPush)}`;
 $("anPlank").textContent=d.currentPlank==null?"—":`${d.currentPlank} s`;$("anPlankDelta").textContent=d.currentPlank==null||d.startPlank==null?"Sin comparación":`Desde inicio: ${fmtDelta(d.currentPlank-d.startPlank," s")}`;'''
a=once(a,old,new,'null-safe analytics cards')

old_table='''$("comparisonTable").innerHTML=`<table><thead><tr><th>Métrica</th><th>Inicio</th><th>Actual</th><th>Cambio</th></tr></thead><tbody><tr><td>Peso</td><td>${d.startWeight.toFixed(1)} kg</td><td>${d.currentWeight.toFixed(1)} kg</td><td>${fmtDelta(d.currentWeight-d.startWeight," kg")}</td></tr><tr><td>Cintura</td><td>${d.startWaist==null?"—":d.startWaist.toFixed(1)+" cm"}</td><td>${d.currentWaist==null?"—":d.currentWaist.toFixed(1)+" cm"}</td><td>${d.currentWaist==null||d.startWaist==null?"—":fmtDelta(d.currentWaist-d.startWaist," cm")}</td></tr><tr><td>Flexiones</td><td>${d.startPush}</td><td>${d.currentPush}</td><td>${fmtDelta(d.currentPush-d.startPush)}</td></tr><tr><td>Plancha</td><td>${d.startPlank} s</td><td>${d.currentPlank} s</td><td>${fmtDelta(d.currentPlank-d.startPlank," s")}</td></tr></tbody></table>`;'''
new_table='''$("comparisonTable").innerHTML=`<table><thead><tr><th>Métrica</th><th>Inicio</th><th>Actual</th><th>Cambio</th></tr></thead><tbody><tr><td>Peso</td><td>${d.startWeight==null?"—":d.startWeight.toFixed(1)+" kg"}</td><td>${d.currentWeight==null?"—":d.currentWeight.toFixed(1)+" kg"}</td><td>${d.currentWeight==null||d.startWeight==null?"—":fmtDelta(d.currentWeight-d.startWeight," kg")}</td></tr><tr><td>Cintura</td><td>${d.startWaist==null?"—":d.startWaist.toFixed(1)+" cm"}</td><td>${d.currentWaist==null?"—":d.currentWaist.toFixed(1)+" cm"}</td><td>${d.currentWaist==null||d.startWaist==null?"—":fmtDelta(d.currentWaist-d.startWaist," cm")}</td></tr><tr><td>Flexiones</td><td>${metricText(d.startPush)}</td><td>${metricText(d.currentPush)}</td><td>${d.currentPush==null||d.startPush==null?"—":fmtDelta(d.currentPush-d.startPush)}</td></tr><tr><td>Plancha</td><td>${metricText(d.startPlank," s")}</td><td>${metricText(d.currentPlank," s")}</td><td>${d.currentPlank==null||d.startPlank==null?"—":fmtDelta(d.currentPlank-d.startPlank," s")}</td></tr></tbody></table>`;'''
a=once(a,old_table,new_table,'comparison table null safety')

a=once(a,
'function renderHistory(){$("history").innerHTML=[...view.reviews].reverse().map(r=>`<tr><td>${r.date}</td><td>${r.weight}</td><td>${r.waist??"—"}</td><td>${r.pushups}</td><td>${r.plank}s</td><td>${r.pain}/10</td></tr>`).join("")||\'<tr><td colspan="6" class="muted">Sin revisiones aún.</td></tr>\'}',
'function renderHistory(){$("history").innerHTML=[...view.reviews].reverse().map(r=>`<tr><td>${r.date}</td><td>${metricText(r.weight)}</td><td>${metricText(r.waist)}</td><td>${metricText(r.pushups)}</td><td>${metricText(r.plank," s")}</td><td>${metricText(r.pain,"/10")}</td></tr>`).join("")||\'<tr><td colspan="6" class="muted">Sin revisiones aún.</td></tr>\'}',
'history null display')

ap.write_text(a,encoding='utf-8')

# Static guarantees.
if 'if(l>=29)return"ASCENDENTE"' not in a: raise SystemExit('extended rank ladder missing')
if '??110' in a or '??6' in a or '??30' in a: raise SystemExit('fabricated analytics baseline remains')
if 'metricText(r.weight)' not in a: raise SystemExit('history null formatting missing')
print('v2.0.10 analytics/rank hardening PASS')
