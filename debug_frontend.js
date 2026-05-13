const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  page.on('console', msg => {
    console.log('BROWSER LOG:', msg.text());
  });

  page.on('pageerror', err => {
    console.log('BROWSER ERROR:', err.toString());
  });

  await page.goto('http://localhost:8080/?nocache=' + Date.now(), { waitUntil: 'networkidle2' });
  
  const results = await page.evaluate(async () => {
    document.getElementById('hist-period').value = 'today';
    await window.executeHistorySearch();
    return {
      todosRawCount: document.getElementById('hist-stat-todo').innerText,
      projRawCount: document.getElementById('hist-stat-proj').innerText,
      totalCount: document.getElementById('hist-stat-total').innerText,
      errorDiv: document.querySelector('.rv-empty') ? document.querySelector('.rv-empty').innerText : null
    };
  });
  console.log('Final DOM state:', results);
  
  await browser.close();
})();
