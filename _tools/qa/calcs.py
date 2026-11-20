import asyncio, sys, json, re
from playwright.async_api import async_playwright
from pw import open_page
# használat: calcs.py <page> — a mini-kalkulátorok és a rétegzett kalkulátor (mintapélda-adatokkal) eredményei
page=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b,pg,errs=await open_page(p,1440,900,page)
        await pg.evaluate("setChapter('mintapeldak')"); await pg.wait_for_timeout(800)
        r=await pg.evaluate("[...document.querySelectorAll('.calc')].map(c=>[c.id,(c.querySelector('.verdict')||{}).innerText||'', [...c.querySelectorAll('.res-row')].map(x=>x.innerText.replace(/\\s+/g,' ')).filter(t=>/A′|R.?p|adh|súrl|fric/.test(t)).join(' | ')])")
        for x in r: print(x[0],'::',re.sub(r'\s+',' ',x[1]),'::',x[2][:150])
        ps=await pg.evaluate("Object.keys(KALK.PRESETS)")
        for k in ps:
            await pg.evaluate(f"openPreset('{k}')"); await pg.wait_for_timeout(500)
            t=await pg.evaluate("[...document.querySelectorAll('#k-tiles > *')].map(e=>e.innerText.replace(/\\s+/g,' ')).join(' ## ')")
            print('KALK',k,'::',t[:330])
        print('errors',errs); await b.close()
asyncio.run(main())
