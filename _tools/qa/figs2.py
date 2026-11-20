import asyncio, sys, os
from playwright.async_api import async_playwright
from pw import open_page
# használat: figs2.py <page> <outdir> <width> <dpr> [indexek…]  — a „figure > svg” ábrák képe
page,out,w,dpr=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]); only=[int(x) for x in sys.argv[5:]]
os.makedirs(out,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b,pg,errs=await open_page(p,w,900,page,dpr)
        n=await pg.evaluate("document.querySelectorAll('figure svg').length")
        for i in range(n):
            if only and i not in only: continue
            ch=await pg.evaluate(f"(()=>{{const e=document.querySelectorAll('figure svg')[{i}]; return e.closest('.chapter-page').dataset.ch}})()")
            await pg.evaluate(f"setChapter('{ch}')"); await pg.wait_for_timeout(250)
            h=await pg.evaluate_handle(f"document.querySelectorAll('figure svg')[{i}]")
            el=h.as_element(); await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
            await el.screenshot(path=f'{out}/fig{i:02d}.png')
        print(n,'errors',errs); await b.close()
asyncio.run(main())
