const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const urlMatch = html.match(/SUPABASE_URL\s*=\s*'([^']+)'/);
const keyMatch = html.match(/SUPABASE_KEY\s*=\s*'([^']+)'/);

if (!urlMatch || !keyMatch) {
  console.log("Keys not found");
  process.exit(1);
}

const sb = createClient(urlMatch[1], keyMatch[1]);

async function check() {
  const { data, error } = await sb.from('todos').select('*');
  if (error) console.log("Error:", error);
  else {
    console.log("Total todos:", data.length);
    console.log("Done todos:", data.filter(d => d.done).length);
    console.log("Done todos users:", [...new Set(data.filter(d => d.done).map(d => d.user_id))]);
  }
}
check();
