import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix generateWeeklyAIReview
old_weekly_save = """    // Supabase에 저장
    const { data: { user } } = await sb.auth.getUser();
    if (user) {
      const weekKey = getISOWeekKey(weekStart);
      await sb.from('ai_reviews').upsert({
        user_id: user.id,
        type: 'weekly',
        period: weekKey,
        content: formatted
      }, { onConflict: 'user_id,type,period' });
    }"""

new_weekly_save = """    // Supabase에 저장
    const { data: sessionData } = await sb.auth.getSession();
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

if old_weekly_save in content:
    content = content.replace(old_weekly_save, new_weekly_save)

# 2. Fix loadWeeklyPage
old_weekly_load = """  const weekKey = getISOWeekKey(startStr);
  const { data: { user } } = await sb.auth.getUser();
  const [{ data: todoData }, { data: routineData }, { data: reflectData }, { data: routinesData }, { data: savedReview }] = await Promise.all([
    sb.from('todos').select('*').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('*').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('*').gte('log_date', startStr).lte('log_date', endStr).order('log_date', {ascending:false}),
    sb.from('routines').select('*').eq('year', currentYear).eq('month', currentMonth),
    user ? sb.from('ai_reviews').select('content').eq('user_id', user.id).eq('type', 'weekly').eq('period', weekKey).maybeSingle() : Promise.resolve({data:null})
  ]);"""

new_weekly_load = """  const weekKey = getISOWeekKey(startStr);
  const [{ data: todoData }, { data: routineData }, { data: reflectData }, { data: routinesData }, { data: savedReview }] = await Promise.all([
    sb.from('todos').select('*').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('*').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('*').gte('log_date', startStr).lte('log_date', endStr).order('log_date', {ascending:false}),
    sb.from('routines').select('*').eq('year', currentYear).eq('month', currentMonth),
    sb.from('ai_reviews').select('content').eq('type', 'weekly').eq('period', weekKey).maybeSingle()
  ]);"""

if old_weekly_load in content:
    content = content.replace(old_weekly_load, new_weekly_load)

# 3. Fix generateMonthlyAIReview
old_monthly_save = """    const { data: { user } } = await sb.auth.getUser();
    if (user) {
      const monthKey = getMonthKey(startStr);
      await sb.from('ai_reviews').upsert({
        user_id: user.id,
        type: 'monthly',
        period: monthKey,
        content: formatted
      }, { onConflict: 'user_id,type,period' });
    }"""

new_monthly_save = """    const { data: sessionData } = await sb.auth.getSession();
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

if old_monthly_save in content:
    content = content.replace(old_monthly_save, new_monthly_save)

# 4. Fix loadMonthlyPage
old_monthly_load = """  const monthKey = getMonthKey(startStr);
  const { data: { user } } = await sb.auth.getUser();
  const [{ data: todoData }, { data: routineData }, { data: reflectData }, { data: savedReview }] = await Promise.all([
    sb.from('todos').select('log_date,category,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('log_date,routine_id,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('log_date').gte('log_date', startStr).lte('log_date', endStr),
    user ? sb.from('ai_reviews').select('content').eq('user_id', user.id).eq('type', 'monthly').eq('period', monthKey).maybeSingle() : Promise.resolve({data:null})
  ]);"""

new_monthly_load = """  const monthKey = getMonthKey(startStr);
  const [{ data: todoData }, { data: routineData }, { data: reflectData }, { data: savedReview }] = await Promise.all([
    sb.from('todos').select('log_date,category,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('log_date,routine_id,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('log_date').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('ai_reviews').select('content').eq('type', 'monthly').eq('period', monthKey).maybeSingle()
  ]);"""

if old_monthly_load in content:
    content = content.replace(old_monthly_load, new_monthly_load)

# 5. Fix generateYearlyAIReview
old_yearly_save = """    const { data: { user } } = await sb.auth.getUser();
    if (user) {
      const yearKey = getYearKey(startStr);
      await sb.from('ai_reviews').upsert({
        user_id: user.id,
        type: 'yearly',
        period: yearKey,
        content: formatted
      }, { onConflict: 'user_id,type,period' });
    }"""

new_yearly_save = """    const { data: sessionData } = await sb.auth.getSession();
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

if old_yearly_save in content:
    content = content.replace(old_yearly_save, new_yearly_save)

# 6. Fix loadYearlyPage
old_yearly_load = """  const yearKey = getYearKey(startStr);
  const { data: { user } } = await sb.auth.getUser();
  const [{ data: todoData }, { data: routineData }, { data: reflectData }, { data: savedReview }] = await Promise.all([
    sb.from('todos').select('log_date,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('log_date,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('log_date').gte('log_date', startStr).lte('log_date', endStr),
    user ? sb.from('ai_reviews').select('content').eq('user_id', user.id).eq('type', 'yearly').eq('period', yearKey).maybeSingle() : Promise.resolve({data:null})
  ]);"""

new_yearly_load = """  const yearKey = getYearKey(startStr);
  const [{ data: todoData }, { data: routineData }, { data: reflectData }, { data: savedReview }] = await Promise.all([
    sb.from('todos').select('log_date,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('log_date,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('log_date').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('ai_reviews').select('content').eq('type', 'yearly').eq('period', yearKey).maybeSingle()
  ]);"""

if old_yearly_load in content:
    content = content.replace(old_yearly_load, new_yearly_load)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done fixing ai_reviews bugs")
