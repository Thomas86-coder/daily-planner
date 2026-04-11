const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('LOG:', msg.text()));
  page.on('pageerror', err => console.log('ERROR:', err.message));

  await page.goto('file:///Users/jaehyun/인생관리시스템/index.html');
  await page.waitForTimeout(500); // let flatpickr init

  console.log('Testing date display click...');
  try {
    const error = await page.evaluate(() => {
      try {
        const el = document.querySelector('.center-date-text');
        el.click();
        return null;
      } catch (e) {
        return e.message;
      }
    });
    if (error) console.log('EVAL ERROR:', error);
    
    // Check if flatpickr instance exists
    const hasInstance = await page.evaluate(() => !!document.getElementById('dateInputH')._flatpickr);
    console.log('Has Flatpickr Instance:', hasInstance);
  } catch(e) {
    console.log('Exception:', e);
  }

  await page.waitForTimeout(500);
  await browser.close();
})();
