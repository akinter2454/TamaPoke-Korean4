# TamaPoke KO v3.61.6 — 새 ChatGPT 계정 인수인계 문서

## 0. 이 문서를 먼저 읽을 것

이 프로젝트는 Waveshare 원형 AMOLED용 TamaPoke 한국어판을 장기간 수정해 온 프로젝트다. 새 계정/새 대화에서는 **이 HANDOFF 문서와 v3.61.6 전체 GitHub ZIP을 함께 업로드한 뒤 작업을 시작**한다. 과거 v3.2x~v3.60 실험판으로 되돌리지 말고, 반드시 **v3.61.6 IV Growth + Casual Battle**를 최신 기준선으로 사용한다.

사용자는 기존 세이브를 지우고 새로 시작할 예정이므로 구버전 세이브 호환성은 최우선 제약이 아니다. 다만 이미 안정화된 species ID와 catalog lock을 불필요하게 재배치하지 않는다.

## 1. 현재 기준

- 프로젝트: **TamaPoke KO**
- 펌웨어: **v3.61.6**
- 계보: v3.58 Alola → v3.61 FULL PMDCollab catalog → v3.61.1 size-safe → v3.61.2 stability → v3.61.3 no-frame-drop → v3.61.4 power-save/modern gyms → v3.61.5 touch power fix → **v3.61.6 IV growth + casual battle**
- 배포: **GitHub Actions → GitHub Pages**
- Netlify는 사용하지 않는다.
- UI: 한국어 우선
- 사용자 응답: 존댓말

## 2. 하드웨어

- Waveshare ESP32-S3-Touch-AMOLED-1.75
- 466×466 원형 AMOLED
- CO5300 QSPI display
- CST9217 I2C touch
- ES8311 audio codec + onboard speaker
- 16MB flash / OPI PSRAM
- Arduino FQBN:

```text
esp32:esp32:esp32s3:CDCOnBoot=cdc,FlashSize=16M,PSRAM=opi,PartitionScheme=app3M_fat9M_16MB
```

Display는 `Arduino_Canvas` 466×466 RGB565 full framebuffer를 PSRAM에 두고, 검증된 QSPI **80MHz**를 유지한다. 더 높은 bus clock으로 FPS를 억지로 올려 안정성을 희생하지 않는다.

## 3. 포켓몬/폼 정책

PMDCollab에 실제 행동 도트 sprite가 있는 공식 포켓몬과 일반적인 공식 폼을 가능한 범위에서 전체 수록한다.

포함:
- 관동~팔데아 National Dex 포켓몬
- 알로라/가라르/히스이/팔데아 지역폼
- 로토무/테오키스 등 일반적인 공식 폼체인지
- 폼체인지는 별도 TamaPoke species

제외:
- Mega Evolution
- Gigantamax / Dynamax
- Primal
- Eternamax
- Ultra Burst / Ash-Bond
- Crowned
- Totem
- Terastal / Stellar 및 기타 일시적 전투 기믹

### ID 규칙

- 1..809: 기존 National Dex
- 810..827: 고정 알로라 폼 18종
- 이후 base species: 기본적으로 `natdex + 18`
- 추가 독립 폼: 1200 이상 `tools/catalog_lock.json`으로 고정
- 첫 성공 Actions 빌드 이후 생성된 **최신 `tools/catalog_lock.json`은 계정/저장소 이전 시 반드시 함께 보존**한다.
- 행동 sprite가 없는 항목은 `DEX_ENABLED`로 비활성화할 수 있다.

## 4. 진화 정책

- 돌/친밀도/시간대/교환/기술 등 특수 진화조건을 모두 **레벨업 진화**로 단순화한다.
- 실제 최소 레벨이 있으면 가능한 한 사용한다.
- 특수 조건만 있으면 대체 레벨을 부여한다.
- 여러 진화형으로 갈라지면 Eevee-style generic branch selector:
  1. 현재 hunt 대상 진화형 우선
  2. 아직 미등록인 진화형 우선
  3. 모두 등록된 후 랜덤

## 5. 지역/알 그룹

1. Kanto
2. Johto
3. Hoenn
4. Sinnoh
5. Unova
6. Kalos
7. Alola
8. Galar
9. Hisui
10. Paldea
11. ALL

알 그룹과 도감 지역 선택도 동일한 구조를 사용한다.

## 6. PMDCollab sprite 시스템

정책은 **실제 PMDCollab SpriteCollab 행동 도트 애니메이션만 사용**한다. 정지 artwork를 행동 sprite처럼 대체하지 않는다.

SD 경로:

```text
/mons/pNNN.bin
/mons/psNNN.bin
```

### TPK2 + TPK3

- 기존/원본 지역팩: **TPK2**를 계속 지원
- Actions가 생성하는 810+ catalog sprite: **TPK3**
- TPK3는 TPK2와 같은 indexed-pixel/action 구조에 각 frame의 `L,T,R,B` visible bounds를 추가한다.
- 따라서 큰 신규 sprite를 SD에서 load할 때 pixel blob 전체를 다시 scan하지 않는다.
- legacy TPK2는 load 시 exact frame bounds를 한 번 계산한다.
- `PmdAct.totalMs`도 load 시 캐시한다.
- 현재 renderer는 current frame의 exact bounds만 순회한다.

### size-safe

- 펌웨어 단일 PMD load hard limit: 3MiB
- Actions 생성 목표: **2.8MiB 이하**
- 큰 sprite는 프레임/부가 action을 단계적으로 compact하되 Idle/Walk 등 실제 움직임을 유지한다.
- pack 단계에서 action 전체 샘플의 투명 union을 crop한다.

## 7. v3.61.3 No-Frame-Drop 안정화 — 가장 중요

사용자가 명시적으로 **안정화를 위해 FPS를 낮추는 것을 원하지 않는다.** 따라서 이후 작업에서도 전체 FPS를 낮추는 방식은 기본 해결책으로 사용하지 않는다.

### 7.1 프레임 스케줄러

현재 목표:
- game / sack / speed / battle: **85ms start-to-start** (~11.8 fps)
- 일반 animated UI: **100ms start-to-start** (10 fps)

v3.61.2의:
- PMD-heavy 120ms
- 기타 125ms
- overrun 뒤 20~36ms recovery guard

를 제거했다.

한 프레임이 목표 시간을 넘겨도 추가 recovery delay를 넣지 않고, 완료 직후 다음 loop가 바로 eligible하다. 즉 스케줄러가 의도적으로 프레임을 더 떨어뜨리지 않는다.

### 7.2 release 진단 출력

```cpp
#define TAMAPOKE_FRAME_DIAG 0
```

이 기본값을 유지한다. USB CDC `Serial.printf` 자체가 순간적인 hitch를 만들 수 있으므로 일반 빌드에서는 frame stats를 완전히 비활성화한다. 실제 성능 분석이 필요할 때만 1로 바꾸고 `FRAME10S`, `RENDER slow`를 수집한다.

### 7.3 Canvas fast path

PMD indexed sprite의 horizontal color run을 `gfx->fillRect()` 수천 번 호출하지 않고:
- `Arduino_Canvas::getFramebuffer()`의 RGB565 buffer에 직접 기록
- 첫 확대 행을 쓴 뒤 동일한 세로 확대 행은 `memcpy`로 복사

한다.

같은 fast path를 battle backdrop, avatar/map pixel art에도 적용했다. 출력 픽셀과 animation timing은 바뀌지 않는다.

### 7.4 Home partial present

홈 화면에서 care panel은 `y>=312`, 움직이는 scene/Pokemon은 주로 `y<312`에 있다.

일반 animation frame:

```text
full:  466×466×2 = 434,312 bytes
upper: 466×312×2 = 290,784 bytes
```

따라서 변경 없는 care panel을 매 frame 다시 QSPI로 보내지 않고 **0..311 band만 panel에 present**한다. 전송량은 약 33% 감소하지만 animation frame target은 유지한다.

Full present 조건:
- home 첫 진입/재진입
- fullness/joy/energy/hygiene/poop/sleep/night/language/button-disabled 상태 변경
- menu/feed/confirm/choice/egg처럼 band 경계를 가로지르는 UI

중요: v3.61.2의 10초 주기 강제 full refresh는 삭제했다. 그것은 주기적인 긴 프레임을 만들 수 있었다.

또한 home scene의 terrain은 y=312 아래를 매 frame 다시 그리지 않는다. ceremony는 예외로 full scene을 유지한다.

### 7.5 Pokedex detail partial present

- 첫 detail frame: full present
- hunt 상태 변경: full present
- 이후 등록된 포켓몬 animation: sprite가 있는 상단 band만 present
- 미등록 silhouette은 정적이므로 첫 표시 후 불필요한 panel transfer 없음

### 7.6 Crash breadcrumb

과거 매 render마다 `ESP.getFreeHeap()`을 읽던 breadcrumb를:
- screen 변경 즉시
- 같은 screen에서는 최대 1초 1회

로 제한했다. crash screen 기능은 유지하면서 hot path 부하를 없앤다.

## 8. 프레임 안정화 원칙

향후 끊김을 발견하면 아래 순서로 원인을 찾는다.

1. 특정 PMD frame/canvas 크기 확인
2. `pmd_sprite_report.txt`의 crop/size profile 확인
3. SD load hitch인지 지속 render bottleneck인지 구분
4. partial present 가능한 정적 UI인지 확인
5. Canvas draw call 수/visible bounds 확인
6. 필요할 때만 `TAMAPOKE_FRAME_DIAG=1`
7. **전체 frame interval을 120~150ms로 낮추는 방식은 최후 수단으로도 사용자와 상의 없이 적용하지 않는다.**

## 9. 주요 파일 책임

- `TamaPoke.ino`: main loop, render scheduler, partial present, Canvas fast path, touch/UI, battle orchestration, PMD draw
- `pet.cpp/.h`: 육성/알/진화/도감/hunt/save scalar
- `sdmon.cpp/.h`: SD, TPK2/TPK3 PMD load/unload, thumbs, serial PUT
- `care_slots.cpp/.h`: 3마리 육성 슬롯
- `party.cpp/.h`: 파티/박스
- `save.cpp/.h`: 저장 백업/복원 guard
- `audio.cpp/.h`: 게임음/UI음
- `game_extras.cpp/.h`: 미션/아이템/탐험/보스/배틀타워/날씨/라이벌
- `dex.h`: Actions 동적 도감/진화/지역
- `ko_species.h`: Actions 동적 한국어 종명
- `tools/sync_pmd_catalog.py`: PMDCollab tracker + PokeAPI → catalog/dex
- `tools/pack_pmd_catalog.py`: PMD 행동 PNG/XML → cropped/size-safe **TPK3**
- `tools/build_sprite_paks.py`: Web Serial chunked `.pak`
- `tools/embed_tamapoke_firmware.py`: compiled bin → installer embed
- `.github/workflows/main.yml`: catalog sync → sprite pack → policy/stability verify → Arduino compile → GitHub Pages deploy

## 10. GitHub Pages 배포

최초 한 번:

`Settings → Pages → Build and deployment → Source = GitHub Actions`

그 뒤:

`Actions → TamaPoke v3.61.6 PMDCatalog - IV Growth + Casual Battle GitHub Pages → Run workflow`

정상 완료:

```text
build  ✅
deploy ✅
```

Code 탭에 `site/`가 남지 않아도 정상이다. Actions artifact로 Pages에 직접 배포한다.

## 11. Actions 외부 데이터

- PMDCollab SpriteCollab tracker/sprite 원본
- PokeAPI species/evolution 데이터

빌드 후 반드시 확인:
- `tools/pmd_catalog_report.txt`
- `tools/pmd_sprite_report.txt`

## 12. 실제 기기 검증 우선순위

1. 큰 PMD 포켓몬 홈 화면 10분
2. bath/eat/weather/CTA가 있는 홈에서 lower-panel 경계 이상 여부
3. 도감 상세 20종 연속 전환
4. 배틀 10회, PMD 2마리 동시 표시
5. 공격/방어/스피드 훈련 각 10분
6. 30~60분 soak
7. 특정 종에서만 문제가 있으면 그 dex부터 분석

성능 계측이 필요하면 `TAMAPOKE_FRAME_DIAG=1`로 임시 빌드하고 `FRAME10S`의 `over`를 본다. 특정 포켓몬에서만 over가 높다면 전체 FPS를 낮추지 말고 그 sprite를 최적화한다.

## 13. 개발 원칙

- 실제 PMD sprite가 없는 항목을 정지 일러스트로 속여 넣지 않는다.
- 메가/거다이맥스 등 사용자가 제외한 기믹을 다시 넣지 않는다.
- UI draw rect와 touch hit rect를 함께 확인한다.
- game loop에 잦은 NVS write를 추가하지 않는다.
- SD/PSRAM 큰 blob은 화면 전환 시 적절히 unload한다.
- display QSPI 80MHz 유지.
- 최종 컴파일은 GitHub Actions arduino-cli `Success` 기준.
- Pages deploy까지 성공해야 배포 완료.
- **안정화를 명분으로 FPS를 임의로 낮추지 않는다.**

## 14. v3.61.4 추가 변경 — 절전 / 가라르·팔데아 체육관

### 화면 절전
- 5분 무입력 시 `screenOff=true`로 전환하고 AMOLED brightness=0뿐 아니라 render/flush를 중단한다.
- 화면 OFF 중 touch IRQ는 latch 해제를 위해 읽기만 하며 `screenOff`를 해제하거나 UI를 실행하지 않는다.
- 깨우기는 AXP2101 물리 side button short-press만 허용한다.
- 화면 OFF 중 `audioSetScreenAwake(false)`가 queue를 비우고 PA를 끄며 SFX를 차단한다. 사용자 `snd/btnsnd` 설정은 바꾸지 않는다.
- 화면 ON FPS는 v3.61.3과 동일하게 active 85ms / normal 100ms이다. 절전을 위해 visible FPS를 낮추지 않는다.

### Gym ladder
- `GYM_REGIONS=9`: Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar, Paldea.
- Hisui는 본가 설정상 전통 Gym/Badge 리그가 없으므로 gym ladder에서는 건너뛴다. `TrainerSet.regionId`가 Galar=7, Paldea=9를 dex region에 매핑한다.
- Galar는 Sword 버전의 8 gym leader를 사용하고 Dynamax/Gigantamax는 무시한다. 후반 5칸은 Champion Cup/endgame을 TamaPoke의 공통 13-trainer 구조에 맞춘다.
- Paldea는 8 gym + 실제 Elite Four 4명 + Geeta를 그대로 13칸에 배치하고 Terastallization은 무시한다.
- Galar/Paldea badge는 외부 ripped art 대신 type-coloured original device pixel emblems로 win screen/player card에 표시한다.
- PMDCollab에 어떤 modern roster sprite가 일시적으로 없으면 `trainerDexWithArt()`가 같은 type의 classic animated sprite로 fallback한다.

### Save
사용자는 기존 세이브 데이터를 삭제할 예정이므로 `GYM_REGIONS` 확장에 따른 과거 badge blob 호환은 blocking requirement가 아니다. 새 세이브에서 9-region badge arrays가 정상 기준이다.


## 15. v3.61.6 기준 SHA-256

```text
48a1a2a55537a2ab844a6b89650fba2a72dc4679f1ccbe0898974d01b8ad517d  TamaPoke.ino
6aff327b64e10370b912a6dacbb1fdb1c5814646558103521f00553aba2fa14c  trainers.h
6f24d4ae417479efc667462550abd3ff78396181bb96706c2591cd2f7c17dff8  audio.cpp
ccede9c3e35ebdc81a82e608ae85861834a3d91063a82e18ccd49d7106b48771  audio.h
18b9eed9fac9a61e836d768498176d78960f3b935b90c809b7fbe571851b03b9  .github/workflows/main.yml
1d577979a9a35ed39cdfd5e080527b7d395d1f562dbdf057b5159124fe4630a2  battle.cpp
d5c1995c27129ce4f0ea7c6fee1c1510412c2e3e41331fa9006360b145783b18  game_extras.cpp
c3cb749792bbe69017c1513d357e517f0f2536d0c93b0e22298c85c646b6e6de  game_extras.h
dd10fb2976bf1f03543e740d7b1ec18221064467e4a96c8778534d13f98ffb66  moves.h
790e488f5fd428e5555bba5fea1d8c477dab24a11c009d41a233c4654cd5fff7  pet.h
4fddb23f825e42febbb240eb587d3ba154615835c912067ea584e7840228e0d7  personality.h
9a7c4998c212d858a4ff386fa6025a003a2c7aba17d538122ef0d8eb0be24919  tools/sync_pmd_catalog.py
3fd45efc3b11ae7cc9fc9db88295f22cb9c4346a8687da66dea2f5d73fd7cf06  tools/pack_pmd_catalog.py
```

## 16. v3.61.5 긴급 수정 — 터치 직후 화면 OFF 방지 (v3.61.6에서 유지)

- v3.61.4에서 `loop()` 시작 시점의 `now`보다 `handleTouch()`가 기록한 `lastInteract`가 수 ms 미래가 될 수 있었다.
- `uint32_t idle = now - lastInteract`가 unsigned 언더플로우하여 약 49일의 무입력처럼 보였고, 터치 직후 5분 자동 screen-off 조건이 발동했다.
- v3.61.5에서 `safeElapsedMs()`를 사용해 미래 입력 timestamp를 0ms idle로 처리하고, 입력 처리 직후 `now = millis()`로 재동기화했으며 v3.61.6에서도 그대로 유지한다.
- `screenOff` 상태 변경은 `setScreenOffState()` 하나로 집중시켰다. 터치는 화면이 꺼져 있을 때 wake도 off도 하지 않으며, AXP2101 물리 버튼만 wake한다.
- 화면 OFF 중 `audioSetScreenAwake(false)`가 유지되어 이벤트 SFX 큐와 PA는 계속 차단된다.
- GitHub Actions에 미래 timestamp, 정상 elapsed, `millis()` wrap-around 회귀 검사를 추가했다.
- 프레임 목표는 v3.61.3 이후와 동일한 85ms/100ms이며 이번 수정은 FPS를 낮추지 않는다.


## 17. v3.61.6 — IV 성장 / 캐주얼 전투 / 체육관 시작 수정

- 기존 `ivAtk/ivDef/ivSpe/ivHp`(0~31)에 직접 성장 경로를 추가했다.
- 기존 아이템 ID 0~5는 그대로 두고 뒤에 `XITEM_IV_ATK/DEF/SPE/HP`, `XITEM_GOLD_CROWN`을 추가하여 예전 `xitem` NVS prefix와 호환한다.
- 개체캡슐은 해당 IV +1, 금빛왕관은 31 미만인 네 IV를 각각 +1 한다. 이미 효과가 없으면 소비하지 않는다.
- 랜덤 이벤트 8번 `개체 훈련 키트!`에서 IV 캡슐을 지급하며 낮은 확률로 금빛왕관이 나온다.
- 방어/공격/스피드 훈련에서 성적 조건을 넘으면 IV 캡슐이 희귀 드롭된다. HP 캡슐은 성공 드롭의 일부에서 보조 보상으로 등장한다.
- 체육관 파티 선택 후 홈으로 빠지던 문제를 수정했다. 라이브 펫이 알이어도 선택한 보관 파티가 있으면 체육관 배틀을 시작할 수 있고, 스쿼드 구성 실패 시 파티 선택 화면을 유지한다.
- 캐주얼 전투 규칙으로 공격/특공 및 방어/특방 분화를 제거했다. 데이터 구조는 호환을 위해 남기지만 모든 공격 기술은 공격 vs 방어를 사용하며 특공/특방 랭크 기술도 공격/방어 랭크로 합쳐진다. 특성 시스템은 추가하지 않는다.
- National Dex 810+의 fallback 기술배치를 약한 기술 고정 방식에서 레벨/타입별 대표 기술로 강화했다.
- v3.61.5의 5분 true screen-off, 물리 버튼 wake, safeElapsedMs 보호, FPS 정책은 그대로 유지한다.
