# Bible — CUVMPT Verse Lookup

> 和合本現代標點繁體聖經（CUVMPT）經文查詢工具  
> Claude Code skill and Python script for looking up biblical verses in the **Chinese Union Version with Modern Punctuation Traditional** (CUVMPT / 中文聖經和合本現代標點繁體).

---

## `/cuvmpt` — Claude Code Skill

### Installation

Copy `.claude/commands/cuvmpt.md` into your project's `.claude/commands/` folder, or reference this repo as a custom command source.

### Usage

```
/cuvmpt <text containing one or more biblical verse references>
```

**Examples:**

```
/cuvmpt John 3:16
```
```
/cuvmpt For God so loved the world — see John 3:16. Also read Romans 8:28 and Philippians 4:13.
```
```
/cuvmpt 請閱讀約翰福音3:16和詩篇23:1-6的內容。
```

### What it does

1. **Extracts** every biblical verse reference from the supplied text — English, abbreviated, ranged, or Chinese format.
2. **Fetches** each verse from the getbible.net v2 API using translation code `cunptt` (Chinese Union New Punctuation Traditional Text = CUVMPT).
3. **Displays** the Traditional Chinese text alongside the original reference.

**Sample output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖  約翰福音 3:16
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
「神愛世人，甚至將他的獨生子賜給他們，叫一切信他的，不至滅亡，
反得永生。」

（參考經文：John 3:16）
```

---

## `scripts/lookup_verse.py` — Command-line Tool

### Requirements

- Python 3.8+
- Internet access (calls `getbible.net`)

### Usage

```bash
# Single verse
python scripts/lookup_verse.py "John 3:16"

# Verse range
python scripts/lookup_verse.py "Romans 8:28-30"

# Entire chapter
python scripts/lookup_verse.py "Psalm 23"

# Chinese reference
python scripts/lookup_verse.py "約翰福音 3:16"

# Free text — all references are extracted automatically
python scripts/lookup_verse.py "Paul writes in Phil 4:13 and Eph 2:8-9 about grace and strength."
```

---

## API

Verses are fetched from the free [getbible.net v2 API](https://getbible.net):

```
https://getbible.net/v2/cunptt/{book_number}/{chapter}.json
```

Translation code: **`cunptt`** = Chinese Union New Punctuation Traditional Text (CUVMPT 和合本現代標點繁體)

---

## Supported Reference Formats

| Type | Examples |
|------|----------|
| Full English | `John 3:16`, `Genesis 1:1`, `Revelation 22:20` |
| Abbreviated | `Jn 3:16`, `Gen 1:1`, `Rev 22:20`, `Ps 23:1` |
| Verse range | `Matthew 5:3-12`, `Romans 8:28-30` |
| Whole chapter | `Psalm 23`, `John 3` |
| Chinese | `約翰福音3:16`, `創世記1:1`, `詩篇23:1` |

---

## License

MIT
