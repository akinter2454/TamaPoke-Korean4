TamaPoke 한국어판 v3.62.0 PMDCatalog - Mega36 Level Evolutions + Evolution Guard

기준선
- v3.58 Alola PMDCollab 기준에서 확장
- v3.57.1~v3.57.5 저장 안정화/듀얼 속도 레벨 시스템 유지
- PMDCollab 행동 sprite가 충분한 메가진화 36종만 Lv.70 영구 진화로 허용; 그 외 거다이맥스/다이맥스/원시회귀/울트라버스트/왕관폼/테라스탈 및 비승인 메가폼 제외
- 사용자는 새 세이브로 시작할 예정이므로 과거 실험판 세이브 호환보다 구조 안정성을 우선

포켓몬/폼
- GitHub Actions 실행 시 PMDCollab/SpriteCollab 최신 tracker.json을 읽음
- 실제 행동 도트 스프라이트가 있는 공식 포켓몬/일반 폼을 자동 수집
- 지역폼/일반 폼체인지는 별도 species로 도감/파티/박스에 등록
- 1~809 및 알로라 폼 810~827 ID는 기준 ID로 유지
- 신규 National Dex 기본종은 natdex+18 규칙
- 추가 독립 폼은 1200+ catalog_lock.json으로 ID 고정
- 진화는 모두 레벨업 방식
- 분기진화는 찾기 대상 -> 미등록 진화형 -> 이후 랜덤의 Eevee-style generic branch selector
- 관동/성도/호연/신오/하나/칼로스/알로라/가라르/히스이/팔데아/ALL 지역 구조

스프라이트
- PMDCollab AnimData.xml + 행동 도트만 사용
- 정지 artwork/PokeAPI/Showdown 대체 그림을 행동 sprite로 사용하지 않음
- 일반: /mons/pNNN.bin, shiny: /mons/psNNN.bin
- 원래 지역팩 TPK2와 신규 catalog TPK3를 모두 읽음
- TPK3에는 frame별 실제 불투명 bounds가 저장되어 큰 sprite load/render 비용을 줄임
- Actions 생성 sprite는 2.8MiB 이하 size-safe 유지
- PMDCollab 행동별 투명 여백은 pack 단계에서 crop

v3.61.3 No-Frame-Drop 안정화
- 85ms active / 100ms normal visible cadence 유지

v3.61.4 절전 + 체육관
- 5분 무입력 시 true screen-off, 터치로는 깨어나지 않음
- 옆 AXP2101 물리 버튼만 화면 wake
- 화면 OFF 중 게임/이벤트 SFX 및 PA 자동 mute
- v3.61.5: 터치 직후 lastInteract가 loop의 old now보다 새로워 unsigned idle 언더플로우가 나던 문제 수정
- safeElapsedMs + 입력 직후 millis 재동기화로 터치는 ON 상태에서 절대 자동 screen-off를 유발하지 않음
- OFF 중 화면 render/flush 중단 (화면 ON FPS는 기존과 동일)
- 가라르(Sword) 8체육관 + Champion Cup/Leon
- 팔데아 8체육관 + Elite Four + Geeta
- 가라르/팔데아 전용 경량 픽셀 배지 표시
- 프레임 목표를 낮추지 않음: game/battle 85ms, 일반 animated UI 100ms start-to-start
- v3.61.2의 120~125ms heavy pacing 및 오버런 뒤 20~36ms recovery delay 제거
- PMD/배틀 도트 run을 Arduino_Canvas RGB565 framebuffer에 직접 기록
- 확대된 동일 행은 memcpy로 반복하여 PSRAM write overhead 절감
- 홈의 일반 animation frame은 화면 전체 대신 y=0..311만 panel로 전송
  full 434,312 bytes -> upper band 290,784 bytes, 약 33% 전송 감소
- y>=312 care panel은 값/상태가 바뀔 때만 다시 그리고 full present
- 10초 주기 강제 full refresh 제거
- 도감 상세도 첫 frame만 full, 이후 sprite band만 갱신
- crash breadcrumb/heap query는 화면 변경 또는 최대 1초 1회
- release build는 TAMAPOKE_FRAME_DIAG=0. Serial 진단 자체가 stutter를 만들지 않게 함

GitHub Pages
1. ZIP 내용물을 GitHub 저장소 루트에 업로드
2. Settings -> Pages -> Source = GitHub Actions
3. Actions -> "TamaPoke v3.62.0 PMDCatalog - Mega36 Level Evolutions GitHub Pages" -> Run workflow
4. build와 deploy가 모두 성공해야 최종 배포 완료
5. deploy에 표시되는 GitHub Pages 주소를 Chrome/Edge에서 열어 펌웨어/스프라이트 전송

Actions 최종 검증
- 최신 catalog 생성/기믹 제외 검사
- 810+ sprite가 TPK3이고 2.8MiB 이하인지 검사
- no-frame-drop scheduler/partial-present/fast blit guard 검사
- arduino-cli ESP32-S3 실제 컴파일
- GitHub Pages artifact/deploy

생성 보고서
- pmd_catalog_report.txt: 포함/제외/스프라이트 미존재 목록
- pmd_sprite_report.txt: 실제 PMD 패킹 결과
- pmd_catalog.json: ID/National Dex/폼/지역/활성 상태
- sprite-manifest.json: 지역별 분할 .pak 목록

중요
- 첫 성공 빌드 이후 생성된 tools/catalog_lock.json은 다른 저장소/ChatGPT 계정으로 이전할 때 반드시 함께 보존
- 실제 최종 검증은 GitHub Actions arduino-cli compile 성공 + Pages deploy 성공
- 프레임 문제가 특정 종에서만 발생하면 전체 FPS를 낮추지 말고 해당 dex의 PMD report와 sprite를 분석


v3.61.6 IV 성장 + 캐주얼 배틀
- IV 캡슐 4종 / 금빛왕관 추가 (기존 세이브 item ID 유지)
- 랜덤 이벤트 및 공격/방어/스피드 훈련에서 희귀 IV 보상
- 체육관 파티 선택 후 홈 복귀 버그 수정
- 공격/특공, 방어/특방 분화 없이 공격 vs 방어로 통합
- 도감 810+ 포켓몬의 타입/레벨별 대표 기술 fallback 개선


v3.61.7 메뉴 종료 잔상 수정
- 홈 화면의 0..311 부분 전송 최적화는 그대로 유지합니다.
- 메뉴/먹이창/확인창/알처럼 y=312 아래까지 덮는 프레임은 더 이상 깨끗한 홈 하단 캐시로 기록하지 않습니다.
- 해당 화면이 사라진 첫 홈 프레임만 전체 466x466을 전송해 AMOLED 잔상을 제거하고, 그 다음 프레임부터 다시 부분 전송으로 돌아갑니다.
- IV 아이템은 상점에 추가하지 않으며 랜덤 이벤트와 훈련 보상 전용이라는 v3.61.6 정책을 유지합니다.


v3.61.8 IV 보상 확률 소폭 상향
- 일반 성적 훈련 IV 드롭: 18% -> 22%
- 우수 성적 훈련 IV 드롭: 32% -> 38%
- 랜덤 이벤트 중 개체 훈련 키트: 12.5% -> 16%
- 개체 훈련 키트에서 금빛왕관: 6% -> 8%
- 상점 판매는 추가하지 않으며 랜덤 이벤트/훈련 보상 전용 정책 유지


v3.61.9 진화 레벨 오버플로우 수정
- 정적 도감 1~827 진화 레벨 전수 검사: 직접 진화 최대값 Lv.64, 데이터 자체는 정상
- 문제 원인: 구형 조기 은퇴 페널티 +144레벨이 현재 MAX_LEVEL=100과 충돌
- 조기 은퇴 페널티를 +12레벨로 정상화하고 기존 저장값 144도 자동 변환
- effectiveEvolutionLevel()이 기본 레벨 + 돌봄 실수 + 은퇴 페널티를 계산한 뒤 Lv.100에서 상한 처리
- 돌봄 실수는 MAX_LEVEL에서 포화되어 uint8_t 255->0 래핑 방지
- Actions에서 tools/verify_evolution_levels.py를 실행해 동적 Galar/Hisui/Paldea/폼 진화 데이터도 2~100 범위인지 검증
- IV 보상 22%/38%, 이벤트 16%, 금빛왕관 8%, 상점 미판매 정책은 v3.61.8 그대로 유지


v3.62.0 Mega36 레벨진화
- 2026-09-06 기준 PMDCollab에서 충분한 행동 sprite가 확인된 메가폼 36종만 화이트리스트 추가
- 각 메가폼은 원본 포켓몬에서 Lv.70 영구 진화, 도감 별도 등록, 알 획득 제외
- 리자몽 -> m.리자몽X만 / 뮤츠 -> m.뮤츠Y만 단일 진화
- Mega Charizard Y, Mega Mewtwo X 및 행동 sprite 미완성/비승인 메가폼은 포함하지 않음
- Mega Lucario Z 같은 이후 추가 X/Y/Z 변형도 자동 허용하지 않음
- 플라엣테 등 기존 분기와 Mega 분기의 요구 레벨을 target별로 따로 검사하여 Lv.70 이전 Mega 조기 진화를 방지
- 전체 대상은 MEGA36_SOURCE_MAP.txt 참조

[v3.62.1] 기존 v3.61.x microSD에서 Mega36만 추가할 때는 설치 페이지의 `메가진화 36종만 추가` 버튼을 사용하세요. 기존 추가 스프라이트 전체 재전송은 필요하지 않습니다.
