const { createClient } = require('@supabase/supabase-js');
const SUPABASE_URL = 'https://qxqkpgkiuzdvkdieqynf.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4cWtwZ2tpdXpkdmtkaWVxeW5mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3MjI3OTAsImV4cCI6MjA5MDI5ODc5MH0.T6FT8YQKAPwIgPfKU1guaRx-izWvta7fM1nLMuzggZI';
const sb = createClient(SUPABASE_URL, SUPABASE_KEY);

async function fix() {
  // 1. Get all todos with done=true and completed_at=null
  const { data: todos } = await sb.from('todos').select('*').eq('done', true).is('completed_at', null);
  console.log('Todos to fix:', todos?.length);
  if (todos && todos.length > 0) {
    for (const t of todos) {
      // Use log_date if possible, else created_at
      let fallback = t.log_date ? new Date(t.log_date).toISOString() : t.created_at;
      await sb.from('todos').update({ completed_at: fallback }).eq('id', t.id);
    }
  }

  // 2. Get all project_todos with done=true and completed_at=null
  const { data: pTodos } = await sb.from('project_todos').select('*').eq('done', true).is('completed_at', null);
  console.log('Project Todos to fix:', pTodos?.length);
  if (pTodos && pTodos.length > 0) {
    for (const t of pTodos) {
      await sb.from('project_todos').update({ completed_at: t.created_at }).eq('id', t.id);
    }
  }
  
  console.log('Fix complete.');
}
fix();
