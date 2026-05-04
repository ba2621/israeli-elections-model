import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    import pandas as pd

    election_map_2024 = pd.read_csv("24th Knesset by City.csv", encoding="windows-1255")
    return election_map_2024, pd


@app.cell
def _(election_map_2024):
    election_map_2024.describe()
    return


@app.cell
def _(pd):
    _df = pd.read_csv("19th Knesset.csv", encoding="utf-8-sig")
    _df.columns = _df.columns.str.strip()  # leading space in first column

    rename_map_19 = {
        "שם ישוב": "city_name",
        "סמל ישוב": "city_code",
        "בזב": "eligible_voters",
        "מצביעים": "votes_cast",
        "פסולים": "invalid_votes",
        "כשרים": "valid_votes",
        # Major parties
        "אמת": "Labor",
        "ג": "UTJ",
        "ד": "Balad",
        "ו": "Hadash",
        "טב": "Jewish Home",
        "כן": "Kadima",
        "מחל": "Likud-Beiteinu",
        "מרץ": "Meretz",
        "נץ": "Otzma LeYisrael",
        "עם": "Raam-Taal",
        "פה": "Yesh Atid",
        "צפ": "The Movement (Hatnuah)",
        "שס": "Shas",
        "ץ": "Am Shalem",
        # Notable minor parties
        "קנ": "Green Leaf",
        "פז": "Minor Party (פז)",
        "ז": "Minor Party (ז)",
        "יק": "Bible Bloc",
        "רק": "Minor Party (רק)",
        "זך": "Minor Party (זך)",
        "הפ": "Minor Party (הפ)",
        "ק": "Minor Party (ק)",
        "צק": "Minor Party (צק)",
        "פנ": "Minor Party (פנ)",
        "פץ": "Minor Party (פץ)",
        "פי": "Minor Party (פי)",
        "פ": "Minor Party (פ)",
        "נק": "Minor Party (נק)",
        "ני": "Minor Party (ני)",
        "נ": "Minor Party (נ)",
        "הק": "Minor Party (הק)",
        "הי": "Minor Party (הי)",
        "פך": "Minor Party (פך)",
        "זה": "Minor Party (זה)",
    }

    df_19 = _df.rename(columns=rename_map_19)
    df_19.to_csv("knesset_19_en.csv", index=False)
    df_19.head()
    return df_19, rename_map_19


@app.cell
def _(df_19):
    df_19.tail(15)
    return


@app.cell
def _(pd):
    _df = pd.read_csv("20th_Knesset.csv", encoding="windows-1255")
    _df.columns = _df.columns.str.strip()  # leading space in first column

    rename_map_20 = {
        "שם ישוב": "city_name",
        "סמל ישוב": "city_code",
        "בזב": "eligible_voters",
        "מצביעים": "votes_cast",
        "פסולים": "invalid_votes",
        "כשרים": "valid_votes",
        # Major parties
        "אמת": "Zionist Union",
        "ג": "UTJ",
        "ודעם": "Joint List",
        "טב": "Jewish Home",
        "כ": "Kulanu",
        "ל": "Yisrael Beiteinu",
        "מחל": "Likud",
        "מרצ": "Meretz",
        "פה": "Yesh Atid",
        "שס": "Shas",
        # Notable sub-threshold parties
        "קץ": "Yachad-Ha'am Itanu",
        "קנ": "Green Leaf",
        # Minor parties
        "ז": "Minor Party (ז)",
        "זך": "Minor Party (זך)",
        "זץ": "Tzomet",
        "י": "Minor Party (י)",
        "יז": "Minor Party (יז)",
        "יך": "Minor Party (יך)",
        "יץ": "Minor Party (יץ)",
        "נז": "Minor Party (נז)",
        "ני": "Minor Party (ני)",
        "נץ": "Straw Party (נץ)",
        "ע": "Minor Party (ע)",
        "ף": "Pirate Party",
        "ףץ": "Minor Party (ףץ)",
        "רק": "Minor Party (רק)",
    }

    df_20 = _df.rename(columns=rename_map_20)
    df_20.to_csv("knesset_20_en.csv", index=False)
    df_20.head()
    return df_20, rename_map_20


@app.cell
def _(df_20):
    df_20.tail(15)
    return


@app.cell
def _(pd):
    _df = pd.read_csv("21st Knesset Data.csv", encoding="windows-1255")

    rename_map_21 = {
        "שם ישוב": "city_name",
        "סמל ישוב": "city_code",
        "בזב": "eligible_voters",
        "מצביעים": "votes_cast",
        "פסולים": "invalid_votes",
        "כשרים": "valid_votes",
        # Major parties
        "אמת": "Labor",
        "ג": "UTJ",
        "דעם": "Raam-Balad",
        "ום": "Hadash-Taal",
        "ז": "Zehut",
        "זץ": "Tzomet",
        "טב": "Union of Right-Wing Parties",
        "כ": "Kulanu",
        "ל": "Yisrael Beiteinu",
        "מחל": "Likud",
        "מרצ": "Meretz",
        "נ": "New Right",
        "נר": "Gesher",
        "פה": "Blue and White",
        "שס": "Shas",
        # Minor parties
        "ן": "Ani VeAtah",
        "ר": "Rapeh (Health)",
        "צק": "Minor Party (צק)",
        "נץ": "Minor Party (נץ)",
        "ק": "Minor Party (ק)",
        "י": "Minor Party (י)",
        "נז": "Minor Party (נז)",
        "זי": "Minor Party (זי)",
        "קף": "Minor Party (קף)",
        "ףז": "Pirate Party",
        "ףי": "Minor Party (ףי)",
        "קי": "Minor Party (קי)",
        "ףץ": "Minor Party (ףץ)",
        "קן": "Minor Party (קן)",
        "ךק": "Minor Party (ךק)",
        "ץ": "Da'am",
        "ףך": "Minor Party (ףך)",
        "יץ": "Minor Party (יץ)",
        "ןך": "Minor Party (ןך)",
        "ףנ": "Minor Party (ףנ)",
        "ןנ": "Minor Party (ןנ)",
        "ץי": "Minor Party (ץי)",
        "יז": "Minor Party (יז)",
        "ין": "Minor Party (ין)",
        "זך": "Minor Party (זך)",
        "ץז": "Minor Party (ץז)",
        "זנ": "Minor Party (זנ)",
        "נך": "Minor Party (נך)",
    }

    df_21 = _df.rename(columns=rename_map_21)
    df_21.to_csv("knesset_21_en.csv", index=False)
    df_21.head()
    return df_21, rename_map_21


@app.cell
def _(df_21):
    df_21.tail(15)
    return


@app.cell
def _(pd):
    _df = pd.read_csv("22nd Knesset Data.csv", encoding="windows-1255")

    rename_map_22 = {
        "סמל ועדה": "committee_code",
        "שם ישוב": "city_name",
        "סמל ישוב": "city_code",
        "בזב": "eligible_voters",
        "מצביעים": "votes_cast",
        "פסולים": "invalid_votes",
        "כשרים": "valid_votes",
        # Major parties
        "אמת": "Labor-Gesher",
        "ג": "UTJ",
        "ודעם": "Joint List",
        "זץ": "Tzomet",
        "טב": "Yamina",
        "כף": "Otzma Yehudit",
        "ל": "Yisrael Beiteinu",
        "מחל": "Likud",
        "מרצ": "Democratic Union",
        "פה": "Blue and White",
        "שס": "Shas",
        # Minor parties
        "זכ": "Democratura",
        "זן": "Minor Party (זן)",
        "י": "Minor Party (י)",
        "יז": "Adom Lavan",
        "ינ": "Common Alliance",
        "יף": "Human Dignity",
        "יק": "Bible Bloc",
        "כ": "Noam (withdrew)",
        "כי": "United People",
        "נ": "Minor Party (נ)",
        "נך": "Honor and Equality",
        "נץ": "Minor Party (נץ)",
        "ץ": "Da'am",
        "ק": "Minor Party (ק)",
        "ןז": "Pirate Party",
        "ףז": "Pirate Party",
        "צ": "Minor Party (צ)",
        "צן": "North",
        "קך": "New Order",
        "קץ": "Mishpat Tzedek",
        "רק": "Ron Kobi",
        "ז": "Minor Party (ז)",
    }

    df_22 = _df.rename(columns=rename_map_22)
    df_22.to_csv("knesset_22_en.csv", index=False)
    df_22.head()
    return df_22, rename_map_22


@app.cell
def _(df_22):
    df_22.tail(15)
    return


@app.cell
def _(pd):
    _df = pd.read_csv("23rd Knesset Data.csv", encoding="windows-1255")

    rename_map_23 = {
        "סמל ועדה": "committee_code",
        "שם ישוב": "city_name",
        "סמל ישוב": "city_code",
        "בזב": "eligible_voters",
        "מצביעים": "votes_cast",
        "פסולים": "invalid_votes",
        "כשרים": "valid_votes",
        # Major parties
        "אמת": "Labor-Gesher-Meretz",
        "ג": "UTJ",
        "ודעם": "Joint List",
        "זץ": "Tzomet",
        "טב": "Yamina",
        "ל": "Yisrael Beiteinu",
        "מחל": "Likud",
        "נץ": "Otzma Yehudit",
        "פה": "Blue and White",
        "שס": "Shas",
        # Minor parties
        "ז": "Minor Party (ז)",
        "זך": "Action for Israel",
        "י": "Minor Party (י)",
        "יז": "Adom Lavan",
        "ינ": "Common Alliance",
        "יף": "Human Dignity",
        "יק": "Bible Bloc",
        "יר": "Social Leadership",
        "כ": "Jewish Heart",
        "כן": "Ani VeAtah",
        "נ": "Women's Voice",
        "נז": "Power to Influence",
        "ני": "Kama",
        "נק": "Minor Party (נק)",
        "ץ": "Da'am",
        "ףז": "Pirate Party",
        "ק": "Israelist",
        "קי": "Shema",
        "קך": "New Order",
        "קץ": "Mishpat Tzedek",
    }

    df_23 = _df.rename(columns=rename_map_23)
    df_23.to_csv("knesset_23_en.csv", index=False)
    df_23.head()
    return df_23, rename_map_23


@app.cell
def _(df_23):
    df_23.tail(15)
    return


@app.cell
def _(pd):
    _df = pd.read_csv("24th Knesset by City.csv", encoding="windows-1255")

    rename_map = {
          "סמל ועדה": "committee_code",
          "שם ישוב": "city_name",
          "סמל ישוב": "city_code",
          "בזב": "eligible_voters",
          "מצביעים": "votes_cast",
          "פסולים": "invalid_votes",
          "כשרים": "valid_votes",
          "אמת": "Labor",
          "ב": "Yamina",
          "ג": "UTJ",
          "ודעם": "Joint List",
          "ז": "The Israelis",
          "זץ": "Tzomet",
          "ט": "Religious Zionist",
          "י": "Social Bang",
          "יז": "New Economic Party",
          "ינ": "Common Alliance",
          "יף": "Human Dignity",
          "יק": "Bible Bloc",
          "יר": "Social Leadership",
          "כ": "Jewish Heart",
          "כך": "Me and You",
          "כן": "Blue and White",
          "ל": "Yisrael Beiteinu",
          "מחל": "Likud",
          "מרצ": "Meretz",
          "נ": "Kama",
          "ני": "New World",
          "נר": "Us",
          "עם": "United Arab List",
          "פה": "Yesh Atid",
          "ףז": "Pirate Party",
          "צי": "Atzmeinu",
          "צכ": "Ma'an",
          "צף": "Hetz",
          "ץ": "Da'am",
          "ק": "The Impossible",
          "קי": "Shama",
          "קך": "New Order",
          "קץ": "Mishpat Tzedek",
          "ר": "Rapeh",
          "רנ": "Hope for Change",
          "רף": "Am Shalem",
          "רק": "Democratic Party",
          "שס": "Shas",
          "ת": "New Hope",
    }

    df_24 = _df.rename(columns=rename_map)
    df_24.to_csv("knesset_24_en.csv", index=False)
    return df_24, rename_map


@app.cell
def _(df_24):
    df_24.tail(15)
    return


@app.cell
def _(pd):
    df_25 = pd.read_csv("25th Knesset by City.csv", encoding="utf-8-sig")

    rename_map_25 = {
          "סמל ועדה": "committee_code",
          "שם ישוב": "city_name",
          "סמל ישוב": "city_code",
          "בזב": "eligible_voters",
          "מצביעים": "votes_cast",
          "פסולים": "invalid_votes",
          "כשרים": "valid_votes",
          "אמת": "Labor",
          "אצ": "Economic Freedom",
          "ב": "Jewish Home",
          "ג": "UTJ",
          "ד": "Balad",
          "ום": "Hadash-Taal",
          "ז": "Social Power",
          "זך": "Human Dignity",
          "זנ": "Power to Influence",
          "זץ": "Tzomet",
          "ט": "Religious Zionism",
          "י": "Free Democratic Israel",
          "יז": "New Economic Party",
          "ינ": "Common Alliance",
          "יץ": "Taxi Emergency Order",
          "יק": "Bible Bloc",
          "כן": "National Unity",
          "ך": "Me and You",
          "ל": "Yisrael Beiteinu",
          "מחל": "Likud",
          "מרצ": "Meretz",
          "נז": "Human Dignity (new)",
          "ני": "Path Together",
          "נף": "Hear",
          "נץ": "New Independents",
          "נק": "Every Vote Counts",
          "נר": "We Together",
          "עם": "Raam",
          "פה": "Yesh Atid",
          "ף": "Pirate Party",
          "צ": "Young and Burning",
          "ץ": "Social Leadership",
          "ק": "Environmental Voice",
          "קי": "Jewish Heart",
          "קך": "New Order",
          "קנ": "Voice",
          "קץ": "Courage",
          "רז": "Thirty-Forty",
          "שס": "Shas",
          "ת": "Green Leaf",
      }

    df_25 = df_25.rename(columns=rename_map_25)
    df_25.to_csv("knesset_25_en.csv", index=False)
    df_25.head()
    return df_25, rename_map_25


@app.cell
def _(df_25):
    df_25.tail(15)
    return


if __name__ == "__main__":
    app.run()
