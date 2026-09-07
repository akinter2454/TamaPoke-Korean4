TamaPoke 한국어판 v3.62.7 SingleRelease FullSD + BasePackGuard + Canonical Forms + Regional Evolution + Reliable SD Sync + Mega36

설치/업데이트
1. 이 ZIP의 파일을 기존 GitHub 저장소 루트에 덮어씁니다. 저장소를 비우지 마세요.
2. 기존 tools/catalog_lock.json이 있다면 반드시 보존합니다.
3. Actions -> v3.62.7 workflow -> Run workflow.
4. build/deploy 성공 후 Pages 설치기를 사용합니다.

v3.62.7 핵심
- PC용 전체 sprite ZIP은 `sprites-current` GitHub Release 한 곳에만 유지됩니다.
- asset 이름은 `TamaPoke-SD-Sprites-Current-Full.zip`으로 고정되고 새 build가 같은 파일을 교체합니다.
- 전체 sprite ZIP은 Actions Artifact에 업로드하지 않습니다.
- 과거 자동 생성 `sprites-vX.Y.Z` sprite Release는 workflow가 정리합니다.
- GitHub Pages에는 대용량 ZIP 자체를 넣지 않습니다.
- BasePackGuard / Canonical Forms / 지역폼 진화 / Mega36 / SD proto=3 정책은 그대로 유지됩니다.

중요
- 이 업데이트만으로 microSD sprite를 다시 복사할 필요는 없습니다.
- 기존 tools/catalog_lock.json을 삭제하지 마세요.

- 과거 Actions Artifact 중 `TamaPoke-vX.Y.Z-full-sd-sprites` 이름의 대용량 백업도 다음 성공 build에서 자동 정리됩니다.
