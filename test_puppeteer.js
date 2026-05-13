const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  page.on('console', msg => {
    if (msg.type() === 'error' || msg.text().includes('완료 결과')) {
      console.log('BROWSER LOG:', msg.text());
    }
  });

  await page.goto('http://localhost:8080/?nocache=' + Date.now(), { waitUntil: 'networkidle0' });
  
  const result = await page.evaluate(async () => {
    // try calling executeHistorySearch manually
    await window.executeHistorySearch();
    return {
      todosRawCount: document.getElementById('hist-stat-todo').innerText,
      projRawCount: document.getElementById('hist-stat-proj').innerText,
    };
  });
  console.log('Result:', result);
  await browser.close();
})();
