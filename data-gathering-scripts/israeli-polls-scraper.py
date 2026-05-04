import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    """
    Israeli 2026 Knesset Election — Poll Scraper v2
    ================================================
    Uses pd.read_html (which correctly expands rowspan/colspan cells) instead of
    manual BeautifulSoup row iteration, which was producing shifted/garbage rows.

    Usage:
        pip install requests beautifulsoup4 pandas lxml
        python israeli_polls_scraper.py

    Output:
        israeli_polls.csv
    """

    import re
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    from io import StringIO

    # ── URLs ───────────────────────────────────────────────────────────────────────

    URLS = [
        # (url, year_hint)  — year_hint is the LATEST year on the page
        ("https://en.wikipedia.org/wiki/2022%E2%80%932023_opinion_polling_for_the_2026_Israeli_legislative_election", 2023),
        ("https://en.wikipedia.org/wiki/2024_opinion_polling_for_the_2026_Israeli_legislative_election", 2024),
        ("https://en.wikipedia.org/wiki/2025_opinion_polling_for_the_2026_Israeli_legislative_election", 2025),
        ("https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_Israeli_legislative_election", 2026),
    ]

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    # ── Column mapping ─────────────────────────────────────────────────────────────

    # Ordered list of (fragment, canonical_name). Earlier entries win on ambiguity.
    COLUMN_MAP = [
        ("fieldwork",          "date"),
        ("polling firm",       "firm"),
        ("publisher",          "publisher"),
        ("lead",               "lead"),
        ("gov.",               "gov_total"),
        ("opp.",               "opp_total"),
        ("government bloc",    "gov_bloc"),
        ("opposition bloc",    "opp_bloc"),
        ("unaligned",          "unaligned_bloc"),
        # Coalition parties
        ("likud",              "Likud"),
        ("religious zionism",  "Rel_Zionism"),
        ("rel. zionism",       "Rel_Zionism"),
        ("otzma yehudit",      "Otzma_Yehudit"),
        ("otzma",              "Otzma_Yehudit"),
        ("shas",               "Shas"),
        ("united torah",       "UTJ"),
        ("utj",                "UTJ"),
        ("new hope",           "New_Hope"),
        ("noam",               "Noam"),
        # Opposition parties
        ("yesh atid",          "Yesh_Atid"),
        ("blue",               "Blue_White"),
        ("national unity",     "National_Unity"),
        ("yisrael beiteinu",   "Yisrael_Beiteinu"),
        ("democrat",           "Democrats"),
        ("bennett",            "Bennett_2026"),
        ("beyachad",           "BeYachad"),
        ("together",           "BeYachad"),
        ("yashar",             "Yashar"),
        ("labor",              "Labor"),
        ("meretz",             "Meretz"),
        # Unaligned
        ("ra'am",              "Raam"),
        ("raam",               "Raam"),
        ("hadash",             "Hadash_Taal"),
        ("balad",              "Balad"),
        ("reserv",             "Reservists"),
        ("joint list",         "Joint_List"),
    ]

    PARTY_COLS = [
        "Likud", "Rel_Zionism", "Otzma_Yehudit", "Shas", "UTJ", "New_Hope", "Noam",
        "Yesh_Atid", "Blue_White", "National_Unity", "Yisrael_Beiteinu", "Democrats",
        "Bennett_2026", "BeYachad", "Yashar", "Labor", "Meretz",
        "Raam", "Hadash_Taal", "Balad", "Reservists", "Joint_List",
    ]

    MONTH_ABBRS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    MONTH_NUM   = {m: i + 1 for i, m in enumerate(MONTH_ABBRS)}
    MONTH_RE    = r"(?:" + "|".join(MONTH_ABBRS) + r")"


    # ── Header utilities ───────────────────────────────────────────────────────────

    def map_header(raw: str) -> str:
        text = re.sub(r"\[.*?\]", "", str(raw)).strip().lower()
        for fragment, canonical in COLUMN_MAP:
            if fragment in text:
                return canonical
        slug = re.sub(r"\W+", "_", text).strip("_")
        return slug or "unknown"


    def flatten_multiindex(mi) -> list:
        result = []
        for col in mi:
            if not isinstance(col, tuple):
                result.append(map_header(str(col)))
                continue
            parts = []
            for level in col:
                s = str(level).strip()
                if s and not s.startswith("Unnamed"):
                    parts.append(s)
            # Remove consecutive duplicates
            unique = []
            for p in parts:
                if not unique or p != unique[-1]:
                    unique.append(p)
            result.append(map_header(" ".join(unique)))
        return result


    def dedupe_cols(cols: list) -> list:
        seen: dict = {}
        out = []
        for c in cols:
            if c in seen:
                seen[c] += 1
                out.append(f"{c}_{seen[c]}")
            else:
                seen[c] = 0
                out.append(c)
        return out


    # ── Date utilities ─────────────────────────────────────────────────────────────

    def extract_last_date(raw) -> str | None:
        """
        Extracts the END date from any Wikipedia date format:
          "26 Feb"         -> "26 Feb"
          "25-26 Feb"      -> "26 Feb"
          "29 Oct - 1 Nov" -> "1 Nov"
          "31 Dec - 1 Jan" -> "1 Jan"
        Returns None for event rows, blank cells, numeric fragments.
        """
        if not isinstance(raw, str):
            return None
        s = re.sub(r"\[.*?\]", "", raw).strip()
        if not s or s in ("-", "–", "—"):
            return None
        # Find every "DD Mon" or "D Mon" occurrence
        matches = re.findall(rf"\b(\d{{1,2}})\s+({MONTH_RE})\b", s, re.IGNORECASE)
        if matches:
            day, mon = matches[-1]
            return f"{day} {mon.capitalize()}"
        # Purely numeric / dash-only -> broken rowspan fragment
        if re.match(r"^[\d\s\u2013\u2014\-]+$", s):
            return None
        return None  # event-note row, not a date


    def assign_years(date_series: pd.Series, year_hint: int) -> list:
        """
        Walk the date column (which is in REVERSE chronological order as Wikipedia
        lists polls most-recent-first) and detect year rollovers.

        When month number INCREASES while going down the table (i.e., time went
        forward = we crossed a New Year boundary going backward), decrement the
        working year.
        """
        years = []
        current_year = year_hint
        prev_month = None

        for raw in date_series:
            if not isinstance(raw, str):
                years.append(current_year)
                continue
            m = re.search(rf"\b({MONTH_RE})\b", raw, re.IGNORECASE)
            if not m:
                years.append(current_year)
                continue
            mon_num = MONTH_NUM.get(m.group(1).capitalize(), 0)
            if prev_month is not None and mon_num > prev_month:
                current_year -= 1
            years.append(current_year)
            prev_month = mon_num

        return years


    # ── Row filtering / value cleaning ────────────────────────────────────────────

    def is_valid_firm(val) -> bool:
        try:
            if pd.isna(val):
                return False
        except (TypeError, ValueError):
            pass
        s = str(val).strip()
        if not s or s in ("nan", "None", "–", "—", "-"):
            return False
        # Pure number = shifted seat count from mis-parsed rowspan row
        if re.match(r"^[\d\.\-]+$", s):
            return False
        return True


    def clean_seat(val) -> float | None:
        try:
            if pd.isna(val):
                return None
        except (TypeError, ValueError):
            pass
        s = str(val).strip()
        if not s or s in ("nan", "None", "–", "—", "-"):
            return None
        # Sub-threshold notation: "(2.3%)" or "2.3%"
        m = re.match(r"^\(?\s*(\d+\.?\d*)\s*%\s*\)?$", s)
        if m:
            return -float(m.group(1))   # negative = below electoral threshold
        try:
            return float(s)
        except ValueError:
            return None


    # ── Core scraper ───────────────────────────────────────────────────────────────

    def scrape_page(url: str, year_hint: int) -> pd.DataFrame:
        print(f"Fetching {url} …")
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        tables = soup.find_all("table", class_=re.compile(r"wikitable"))

        def is_seats_table(t) -> bool:
            txt = t.get_text().lower()
            return "likud" in txt and ("fieldwork" in txt or "polling firm" in txt)

        seats_tables = [t for t in tables if is_seats_table(t)]
        if not seats_tables:
            print("  ⚠  No seats table found")
            return pd.DataFrame()

        main_table = max(seats_tables, key=lambda t: len(t.find_all("tr")))

        # pd.read_html correctly handles rowspan/colspan — critical for Wikipedia tables
        try:
            raw = pd.read_html(StringIO(str(main_table)), header=[0, 1], flavor="lxml")
        except Exception:
            raw = pd.read_html(StringIO(str(main_table)), header=[0, 1])

        df = raw[0].copy()

        # Flatten MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = dedupe_cols(flatten_multiindex(df.columns))
        else:
            df.columns = dedupe_cols([map_header(str(c)) for c in df.columns])

        df["_year_hint"] = year_hint
        df["source_url"] = url
        return df


    # ── Post-processing ────────────────────────────────────────────────────────────

    def process_page(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        year_hint = int(df["_year_hint"].iloc[0])

        # ── Date resolution ────────────────────────────────────────────────────────
        if "date" in df.columns:
            df["date_clean"] = df["date"].apply(extract_last_date)
            # Forward-fill for scenario sub-rows that share a parent's date
            df["date_clean"] = df["date_clean"].ffill()
            years = assign_years(df["date_clean"], year_hint)
            df["date"] = [
                f"{d} {y}" if isinstance(d, str) else d
                for d, y in zip(df["date_clean"], years)
            ]
            df["date_parsed"] = pd.to_datetime(
                df["date"], dayfirst=True, errors="coerce", format="mixed"
            )
            df.drop(columns="date_clean", inplace=True)

        # ── Filter non-poll rows ───────────────────────────────────────────────────
        if "firm" in df.columns:
            df = df[df["firm"].apply(is_valid_firm)].copy()

        # ── Numeric conversion ────────────────────────────────────────────────────
        for col in PARTY_COLS + ["gov_total", "opp_total", "gov_bloc", "opp_bloc"]:
            if col in df.columns:
                df[col] = df[col].apply(clean_seat)

        df.drop(columns="_year_hint", inplace=True, errors="ignore")
        return df.reset_index(drop=True)


    # ── Main ───────────────────────────────────────────────────────────────────────

    if __name__ == "__main__":
        all_dfs = []

        for url, year_hint in URLS:
            raw_df = scrape_page(url, year_hint)
            if raw_df.empty:
                continue
            clean_df = process_page(raw_df)
            print(f"  → {len(clean_df)} clean rows, {len(clean_df.columns)} columns")
            all_dfs.append(clean_df)

        if not all_dfs:
            print("No data scraped.")
        else:
            combined = pd.concat(all_dfs, ignore_index=True, sort=False)
            combined = combined.sort_values(
                "date_parsed", na_position="last"
            ).reset_index(drop=True)

            print(f"\n✓ Combined: {combined.shape[0]} rows × {combined.shape[1]} columns")

            if "date_parsed" in combined.columns:
                valid = combined["date_parsed"].dropna()
                print(f"Date range: {valid.min().date()} → {valid.max().date()}")
                print(f"Rows with parsed dates: {len(valid)} / {len(combined)}")
                bad = combined[combined["date_parsed"].isna()]
                if len(bad):
                    print(f"\n⚠  {len(bad)} rows still missing dates:")
                    show = [c for c in ["date", "firm", "publisher"] if c in bad.columns]
                    print(bad[show].to_string())

            preview_cols = [c for c in [
                "date_parsed", "firm", "publisher",
                "Likud", "Bennett_2026", "BeYachad", "Yesh_Atid",
                "Rel_Zionism", "Shas", "UTJ", "gov_total", "opp_total",
            ] if c in combined.columns]

            print("\nFirst 5 rows (oldest polls):")
            print(combined[preview_cols].head(5).to_string())
            print("\nLast 5 rows (most recent polls):")
            print(combined[preview_cols].tail(5).to_string())

            combined.to_csv("israeli_polls.csv", index=False)
            print("\n✓ Saved to israeli_polls.csv")
    return (combined,)


@app.cell
def _(combined):
    combined.tail(10)
    return


@app.cell
def _(combined):
    combined.describe()
    return


@app.cell
def _(combined):
    complete = combined[combined["Likud"].notna()]
    complete.describe()
    return (complete,)


@app.cell
def _(complete):
    complete.to_csv("israeli_polls_april_30.csv", index=False)
    return


if __name__ == "__main__":
    app.run()
