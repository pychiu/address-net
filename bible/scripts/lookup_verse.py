#!/usr/bin/env python3
"""
CUVMPT Biblical Verse Lookup Script
Chinese Union Version with Modern Punctuation Traditional (和合本現代標點繁體)

Usage:
    python lookup_verse.py "John 3:16"
    python lookup_verse.py "Genesis 1:1-3"
    python lookup_verse.py "Psalm 23"
    python lookup_verse.py "約翰福音 3:16"

API: https://getbible.net/v2/cunptt  (cunptt = Chinese Union New Punctuation Traditional Text)
"""

import sys
import json
import re
import urllib.request
import urllib.error

# ── Bible book mapping ────────────────────────────────────────────────────────

BOOK_MAP = {
    # English full names
    "genesis": (1, "創世記"), "exodus": (2, "出埃及記"), "leviticus": (3, "利未記"),
    "numbers": (4, "民數記"), "deuteronomy": (5, "申命記"), "joshua": (6, "約書亞記"),
    "judges": (7, "士師記"), "ruth": (8, "路得記"),
    "1samuel": (9, "撒母耳記上"), "2samuel": (10, "撒母耳記下"),
    "1kings": (11, "列王紀上"), "2kings": (12, "列王紀下"),
    "1chronicles": (13, "歷代志上"), "2chronicles": (14, "歷代志下"),
    "ezra": (15, "以斯拉記"), "nehemiah": (16, "尼希米記"), "esther": (17, "以斯帖記"),
    "job": (18, "約伯記"), "psalms": (19, "詩篇"), "psalm": (19, "詩篇"),
    "proverbs": (20, "箴言"), "ecclesiastes": (21, "傳道書"),
    "songofsolomon": (22, "雅歌"), "songs": (22, "雅歌"),
    "isaiah": (23, "以賽亞書"), "jeremiah": (24, "耶利米書"),
    "lamentations": (25, "耶利米哀歌"), "ezekiel": (26, "以西結書"),
    "daniel": (27, "但以理書"), "hosea": (28, "何西阿書"), "joel": (29, "約珥書"),
    "amos": (30, "阿摩司書"), "obadiah": (31, "俄巴底亞書"), "jonah": (32, "約拿書"),
    "micah": (33, "彌迦書"), "nahum": (34, "那鴻書"), "habakkuk": (35, "哈巴谷書"),
    "zephaniah": (36, "西番雅書"), "haggai": (37, "哈該書"),
    "zechariah": (38, "撒迦利亞書"), "malachi": (39, "瑪拉基書"),
    "matthew": (40, "馬太福音"), "mark": (41, "馬可福音"), "luke": (42, "路加福音"),
    "john": (43, "約翰福音"), "acts": (44, "使徒行傳"), "romans": (45, "羅馬書"),
    "1corinthians": (46, "哥林多前書"), "2corinthians": (47, "哥林多後書"),
    "galatians": (48, "加拉太書"), "ephesians": (49, "以弗所書"),
    "philippians": (50, "腓立比書"), "colossians": (51, "歌羅西書"),
    "1thessalonians": (52, "帖撒羅尼迦前書"), "2thessalonians": (53, "帖撒羅尼迦後書"),
    "1timothy": (54, "提摩太前書"), "2timothy": (55, "提摩太後書"),
    "titus": (56, "提多書"), "philemon": (57, "腓利門書"), "hebrews": (58, "希伯來書"),
    "james": (59, "雅各書"), "1peter": (60, "彼得前書"), "2peter": (61, "彼得後書"),
    "1john": (62, "約翰一書"), "2john": (63, "約翰二書"), "3john": (64, "約翰三書"),
    "jude": (65, "猶大書"), "revelation": (66, "啟示錄"),
    # Common abbreviations
    "gen": (1, "創世記"), "ex": (2, "出埃及記"), "exo": (2, "出埃及記"),
    "lev": (3, "利未記"), "num": (4, "民數記"), "deut": (5, "申命記"),
    "dt": (5, "申命記"), "josh": (6, "約書亞記"), "judg": (7, "士師記"),
    "1sam": (9, "撒母耳記上"), "2sam": (10, "撒母耳記下"),
    "1ki": (11, "列王紀上"), "2ki": (12, "列王紀下"),
    "1chr": (13, "歷代志上"), "2chr": (14, "歷代志下"),
    "ezr": (15, "以斯拉記"), "neh": (16, "尼希米記"), "est": (17, "以斯帖記"),
    "ps": (19, "詩篇"), "psa": (19, "詩篇"), "prov": (20, "箴言"),
    "ecc": (21, "傳道書"), "eccl": (21, "傳道書"), "song": (22, "雅歌"),
    "ss": (22, "雅歌"), "isa": (23, "以賽亞書"), "jer": (24, "耶利米書"),
    "lam": (25, "耶利米哀歌"), "ezek": (26, "以西結書"), "ez": (26, "以西結書"),
    "dan": (27, "但以理書"), "hos": (28, "何西阿書"), "am": (30, "阿摩司書"),
    "obad": (31, "俄巴底亞書"), "ob": (31, "俄巴底亞書"), "jon": (32, "約拿書"),
    "mic": (33, "彌迦書"), "nah": (34, "那鴻書"), "hab": (35, "哈巴谷書"),
    "zeph": (36, "西番雅書"), "zep": (36, "西番雅書"), "hag": (37, "哈該書"),
    "zech": (38, "撒迦利亞書"), "zec": (38, "撒迦利亞書"), "mal": (39, "瑪拉基書"),
    "mt": (40, "馬太福音"), "matt": (40, "馬太福音"), "mk": (41, "馬可福音"),
    "lk": (42, "路加福音"), "jn": (43, "約翰福音"), "joh": (43, "約翰福音"),
    "ac": (44, "使徒行傳"), "rom": (45, "羅馬書"), "ro": (45, "羅馬書"),
    "1co": (46, "哥林多前書"), "1cor": (46, "哥林多前書"),
    "2co": (47, "哥林多後書"), "2cor": (47, "哥林多後書"),
    "gal": (48, "加拉太書"), "eph": (49, "以弗所書"), "php": (50, "腓立比書"),
    "phil": (50, "腓立比書"), "col": (51, "歌羅西書"),
    "1th": (52, "帖撒羅尼迦前書"), "1thess": (52, "帖撒羅尼迦前書"),
    "2th": (53, "帖撒羅尼迦後書"), "2thess": (53, "帖撒羅尼迦後書"),
    "1ti": (54, "提摩太前書"), "1tim": (54, "提摩太前書"),
    "2ti": (55, "提摩太後書"), "2tim": (55, "提摩太後書"),
    "tit": (56, "提多書"), "phm": (57, "腓利門書"), "heb": (58, "希伯來書"),
    "jas": (59, "雅各書"), "jm": (59, "雅各書"),
    "1pe": (60, "彼得前書"), "1pet": (60, "彼得前書"),
    "2pe": (61, "彼得後書"), "2pet": (61, "彼得後書"),
    "1jn": (62, "約翰一書"), "1jo": (62, "約翰一書"),
    "2jn": (63, "約翰二書"), "2jo": (63, "約翰二書"),
    "3jn": (64, "約翰三書"), "3jo": (64, "約翰三書"),
    "rev": (66, "啟示錄"), "re": (66, "啟示錄"),
    # Chinese names
    "創世記": (1, "創世記"), "出埃及記": (2, "出埃及記"), "利未記": (3, "利未記"),
    "民數記": (4, "民數記"), "申命記": (5, "申命記"), "約書亞記": (6, "約書亞記"),
    "士師記": (7, "士師記"), "路得記": (8, "路得記"), "撒母耳記上": (9, "撒母耳記上"),
    "撒母耳記下": (10, "撒母耳記下"), "列王紀上": (11, "列王紀上"),
    "列王紀下": (12, "列王紀下"), "歷代志上": (13, "歷代志上"),
    "歷代志下": (14, "歷代志下"), "以斯拉記": (15, "以斯拉記"),
    "尼希米記": (16, "尼希米記"), "以斯帖記": (17, "以斯帖記"), "約伯記": (18, "約伯記"),
    "詩篇": (19, "詩篇"), "箴言": (20, "箴言"), "傳道書": (21, "傳道書"),
    "雅歌": (22, "雅歌"), "以賽亞書": (23, "以賽亞書"), "耶利米書": (24, "耶利米書"),
    "耶利米哀歌": (25, "耶利米哀歌"), "以西結書": (26, "以西結書"),
    "但以理書": (27, "但以理書"), "何西阿書": (28, "何西阿書"), "約珥書": (29, "約珥書"),
    "阿摩司書": (30, "阿摩司書"), "俄巴底亞書": (31, "俄巴底亞書"),
    "約拿書": (32, "約拿書"), "彌迦書": (33, "彌迦書"), "那鴻書": (34, "那鴻書"),
    "哈巴谷書": (35, "哈巴谷書"), "西番雅書": (36, "西番雅書"), "哈該書": (37, "哈該書"),
    "撒迦利亞書": (38, "撒迦利亞書"), "瑪拉基書": (39, "瑪拉基書"),
    "馬太福音": (40, "馬太福音"), "馬可福音": (41, "馬可福音"),
    "路加福音": (42, "路加福音"), "約翰福音": (43, "約翰福音"),
    "使徒行傳": (44, "使徒行傳"), "羅馬書": (45, "羅馬書"),
    "哥林多前書": (46, "哥林多前書"), "哥林多後書": (47, "哥林多後書"),
    "加拉太書": (48, "加拉太書"), "以弗所書": (49, "以弗所書"),
    "腓立比書": (50, "腓立比書"), "歌羅西書": (51, "歌羅西書"),
    "帖撒羅尼迦前書": (52, "帖撒羅尼迦前書"), "帖撒羅尼迦後書": (53, "帖撒羅尼迦後書"),
    "提摩太前書": (54, "提摩太前書"), "提摩太後書": (55, "提摩太後書"),
    "提多書": (56, "提多書"), "腓利門書": (57, "腓利門書"), "希伯來書": (58, "希伯來書"),
    "雅各書": (59, "雅各書"), "彼得前書": (60, "彼得前書"), "彼得後書": (61, "彼得後書"),
    "約翰一書": (62, "約翰一書"), "約翰二書": (63, "約翰二書"),
    "約翰三書": (64, "約翰三書"), "猶大書": (65, "猶大書"), "啟示錄": (66, "啟示錄"),
}

API_BASE = "https://getbible.net/v2/cunptt"
TRANSLATION = "cunptt"  # Chinese Union New Punctuation Traditional Text = CUVMPT


# ── Parsing ───────────────────────────────────────────────────────────────────

def parse_reference(ref: str):
    """Parse a verse reference string into (book_num, chinese_name, chapter, start_verse, end_verse)."""
    ref = ref.strip()

    pattern = re.compile(
        r'^(\d?\s?[A-Za-z一-鿿]+(?:\s[A-Za-z一-鿿]+)*)\s*'
        r'(\d+)'
        r'(?::(\d+)(?:-(\d+))?)?$'
    )
    m = pattern.match(ref)
    if not m:
        return None

    book_raw, chapter_str, verse_str, end_verse_str = m.groups()
    book_key = re.sub(r'\s+', '', book_raw).lower()

    if book_key not in BOOK_MAP:
        return None

    book_num, chinese_name = BOOK_MAP[book_key]
    chapter = int(chapter_str)
    start_verse = int(verse_str) if verse_str else None
    end_verse = int(end_verse_str) if end_verse_str else start_verse

    return book_num, chinese_name, chapter, start_verse, end_verse


def extract_references(text: str) -> list:
    """Extract all verse references from free text."""
    book_names = sorted(BOOK_MAP.keys(), key=len, reverse=True)
    escaped = [re.escape(b) for b in book_names]
    book_pattern = '|'.join(escaped)

    full_pattern = re.compile(
        rf'({book_pattern})\s*(\d+)(?::(\d+)(?:-(\d+))?)?',
        re.IGNORECASE
    )

    refs = []
    for m in full_pattern.finditer(text):
        refs.append(m.group(0).strip())
    return list(dict.fromkeys(refs))


# ── API fetch ─────────────────────────────────────────────────────────────────

def fetch_chapter(book_num: int, chapter: int):
    """Fetch chapter data from getbible.net."""
    url = f"{API_BASE}/{book_num}/{chapter}.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"  ⚠️  API error: {e}", file=sys.stderr)
        return None


def get_verses(book_num: int, chapter: int, start, end):
    """Return verse text(s) for the given reference."""
    data = fetch_chapter(book_num, chapter)
    if not data:
        return []

    verses_data = data.get("verses", [])
    if start is None:
        return [v["verse"] for v in verses_data]

    result = []
    for v in verses_data:
        vnum = v.get("verse_nr") or v.get("verse_number") or verses_data.index(v) + 1
        if start <= vnum <= (end or start):
            result.append(v["verse"])
    return result


# ── Display ───────────────────────────────────────────────────────────────────

SEPARATOR = "━" * 50

def display_verse(ref_str: str, parsed, verses: list):
    book_num, chinese_name, chapter, start, end = parsed
    if start and end and start != end:
        ref_label = f"{chapter}:{start}–{end}"
    elif start:
        ref_label = f"{chapter}:{start}"
    else:
        ref_label = f"第 {chapter} 章"

    print(f"\n{SEPARATOR}")
    print(f"📖  {chinese_name} {ref_label}")
    print(SEPARATOR)
    for verse in verses:
        print(verse)
    print(f"\n（參考經文：{ref_str}）")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("用法：python lookup_verse.py \"John 3:16\"")
        print("      python lookup_verse.py \"<free text containing references>\"")
        sys.exit(1)

    text = " ".join(sys.argv[1:])

    parsed = parse_reference(text)
    if parsed:
        refs = [text]
        parsed_map = {text: parsed}
    else:
        refs = extract_references(text)
        parsed_map = {}
        for r in refs:
            p = parse_reference(r)
            if p:
                parsed_map[r] = p

    if not refs:
        print("ℹ️  未在提供的文字中找到任何聖經經文引用。")
        sys.exit(0)

    print(f"找到 {len(refs)} 個經文引用，正在從 CUVMPT 取得內容……")

    for ref in refs:
        if ref not in parsed_map:
            print(f"\n⚠️  無法解析：{ref}")
            continue

        parsed = parsed_map[ref]
        book_num, chinese_name, chapter, start, end = parsed

        verses = get_verses(book_num, chapter, start, end)
        if verses:
            display_verse(ref, parsed, verses)
        else:
            print(f"\n❌  無法取得：{ref}")
            print(f"   請至 https://www.biblegateway.com/passage/?search={ref.replace(' ', '+')}&version=CUVMPT 查閱")

    print(f"\n{SEPARATOR}")
    print("（譯文來源：和合本現代標點繁體聖經 CUVMPT via getbible.net）")


if __name__ == "__main__":
    main()
