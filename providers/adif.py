# CURRENTLY NOT USED


from playwright.sync_api import sync_playwright


URL = "https://www.adifaltavelocidad.es/es/web/adif/empleo/oferta-empleo-publico/plazo-solicitud-abierto"

NO_PROCESS_TEXT = (
    "En estos momentos no hay ninguna oferta de empleo público."
)


def get_status():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto(
            URL,
        )

        html = page.content()

        text = page.locator("body").inner_text()

        browser.close()

        print(text)

    return {
        "has_open_process": NO_PROCESS_TEXT not in html
    }