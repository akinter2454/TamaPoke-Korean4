TamaPoke KO v3.62.0 계정 이전 패키지

새 ChatGPT 대화/계정에서 아래 순서로 사용하세요.
1. TamaPoke-KO-v3.62.0-Mega36-LevelEvolution-GitHubPages.zip 업로드
2. TamaPoke-v3.62.0-HANDOFF.md 업로드
3. START_HERE_NEW_ACCOUNT.txt 내용을 첫 메시지로 붙여넣기
4. 실제 GitHub Actions가 생성/갱신한 tools/catalog_lock.json이 있다면 최신 저장소의 것을 우선 유지

v3.62.0 핵심:
- 진화 요구 레벨 계산을 Lv.100에서 강제 상한 처리하여 160/208 같은 비정상 값 제거
- 구형 조기 은퇴 페널티 144레벨 -> 12레벨, 기존 저장값도 자동 마이그레이션
- 돌봄 실수 카운터가 255->0으로 되감기는 uint8 오버플로우 방지
- GitHub Actions에서 생성 도감 전체 진화 레벨 자동 검사 추가
- 개체캡슐 4종 + 금빛왕관 (IV +1, 31 상한에서 미소비)
- 랜덤 이벤트 '개체 훈련 키트!' 및 훈련 성적 기반 희귀 IV 보상
- 체육관 파티 선택 후 홈으로 빠지는 배틀 시작 버그 수정
- 공격/특공, 방어/특방 분화 제거: 모든 공격 기술은 공격 vs 방어
- 특성 시스템은 추가하지 않음
- NatDex 810+ 타입/레벨별 대표 기술 fallback 개선
- v3.61.5 절전/물리 버튼 wake/touch timestamp/no-frame-drop 보호 유지
- 메뉴 종료 시 y>=312 AMOLED 하단 잔상 제거: 종료 첫 프레임만 clean full present
- 이후 홈 화면은 기존 partial present로 즉시 복귀하여 FPS 정책 유지
- IV 아이템은 상점 판매 없음: 랜덤 이벤트/훈련 보상 전용

- 훈련 IV 드롭 확률을 22%/38%로 소폭 상향
- 랜덤 이벤트의 개체 훈련 키트 등장률을 16%로 상향
- 금빛왕관은 해당 이벤트 내 8%로 여전히 희귀

- 승인된 PMDCollab 행동 sprite 메가폼 36종을 Lv.70 영구 진화 + 별도 도감 species로 추가
- 리자몽은 m.리자몽X, 뮤츠는 m.뮤츠Y만 단일 진화
- 분기별 진화 레벨 필터로 Mega Lv.70 조기 선택 방지
- 비승인 Mega/G-Max/Dynamax/Primal/Terastal은 계속 제외
