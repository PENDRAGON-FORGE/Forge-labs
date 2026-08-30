from pathlib import Path

# Build on v2.0.15 Android integration hardening.
exec(Path('audit_v215.py').read_text(encoding='utf-8'))

def once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'Patch anchor missing: {label}')
    return text.replace(old,new,1)

ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')

# 1) Bound backup imports in both browser and native bridge paths.
a=once(a,
'function importBackupText(text){try{state=STORE.importPayload(JSON.parse(text));view=legacy();save();$("dataMsg").textContent="Respaldo importado, migrado y validado.";fillProfile();fillForms();refresh();return true}catch{$("dataMsg").textContent="Archivo inválido: no se importó ningún dato.";return false}}',
'const BACKUP_MAX_BYTES=5*1024*1024;\nfunction importBackupText(text){text=String(text||"");if(new Blob([text]).size>BACKUP_MAX_BYTES){$("dataMsg").textContent="Respaldo demasiado grande: máximo 5 MB.";return false}try{state=STORE.importPayload(JSON.parse(text));view=legacy();save();$("dataMsg").textContent="Respaldo importado, migrado y validado.";fillProfile();fillForms();refresh();return true}catch{$("dataMsg").textContent="Archivo inválido: no se importó ningún dato.";return false}}',
'bounded import text')
a=once(a,
' const f=e.target.files[0];if(!f)return;const reader=new FileReader();',
' const f=e.target.files[0];if(!f)return;if(f.size>BACKUP_MAX_BYTES){$("dataMsg").textContent="Respaldo demasiado grande: máximo 5 MB.";e.target.value="";return}const reader=new FileReader();',
'browser file size guard')

# 2) Flush canonical state whenever Android/browser backgrounds or unloads the WebView.
a += '''\n\nwindow.FORGE_FLUSH_STATE=function(){try{save();return true}catch(e){console.error("FORGE ASCENT flush failed",e);return false}};\ndocument.addEventListener("visibilitychange",()=>{if(document.visibilityState==="hidden")window.FORGE_FLUSH_STATE()});\nwindow.addEventListener("pagehide",()=>window.FORGE_FLUSH_STATE());\nwindow.addEventListener("beforeunload",()=>window.FORGE_FLUSH_STATE());\n'''
ap.write_text(a,encoding='utf-8')

checks=[
 ('5mb guard','BACKUP_MAX_BYTES=5*1024*1024' in a),
 ('browser size guard','f.size>BACKUP_MAX_BYTES' in a),
 ('flush helper','window.FORGE_FLUSH_STATE=function()' in a),
 ('visibility flush','visibilitychange' in a and 'visibilityState==="hidden"' in a),
 ('pagehide flush','pagehide' in a),
 ('beforeunload flush','beforeunload' in a),
]
for name,ok in checks:
    if not ok: raise SystemExit(f'{name} missing')
print('v2.0.16 lifecycle/backup safety hardening PASS')
