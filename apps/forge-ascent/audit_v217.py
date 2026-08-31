from pathlib import Path

# Build on v2.0.16 lifecycle and backup hardening.
exec(Path('audit_v216.py').read_text(encoding='utf-8'))

ap=Path('www/app.js')
a=ap.read_text(encoding='utf-8')

# v2.0.17 adds explicit backup integrity metadata and verifies it on import.
old='const json=JSON.stringify(STORE.exportPayload(state),null,2),native=androidNative();'
new='const payload=STORE.exportPayload(state);payload.integrity={product:"FORGE ASCENT",schema:2,exportedAt:new Date().toISOString(),sessionCount:Array.isArray(state.sessions)?state.sessions.length:0};const json=JSON.stringify(payload,null,2),native=androidNative();'
if old not in a: raise SystemExit('export integrity anchor missing')
a=a.replace(old,new,1)

old='function importBackupText(text){text=String(text||"");if(new Blob([text]).size>BACKUP_MAX_BYTES){$("dataMsg").textContent="Respaldo demasiado grande: máximo 5 MB.";return false}try{state=STORE.importPayload(JSON.parse(text));'
new='function importBackupText(text){text=String(text||"");if(new Blob([text]).size>BACKUP_MAX_BYTES){$("dataMsg").textContent="Respaldo demasiado grande: máximo 5 MB.";return false}try{const raw=JSON.parse(text);if(raw.integrity&&raw.integrity.product!=="FORGE ASCENT")throw new Error("backup product mismatch");state=STORE.importPayload(raw);'
if old not in a: raise SystemExit('import integrity anchor missing')
a=a.replace(old,new,1)

ap.write_text(a,encoding='utf-8')

checks=[
 ('integrity metadata','payload.integrity={product:"FORGE ASCENT",schema:2' in a),
 ('integrity product check','backup product mismatch' in a),
 ('5mb guard retained','BACKUP_MAX_BYTES=5*1024*1024' in a),
 ('flush retained','FORGE_FLUSH_STATE' in a),
 ('native import retained','native.importJson()' in a),
 ('native export retained','native.exportJson(json' in a),
]
for name,ok in checks:
    if not ok: raise SystemExit(f'{name} missing')
print('v2.0.17 backup integrity hardening PASS')
