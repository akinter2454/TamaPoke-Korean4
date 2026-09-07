# TamaPoke KO v3.62.8 handoff

## Baseline
- Hardware: Waveshare ESP32-S3-Touch-AMOLED-1.75, 466x466 round AMOLED, microSD.
- Preserve existing `tools/catalog_lock.json` when updating the GitHub repository.
- Existing Canonical Forms, Alola/Galar/Hisui/Paldea regional evolution guards, Mega36, BasePackGuard, Full SD ZIP and `sprites-current` single-Release storage policy remain.

## v3.62.8 change: Web Serial transport stabilization
The user-facing installation method is intentionally unchanged. The old proto=3 raw PUT stream could accept a partial `Serial.readBytes(buf, 2048)` result as a complete block, so CDC fragmentation could shift the stream and later appear as random `데이터 ACK 누락` at unrelated files/blocks.

Proto=4 uses `PUT4` plus framed `BLK4` messages. Each 2 KiB block carries sequence, exact length and CRC32. The firmware accumulates exact payload length, validates CRC, sends numbered ACK/NAK, and treats duplicate seq as ACK-loss recovery without rewriting SD data. The browser retries a block up to four sends and the file once.

The receiver waits for `END4` after all data, verifies whole-file CRC, and only then replaces the target. New data is written to `.part`; the old target is temporarily renamed to `.bak4` while the commit rename happens. `ABT4` releases an active failed session and `PUTSTAT` verifies the last completed size/CRC if `DONE4` alone was lost.

Legacy `PUT` remains in firmware for older installer compatibility, but the current installer requires `SDINFO proto=4` and uses only `PUT4`.

## Validation
- `tools/verify_sd_serial_protocol.py`: source guards + CRC known vector + fragmented-read model + duplicate ACK-loss/CRC retry model.
- Installer JavaScript must pass `node --check`.
- Workflow YAML and Python scripts must parse.
- Actual ESP32-S3 compile and live PMDCollab catalog generation remain authoritative in GitHub Actions.
