"""Download foreign trade (export) data from the Statistical Office API.

This script fetches the CSV file with export data from the Statistical Office
of the Slovak Republic and stores it locally.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import urllib.request

DEFAULT_HEADERS = {"User-Agent": "susr-data-automation/1.0 (+https://data.statistics.sk/)"}

API_URL = (
    "https://data.statistics.sk/api/v2/dataset/zo0001ms/all/"
    "1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12./UKAZ02/MJ01?lang=en&type=csv"
)


def fetch_csv(url: str = API_URL, *, headers: dict[str, str] | None = None) -> str:
    """Retrieve CSV data from the provided API URL.

    Args:
        url: The API endpoint to download the CSV data from.
        headers: Optional HTTP headers to include in the request.

    Returns:
        The CSV content as a decoded UTF-8 string.
    """

    request = urllib.request.Request(url, headers=headers or DEFAULT_HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:  # type: ignore[arg-type]
        return response.read().decode("utf-8")


def save_csv(content: str, output_path: pathlib.Path) -> None:
    """Save CSV content to the provided path."""

    output_path.write_text(content, encoding="utf-8")


def download_foreign_trade_data(
    output_path: pathlib.Path,
    *,
    url: str = API_URL,
    headers: dict[str, str] | None = None,
) -> pathlib.Path:
    """Download export data and persist it to disk.

    Args:
        output_path: Destination path for the downloaded CSV file.
        url: API endpoint to download the CSV file from.
        headers: Optional HTTP headers to include in the request.

    Returns:
        The path to the saved CSV file.
    """

    csv_content = fetch_csv(url, headers=headers)
    save_csv(csv_content, output_path)
    return output_path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Download foreign trade export data as CSV.",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("foreign_trade_export.csv"),
        help="Path to save the downloaded CSV file (default: %(default)s)",
    )
    parser.add_argument(
        "--url",
        default=API_URL,
        help="API endpoint to download data from (default: official Statistical Office URL)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        destination = download_foreign_trade_data(args.output, url=args.url)
    except Exception as exc:  # pragma: no cover - runtime safeguard
        print(
            "Failed to download CSV data. Check network access or try a different URL via --url.",
            file=sys.stderr,
        )
        raise exc

    print(f"Saved foreign trade export data to {destination.resolve()}")


if __name__ == "__main__":
    main()
