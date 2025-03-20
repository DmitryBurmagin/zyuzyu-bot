from playwright.async_api import async_playwright


async def parse_website(url, xpath):
    async with async_playwright() as p:
        try:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()

            await page.goto(url)

            await page.wait_for_selector(xpath)

            price_element = await page.query_selector(xpath)

            if price_element:
                price = await price_element.text_content()
                if price:
                    print(f"Цена: {price.strip()}")
                else:
                    print("Текст не найден в элементе.")
            else:
                print("Элемент с ценой не найден.")

        except Exception as e:
            print(f"Ошибка при обработке страницы: {e}")

        finally:
            await browser.close()
