from pathlib import Path

# Build on v2.0.14 long-term/adherence hardening.
exec(Path('audit_v214.py').read_text(encoding='utf-8'))

def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Patch anchor missing: {label}')
    return text.replace(old,new,1)

ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')

# 1) Native Android backup bridge with browser fallback.
old='''$("exportBtn").addEventListener("click",()=>{\n const payload=STORE.exportPayload(state),blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"}),a=document.createElement("a");\n a.href=URL.createObjectURL(blob);a.download="forge-ascent-v2-backup.json";a.click();setTimeout(()=>URL.revokeObjectURL(a.href),0);\n});\n$("importFile").addEventListener("change",e=>{\n const f=e.target.files[0];if(!f)return;const reader=new FileReader();\n reader.onload=()=>{try{state=STORE.importPayload(JSON.parse(reader.result));view=legacy();save();$("dataMsg").textContent="Respaldo importado, migrado y validado.";fillProfile();fillForms();refresh()}catch{$("dataMsg").textContent="Archivo inválido: no se importó ningún dato."}};\n reader.readAsText(f);e.target.value="";\n});'''
new='''function androidNative(){return window.ForgeAscentAndroid&&typeof window.ForgeAscentAndroid.exportJson==="function"?window.ForgeAscentAndroid:null}\nfunction importBackupText(text){try{state=STORE.importPayload(JSON.parse(text));view=legacy();save();$("dataMsg").textContent="Respaldo importado, migrado y validado.";fillProfile();fillForms();refresh();return true}catch{$("dataMsg").textContent="Archivo inválido: no se importó ningún dato.";return false}}\nwindow.FORGE_NATIVE_IMPORT=text=>importBackupText(String(text||""));\nwindow.FORGE_NATIVE_STATUS=msg=>{$("dataMsg").textContent=String(msg||"")};\n$("exportBtn").addEventListener("click",()=>{\n const json=JSON.stringify(STORE.exportPayload(state),null,2),native=androidNative();\n if(native){native.exportJson(json,"forge-ascent-v2-backup.json");return}\n const blob=new Blob([json],{type:"application/json"}),a=document.createElement("a");\n a.href=URL.createObjectURL(blob);a.download="forge-ascent-v2-backup.json";a.click();setTimeout(()=>URL.revokeObjectURL(a.href),0);\n});\n$("importFile").addEventListener("click",e=>{const native=androidNative();if(native){e.preventDefault();native.importJson()}});\n$("importFile").addEventListener("change",e=>{\n const f=e.target.files[0];if(!f)return;const reader=new FileReader();\n reader.onload=()=>importBackupText(reader.result);reader.readAsText(f);e.target.value="";\n});'''
a=once(a,old,new,'native backup bridge')

# 2) Android back semantics: close overlays first, then return to Inicio, then let Android exit.
a += '''\n\nwindow.FORGE_ANDROID_BACK=function(){\n const guided=$("guidedSession"),closeout=$("missionCloseout"),complete=$("missionComplete");\n if(closeout&&!closeout.classList.contains("hidden")){closeout.classList.add("hidden");if(guided)guided.classList.remove("hidden");try{guidedRender()}catch{}return true}\n if(complete&&!complete.classList.contains("hidden")){complete.classList.add("hidden");try{renderTraining()}catch{}return true}\n if(guided&&!guided.classList.contains("hidden")){try{guidedClose()}catch{guided.classList.add("hidden")}return true}\n const active=document.querySelector(".view.active");if(active&&active.id!=="home"){window.setView("home");return true}\n return false\n};\n'''
ap.write_text(a,encoding='utf-8')

checks=[
 ('native bridge detector','function androidNative()' in a),
 ('native export','native.exportJson(json' in a),
 ('native import','native.importJson()' in a and 'FORGE_NATIVE_IMPORT' in a),
 ('browser fallback','URL.createObjectURL(blob)' in a),
 ('android back handler','window.FORGE_ANDROID_BACK=function()' in a),
 ('back to home','window.setView("home")' in a),
]
for name,ok in checks:
    if not ok: raise SystemExit(f'{name} missing')
print('v2.0.15 Android integration hardening PASS')
