from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

URL = 'https://maharera.maharashtra.gov.in/'


def run():
    try:
        with sync_playwright() as p:
            with p.chromium.launch(headless=True) as browser:
                context = browser.new_context()
                page = context.new_page()
                print(f'Navigating to: {URL}')
                page.goto(URL, timeout=60000)
                title = page.title()
                print(f'Page title: {title}')

    except PlaywrightTimeoutError as te:
        print(f'ERROR: Page navigation timeout: {te}')
        raise
    except Exception as exc:
        print(f'ERROR: Unexpected failure: {exc}')
        raise


if __name__ == '__main__':
    run()
