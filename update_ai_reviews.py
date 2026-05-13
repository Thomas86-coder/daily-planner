import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 헬퍼 함수 추가
helpers = """
// ── AI 리뷰 키 생성 헬퍼 ──
function getISOWeekKey(dateStr) {
  const d = new Date(dateStr);
  d.setHours(0, 0, 0, 0);
  d.setDate(d.getDate() + 3 - (d.getDay() + 6) % 7);
  const week1 = new Date(d.getFullYear(), 0, 4);
  const weekNumber = 1 + Math.round(((d.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
  return `${d.getFullYear()}-${String(weekNumber).padStart(2, '0')}`;
}
function getMonthKey(dateStr) {
  return dateStr.substring(0, 7); // YYYY-MM
}
function getYearKey(dateStr) {
  return dateStr.substring(0, 4); // YYYY
}
"""
if "function getISOWeekKey" not in content:
    content = content.replace("async function generateWeeklyAIReview", helpers + "\nasync function generateWeeklyAIReview")

# 2. generateWeeklyAIReview 수정
old_success = """    resultArea.innerHTML = `
      <div style="line-height:1.9;font-size:15px;color:#333;padding:8px 0;">
        ${formatted}
      </div>
    `;
    btn.style.display = 'none';"""

new_success = """    resultArea.innerHTML = `
      <div style="line-height:1.9;font-size:15px;color:#333;padding:8px 0;">
        ${formatted}
      </div>
    `;
    btn.innerHTML = '🔄 다시 생성하기';
    btn.disabled = false;

    // Supabase에 저장
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

if old_success in content:
    content = content.replace(old_success, new_success)


# 3. loadWeeklyPage 수정
old_weekly_query = """  const [{ data: todoData }, { data: routineData }, { data: reflectData }, { data: routinesData }] = await Promise.all([
    sb.from('todos').select('*').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('*').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('*').gte('log_date', startStr).lte('log_date', endStr).order('log_date', {ascending:false}),
    sb.from('routines').select('*').eq('year', currentYear).eq('month', currentMonth)
  ]);"""
new_weekly_query = """  const weekKey = getISOWeekKey(startStr);
  const { data: { user } } = await sb.auth.getUser();
  const [{ data: todoData }, { data: routineData }, { data: reflectData }, { data: routinesData }, { data: savedReview }] = await Promise.all([
    sb.from('todos').select('*').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('*').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('*').gte('log_date', startStr).lte('log_date', endStr).order('log_date', {ascending:false}),
    sb.from('routines').select('*').eq('year', currentYear).eq('month', currentMonth),
    user ? sb.from('ai_reviews').select('content').eq('user_id', user.id).eq('type', 'weekly').eq('period', weekKey).maybeSingle() : Promise.resolve({data:null})
  ]);"""

if old_weekly_query in content:
    content = content.replace(old_weekly_query, new_weekly_query)

old_weekly_html = """    <div id="weekly-ai-result" style="margin-bottom:20px;">
      <div style="text-align:center; padding:20px;">
        <div style="font-size:40px; margin-bottom:12px;">✨</div>
        <div style="font-size:16px; font-weight:bold; color:#374151; margin-bottom:6px;">AI 주간 성찰이 아직 없습니다</div>
        <div style="font-size:13px; color:#6B7280;">이번 주의 활동을 분석하여 맞춤형 피드백을 제공합니다.</div>
      </div>
    </div>

    <button id="weekly-ai-btn" class="ai-review-btn" onclick="generateWeeklyAIReview('${startStr}', '${endStr}')" style="width:100%; background:#8B5CF6; color:white; border:none; padding:14px; border-radius:12px; font-weight:bold; cursor:pointer;">
      ✦ AI 성찰 생성하기
    </button>"""

new_weekly_html = """    <div id="weekly-ai-result" style="margin-bottom:20px;">
      ${savedReview ? `
        <div style="line-height:1.9;font-size:15px;color:#333;padding:8px 0;">
          ${savedReview.content}
        </div>
      ` : `
        <div style="text-align:center; padding:20px;">
          <div style="font-size:40px; margin-bottom:12px;">✨</div>
          <div style="font-size:16px; font-weight:bold; color:#374151; margin-bottom:6px;">AI 주간 성찰이 아직 없습니다</div>
          <div style="font-size:13px; color:#6B7280;">이번 주의 활동을 분석하여 맞춤형 피드백을 제공합니다.</div>
        </div>
      `}
    </div>

    <button id="weekly-ai-btn" class="ai-review-btn" onclick="generateWeeklyAIReview('${startStr}', '${endStr}')" style="width:100%; background:#8B5CF6; color:white; border:none; padding:14px; border-radius:12px; font-weight:bold; cursor:pointer;">
      ${savedReview ? '🔄 다시 생성하기' : '✦ AI 성찰 생성하기'}
    </button>"""

if old_weekly_html in content:
    content = content.replace(old_weekly_html, new_weekly_html)


# 4. loadMonthlyPage 수정
old_monthly_query = """  const [{ data: todoData }, { data: routineData }, { data: reflectData }] = await Promise.all([
    sb.from('todos').select('log_date,category,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('log_date,routine_id,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('log_date').gte('log_date', startStr).lte('log_date', endStr)
  ]);"""
new_monthly_query = """  const monthKey = getMonthKey(startStr);
  const { data: { user } } = await sb.auth.getUser();
  const [{ data: todoData }, { data: routineData }, { data: reflectData }, { data: savedReview }] = await Promise.all([
    sb.from('todos').select('log_date,category,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('log_date,routine_id,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('log_date').gte('log_date', startStr).lte('log_date', endStr),
    user ? sb.from('ai_reviews').select('content').eq('user_id', user.id).eq('type', 'monthly').eq('period', monthKey).maybeSingle() : Promise.resolve({data:null})
  ]);"""

if old_monthly_query in content:
    content = content.replace(old_monthly_query, new_monthly_query)

old_monthly_html = """    <div id="monthly-ai-result" style="margin-bottom:20px;">
      <div style="text-align:center; padding:20px;">
        <div style="font-size:40px; margin-bottom:12px;">✨</div>
        <div style="font-size:16px; font-weight:bold; color:#374151; margin-bottom:6px;">AI 월간 성찰이 아직 없습니다</div>
        <div style="font-size:13px; color:#6B7280;">이번 달의 활동을 분석하여 맞춤형 피드백을 제공합니다.</div>
      </div>
    </div>

    <button id="monthly-ai-btn" class="ai-review-btn" onclick="generateMonthlyAIReview('${startStr}', '${endStr}')" style="width:100%; background:#8B5CF6; color:white; border:none; padding:14px; border-radius:12px; font-weight:bold; cursor:pointer;">
      ✦ AI 성찰 생성하기
    </button>"""

new_monthly_html = """    <div id="monthly-ai-result" style="margin-bottom:20px;">
      ${savedReview ? `
        <div style="line-height:1.9;font-size:15px;color:#333;padding:8px 0;">
          ${savedReview.content}
        </div>
      ` : `
        <div style="text-align:center; padding:20px;">
          <div style="font-size:40px; margin-bottom:12px;">✨</div>
          <div style="font-size:16px; font-weight:bold; color:#374151; margin-bottom:6px;">AI 월간 성찰이 아직 없습니다</div>
          <div style="font-size:13px; color:#6B7280;">이번 달의 활동을 분석하여 맞춤형 피드백을 제공합니다.</div>
        </div>
      `}
    </div>

    <button id="monthly-ai-btn" class="ai-review-btn" onclick="generateMonthlyAIReview('${startStr}', '${endStr}')" style="width:100%; background:#8B5CF6; color:white; border:none; padding:14px; border-radius:12px; font-weight:bold; cursor:pointer;">
      ${savedReview ? '🔄 다시 생성하기' : '✦ AI 성찰 생성하기'}
    </button>"""

if old_monthly_html in content:
    content = content.replace(old_monthly_html, new_monthly_html)

# 5. loadYearlyPage 수정
old_yearly_query = """  const [{ data: todoData }, { data: routineData }, { data: reflectData }] = await Promise.all([
    sb.from('todos').select('log_date,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('log_date,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('log_date').gte('log_date', startStr).lte('log_date', endStr)
  ]);"""
new_yearly_query = """  const yearKey = getYearKey(startStr);
  const { data: { user } } = await sb.auth.getUser();
  const [{ data: todoData }, { data: routineData }, { data: reflectData }, { data: savedReview }] = await Promise.all([
    sb.from('todos').select('log_date,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('routine_logs').select('log_date,done').gte('log_date', startStr).lte('log_date', endStr),
    sb.from('reflections').select('log_date').gte('log_date', startStr).lte('log_date', endStr),
    user ? sb.from('ai_reviews').select('content').eq('user_id', user.id).eq('type', 'yearly').eq('period', yearKey).maybeSingle() : Promise.resolve({data:null})
  ]);"""

if old_yearly_query in content:
    content = content.replace(old_yearly_query, new_yearly_query)

old_yearly_html = """    <div id="yearly-ai-result" style="margin-bottom:20px;">
      <div style="text-align:center; padding:20px;">
        <div style="font-size:40px; margin-bottom:12px;">✨</div>
        <div style="font-size:16px; font-weight:bold; color:#374151; margin-bottom:6px;">AI 연간 성찰이 아직 없습니다</div>
        <div style="font-size:13px; color:#6B7280;">올 한 해의 활동을 분석하여 맞춤형 피드백을 제공합니다.</div>
      </div>
    </div>

    <button id="yearly-ai-btn" class="ai-review-btn" onclick="generateYearlyAIReview('${startStr}', '${endStr}')" style="width:100%; background:#8B5CF6; color:white; border:none; padding:14px; border-radius:12px; font-weight:bold; cursor:pointer;">
      ✦ AI 성찰 생성하기
    </button>"""

new_yearly_html = """    <div id="yearly-ai-result" style="margin-bottom:20px;">
      ${savedReview ? `
        <div style="line-height:1.9;font-size:15px;color:#333;padding:8px 0;">
          ${savedReview.content}
        </div>
      ` : `
        <div style="text-align:center; padding:20px;">
          <div style="font-size:40px; margin-bottom:12px;">✨</div>
          <div style="font-size:16px; font-weight:bold; color:#374151; margin-bottom:6px;">AI 연간 성찰이 아직 없습니다</div>
          <div style="font-size:13px; color:#6B7280;">올 한 해의 활동을 분석하여 맞춤형 피드백을 제공합니다.</div>
        </div>
      `}
    </div>

    <button id="yearly-ai-btn" class="ai-review-btn" onclick="generateYearlyAIReview('${startStr}', '${endStr}')" style="width:100%; background:#8B5CF6; color:white; border:none; padding:14px; border-radius:12px; font-weight:bold; cursor:pointer;">
      ${savedReview ? '🔄 다시 생성하기' : '✦ AI 성찰 생성하기'}
    </button>"""

if old_yearly_html in content:
    content = content.replace(old_yearly_html, new_yearly_html)


# 6. generateMonthlyAIReview 및 generateYearlyAIReview 구현 함수 추가
new_functions = """
// ── AI 월간 성찰 생성 ──
async function generateMonthlyAIReview(startStr, endStr) {
  const btn = document.getElementById('monthly-ai-btn');
  const resultArea = document.getElementById('monthly-ai-result');
  
  btn.disabled = true;
  btn.innerHTML = '⏳ 분석 중...';

  try {
    const [{ data: todos }, { data: logs }, { data: reflects }] = await Promise.all([
      sb.from('todos').select('done').gte('log_date', startStr).lte('log_date', endStr),
      sb.from('routine_logs').select('done').gte('log_date', startStr).lte('log_date', endStr),
      sb.from('reflections').select('log_date').gte('log_date', startStr).lte('log_date', endStr)
    ]);

    const totalTasks = todos?.length || 0;
    const totalDone = todos?.filter(t => t.done).length || 0;
    const routineTotal = logs?.length || 0;
    const routineDone = logs?.filter(l => l.done).length || 0;
    const routineRate = routineTotal > 0 ? Math.round(routineDone / routineTotal * 100) : 0;
    const reflectDays = reflects?.length || 0;

    const [yyyy, mm] = startStr.split('-');
    const userMessage = `당신은 따뜻하고 통찰력 있는 인생 코치입니다.
아래는 사용자의 ${yyyy}년 ${mm}월 활동 데이터입니다.

[할일 완료 현황]
- 할일 총 완료: ${totalDone}/${totalTasks}개

[루틴 달성 현황]
- 루틴 달성률: ${routineRate}%

[성찰 기록]
- 성찰 작성일: ${reflectDays}일

위 데이터를 바탕으로 이번 달 총평을 아래 형식으로 작성해주세요:
1. 📊 이번 달 성과 요약 (핵심을 한 문장으로)
2. ✅ 잘한 점 (데이터 기반 2가지)
3. 💡 아쉬운 점 (따뜻한 조언 2가지)
4. 🎯 다음 달 개선 제안 (구체적인 제안 2가지)
5. 💬 응원 한마디 (진심 어린 격려)

전체 분량은 300~500자 정도로, 마크다운 굵은 글씨(**텍스트**)를 활용해 가독성 좋게 작성해주세요.`;

    const response = await fetch(
      'https://qxqkpgkiuzdvkdieqynf.supabase.co/functions/v1/ai-analysis',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4cWtwZ2tpdXpkdmtkaWVxeW5mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3MjI3OTAsImV4cCI6MjA5MDI5ODc5MH0.T6FT8YQKAPwIgPfKU1guaRx-izWvta7fM1nLMuzggZI'
        },
        body: JSON.stringify({ userMessage })
      }
    );

    const data = await response.json();
    const text = data.result || data.message || data.content || data.text || data.response || JSON.stringify(data);

    const formatted = text
      .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
      .replace(/\\n/g, '<br>');

    resultArea.innerHTML = `
      <div style="line-height:1.9;font-size:15px;color:#333;padding:8px 0;">
        ${formatted}
      </div>
    `;
    btn.innerHTML = '🔄 다시 생성하기';
    btn.disabled = false;

    const { data: { user } } = await sb.auth.getUser();
    if (user) {
      const monthKey = getMonthKey(startStr);
      await sb.from('ai_reviews').upsert({
        user_id: user.id,
        type: 'monthly',
        period: monthKey,
        content: formatted
      }, { onConflict: 'user_id,type,period' });
    }

  } catch(e) {
    console.error('AI Monthly Review Error:', e);
    btn.disabled = false;
    btn.innerHTML = '✦ AI 성찰 생성하기';
    resultArea.innerHTML = '<p style="color:red;">오류가 발생했습니다. 다시 시도해주세요.</p>';
  }
}

// ── AI 연간 성찰 생성 ──
async function generateYearlyAIReview(startStr, endStr) {
  const btn = document.getElementById('yearly-ai-btn');
  const resultArea = document.getElementById('yearly-ai-result');
  
  btn.disabled = true;
  btn.innerHTML = '⏳ 분석 중...';

  try {
    const [{ data: todos }, { data: logs }, { data: reflects }] = await Promise.all([
      sb.from('todos').select('log_date,done').gte('log_date', startStr).lte('log_date', endStr),
      sb.from('routine_logs').select('log_date,done').gte('log_date', startStr).lte('log_date', endStr),
      sb.from('reflections').select('log_date').gte('log_date', startStr).lte('log_date', endStr)
    ]);

    const targetYear = startStr.substring(0,4);
    
    // 월별 통계 계산
    const monthStats = Array.from({length:12}, (_,m) => {
      const ms = `${targetYear}-${String(m+1).padStart(2,'0')}`;
      const mTodos = (todos||[]).filter(t => t.log_date.startsWith(ms));
      const rate = mTodos.length > 0 ? Math.round(mTodos.filter(t=>t.done).length/mTodos.length*100) : 0;
      return { month:m+1, rate };
    });
    const bestMonth = monthStats.reduce((b,m) => m.rate > b.rate ? m : b, monthStats[0]);

    const totalTasks = todos?.length || 0;
    const totalDone = todos?.filter(t => t.done).length || 0;
    const routineTotal = logs?.length || 0;
    const routineDone = logs?.filter(l => l.done).length || 0;
    const routineRate = routineTotal > 0 ? Math.round(routineDone / routineTotal * 100) : 0;
    const reflectDays = reflects?.length || 0;

    const userMessage = `당신은 따뜻하고 통찰력 있는 인생 코치입니다.
아래는 사용자의 ${targetYear}년 전체 활동 데이터입니다.

[할일 완료 현황]
- 총 완료 할일: ${totalDone}개

[루틴 달성 현황]
- 루틴 달성률: ${routineRate}%

[성찰 기록]
- 성찰 작성일: ${reflectDays}일

[생산성 지표]
- 가장 생산적인 달: ${bestMonth.month}월 (${bestMonth.rate}%)

위 데이터를 바탕으로 올해 총평을 아래 형식으로 작성해주세요:
1. 📊 올해 성과 요약 (핵심을 한 문장으로)
2. ✅ 잘한 점 (데이터 기반 2가지)
3. 💡 아쉬운 점 (따뜻한 조언 2가지)
4. 🎯 내년을 위한 개선 제안 (구체적인 제안 2가지)
5. 💬 응원 한마디 (진심 어린 격려)

전체 분량은 300~500자 정도로, 마크다운 굵은 글씨(**텍스트**)를 활용해 가독성 좋게 작성해주세요.`;

    const response = await fetch(
      'https://qxqkpgkiuzdvkdieqynf.supabase.co/functions/v1/ai-analysis',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4cWtwZ2tpdXpkdmtkaWVxeW5mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3MjI3OTAsImV4cCI6MjA5MDI5ODc5MH0.T6FT8YQKAPwIgPfKU1guaRx-izWvta7fM1nLMuzggZI'
        },
        body: JSON.stringify({ userMessage })
      }
    );

    const data = await response.json();
    const text = data.result || data.message || data.content || data.text || data.response || JSON.stringify(data);

    const formatted = text
      .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
      .replace(/\\n/g, '<br>');

    resultArea.innerHTML = `
      <div style="line-height:1.9;font-size:15px;color:#333;padding:8px 0;">
        ${formatted}
      </div>
    `;
    btn.innerHTML = '🔄 다시 생성하기';
    btn.disabled = false;

    const { data: { user } } = await sb.auth.getUser();
    if (user) {
      const yearKey = getYearKey(startStr);
      await sb.from('ai_reviews').upsert({
        user_id: user.id,
        type: 'yearly',
        period: yearKey,
        content: formatted
      }, { onConflict: 'user_id,type,period' });
    }

  } catch(e) {
    console.error('AI Yearly Review Error:', e);
    btn.disabled = false;
    btn.innerHTML = '✦ AI 성찰 생성하기';
    resultArea.innerHTML = '<p style="color:red;">오류가 발생했습니다. 다시 시도해주세요.</p>';
  }
}
"""

if "async function generateMonthlyAIReview" not in content:
    weekly_end_marker = "resultArea.innerHTML = '<p style=\"color:red;\">오류가 발생했습니다. 다시 시도해주세요.</p>';\n  }\n}"
    if weekly_end_marker in content:
        content = content.replace(weekly_end_marker, weekly_end_marker + "\n" + new_functions)
    else:
        content += "\n" + new_functions

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done updating index.html")
