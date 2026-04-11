const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://led-with-ai.vercel.app/index.html#/today', { waitUntil: 'networkidle' });
  
  await page.waitForTimeout(3000);
  
  const html = await page.evaluate(() => {
    const el = document.querySelector('#app') || document.body;
    return el.outerHTML;
  });
  
  const styles = await page.evaluate(() => {
    let result = '';
    for(const sheet of document.styleSheets) {
      try {
        for(const rule of sheet.cssRules) {
          result += rule.cssText + '\n';
        }
      } catch(e) {}
    }
    return result;
  });

  fs.writeFileSync('./reference_html.html', html);
  fs.writeFileSync('./reference_css.css', styles);
  
  await browser.close();
  console.log("Scraped successfully");
})();
