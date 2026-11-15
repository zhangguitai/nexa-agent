import os
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "screenshots"
SCREENSHOTS.mkdir(exist_ok=True)
EDGE = Path(
    os.environ.get(
        "BROWSER_PATH",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    )
)


def main() -> None:
    errors: list[str] = []

    def prepare(page, path: Path, wait_ms: int = 380, full_page: bool = True) -> None:
        page.wait_for_timeout(wait_ms)
        page.locator(".toast").evaluate_all("(items) => items.forEach((item) => item.remove())")
        page.screenshot(path=path, full_page=full_page)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=str(EDGE) if EDGE.exists() else None,
        )
        page = browser.new_page(viewport={"width": 1440, "height": 960}, device_scale_factor=1)
        page.on("pageerror", lambda error: errors.append(f"pageerror: {error}"))
        page.on("console", lambda message: errors.append(f"console: {message.text}") if message.type == "error" else None)

        page.goto("http://127.0.0.1:4173", wait_until="networkidle")
        page.wait_for_selector(".dashboard-view")
        prepare(page, SCREENSHOTS / "01-dashboard.png")

        page.keyboard.press("Control+K")
        page.wait_for_selector("#commandOverlay:not([hidden])")
        page.locator("#commandInput").fill("知识库")
        page.wait_for_timeout(120)
        prepare(page, SCREENSHOTS / "11-command-palette.png", 180, False)
        page.keyboard.press("Escape")

        page.locator('[data-view="chat"]').first.click()
        page.wait_for_selector(".chat-view")
        page.locator(".welcome-prompt-grid button").first.click()
        page.wait_for_selector(".assistant-message:not(.pending-message)", timeout=15_000)
        prepare(page, SCREENSHOTS / "02-agent-chat.png", 800)
        page.locator("#chatComposerInput").fill("请把下周建议按执行优先级重新排序")
        page.locator(".send-button").click()
        page.wait_for_function("document.querySelectorAll('.assistant-message:not(.pending-message)').length >= 2", timeout=15_000)

        page.locator('[data-view="workflow"]').first.click()
        page.wait_for_selector(".workflow-view")
        prepare(page, SCREENSHOTS / "03-workflow-builder.png", 400)
        page.locator('[data-action="run-workflow"]').click()
        page.wait_for_timeout(6200)
        prepare(page, SCREENSHOTS / "04-workflow-complete.png")

        page.locator('[data-view="tasks"]').first.click()
        page.wait_for_selector(".tasks-view")
        prepare(page, SCREENSHOTS / "05-task-center.png")

        page.locator('[data-view="knowledge"]').first.click()
        page.wait_for_selector(".knowledge-view")
        prepare(page, SCREENSHOTS / "06-knowledge-base.png")
        before_upload = page.locator(".doc-row").count()
        page.locator("#knowledgeFile").set_input_files(
            {
                "name": "比赛演示知识.txt",
                "mimeType": "text/plain",
                "buffer": "NEXA Agent 知识库上传验收文件。".encode("utf-8"),
            }
        )
        page.wait_for_function(
            "(before) => document.querySelectorAll('.doc-row').length > before",
            arg=before_upload,
        )

        page.locator('[data-view="tools"]').first.click()
        page.wait_for_selector(".tools-view")
        page.locator('[data-action="toggle-tool"]').first.click()
        prepare(page, SCREENSHOTS / "07-tool-connections.png", 300)

        page.locator('[data-view="runs"]').first.click()
        page.wait_for_selector(".runs-view")
        page.locator('[data-action="toggle-run"]').first.click()
        prepare(page, SCREENSHOTS / "08-run-observability.png", 300)

        page.set_viewport_size({"width": 390, "height": 844})
        page.goto("http://127.0.0.1:4173/#dashboard", wait_until="networkidle")
        page.wait_for_selector(".dashboard-view")
        prepare(page, SCREENSHOTS / "09-mobile-dashboard.png")
        page.locator("#mobileMenu").click()
        prepare(page, SCREENSHOTS / "10-mobile-navigation.png", 250, False)

        body_width = page.evaluate("document.body.scrollWidth")
        viewport_width = page.evaluate("window.innerWidth")
        if body_width > viewport_width + 2:
            errors.append(f"horizontal overflow: body={body_width}, viewport={viewport_width}")

        browser.close()

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(f"Visual smoke test passed. Screenshots: {SCREENSHOTS}")


if __name__ == "__main__":
    main()
