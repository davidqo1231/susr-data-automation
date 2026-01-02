import calendar
from pathlib import Path

import pandas as pd


DATA_URL = (
    "https://data.statistics.sk/api/v2/dataset/"
    "zo0001ms/2025%20(p),2024%20(d),2023%20(d),2022%20(d)/"
    "1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12./UKAZ02/MJ01?lang=en&type=csv"
)


def load_raw_data(url: str) -> pd.DataFrame:
    """
    Load raw CSV data from the Statistical Office API.

    The first 7 rows contain metadata and multi-row headers, so they are skipped.
    """
    df = pd.read_csv(url, skiprows=7, header=None)

    # Keep first 5 columns: year, month, indicator, measure, value
    df = df.iloc[:, :5]
    df.columns = ["year_raw", "month_raw", "indicator", "measure", "value"]
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw data into a table with months as rows and years as columns.
    """
    df = df.copy()

    # Extract numeric year from values like "2025 (p)"
    df["year"] = df["year_raw"].astype(str).str.extract(r"(\d{4})").astype(int)

    # Extract numeric month from values like "1.", "2.", ...
    df["month_num"] = df["month_raw"].astype(str).str.extract(r"(\d{1,2})").astype(int)

    # Ensure numeric values
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["year", "month_num", "value"])

    # Month names: jan, feb, mar, ...
    df["month"] = df["month_num"].apply(
        lambda m: calendar.month_abbr[m].lower() if 1 <= m <= 12 else None
    )
    df = df.dropna(subset=["month"])

    # Pivot to have months as rows, years as columns
    pivot = df.pivot_table(
        index="month",
        columns="year",
        values="value",
        aggfunc="first",
    )

    # Order months from jan to dec
    month_order = [calendar.month_abbr[i].lower() for i in range(1, 13)]
    pivot = pivot.reindex(month_order)

    # Order years ascending
    pivot = pivot.reindex(sorted(pivot.columns), axis=1)

    pivot = pivot.reset_index()
    return pivot


def main() -> None:
    raw = load_raw_data(DATA_URL)
    transformed = transform_data(raw)

    output_path = Path(__file__).with_name("foreign_trade_by_month.csv")
    transformed.to_csv(output_path, index=False)
    print(f"Uložené do súboru: {output_path.name}")


if __name__ == "__main__":
    main()
