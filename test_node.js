const { createClient } = require('@supabase/supabase-js');
const SUPABASE_URL = 'https://qxqkpgkiuzdvkdieqynf.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4cWtwZ2tpdXpkdmtkaWVxeW5mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3MjI3OTAsImV4cCI6MjA5MDI5ODc5MH0.T6FT8YQKAPwIgPfKU1guaRx-izWvta7fM1nLMuzggZI';
const sb = createClient(SUPABASE_URL, SUPABASE_KEY);

async function run() {
  const now = new Date();
  const offset = now.getTimezoneOffset() * 60000;
  const today = (new Date(now - offset)).toISOString().split('T')[0];
  
  let startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  let endDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 999);

  console.log('검색 조건:', { type: 'all', period: 'today', cat: 'all', today });

  let query = sb.from('todos')
    .select('id, text, done, completed_at, log_date, category')
    .eq('done', true);
  
  query = query.eq('log_date', today);
  query = query.order('completed_at', { ascending: false });

  const { data: todoData, error: todoError } = await query;
  console.log('todos 결과:', todoData, todoError);

  let ptQuery = sb.from('project_todos')
    .select('id, text, done, completed_at, projects(name, category)')
    .eq('done', true);
  
  ptQuery = ptQuery.gte('completed_at', startDate.toISOString());
  ptQuery = ptQuery.lte('completed_at', endDate.toISOString());
  ptQuery = ptQuery.order('completed_at', { ascending: false });

  const { data: ptData, error: ptError } = await ptQuery;
  console.log('project_todos 결과:', ptData, ptError);
}
run();
