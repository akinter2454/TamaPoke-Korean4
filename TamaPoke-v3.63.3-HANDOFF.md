# TamaPoke KO v3.63.3 — current handoff

Current baseline: **v3.63.3 Shiny Berry Compile Fix + Stability Diagnostics**, built on v3.63.2 runtime/persistence stability, v3.63.1 training rewards and v3.63.0 learnset expansion.

## Current behavior
- Successful training: one matching IV berry guaranteed; 30% chance to receive two.
- Training: separate 3% chance for a Shiny Berry that changes the current Pokemon to Shiny.
- Existing Shiny Charm remains the next-egg Shiny probability booster and is unchanged.
- Training persistence remains staggered so gameplay does not burst-write multiple NVS domains.
- Expanded level-up learnsets and existing runtime/battle/audio stability changes remain enabled.

## v3.63.3 compile fix
- `GameExtras::useItem()` no longer calls private `Pet::registerSpecies()`.
- Added public `Pet::makeCurrentShiny()`; Pet itself sets the Shiny flag and records the Shiny Pokedex entry.
- Training reward regression now fails if external code directly calls the private Pokedex helper again.
- GitHub Actions compile step captures `compile.log` and reprints real compiler errors at the bottom on failure. SensorLib `TouchDrvCSTXXX.hpp is deprecated` is only a warning and is not treated as the build failure.

## Release hygiene
- Do not include historical UPDATE/FINAL_VALIDATION/PROJECT_STATE change-log files in release ZIPs.
- Do not create or include SHA-256 checksum files for the user-facing TamaPoke release packages.

Use v3.63.3 as the latest baseline.
