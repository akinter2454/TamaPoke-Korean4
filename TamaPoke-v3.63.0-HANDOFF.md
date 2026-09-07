# TamaPoke KO v3.63.0 handoff

## Baseline
- Current firmware baseline: **v3.63.0 Learnset Expansion + Stability Guard** (built on v3.62.9 Runtime Stability).
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


## v3.63.0 learnset expansion + stability guard

### Natural level-up move coverage
- The frozen 1..809 learnset contains many legal TM entries but numerous species have only 3-4 natural level-up entries. v3.63.0 leaves all original entries and move IDs intact, then adds a small supplemental layer.
- Legacy species with fewer than 7 natural moves can promote a few moves from their **existing legal/TM pool** into level-gated natural learning. Species already at 7+ natural moves are unchanged.
- Extremely tiny intentional pools (`total <= 2`, e.g. transform/cocoon/Magikarp-like cases) are not generalized.
- Audit result on the frozen 1..809 table: species with <=4 natural moves drop from **295 to 28**, while **754** species reach at least 7 natural moves.

### National Dex 810+
- The previous post-809 fallback only returned a current-level type kit and did not participate in `checkLearnGates()`, so modern species did not truly learn new moves on level-up.
- v3.63.0 exposes up to 9 staged natural entries (early basic/STAB -> mid STAB -> later strong STAB/generic coverage), so the normal learn queue, move picker and relearn paths all see the same pool.

### Stability guards
- `learnQueue` grows from 8 to 12 RAM-only entries so large level jumps are less likely to drop queued learn offers.
- `pendingLearnables()` no longer assumes every later entry is sorted behind future gates and excludes TM level-0 entries from natural pending results.
- Move-row, battle SFX/grid and TM replacement rendering now validate `moveId < MOVE_COUNT` before indexing `MOVE_TBL`.
- v3.62.9 Battle Tower, boss BGM and staggered training NVS persistence fixes remain unchanged.

### Validation
- `tools/verify_learnset_expansion.py` audits sparse learnset reduction, tiny-pool preservation, post-809 support markers, queue size and move-ID guards.
- `tools/verify_runtime_stability.py` still guards Battle Tower/BGM/training persistence and 85/100 ms cadence.
- `moves.h` is syntax-checked as C++17 in local validation; GitHub Actions remains authoritative for the ESP32 build and live catalog generation.

### Sprite/download note
v3.63.0 changes no sprite IDs or sprite assets. A complete v3.62.8/v3.62.9 SD sprite set does not need to be transferred again.

### GitHub Actions installer marker fix
- The v3.63.0 installer template already used the new `3.63.0-ko-learnset-expansion-stability-...` marker, but the embed step still grepped the old v3.62.9 marker after successfully writing `index.html`. That stale grep returned exit code 1 and aborted the workflow.
- The workflow now reads `FW_VERSION` directly from `TamaPoke-KO-OneClick-Installer.html` and verifies that exact marker in the generated `index.html`; the check is no longer hard-coded to a release string.
- Remaining operational v3.62.9 labels in the compile/build-info/commit/Pages summary paths were updated or made version-neutral/dynamic.
