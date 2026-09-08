TamaPoke 한국어판 v3.63.3 Compile Fix + Stability

1. ZIP을 풀어 GitHub 저장소 루트에 덮어씁니다.
2. 기존 tools/catalog_lock.json이 있다면 유지합니다.
3. GitHub Pages Source는 GitHub Actions를 사용합니다.
4. Actions에서 v3.63.3 workflow를 실행합니다.
5. build/deploy 성공을 확인합니다.
6. Pages 설치기에서 v3.63.3 펌웨어를 설치하고 기기를 재부팅합니다.

v3.63.3 핵심
- 샤이니열매 사용 시 private Pet::registerSpecies()를 직접 호출하던 컴파일 오류 수정
- Pet::makeCurrentShiny() 공개 API 추가: Shiny 전환 + Shiny 도감 등록을 Pet 내부에서 안전하게 처리
- Actions 컴파일 실패 시 실제 error 줄을 로그 마지막에 다시 출력하도록 진단 강화
- v3.63.1 훈련 보상(개체열매 1개 확정, 30% x2, 샤이니열매 3%) 유지
- 기존 반짝부적의 다음 알 Shiny 확률 증가 기능 유지
- GitHub Actions에 남아 있던 구형 훈련 보상 검사 제거
- 훈련 보상 회귀검사를 Actions의 두 검증 단계에서 모두 실행
- 훈련 결과 화면에서도 pet/extras 저장을 한 번에 하나씩 분산 저장하여 보상 유실 가능성 감소
- 일반 idle/sleep 저장이 훈련 분산 저장을 우회하지 못하도록 보호
- 반짝부적 적용 안내와 아이템 4번째 줄의 UI 겹침 수정
- v3.63.0 기술폭 확장 및 기존 런타임 안정화 유지
