# 항공권 조건 검색기 (Naver + Skyscanner)

원하는 **날짜/시간/최대 금액**을 지정하면, 여러 사이트에서 결과를 수집해 조건에 맞는 항공권만 보여주는 CLI 프로그램입니다.

## 기능
- 출발지/도착지/출발일 조건 검색
- 출발 시간 범위 필터 (`--earliest`, `--latest`)
- 최대 금액 필터 (`--max-price`)
- 제공자별 결과 비교 (현재: 네이버 항공권, 스카이스캐너)

## 설치 (개발/로컬 실행)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 사용 예시
```bash
flight-search \
  --origin ICN \
  --destination NRT \
  --date 2026-03-01 \
  --earliest 09:00 \
  --latest 14:00 \
  --max-price 250000 \
  --currency KRW
```

## Windows에서 EXE 만들기
PowerShell에서 프로젝트 루트로 이동 후:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows_exe.ps1
```

빌드가 완료되면 아래 파일이 생성됩니다.
- `dist\flight-search.exe`

실행 예시:
```powershell
.\dist\flight-search.exe --origin ICN --destination NRT --date 2026-03-01 --earliest 09:00 --latest 14:00 --max-price 250000 --currency KRW
```

## 다운로드 가능한 EXE 만들기 (GitHub Actions)
레포에 푸시한 뒤 GitHub에서:
1. `Actions` 탭 이동
2. `Build Windows EXE` 워크플로우 실행 (`Run workflow`)
3. 실행 완료 후 Artifacts에서 `flight-search-windows-exe` 다운로드

## 릴리즈 페이지에 EXE 자동 첨부
`Release`를 `Published` 상태로 생성하면 워크플로우가 자동으로 Windows EXE를 빌드하고,
해당 릴리즈의 Assets에 `flight-search.exe`를 자동 첨부합니다.

워크플로우 파일:
- `.github/workflows/build-windows-exe.yml`

## 주의 사항
- 네이버/스카이스캐너는 공식 공개 검색 API가 제한적이어서, 현재 구현은 HTML 파싱 기반입니다.
- 사이트 구조 변경, 동적 렌더링, 봇 차단 정책에 따라 결과가 비어 있거나 실패할 수 있습니다.
- 실제 서비스 수준으로 운영하려면:
  - 공식 제휴 API 또는 안정적인 데이터 소스 확보
  - 재시도/프록시/헤드리스 브라우저 전략
  - 법적/이용약관 검토
