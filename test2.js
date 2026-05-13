const { createClient } = require('@supabase/supabase-js');
// Mocking the call
async function test() {
  try {
    const sb = createClient('http://127.0.0.1:54321', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlZmF1bHQiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYxNDU1MTQ2MSwiZXhwIjoxOTMwMTI3NDYxfQ.something');
    const { data: { user } } = await sb.auth.getUser();
    console.log("Success:", user);
  } catch (e) {
    console.log("Crash:", e.message);
  }
}
test();
