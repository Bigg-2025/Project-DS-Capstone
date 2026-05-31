import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from datetime import datetime

URL = "https://sampahnasional.kemenlh.go.id/#data-section"
OUTPUT_FILE = "data_sampah_nasional.xlsx"


async def scrape():
    all_data = []

    # Waktu scraping
    scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Membuka halaman...")
        await page.goto(URL, wait_until="networkidle", timeout=60000)

        # Tunggu tabel muncul
        await page.wait_for_selector("table", timeout=30000)
        try:
            select = page.locator("select").first
            await select.select_option(value="100")
            await page.wait_for_timeout(2000)
            print("Set 100 entri per halaman")
        except Exception as e:
            print(f"Tidak bisa ubah entri per halaman: {e}")

        headers = []
        header_cells = await page.locator("table thead th").all()

        for th in header_cells:
            headers.append((await th.inner_text()).strip())

        # Tambahkan header waktu scraping
        headers.append("waktu_scraping")

        print(f"Kolom: {headers}")

        page_num = 1

        while True:
            print(f"Scraping halaman {page_num}...")

            # Ambil semua baris tabel
            rows = await page.locator("table tbody tr").all()

            for row in rows:
                cells = await row.locator("td").all()

                row_data = []

                for cell in cells:
                    row_data.append((await cell.inner_text()).strip())

                if row_data:
                    # waktu scraping ke setiap baris
                    row_data.append(scrape_time)
                    all_data.append(row_data)

            # Cek tombol next
            next_btn = page.locator(
                "a:has-text('Selanjutnya'), a:has-text('Next'), li.next:not(.disabled) a"
            )

            count = await next_btn.count()

            if count == 0:
                print("Tidak ada tombol next, selesai.")
                break

            # Cek disabled
            is_disabled = await next_btn.first.get_attribute("class") or ""

            parent_class = ""
            try:
                parent_class = (
                    await next_btn.first.locator("..").get_attribute("class") or ""
                )
            except:
                pass

            if "disabled" in is_disabled or "disabled" in parent_class:
                print("Tombol next disabled, selesai.")
                break

            await next_btn.first.click()
            await page.wait_for_timeout(2000)

            page_num += 1

        await browser.close()

    # Simpan ke Excel 
    print(f"\nTotal baris terkumpul: {len(all_data)}")

    if all_data:
        if headers and len(headers) != len(all_data[0]):
            print(
                f"Warning: {len(headers)} header vs {len(all_data[0])} kolom data"
            )
            headers = headers[:len(all_data[0])]

        df = pd.DataFrame(all_data, columns=headers if headers else None)

        df.to_excel(OUTPUT_FILE, index=False)

        print(f"Data berhasil disimpan ke: {OUTPUT_FILE}")
        print(df.head())

    else:
        print("Tidak ada data yang berhasil diambil.")


if __name__ == "__main__":
    asyncio.run(scrape())