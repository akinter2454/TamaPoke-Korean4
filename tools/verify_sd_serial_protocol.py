from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
ino = (root / 'TamaPoke.ino').read_text(encoding='utf-8')
sd = (root / 'sdmon.cpp').read_text(encoding='utf-8')
html = (root / 'TamaPoke-KO-OneClick-Installer.html').read_text(encoding='utf-8')

m = re.search(r'^#define\s+FW_VERSION\s+"([^"]+)"', ino, re.M)
assert m and m.group(1) == '3.62.4', m.group(1) if m else 'missing'

# Normal gameplay must remain non-blocking, but explicit PUT must temporarily
# make USB TX reliable so OK/#/DONE flow-control cannot be silently discarded.
assert 'Serial.setTxTimeoutMs(0);' in ino
assert 'if (line == "SDINFO")' in sd
assert 'SDINFO OK proto=2' in sd
assert sd.count('Serial.setTxTimeoutMs(1000);') >= 2
assert sd.count('Serial.flush();') >= 5
assert 'size_t wr = f.write(buf, n);' in sd
assert 'if (wr != n)' in sd
assert 'Serial.setTxTimeoutMs(0);' in sd
assert 'Serial.setTimeout(8000);' in sd

# Browser must verify firmware/SD before enabling transfer and use long, staged
# ACK waits with a single pending WebSerial read.
assert "await writer.write(enc.encode('SDINFO\\n'));" in html
assert 'async function preflightSd()' in html
assert 'pendingRead = reader.read()' in html
assert "waitFor('OK', 15000)" in html
assert "waitFor('#', 15000)" in html
assert "waitFor('DONE', 30000)" in html
assert '데이터 ACK 누락' in html
assert 'SD 준비 완료' in html
assert '3.62.4-ko-regional-evolution-reliable-fullsync-mega36' in html

print('SD/WebSerial protocol regression OK: fw=3.62.4 proto=2 reliable ACK + preflight')
