import pytest
from load_scores import load_scores


# ── 정상 ──────────────────────────────────────────
def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5


def test_빈_줄은_건너뛴다():
    kept, skipped = load_scores("scores.csv")
    assert ("윤보람", 64) in kept          # 빈 줄 바로 다음 줄도 읽힌다


def test_이름에_쉼표가_있어도_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert ("최,네번", 77) in kept


# ── 예외 ──────────────────────────────────────────
def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []

def test_이름이_비면_건너뛴다():
    kept, skipped = load_scores("weird.csv")
    assert (2, ",90", "이름이 비어 있음") in skipped


# ── 경계값 ────────────────────────────────────────
def 쓰기(path, 점수):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"name,score\n테스트,{점수}\n")


@pytest.mark.parametrize("점수, 유효한가", [
    (-1,  False),   # 경계 바로 아래
    (0,   True),    # ★ 아래쪽 경계
    (1,   True),
    (99,  True),
    (100, True),    # ★ 위쪽 경계
    (101, False),   # 경계 바로 위
])
def test_점수_경계값(점수, 유효한가):
    쓰기("임시.csv", 점수)
    kept, skipped = load_scores("임시.csv")
    assert (len(kept) == 1) == 유효한가