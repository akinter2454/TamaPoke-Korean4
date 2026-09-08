# TamaPoke KO v3.63.2 — current handoff

Current baseline: **v3.63.2 Training Reward Persistence + Pipeline Stability**, built on v3.63.1 training rewards and v3.63.0 learnset/runtime stabilization.

## Required baseline
- Waveshare ESP32-S3-Touch-AMOLED-1.75, 466×466 round AMOLED
- GitHub Actions → GitHub Pages
- Preserve the repository's existing `tools/catalog_lock.json` when overwriting the source tree.
- Do not lower the established visible frame cadence (active 85 ms / normal 100 ms) just to hide a hitch.

## Current reward policy
- Properly completed training always awards 1 IV berry.
- 30% chance: 2 of that IV berry instead of 1.
- 3% chance: one Shiny Berry, which changes the current living Pokemon to Shiny.
- The existing Shiny Charm remains separate and only boosts the next egg's Shiny chance.

## v3.63.2 stability hardening
- Removed the stale GitHub Actions grep that still expected the old probabilistic IV-drop formula.
- `verify_training_rewards.py` now runs in both major workflow verification stages.
- Training pet/extras saves remain staggered one NVS domain per loop pass.
- Static training result screens are now safe persistence points, so rewards become durable before the result is dismissed.
- Generic idle/sleep flushing cannot bypass the staggered training-save path.
- Shiny Berry inventory migration, save-backup inclusion, and normal-sprite fallback are regression checked.
- The active Shiny Charm label no longer overlaps the fourth utility-item row.

## Packaging policy
- Do not include old update-note/changelog/history files.
- Do not generate or include SHA-256/checksum files.
