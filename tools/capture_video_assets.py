from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tmp" / "video" / "captures"
OUT.mkdir(parents=True, exist_ok=True)
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def shot(page, name: str) -> None:
    page.wait_for_timeout(450)
    page.locator(".toast").evaluate_all("(items) => items.forEach((item) => item.remove())")
    page.screenshot(path=OUT / name, full_page=False)


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=str(EDGE))
        page = browser.new_page(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1,
        )
        page.goto("http://127.0.0.1:4173", wait_until="networkidle")
        page.wait_for_selector(".dashboard-view")
        shot(page, "dashboard.png")

        page.locator('[data-view="chat"]').first.click()
        page.locator(".welcome-prompt-grid button").first.click()
        page.wait_for_selector(".assistant-message:not(.pending-message)", timeout=15_000)
        page.wait_for_timeout(600)
        shot(page, "chat.png")

        page.locator('[data-view="workflow"]').first.click()
        page.wait_for_selector(".workflow-view")
        page.locator('[data-action="run-workflow"]').click()
        page.wait_for_timeout(6100)
        shot(page, "workflow.png")

        page.locator('[data-view="tasks"]').first.click()
        page.wait_for_selector(".tasks-view")
        shot(page, "tasks.png")

        page.locator('[data-view="knowledge"]').first.click()
        page.wait_for_selector(".knowledge-view")
        shot(page, "knowledge.png")

        page.locator('[data-view="tools"]').first.click()
        page.wait_for_selector(".tools-view")
        shot(page, "tools.png")

        page.locator('[data-view="runs"]').first.click()
        page.wait_for_selector(".runs-view")
        page.locator('[data-action="toggle-run"]').first.click()
        shot(page, "runs.png")

        page.set_viewport_size({"width": 390, "height": 844})
        page.goto("http://127.0.0.1:4173/#dashboard", wait_until="networkidle")
        page.wait_for_selector(".dashboard-view")
        page.wait_for_timeout(500)
        page.screenshot(path=OUT / "mobile.png", full_page=False)

        browser.close()
    print(OUT)


if __name__ == "__main__":
    main()
