TamaPoke 한국어판 v3.62.5 PMDCatalog - Canonical Forms + Regional Evolution + Reliable SD Sync + Mega36

설치/업데이트
1. 이 ZIP의 내용을 기존 GitHub 저장소 루트에 덮어씁니다. 저장소를 비우지 마세요.
2. 기존 tools/catalog_lock.json이 있다면 반드시 보존합니다. v3.62.5 Actions가 그 파일에서 AltColor/Alternate/Cutscene/Beta 항목만 안전하게 퇴역 처리합니다.
3. Actions -> "TamaPoke v3.62.5 PMDCatalog - Canonical Forms + Regional Evolutions + Reliable SD Sync + Mega36 GitHub Pages" -> Run workflow.
4. Sync 단계에서 regional evolution audit와 canonical forms audit가 모두 OK여야 합니다.
5. build/deploy 성공 후 Pages 설치기에서 v3.62.5 펌웨어를 먼저 설치하고 기기를 재부팅합니다.
6. microSD -> 전체 스프라이트 -> 모든 스프라이트 한 번에 설치/동기화를 1회 실행하는 것을 권장합니다.

v3.62.5 핵심
- PMDCollab AltColor/Alt Colour, Alternate, Cutscene, Beta는 더 이상 독립 포켓몬/도감/진화형으로 만들지 않습니다.
- 과거 잘못 생성된 ID는 다른 포켓몬에 재사용하지 않고 퇴역합니다.
- 리자몽 Altcolor처럼 잘못 저장된 육성 개체는 정상 species ID로 자동 복구하며 레벨/IV/닉네임은 유지합니다.
- 지역 표시가 붙은 Alternate는 해당 정상 지역폼으로 복구합니다.
- 리자드 -> 정상 리자몽 -> Lv.70 m.리자몽X 경로를 보호합니다.
- v3.62.4의 알로라/가라르/히스이/팔데아 지역폼 진화 검증을 계속 유지합니다.
- SDINFO proto=3 + restricted DEL로 퇴역 스프라이트 파일을 전체/추가 동기화 시 자동 정리합니다.
- 전체 스프라이트 탭, 리소스 검수, catalog fingerprint, Mega36, IV 랜덤/훈련 보상, 진화 Lv.100 상한, 절전/체육관/메뉴 수정은 유지합니다.
