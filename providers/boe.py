from playwright.sync_api import sync_playwright

def search(query):
    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            channel="chrome",
            headless=True
        )

        page = browser.new_page()

        for attempt in range(2):
            try:
                page.goto(
                    "https://www.boe.es/buscar/",
                    wait_until="domcontentloaded",
                    timeout=20000
                )
                break
            except Exception:
                if attempt == 1:
                    raise

        page.select_option("#bd", "boe")

        page.fill("#texto_a_buscar", query)

        page.locator("input[type='image']").click()

        page.wait_for_load_state("networkidle")

        links = page.locator("a.resultado-busqueda-link-defecto")

        for i in range(links.count()):

            link = links.nth(i)

            href = link.get_attribute("href")

            item = link.locator("xpath=ancestor::li")

            title = item.inner_text().strip()

            if not href:
                continue

            if "BOE-B-" not in href:
                continue

            boe_id = href.split("id=")[1]

            results.append({
                "id": boe_id,
                "title": title,
                "url": "https://www.boe.es/buscar/" + href.replace("../buscar/", "")
            })

        browser.close()

    return results

def contains_keywords(text, keywords):

    text = text.upper()

    return any(
        keyword.upper() in text
        for keyword in keywords
    )