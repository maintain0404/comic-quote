from __future__ import annotations

from comic_quote.domain.quote.entity import Quote

QUOTES = [
    Quote(
        id=1,
        content="우리는 모습이 없는 까닭에 그것을 두려워한다.",
        artwork_name="블리치",
        character="권두시",
        where="1권",
    ),
    Quote(
        id=2,
        content=(
            "그만둬라. 니들 공격 정도론 난 죽지 않아.\n"
            "사람이 언제 죽는다고 생각하나...?\n"
            "심장이 총알에 뚫렸을 때...? ...아니.\n"
            "불치의 병에 걸렸을 때? ...아니.\n"
            "맹독 버섯 스프를 마셨을 때...? 아니야!!!\n"
            "...사람들에게서 잊혀졌을 때다...!!!"
        ),
        artwork_name="원피스",
        character="Dr. 히루루크",
        where="16권",
    ),
    Quote(
        id=3,
        content=(
            "사람은 그 무언가의 희생 없이는 아무것도 얻을 수 없다. "
            "무언가를 얻기 위해서는 그와 동등한 대가를 치러야 한다."
        ),
        artwork_name="강철의 연금술사",
        character="에드워드 엘릭",
    ),
]


class QuoteRepo:
    async def get_all_count(self) -> int:
        return len(QUOTES)

    async def get_by_id(self, id: int) -> Quote:
        if not (0 < id <= len(QUOTES)):
            raise ValueError
        return QUOTES[id - 1]
