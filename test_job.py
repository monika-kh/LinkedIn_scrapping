import asyncio
from bs4 import BeautifulSoup
import logging
from playwright.async_api import async_playwright
import sys
import csv

logger = logging.getLogger(__name__)

async def linked_login(page):
    """
    Login to LinkedIn using the provided credentials.
    """
    logger.info("Login In")
    button_element = await page.wait_for_selector(".authwall-join-form__form-toggle--bottom")
    await button_element.click()

    # Fill email
    element_id = "session_key"
    element = await page.wait_for_selector(f"#{element_id}")
    value = "hajaseb669@devswp.com"
    await element.fill(value)

    # Fill password
    element_id = "session_password"
    element = await page.wait_for_selector(f"#{element_id}")
    value = "Justchill@230193"
    await element.fill(value)

    # Sign In
    submit_button = ".sign-in-form__submit-btn--full-width"
    sub = await page.wait_for_selector(submit_button)
    await sub.click()
    logger.info("Logged In")


async def get_linkedin_url(company_name):
    """
    Get the LinkedIn URL of the company from Google search.
    """
    search_url = f"https://www.google.com/search?q={company_name}+site:linkedin.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()

        page = await context.new_page()
        await page.set_extra_http_headers(headers)

        await page.goto(search_url)

        await page.wait_for_load_state("networkidle")

        content = await page.content()

    soup = BeautifulSoup(content, "html.parser")
    search_results = soup.select(".yuRUbf > a")
    for result in search_results:
        href = result.get("href")
        if "linkedin.com/company/" in href:
            linkedin_url = href.replace("/url?q=", "").split("&")[0]
            return linkedin_url

    return None


async def main():
    csv_file_path = sys.argv[1]  # CSV file path passed as command-line argument
    with open(csv_file_path, "r+", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames + ["Employee"]
        data = []
        for row in reader:
            print(row["Company"])
            try:
                linkedin_url = await get_linkedin_url(row["Company"])

                if linkedin_url:
                    print("LinkedIn URL:", linkedin_url)
                    async with async_playwright() as playwright:
                        browser = await playwright.chromium.launch(headless=False)
                        context = await browser.new_context()
                        # Open new page
                        page = await context.new_page()
                        await page.goto(linkedin_url)
                        await linked_login(page)
                        await page.goto(linkedin_url)
                        employee_count_element = await page.wait_for_selector(
                            ".org-top-card-summary-info-list__info-item:last-child"
                        )
                        employee_count = await employee_count_element.inner_text()
                        print(employee_count)
                        if employee_count:
                            row["Employee"] = employee_count.split(" ")[0]
                        else:
                            row["Employee"] = "Not Found"
                        data.append(row)
                        await context.close()
                        await browser.close()
                else:
                    logger.error("LinkedIn URL not found.")
                    row["Employee"] = "Not Found"
                    data.append(row)
            except Exception as e:
                logger.error(str(e))
                row["Employee"] = "Error"
                data.append(row)
        csvfile.seek(0)  # Move the file pointer to the beginning of the file

        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    asyncio.run(main())
