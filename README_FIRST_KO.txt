TamaPoke 한국어판 v3.63.5 Workflow Guard + Training Reward Boost + Stability

1. ZIP을 풀어 GitHub 저장소 루트에 덮어씁니다.
2. 기존 tools/catalog_lock.json이 있다면 유지합니다.
3. GitHub Pages Source는 GitHub Actions를 사용합니다.
4. Actions에서 `TamaPoke PMDCatalog` workflow를 실행합니다.
5. build/deploy 성공을 확인합니다.
6. Pages 설치기에서 v3.63.5 펌웨어를 설치하고 기기를 재부팅합니다.

현재 버전 핵심
- 정상 훈련 완료 시 해당 개체열매 5개 확정 지급
- 30% 확률로 개체열매 보상이 총 9개로 증가
- 훈련 완료 시 별도 30% 확률로 샤이니열매 1개 지급
- 샤이니열매는 현재 포켓몬을 Shiny로 변경
- 기존 반짝부적의 다음 알 Shiny 확률 증가 기능 유지
- 훈련 결과 저장은 기존 분산 저장 구조 유지
- 샤이니 전환은 Pet::makeCurrentShiny() 공개 API를 통해 안전하게 처리
- 기술폭 확장, 배틀/오디오/화면/SD 런타임 안정화 유지
- 과거 업데이트 노트와 SHA-256 파일은 배포 ZIP에 포함하지 않음
