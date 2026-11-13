"""kr.json + us.json -> data.json (섹터 순서·이름 고정)."""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).parent
SECTORS = [
    ("semis", "반도체·AI 하드웨어"),
    ("software", "인터넷·소프트웨어"),
    ("health", "헬스케어·바이오"),
    ("finance", "금융"),
    ("industrial", "산업재·방산·조선"),
    ("energy", "에너지·2차전지·소재"),
]
BASIS = ("증권사 컨센서스 기준 향후 12개월 EPS·영업이익 증가율과 최근 추정치 상향을 우선해 고르고, "
         "ETF는 해당 분야 이익 개선 기대가 큰 대형 ETF를 골랐습니다.")

import sys
DOCS_ONLY = "--docs-only" in sys.argv  # data.json은 그대로 두고 docs/만 다시 만든다

kr = json.loads((HERE / "kr.json").read_text(encoding="utf-8"))
us = json.loads((HERE / "us.json").read_text(encoding="utf-8"))
kst = timezone(timedelta(hours=9))
data = {
    "updatedAt": datetime.now(kst).isoformat(timespec="minutes"),
    "basis": BASIS,
    "sectors": [
        {"id": sid, "name": name,
         "kr": kr.get(sid, {"stocks": [], "etfs": []}),
         "us": us.get(sid, {"stocks": [], "etfs": []})}
        for sid, name in SECTORS
    ],
}
for s in data["sectors"]:
    for m in ("kr", "us"):
        for k in ("stocks", "etfs"):
            n = len(s[m].get(k, []))
            if n != 3:
                print(f"warning: {s['id']}.{m}.{k} has {n} items")
if not DOCS_ONLY:
    (HERE / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("data.json written", data["updatedAt"])

# GitHub Pages용 사본: docs/ 아래에 완전한 HTML 문서로 감싸서 쓴다
docs = HERE / "docs"
docs.mkdir(exist_ok=True)
page = (HERE / "index.html").read_text(encoding="utf-8")
(docs / "index.html").write_text(
    '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    "</head>\n<body>\n" + page + "\n</body>\n</html>\n",
    encoding="utf-8",
)
(docs / "data.json").write_text((HERE / "data.json").read_text(encoding="utf-8"), encoding="utf-8")
(docs / ".nojekyll").write_text("", encoding="utf-8")
print("docs/ updated for GitHub Pages")
