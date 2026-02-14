# 항공권 조건 검색기 (Naver + Skyscanner)

원하는 **날짜/시간/최대 금액**을 지정하면, 여러 사이트에서 결과를 수집해 조건에 맞는 항공권만 보여주는 CLI 프로그램입니다.

## 기능
- 출발지/도착지/출발일 조건 검색
- 출발 시간 범위 필터 (`--earliest`, `--latest`)
- 최대 금액 필터 (`--max-price`)
- 제공자별 결과 비교 (현재: 네이버 항공권, 스카이스캐너)

## 설치
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

## 주의 사항
- 네이버/스카이스캐너는 공식 공개 검색 API가 제한적이어서, 현재 구현은 HTML 파싱 기반입니다.
- 사이트 구조 변경, 동적 렌더링, 봇 차단 정책에 따라 결과가 비어 있거나 실패할 수 있습니다.
- 실제 서비스 수준으로 운영하려면:
  - 공식 제휴 API 또는 안정적인 데이터 소스 확보
  - 재시도/프록시/헤드리스 브라우저 전략
  - 법적/이용약관 검토
