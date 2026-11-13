# 실적전망 상위 종목 페이지 — 업데이트 절차

이 폴더의 `data.json`을 오늘 기준 최신 정보로 다시 쓰고, Artifact를 재게시한다.

## 무엇을 고르나

분야(섹터) 6개 × 시장 2개(국내 kr, 미국 us) × 종류 2개(stocks 개별주식, etfs ETF) × 각 3개.

섹터 id와 이름은 고정한다:

| id | name |
|---|---|
| semis | 반도체·AI 하드웨어 |
| software | 인터넷·소프트웨어 |
| health | 헬스케어·바이오 |
| finance | 금융 |
| industrial | 산업재·방산·조선 |
| energy | 에너지·2차전지·소재 |

## 선정 기준 (실적전망 우선)

- 개별주식: 증권사 컨센서스 기준 **향후 12개월(또는 내년) EPS·영업이익 증가율**이 높고, 최근 1~3개월 동안 실적 추정치가 **상향**된 종목. 시가총액이 작은 종목(국내 5천억 원 미만, 미국 20억 달러 미만)은 제외.
  - 국내 참고처: FnGuide/에프앤가이드 컨센서스, 한경 컨센서스, 네이버 증권, 증권사 리포트 기사.
  - 미국 참고처: 애널리스트 컨센서스(EPS 추정치, 목표주가)를 다루는 최근 기사, Zacks, MarketBeat, Nasdaq.com, Yahoo Finance 등.
- ETF: ETF 자체는 실적이 없으므로 **해당 섹터 실적 개선 기대가 큰 테마를 담은, 순자산이 큰 ETF**를 고른다. 국내는 국내 상장 ETF(KODEX, TIGER, ACE, SOL, RISE 등), 미국은 미국 상장 ETF(SMH, XLK, XLV 등). metric에는 총보수나 최근 수익률보다 **편입 상위 종목의 이익 전망**과 연결되는 근거를 적는다(예: "상위 10종목 내년 EPS +25% 전망").
- 숫자는 모두 웹 검색으로 확인한 값만 쓴다. 확인하지 못한 값은 지어내지 말고 `null`로 둔다.
- 전날 데이터와 비교해 바뀐 이유가 없으면 종목을 무리하게 바꾸지 않는다.

## data.json 스키마

```json
{
  "updatedAt": "2026-11-13T08:00:00+09:00",
  "basis": "선정 기준 한 문장",
  "sectors": [
    {
      "id": "semis",
      "name": "반도체·AI 하드웨어",
      "kr": { "stocks": [Item, Item, Item], "etfs": [Item, Item, Item] },
      "us": { "stocks": [Item, Item, Item], "etfs": [Item, Item, Item] }
    }
  ]
}
```

Item:

```json
{
  "name": "SK하이닉스",
  "ticker": "000660",
  "metricLabel": "2027E 영업이익 증가율",
  "metricValue": "+32%",
  "upside": "+18%",
  "thesis": "HBM 수요 확대로 내년 이익 추정치가 3개월간 상향 (한 문장, 60자 안팎)",
  "source": "https://... (근거 기사·자료 URL 1개)"
}
```

- `upside`: 컨센서스 목표주가 대비 현재가 상승여력. ETF나 확인 불가 시 `null`.
- `thesis`는 한국어 한 문장.
- 섹터 순서는 위 표 순서.

## 게시

1. 국내 결과를 `kr.json`, 미국 결과를 `us.json`에 섹터 id별로 쓴다(`{"semis":{"stocks":[...],"etfs":[...]}, ...}`). 국내·미국 조사는 서브에이전트 두 개로 나눠 병렬로 해도 된다. 그다음 `python merge.py`로 `data.json`을 만든다. 경고가 나오면 빠진 항목을 채운다.
2. Artifact 도구로 재게시: `file_path` = 이 폴더의 `index.html`, `url` = `ARTIFACT_URL.txt`에 적힌 주소, `files` = `{"data.json": "<이 폴더>/data.json"}`. icon은 넘기지 않는다.
3. GitHub에 올린다(`merge.py`가 `docs/`도 갱신함): `git add -A && git commit -m "data: YYYY-MM-DD 갱신" && git push`. GitHub Pages(https://sunnymoonday.github.io/stock-outlook/)가 몇 분 안에 반영된다.
