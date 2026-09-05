import sys, asyncio, pathlib
from playwright.async_api import async_playwright
async def main(paths, out):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1240,"height":900})
        cells = "".join(f'<figure><img src="file://{pathlib.Path(x).resolve()}"><figcaption>{pathlib.Path(x).name}</figcaption></figure>' for x in paths)
        html = f'<html><body style="background:#f4efe6;margin:0;padding:10px;display:flex;flex-wrap:wrap;gap:8px;font-family:sans-serif">{cells}</body></html>'
        html = html.replace("<figure>", '<figure style="margin:0;width:auto;max-width:600px;text-align:center"><div style="border:1px solid #ccc;background:#f9f6ef">').replace("<figcaption>", "</div><figcaption>")
        open("/tmp/_sheet.html","w").write(html); await pg.goto("file:///tmp/_sheet.html"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=out, full_page=True)
        await b.close()
asyncio.run(main(sys.argv[2:], sys.argv[1]))
