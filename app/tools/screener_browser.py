from pathlib import Path
import os
import time
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from dotenv import load_dotenv
from playwright.sync_api import (
    sync_playwright,
    Browser,
    Page,
    TimeoutError,
)

load_dotenv()


class ScreenerBrowser:
    """
    Stable Playwright automation for Screener.in

    FINAL BEHAVIOR:
    - Reuse session if available
    - Login only if required
    - Navigate to Explore page
    - Create new screen
    - Run query
    - Force 25 results per page
    - Detect total pages from UI
    - Paginate using URL (?page=N) — NOT Next button
    - Return combined HTML
    """

    BASE_URL = "https://www.screener.in"
    LOGIN_URL = "https://www.screener.in/login/"
    DASH_URL = "https://www.screener.in/dash/"
    EXPLORE_URL = "https://www.screener.in/explore/"

    def __init__(
        self,
        headless: bool = True,
        storage_state_path: str = ".screener_state.json",
        timeout: int = 30_000,
        safety_max_pages: int = 20,
    ):
        self.headless = headless
        self.storage_state_path = Path(storage_state_path)
        self.timeout = timeout
        self.safety_max_pages = safety_max_pages

        self.email = os.getenv("SCREENER_EMAIL")
        self.password = os.getenv("SCREENER_PASSWORD")

        if not self.email or not self.password:
            raise RuntimeError(
                "SCREENER_EMAIL and SCREENER_PASSWORD must be set in .env"
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_query(self, screener_query: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = self._create_context(browser)
            page = context.new_page()

            # 1️⃣ Auth
            self._ensure_logged_in(page)

            # 2️⃣ Navigate
            page.goto(self.EXPLORE_URL, timeout=self.timeout)
            self._open_create_new_screen(page)

            # 3️⃣ Run query
            self._submit_query(page, screener_query)

            # 4️⃣ Force pagination to be real
            self._set_results_per_page(page, per_page=25)

            # 5️⃣ Detect total pages
            detected_pages = self._detect_total_pages(page)
            total_pages = min(detected_pages, self.safety_max_pages)

            # 6️⃣ Collect pages by URL
            html = self._collect_pages_by_url(page, total_pages)

            context.close()
            browser.close()

            return html

    # ------------------------------------------------------------------
    # Context / Authentication
    # ------------------------------------------------------------------

    def _create_context(self, browser: Browser):
        if self.storage_state_path.exists():
            return browser.new_context(storage_state=self.storage_state_path)
        return browser.new_context()

    def _ensure_logged_in(self, page: Page):
        page.goto(self.DASH_URL, timeout=self.timeout)

        if "/login" in page.url:
            self._login(page)
            return

        if "/dash" in page.url:
            return

        if page.locator("a[href='/logout/']").count() > 0:
            return

        self._login(page)

    def _login(self, page: Page):
        page.goto(self.LOGIN_URL, timeout=self.timeout)

        if "/login" not in page.url:
            return

        page.wait_for_selector("input[name='username']", timeout=self.timeout)
        page.fill("input[name='username']", self.email)
        page.fill("input[name='password']", self.password)
        page.click("button[type='submit']")

        page.wait_for_url("**/dash/**", timeout=self.timeout)
        page.context.storage_state(path=self.storage_state_path)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _open_create_new_screen(self, page: Page):
        page.wait_for_selector(
            "a.button.button-primary[href='/screen/new/']",
            timeout=self.timeout,
        )
        page.click("a.button.button-primary[href='/screen/new/']")
        page.wait_for_selector("textarea[name='query']", timeout=self.timeout)

    # ------------------------------------------------------------------
    # Query Execution
    # ------------------------------------------------------------------

    def _submit_query(self, page: Page, query: str):
        page.fill("textarea[name='query']", query)
        page.click("button:has-text('Run this Query')")

        page.wait_for_load_state("networkidle", timeout=self.timeout)

        if page.locator("table.data-table").count() > 0:
            return

        if page.locator("text=No matching companies").count() > 0:
            return

        try:
            page.wait_for_selector("table.data-table", timeout=self.timeout)
        except TimeoutError:
            page.screenshot(path="screener_timeout.png")
            raise

    # ------------------------------------------------------------------
    # Pagination helpers
    # ------------------------------------------------------------------

    def _set_results_per_page(self, page: Page, per_page: int):
        """
        Try to force results-per-page (10 / 25 / 50).
        Safe no-op if Screener UI changes.
        """
        try:
            page.click(f"text={per_page}")
            page.wait_for_load_state("networkidle")
            time.sleep(0.3)
        except Exception:
            pass

    def _detect_total_pages(self, page: Page) -> int:
        try:
            page.wait_for_selector("div.sub[data-page-info]", timeout=self.timeout)
            text = page.locator("div.sub[data-page-info]").inner_text()
            match = re.search(r"page\s+\d+\s+of\s+(\d+)", text, re.I)
            return int(match.group(1)) if match else 1
        except TimeoutError:
            return 1

    def _collect_pages_by_url(self, page: Page, total_pages: int) -> str:
        all_pages_html: list[str] = []
        base_url = page.url

        for page_num in range(1, total_pages + 1):
            url = self._with_page_param(base_url, page_num)
            page.goto(url, timeout=self.timeout)
            page.wait_for_selector("table.data-table", timeout=self.timeout)
            page.wait_for_load_state("networkidle")

            all_pages_html.append(page.content())
            time.sleep(0.2)

        return "\n<!-- PAGE BREAK -->\n".join(all_pages_html)

    def _with_page_param(self, url: str, page_num: int) -> str:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        qs["page"] = [str(page_num)]
        new_query = urlencode(qs, doseq=True)
        return urlunparse(parsed._replace(query=new_query))
