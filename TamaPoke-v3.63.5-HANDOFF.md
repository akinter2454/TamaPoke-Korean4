# TamaPoke KO v3.63.5 — current handoff

Current baseline: **v3.63.5 Workflow Guard + Training Reward Boost + Stability**, built on the existing training persistence, Shiny conversion compile fix, learnset expansion, and runtime stability work.

## Current behavior
- Properly completed training always grants **5 matching IV berries**.
- The existing bonus roll remains **30%**; when it succeeds the IV-berry reward is **9 total**, not 5+9.
- A separate **30%** roll grants one Shiny Berry.
- The Shiny Berry changes the current Pokemon to Shiny through `Pet::makeCurrentShiny()` and records the Shiny Pokedex entry internally.
- The existing Shiny Charm remains unchanged and only boosts the next egg's Shiny probability.
- The 10% HP-IV-berry redirect remains so HP IV berries are obtainable without a dedicated HP minigame.
- Training persistence remains staggered so reward/save writes do not burst during active gameplay.
- Expanded level-up learnsets and existing battle/audio/display/SD runtime stability protections remain enabled.
- GitHub Actions no longer hard-codes training reward probability/quantity literals; `verify_training_rewards.py` is the single authority for those checks.
- Version/installer regression checks derive the firmware SemVer dynamically so a normal version bump does not fail on an obsolete verifier string.

## Release hygiene
- Do not include historical UPDATE/FINAL_VALIDATION/PROJECT_STATE change-log files in release ZIPs.
- Do not create or include SHA-256 checksum files in user-facing release packages.

Use v3.63.5 as the latest baseline.
