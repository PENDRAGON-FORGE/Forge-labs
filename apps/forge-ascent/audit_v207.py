from pathlib import Path
import re

# Start from the fully audited v2.0.6 patch.
exec(Path('audit_v206.py').read_text(encoding='utf-8'))

p = Path('www/data-store.js')
s = p.read_text(encoding='utf-8')
old = '''function importPayload(payload){
    const source = payload && payload.product==="FORGE ASCENT" && payload.data ? payload.data : payload;
    return migrate(source);
  }'''
new = '''function importPayload(payload){
    if(!payload || typeof payload !== "object" || Array.isArray(payload)) throw new Error("Invalid backup payload");
    if(Object.prototype.hasOwnProperty.call(payload,"product")){
      if(payload.product !== "FORGE ASCENT" || !payload.data || typeof payload.data !== "object" || Array.isArray(payload.data)) throw new Error("Invalid FORGE ASCENT backup");
      return migrate(payload.data);
    }
    const legacyKeys=["profile","body","progression","reviews","sessionLogs","tests"];
    if(!legacyKeys.some(k=>Object.prototype.hasOwnProperty.call(payload,k))) throw new Error("Unrecognized legacy backup");
    return migrate(payload);
  }'''
if old not in s:
    raise SystemExit('importPayload anchor missing')
s = s.replace(old,new,1)
# Keep imported session duration bounded to a realistic app maximum.
s = s.replace('duration: number(s.duration,1,1440,1),','duration: number(s.duration,1,240,1),',1)
p.write_text(s,encoding='utf-8')

# Static guarantees for the backup path.
if 'Unrecognized legacy backup' not in s or 'Invalid FORGE ASCENT backup' not in s:
    raise SystemExit('strict backup validation missing')
if 'duration: number(s.duration,1,240,1)' not in s:
    raise SystemExit('session duration normalization cap missing')
print('v2.0.7 backup hardening PASS')
