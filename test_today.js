const { createClient } = require('@supabase/supabase-js');
const SUPABASE_URL = 'https://qxqkpgkiuzdvkdieqynf.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4cWtwZ2tpdXpkdmtkaWVxeW5mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3MjI3OTAsImV4cCI6MjA5MDI5ODc5MH0.T6FT8YQKAPwIgPfKU1guaRx-izWvta7fM1nLMuzggZI';
const sb = createClient(SUPABASE_URL, SUPABASE_KEY);

async function run() {
  const now = new Date();
  const startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const endDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 999);
  
  console.log("startDate:", startDate.toISOString());
  console.log("endDate:", endDate.toISOString());

  let query = sb.from('todos').select('*').eq('done', true);
  query = query.gte('completed_at', startDate.toISOString());
  query = query.lte('completed_at', endDate.toISOString());
  
  const { data, error } = await query;
  console.log("Result:", data, error);
}
run();
