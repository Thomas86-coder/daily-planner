const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('LOG:', msg.text()));
  page.on('pageerror', err => console.log('ERR:', err.toString()));

  await page.goto('file:///Users/jaehyun/인생관리시스템/index.html');
  
  // Wait a bit for initialization
  await new Promise(r => setTimeout(r, 1000));
  
  const results = await page.evaluate(async () => {
    document.getElementById('hist-period').value = 'today';
    document.getElementById('hist-type').value = 'all';
    document.getElementById('hist-cat').value = 'all';
    
    await window.executeHistorySearch();
    
    return {
      todosRawCount: document.getElementById('hist-stat-todo').innerText,
      projRawCount: document.getElementById('hist-stat-proj').innerText,
      totalCount: document.getElementById('hist-stat-total').innerText,
      errorDiv: document.querySelector('.rv-empty') ? document.querySelector('.rv-empty').innerText : null
    };
  });
  console.log('Results:', results);
  await browser.close();
})();
