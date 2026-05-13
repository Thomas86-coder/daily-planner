const fs = require('fs');
const html = fs.readFileSync('/Users/jaehyun/인생관리시스템/index.html', 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/g);
if (scriptMatch) {
  let code = scriptMatch[scriptMatch.length - 1].replace(/<\/?script>/g, '');
  try {
    // We can use acorn or similar to parse it, or just eval with dummy vars
    const acorn = require('acorn');
    acorn.parse(code, { ecmaVersion: 'latest' });
    console.log("Syntax is OK!");
  } catch(e) {
    console.log("Syntax error at", e.loc);
    console.log(code.substring(e.pos - 50, e.pos + 50));
  }
}
