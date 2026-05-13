const { createClient } = require('@supabase/supabase-js');
const SUPABASE_URL = 'https://qxqkpgkiuzdvkdieqynf.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4cWtwZ2tpdXpkdmtkaWVxeW5mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3MjI3OTAsImV4cCI6MjA5MDI5ODc5MH0.T6FT8YQKAPwIgPfKU1guaRx-izWvta7fM1nLMuzggZI';
const sb = createClient(SUPABASE_URL, SUPABASE_KEY);

async function run() {
  const { data, error } = await sb.from('todos').select('*').eq('done', true).order('completed_at', { ascending: false });
  console.log("todos count:", data?.length, "error:", error);
  const { data: pData, error: pError } = await sb.from('project_todos').select('*, projects!inner(name, category)').eq('done', true).order('completed_at', { ascending: false });
  console.log("project_todos count:", pData?.length, "error:", pError);
}
run();
