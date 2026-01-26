from bs4 import BeautifulSoup


class ScreenerExtractor:
    """
    Extracts stock rows from Screener HTML.
    Supports paginated HTML separated by <!-- PAGE BREAK -->.
    """

    def extract(self, html: str) -> list[dict]:
        """
        Extract rows from one or more Screener result pages.

        Args:
            html: Combined HTML (possibly with PAGE BREAKs)

        Returns:
            List of row dictionaries
        """
        rows: list[dict] = []
        seen_companies: set[str] = set()

        pages = html.split("<!-- PAGE BREAK -->")

        for page_html in pages:
            soup = BeautifulSoup(page_html, "html.parser")

            table = soup.select_one("table.data-table")
            if not table:
                continue

            for tr in table.select("tbody tr"):
                cells = tr.find_all("td")
                if not cells:
                    continue

                company_tag = cells[1].find("a")
                if not company_tag:
                    continue

                company = company_tag.text.strip()

                # De-duplication across pages
                if company in seen_companies:
                    continue
                seen_companies.add(company)

                row = {"Company": company}

                for idx, td in enumerate(cells[2:], start=1):
                    row[f"col_{idx}"] = td.text.strip()

                rows.append(row)

        return rows
