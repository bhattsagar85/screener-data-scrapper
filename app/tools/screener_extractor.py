from bs4 import BeautifulSoup
import re

class ScreenerExtractor:
    """
    Extracts stock rows from Screener HTML.
    Supports paginated HTML separated by <!-- PAGE BREAK -->.
    """

    def extract(self, html: str) -> list[dict]:
        rows = []
        seen_symbols = set()

        pages = html.split("<!-- PAGE BREAK -->")

        for page_html in pages:
            soup = BeautifulSoup(page_html, "html.parser")
            table = soup.select_one("table.data-table")
            if not table:
                continue

            for tr in table.select("tbody tr"):
                tds = tr.find_all("td")
                if len(tds) < 3:
                    continue

                company_td = tds[1]
                a = company_td.find("a")
                if not a:
                    continue

                company = a.text.strip()
                href = a.get("href", "").strip()

                # 🔑 Extract symbol from URL
                # /company/COALINDIA/consolidated/
                match = re.search(r"/company/([^/]+)/", href)
                symbol = match.group(1) if match else None

                if not company or not symbol:
                    continue

                # Deduplicate
                if symbol in seen_symbols:
                    continue
                seen_symbols.add(symbol)

                row = {
                    "company": company,
                    "symbol": symbol,
                }

                # Map numeric columns safely
                for idx, td in enumerate(tds[2:], start=1):
                    row[f"col_{idx}"] = td.text.strip()

                rows.append(row)

        return rows
