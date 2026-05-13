import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The SQL to output
sql_to_log = """CREATE TABLE ai_reviews (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  type TEXT NOT NULL,
  period TEXT NOT NULL,
  content TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(type, period)
);"""

# Replace Weekly Save
old_weekly_save = """    const { data: sessionData } = await sb.auth.getSession();
    const user = sessionData?.session?.user;
    if (user) {
      const weekKey = getISOWeekKey(weekStart);
      const { data: existing } = await sb.from('ai_reviews').select('id').eq('type', 'weekly').eq('period', weekKey).maybeSingle();
      if (existing) {
        const { error } = await sb.from('ai_reviews').update({ content: formatted }).eq('id', existing.id);
        if (error) console.error("Weekly AI Update Error:", error);
      } else {
        const { error } = await sb.from('ai_reviews').insert({ user_id: user.id, type: 'weekly', period: weekKey, content: formatted });
        if (error) console.error("Weekly AI Insert Error:", error);
      }
    }"""

new_weekly_save = f"""    const weekKey = getISOWeekKey(weekStart);
    const {{ data: existing, error: selErr }} = await sb.from('ai_reviews').select('id').eq('type', 'weekly').eq('period', weekKey).maybeSingle();
    
    if (selErr && selErr.code === 'PGRST205') {{
      console.error("ai_reviews 테이블이 없습니다. 아래 SQL을 Supabase에서 실행해주세요:\\n" + `{sql_to_log}`);
      alert("ai_reviews 테이블이 없습니다. 브라우저 콘솔을 확인해 SQL을 실행해주세요.");
      return;
    }}

    if (existing) {{
      const {{ error }} = await sb.from('ai_reviews').update({{ content: formatted }}).eq('id', existing.id);
      if (error) console.error("Weekly AI Update Error:", error);
    }} else {{
      const {{ error }} = await sb.from('ai_reviews').insert({{ type: 'weekly', period: weekKey, content: formatted }});
      if (error) console.error("Weekly AI Insert Error:", error);
    }}"""

content = content.replace(old_weekly_save, new_weekly_save)

# Replace Monthly Save
old_monthly_save = """    const { data: sessionData } = await sb.auth.getSession();
    const user = sessionData?.session?.user;
    if (user) {
      const monthKey = getMonthKey(startStr);
      const { data: existing } = await sb.from('ai_reviews').select('id').eq('type', 'monthly').eq('period', monthKey).maybeSingle();
      if (existing) {
        const { error } = await sb.from('ai_reviews').update({ content: formatted }).eq('id', existing.id);
        if (error) console.error("Monthly AI Update Error:", error);
      } else {
        const { error } = await sb.from('ai_reviews').insert({ user_id: user.id, type: 'monthly', period: monthKey, content: formatted });
        if (error) console.error("Monthly AI Insert Error:", error);
      }
    }"""

new_monthly_save = f"""    const monthKey = getMonthKey(startStr);
    const {{ data: existing, error: selErr }} = await sb.from('ai_reviews').select('id').eq('type', 'monthly').eq('period', monthKey).maybeSingle();
    
    if (selErr && selErr.code === 'PGRST205') {{
      console.error("ai_reviews 테이블이 없습니다. 아래 SQL을 Supabase에서 실행해주세요:\\n" + `{sql_to_log}`);
      alert("ai_reviews 테이블이 없습니다. 브라우저 콘솔을 확인해 SQL을 실행해주세요.");
      return;
    }}

    if (existing) {{
      const {{ error }} = await sb.from('ai_reviews').update({{ content: formatted }}).eq('id', existing.id);
      if (error) console.error("Monthly AI Update Error:", error);
    }} else {{
      const {{ error }} = await sb.from('ai_reviews').insert({{ type: 'monthly', period: monthKey, content: formatted }});
      if (error) console.error("Monthly AI Insert Error:", error);
    }}"""

content = content.replace(old_monthly_save, new_monthly_save)


# Replace Yearly Save
old_yearly_save = """    const { data: sessionData } = await sb.auth.getSession();
    const user = sessionData?.session?.user;
    if (user) {
      const yearKey = getYearKey(startStr);
      const { data: existing } = await sb.from('ai_reviews').select('id').eq('type', 'yearly').eq('period', yearKey).maybeSingle();
      if (existing) {
        const { error } = await sb.from('ai_reviews').update({ content: formatted }).eq('id', existing.id);
        if (error) console.error("Yearly AI Update Error:", error);
      } else {
        const { error } = await sb.from('ai_reviews').insert({ user_id: user.id, type: 'yearly', period: yearKey, content: formatted });
        if (error) console.error("Yearly AI Insert Error:", error);
      }
    }"""

new_yearly_save = f"""    const yearKey = getYearKey(startStr);
    const {{ data: existing, error: selErr }} = await sb.from('ai_reviews').select('id').eq('type', 'yearly').eq('period', yearKey).maybeSingle();
    
    if (selErr && selErr.code === 'PGRST205') {{
      console.error("ai_reviews 테이블이 없습니다. 아래 SQL을 Supabase에서 실행해주세요:\\n" + `{sql_to_log}`);
      alert("ai_reviews 테이블이 없습니다. 브라우저 콘솔을 확인해 SQL을 실행해주세요.");
      return;
    }}

    if (existing) {{
      const {{ error }} = await sb.from('ai_reviews').update({{ content: formatted }}).eq('id', existing.id);
      if (error) console.error("Yearly AI Update Error:", error);
    }} else {{
      const {{ error }} = await sb.from('ai_reviews').insert({{ type: 'yearly', period: yearKey, content: formatted }});
      if (error) console.error("Yearly AI Insert Error:", error);
    }}"""

content = content.replace(old_yearly_save, new_yearly_save)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished fixing ai_reviews auth/RLS bug.")
