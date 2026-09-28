import asyncio
import os
from playwright.async_api import async_playwright
import fitz

WORKSPACE = r"D:\Python\yangfu-application\01_master_profile"
html_path = os.path.join(WORKSPACE, "09_first_page_overview.html")
pdf_path = os.path.join(WORKSPACE, "09_first_page_overview.pdf")
png_path = os.path.join(WORKSPACE, "09_first_page_overview.png")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        file_url = f"file:///{html_path.replace(os.sep, '/')}"
        await page.goto(file_url, wait_until="networkidle")
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        await browser.close()
    
    doc = fitz.open(pdf_path)
    print(f"Generated PDF page count: {len(doc)}")
    pix = doc[0].get_pixmap(dpi=150)
    pix.save(png_path)
    print("Generated PNG successfully!")

if __name__ == "__main__":
    asyncio.run(main())
