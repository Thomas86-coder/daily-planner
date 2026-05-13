const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  const logs = [];
  page.on('console', msg => {
    logs.push(msg.text());
    console.log('BROWSER LOG:', msg.text());
  });

  await page.goto('http://localhost:8080/?nocache=' + Date.now(), { waitUntil: 'networkidle2' });
  
  await page.evaluate(async () => {
    // Navigate to history tab
    if(typeof showTab === 'function') showTab('history');
    
    // Select today
    const period = document.getElementById('hist-period');
    if (period) period.value = 'today';
    
    // Execute search
    await window.executeHistorySearch();
  });
  
  // wait for query to finish
  await new Promise(r => setTimeout(r, 2000));
  
  const stats = await page.evaluate(() => {
    return {
      todosRawCount: document.getElementById('hist-stat-todo')?.innerText,
      projRawCount: document.getElementById('hist-stat-proj')?.innerText,
      totalCount: document.getElementById('hist-stat-total')?.innerText,
    };
  });
  
  console.log('Final Stats:', stats);
  await browser.close();
})();
