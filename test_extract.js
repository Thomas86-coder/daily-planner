const fs = require('fs');
const html = fs.readFileSync('/Users/jaehyun/인생관리시스템/index.html', 'utf-8');
const searchMatch = html.match(/async function executeHistorySearch\(\) \{([\s\S]*?)\}/);
console.log(searchMatch ? "Found executeHistorySearch" : "Not found");
