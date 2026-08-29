from pathlib import Path

# Build on all v2.0.7 backup/progression hardening.
exec(Path('audit_v207.py').read_text(encoding='utf-8'))

def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Patch anchor missing: {label}')
    return text.replace(old,new,1)

# Harden imported dates so malformed/HTML-like strings cannot enter rendered history tables.
ds=Path('www/data-store.js')
s=ds.read_text(encoding='utf-8')
s=once(s,'  function uniqueNumbers(values,min,max){\n    return [...new Set((Array.isArray(values)?values:[]).map(Number).filter(v=>v>=min&&v<=max))];\n  }','  function uniqueNumbers(values,min,max){\n    return [...new Set((Array.isArray(values)?values:[]).map(Number).filter(v=>v>=min&&v<=max))];\n  }\n  function validDate(v){\n    if(typeof v!=="string" || !/^\\d{4}-\\d{2}-\\d{2}$/.test(v)) return false;\n    const [y,m,d]=v.split("-").map(Number),dt=new Date(y,m-1,d);\n    return dt.getFullYear()===y && dt.getMonth()===m-1 && dt.getDate()===d;\n  }','date validator')
s=once(s,'    if(!s || typeof s !== "object" || typeof s.date !== "string") return null;','    if(!s || typeof s !== "object" || !validDate(s.date)) return null;','session date validation')
s=once(s,'    if(!r || typeof r !== "object" || typeof r.date !== "string") return null;','    if(!r || typeof r !== "object" || !validDate(r.date)) return null;','review date validation')
s=once(s,'    if(!t || typeof t !== "object" || typeof t.date !== "string") return null;','    if(!t || typeof t !== "object" || !validDate(t.date)) return null;','test date validation')
s=once(s,'    if(!m || typeof m !== "object" || typeof m.date !== "string") return null;','    if(!m || typeof m !== "object" || !validDate(m.date)) return null;','measurement date validation')
ds.write_text(s,encoding='utf-8')

ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')
a=once(a,'function localDateISO(d=new Date()){const y=d.getFullYear(),m=String(d.getMonth()+1).padStart(2,"0"),day=String(d.getDate()).padStart(2,"0");return `${y}-${m}-${day}`}','function localDateISO(d=new Date()){const y=d.getFullYear(),m=String(d.getMonth()+1).padStart(2,"0"),day=String(d.getDate()).padStart(2,"0");return `${y}-${m}-${day}`}\nfunction escapeHTML(v){return String(v??"").replace(/[&<>"\']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\\\"":"&quot;","\\\'":"&#39;"}[c]||c))}','html escape helper')
old='''function renderProfileSummary(){
 const p=state.profile,s=STORE.summary(state);
 $("profileSummary").innerHTML=`<p><strong>${p.name}</strong></p><p>${p.age} años · ${p.heightCm} cm</p><p>Peso actual: ${s.currentWeightKg.toFixed(1)} kg</p><p>Meta: ${p.goalWeightKg.toFixed(1)} kg</p><p>${p.trainingDays} días/semana · ${p.sessionMinutes} min/sesión</p><p class="muted">${p.equipment.join(", ")||"Sin equipo registrado"}</p>`;
}'''
new='''function renderProfileSummary(){
 const p=state.profile,s=STORE.summary(state),name=escapeHTML(p.name),objective=escapeHTML(p.objective||"Bajar grasa y ganar músculo"),equipment=escapeHTML(p.equipment.join(", ")||"Sin equipo registrado");
 $("profileSummary").innerHTML=`<p><strong>${name}</strong></p><p>${p.age} años · ${p.heightCm} cm</p><p>Peso actual: ${s.currentWeightKg.toFixed(1)} kg</p><p>Objetivo: ${objective}</p><p>Meta: ${p.goalWeightKg.toFixed(1)} kg</p><p>${p.trainingDays} días/semana · ${p.sessionMinutes} min/sesión</p><p class="muted">${equipment}</p>`;
}'''
a=once(a,old,new,'profile summary escaping')
old2='''if(guidedState.index<s.exerciseIds.length-1){guidedState.index++;guidedState.restSeconds=30;updateRest();guidedRender()}else{
 $("guidedSession").classList.add("hidden");'''
new2='''if(guidedState.index<s.exerciseIds.length-1){guidedState.index++;guidedState.restSeconds=30;updateRest();guidedRender()}else{
 const firstMissing=s.exerciseIds.findIndex((_,i)=>!guidedState.done.has(`${i}:0`));
 if(firstMissing>=0){guidedState.index=firstMissing;guidedState.restSeconds=30;updateRest();guidedRender();return}
 $("guidedSession").classList.add("hidden");'''
a=once(a,old2,new2,'guided full-completion gate')
ap.write_text(a,encoding='utf-8')

# Static checks.
if 'firstMissing=s.exerciseIds.findIndex' not in a: raise SystemExit('guided completion gate missing')
if 'function escapeHTML' not in a: raise SystemExit('escapeHTML missing')
if s.count('!validDate(')<4: raise SystemExit('date validation incomplete')
print('v2.0.8 guided/input hardening PASS')
