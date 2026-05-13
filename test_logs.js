const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  page.on('console', async msg => {
    const args = await Promise.all(msg.args().map(arg => arg.jsonValue()));
    const text = args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' ');
    if (text.includes('===') || text.includes('필터:') || text.includes('날짜 범위:') || text.includes('결과:') || text.includes('컨테이너 찾음?')) {
      console.log(text);
    }
  });

  await page.goto('file:///Users/jaehyun/인생관리시스템/index.html', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 2000));
  await page.click('#nav-completed');
  await new Promise(r => setTimeout(r, 1000));
  await page.select('#ch-filter-period', 'week');
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const searchBtn = btns.find(b => b.textContent.includes('검색'));
    if (searchBtn) searchBtn.click();
  });
  await new Promise(r => setTimeout(r, 3000));
  await browser.close();
})();
