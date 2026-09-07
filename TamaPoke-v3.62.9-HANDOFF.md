# TamaPoke KO v3.62.9 handoff

## Baseline
- Hardware: Waveshare ESP32-S3-Touch-AMOLED-1.75, 466x466 round AMOLED, microSD.
- Preserve existing `tools/catalog_lock.json` when updating the GitHub repository.
- Existing Canonical Forms, Alola/Galar/Hisui/Paldea regional evolution guards, Mega36, BasePackGuard, rolling `sprites-current` Full SD ZIP policy and v3.62.8 framed PUT4 proto=4 remain.
- Visible frame cadence remains active 85 ms / normal 100 ms.

## v3.62.9 runtime stability fixes

### Battle Tower launch
`render()` prioritizes `towerOpen` over `battleOpen`, while touch routing prioritizes the battle. `startTowerBattle()` previously called `startBattle()` successfully but left `towerOpen=true`, so the tower hub remained painted over an active battle. The fix closes `towerOpen` only after `battleOpen` confirms a successful start.

### Type-boss BGM lifecycle
Special boss/tower/rival battles return directly to their hub after result narration. That result-dismiss path now calls `audioMusic(MUS_NONE)` before opening the hub, resets battle menu/phase2 state, and `audioTask()` explicitly `gSyn.allOff()` when music transitions to NONE so the previous note envelope cannot leak into the hub.

### Training intermittent reset / UI jump
Two concrete hazards were found:
1. A move-learning offer could be queued by a level-up during training. Render still showed training, but touch/current-screen logic could prioritize the invisible learn modal. Training now has the same visual/input priority everywhere.
2. Training completion could cause several Preferences/NVS commits back-to-back: Pet save, MIS_PLAY, MIS_TRAIN and an IV reward. Pet minigame training methods now mark `pendingSave`; GameExtras supports batched dirty saves; result paths call `endBatch(false)` and queue persistence. After the minigame closes, the main loop flushes Pet and Extras on separate passes with a delay between them.

## Validation
- `tools/verify_runtime_stability.py` guards tower state, special-battle music cleanup, training input priority, deferred/batched persistence and 85/100 ms cadence.
- `tools/verify_sd_serial_protocol.py` continues to guard PUT4 proto=4.
- `tools/verify_evolution_levels.py` and release-storage guards remain.
- Python syntax, installer JavaScript and workflow YAML are checked locally.
- Live PMDCollab/PokeAPI generation and actual ESP32-S3 compile remain authoritative in GitHub Actions.

## Sprite note
v3.62.9 does not change the catalog or sprite IDs/assets. A successful v3.62.8 sprite set does not need to be downloaded again. If a previous Web Serial transfer was incomplete, rerun only the affected regional/full sync after updating firmware.
