#!/usr/bin/env python3
from pathlib import Path
import re, sys

root=Path(__file__).resolve().parents[1]
ino=(root/'TamaPoke.ino').read_text(encoding='utf-8')
audio=(root/'audio.cpp').read_text(encoding='utf-8')
pet=(root/'pet.cpp').read_text(encoding='utf-8')
geh=(root/'game_extras.h').read_text(encoding='utf-8')
gec=(root/'game_extras.cpp').read_text(encoding='utf-8')
errs=[]

def need(cond,msg):
    if not cond: errs.append(msg)


# Version/installer marker for this runtime stabilization release.
m=re.search(r'^#define\s+FW_VERSION\s+"([^"]+)"', ino, re.M)
need(bool(m) and m.group(1)=='3.63.3','version: FW_VERSION is not 3.63.3')
installer=(root/'TamaPoke-KO-OneClick-Installer.html').read_text(encoding='utf-8')
need('3.63.3-ko-training-reward-persistence-stability-learnset-expansion-framed-put4-single-release-fullsd-canonical-forms-regional-evolution-mega36' in installer,
     'version: installer marker is not v3.63.3 learnset/stability')

def body(src, name):
    pat=re.compile(r'^[^;{}\n]*\b(?:[A-Za-z_]\w*::)?'+re.escape(name)+r'\s*\([^;{}\n]*\)\s*\{', re.M)
    m=pat.search(src)
    if not m: return ''
    brace=src.find('{',m.start())
    i=brace+1; depth=1
    while i<len(src) and depth:
        if src[i]=='{': depth+=1
        elif src[i]=='}': depth-=1
        i+=1
    return src[m.start():i]

# Battle Tower: the hub must close after startBattle succeeds, because render()
# intentionally gives hub overlays priority over battleOpen.
tower=body(ino,'startTowerBattle')
need('startBattle(dex, (uint8_t)lvl);' in tower,'tower: startBattle call missing')
need('if (!battleOpen) return;' in tower,'tower: successful start guard missing')
need('towerOpen = false;' in tower,'tower: hub not closed after successful battle start')
need(tower.find('towerOpen = false;') > tower.find('if (!battleOpen) return;'),
     'tower: hub must stay open when battle start fails')

# Special battle result: dismissing narration must stop music before returning
# to boss/tower/rival hub.
btap=body(ino,'battleTap')
needle='if (btlOver) {'
pos=btap.find(needle)
need(pos>=0,'battle: btlOver dismissal branch missing')
if pos>=0:
    frag=btap[pos:pos+1100]
    need('audioMusic(MUS_NONE);' in frag,'battle: BGM not stopped on special-result exit')
    need('if (btlBoss)' in frag and 'bossOpen = true;' in frag,'boss: result does not return to boss hub')
    need('if (btlTower)' in frag and 'towerOpen = true;' in frag,'tower: result does not return to tower hub')
need('if (playing != MUS_NONE) gSyn.allOff();' in audio,
     'audio: NONE transition does not silence existing synth envelope')

# Training: rendered/touch screen order must agree so a level-up learn offer
# cannot steal an invisible tap.
ui=body(ino,'uiCurrentScreen')
on=body(ino,'onTap')
need(ui.find('if (gameOpen || sackOpen || spdOpen)') < ui.find('if (pet.hasLearnOffer())'),
     'training: uiCurrentScreen gives learn offer priority over active minigame')
need(ui.find('if (trainOpen)') < ui.find('if (pet.hasLearnOffer())'),
     'training: uiCurrentScreen gives learn offer priority over training menu')
need(on.find('if (trainOpen)') < on.find('if (pet.hasLearnOffer())'),
     'training: touch router gives invisible learn offer priority over training menu')

# Training persistence: pet state must queue, not synchronously commit, and
# GameExtras must consolidate mission/reward writes.
for fn in ('playResult','trainSpeed','trainStrength'):
    b=body(pet,fn)
    need('pendingSave = true;' in b,f'training: {fn} does not defer pet save')
    # rewardTraining remains intentionally synchronous for gym battle rewards.
    need('save();' not in b,f'training: {fn} still performs synchronous pet save')
need('void beginBatch();' in geh and 'void endBatch(bool flushNow = true);' in geh,
     'training: GameExtras batch API missing')
need('if (_saveBatchDepth)' in gec and '_saveDirty = true;' in gec,
     'training: GameExtras save batching missing')
need(ino.count('extras.endBatch(false);') >= 5,
     'training: not all minigame result/early-exit paths defer extras save')
need('trainingPersistPhase' in ino and 'extras.flushPendingSave();' in ino,
     'training: staggered post-minigame persistence missing')
need('if (!trainingPersistPhase && pet.savePending()' in ino and
     'if (!trainingPersistPhase && extras.savePending()' in ino,
     'training: generic idle saver can bypass staggered persistence')
need('bool trainingPersistSafe = (!gameOpen && !sackOpen && !spdOpen)' in ino and
     '(gameOpen && gameOverUntil)' in ino and '(sackOpen && sackOverUntil)' in ino and
     '(spdOpen && spdOverUntil)' in ino,
     'training: static result screens are not eligible for early durable persistence')

# Preserve frame cadence; stabilization must not lower FPS.
need('targetFrameMs = activeAnimated ? 85UL : 100UL' in ino,
     'performance: active/normal frame cadence changed')

if errs:
    print('runtime stability audit FAILED')
    for e in errs: print(' -',e)
    sys.exit(1)
print('runtime stability audit OK')
print(' - Battle Tower hub closes only after successful start')
print(' - boss/tower/rival result exit stops BGM')
print(' - training screen/touch priority consistent')
print(' - training NVS writes are batched/deferred and staggered')
print(' - frame cadence remains 85/100 ms')
