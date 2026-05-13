import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# WEEKLY
text = text.replace(
    '''  try {
    // 데이터 조회
    const currentYear = monday.getFullYear();
    const currentMonth = monday.getMonth() + 1;
    console.log('[주간리뷰] weekStart:', startStr, 'weekEnd:', endStr);

    const [todoRes, routineRes, reflectRes, routinesRes] = await Promise.all([''',
    '''  // 데이터 조회
  const currentYear = monday.getFullYear();
  const currentMonth = monday.getMonth() + 1;
  console.log('[주간리뷰] weekStart:', startStr, 'weekEnd:', endStr);

  let todos = [], logs = [], reflects = [], routineMetaList = [];
  try {
    const [todoRes, routineRes, reflectRes, routinesRes] = await Promise.all(['''
)

text = text.replace(
    '''    if (routinesRes.error) console.error('주간 routines 조회 실패:', routinesRes.error);

    const todos = todoRes.data || [];
    const logs = routineRes.data || [];
    const reflects = reflectRes.data || [];
    const routineMetaList = routinesRes.data || [];''',
    '''    if (routinesRes.error) console.error('주간 routines 조회 실패:', routinesRes.error);

    todos = todoRes.data || [];
    logs = routineRes.data || [];
    reflects = reflectRes.data || [];
    routineMetaList = routinesRes.data || [];
  } catch (error) {
    console.error('주간 db 통신(네트워크/RLS) 장애:', error);
  }'''
)

text = text.replace(
    '''  const [lastTodoRes, lastRoutineRes] = await Promise.all([
    sb.from('todos').select('done').gte('log_date', lastStartStr).lte('log_date', lastEndStr),
    sb.from('routine_logs').select('done').gte('log_date', lastStartStr).lte('log_date', lastEndStr)
  ]);

  if (lastTodoRes.error) console.error('전주 todos 조회 실패:', lastTodoRes.error);
  if (lastRoutineRes.error) console.error('전주 routine_logs 조회 실패:', lastRoutineRes.error);

  const lastTodos = lastTodoRes.data || [];
  const lastLogs = lastRoutineRes.data || [];''',
    '''  let lastTodos = [], lastLogs = [];
  try {
    const [lastTodoRes, lastRoutineRes] = await Promise.all([
      sb.from('todos').select('done').gte('log_date', lastStartStr).lte('log_date', lastEndStr),
      sb.from('routine_logs').select('done').gte('log_date', lastStartStr).lte('log_date', lastEndStr)
    ]);
  
    if (lastTodoRes.error) console.error('전주 todos 조회 실패:', lastTodoRes.error);
    if (lastRoutineRes.error) console.error('전주 routine_logs 조회 실패:', lastRoutineRes.error);
  
    lastTodos = lastTodoRes.data || [];
    lastLogs = lastRoutineRes.data || [];
  } catch (error) {
    console.error('전주 db 통신(네트워크/RLS) 장애:', error);
  }'''
)

text = text.replace(
    '''    if (bodyEl) bodyEl.innerHTML = html;
  } catch (error) {
    console.error('주간 데이터 로드 실패:', error);
    if (bodyEl) bodyEl.innerHTML = '<div style="padding:40px 20px; text-align:center; color:#9CA3AF; font-size:15px; background:white; border-radius:12px; border:1px solid #E5E7EB;">데이터를 표시할 수 없습니다.<br>인터넷 연결을 확인하거나 잠시 후 다시 시도해주세요.</div>';
  } finally {
    // 강제 렌더링으로 빠른 확인
    document.querySelectorAll('[class*="loading"], [id*="loading"], .rv-spinner').forEach(el => {
      if (el.textContent && el.textContent.includes('불러오는')) el.style.display = 'none';
    });
    document.querySelectorAll('[class*="weekly"], [id*="weekly"]').forEach(el => {
      if (el.style.display === 'none') el.style.display = 'block';
    });
  }
}''',
    '''  if (bodyEl) bodyEl.innerHTML = html;

  // 강제 렌더링으로 빠른 확인 (try/catch 우회하여 100% 실행 보장)
  document.querySelectorAll('[class*="loading"], [id*="loading"], .rv-spinner').forEach(el => {
    if (el.textContent && el.textContent.includes('불러오는')) el.style.display = 'none';
  });
  document.querySelectorAll('[class*="weekly"], [id*="weekly"]').forEach(el => {
    if (el.style.display === 'none') el.style.display = 'block';
  });
}'''
)

# MONTHLY
text = text.replace(
    '''  try {
    console.log('[월간리뷰] monthStart:', startStr, 'monthEnd:', endStr);

    const [todoRes, routineRes, reflectRes, lastTodoRes, lastRoutineRes] = await Promise.all([''',
    '''  console.log('[월간리뷰] monthStart:', startStr, 'monthEnd:', endStr);

  let todos = [], logs = [], reflects = [];
  try {
    const [todoRes, routineRes, reflectRes, lastTodoRes, lastRoutineRes] = await Promise.all(['''
)

text = text.replace(
    '''    if (lastTodoRes.error) console.error('전월 todos 조회 실패:', lastTodoRes.error);
    if (lastRoutineRes.error) console.error('전월 routine_logs 조회 실패:', lastRoutineRes.error);

    const todos = todoRes.data || [];
    const logs = routineRes.data || [];
    const reflects = reflectRes.data || [];''',
    '''    if (lastTodoRes.error) console.error('전월 todos 조회 실패:', lastTodoRes.error);
    if (lastRoutineRes.error) console.error('전월 routine_logs 조회 실패:', lastRoutineRes.error);

    todos = todoRes.data || [];
    logs = routineRes.data || [];
    reflects = reflectRes.data || [];
  } catch (error) {
    console.error('월간 db 통신(네트워크/RLS) 장애:', error);
  }'''
)

text = text.replace(
    '''    if (bodyEl) bodyEl.innerHTML = html;
  } catch (error) {
    console.error('월간 데이터 로드 실패:', error);
    if (bodyEl) bodyEl.innerHTML = '<div style="padding:40px 20px; text-align:center; color:#9CA3AF; font-size:15px; background:white; border-radius:12px; border:1px solid #E5E7EB;">데이터를 표시할 수 없습니다.<br>인터넷 연결을 확인하거나 잠시 후 다시 시도해주세요.</div>';
  } finally {
    // 강제 렌더링으로 빠른 확인
    document.querySelectorAll('[class*="loading"], [id*="loading"], .rv-spinner').forEach(el => {
      if (el.textContent && el.textContent.includes('불러오는')) el.style.display = 'none';
    });
    document.querySelectorAll('[class*="monthly"], [id*="monthly"]').forEach(el => {
      if (el.style.display === 'none') el.style.display = 'block';
    });
  }
}''',
    '''  if (bodyEl) bodyEl.innerHTML = html;

  // 강제 렌더링으로 빠른 확인
  document.querySelectorAll('[class*="loading"], [id*="loading"], .rv-spinner').forEach(el => {
    if (el.textContent && el.textContent.includes('불러오는')) el.style.display = 'none';
  });
  document.querySelectorAll('[class*="monthly"], [id*="monthly"]').forEach(el => {
    if (el.style.display === 'none') el.style.display = 'block';
  });
}'''
)


# YEARLY
text = text.replace(
    '''  try {
    console.log('[연간리뷰] yearStart:', startStr, 'yearEnd:', endStr);

    const [todoRes, routineRes, reflectRes, lastTodoRes, lastRoutineRes] = await Promise.all([''',
    '''  console.log('[연간리뷰] yearStart:', startStr, 'yearEnd:', endStr);

  let todos = [], logs = [], reflects = [];
  try {
    const [todoRes, routineRes, reflectRes, lastTodoRes, lastRoutineRes] = await Promise.all(['''
)

text = text.replace(
    '''    if (lastTodoRes.error) console.error('작년 todos 조회 실패:', lastTodoRes.error);
    if (lastRoutineRes.error) console.error('작년 routine_logs 조회 실패:', lastRoutineRes.error);

    const todos = todoRes.data || [];
    const logs = routineRes.data || [];
    const reflects = reflectRes.data || [];''',
    '''    if (lastTodoRes.error) console.error('작년 todos 조회 실패:', lastTodoRes.error);
    if (lastRoutineRes.error) console.error('작년 routine_logs 조회 실패:', lastRoutineRes.error);

    todos = todoRes.data || [];
    logs = routineRes.data || [];
    reflects = reflectRes.data || [];
  } catch (error) {
    console.error('연간 db 통신(네트워크/RLS) 장애:', error);
  }'''
)

text = text.replace(
    '''    if (bodyEl) bodyEl.innerHTML = html;
  } catch (error) {
    console.error('연간 데이터 로드 실패:', error);
    if (bodyEl) bodyEl.innerHTML = '<div style="padding:40px 20px; text-align:center; color:#9CA3AF; font-size:15px; background:white; border-radius:12px; border:1px solid #E5E7EB;">데이터를 표시할 수 없습니다.<br>인터넷 연결을 확인하거나 잠시 후 다시 시도해주세요.</div>';
  } finally {
    // 강제 렌더링으로 빠른 확인
    document.querySelectorAll('[class*="loading"], [id*="loading"], .rv-spinner').forEach(el => {
      if (el.textContent && el.textContent.includes('불러오는')) el.style.display = 'none';
    });
    document.querySelectorAll('[class*="yearly"], [id*="yearly"]').forEach(el => {
      if (el.style.display === 'none') el.style.display = 'block';
    });
  }
}''',
    '''  if (bodyEl) bodyEl.innerHTML = html;

  // 강제 렌더링으로 빠른 확인
  document.querySelectorAll('[class*="loading"], [id*="loading"], .rv-spinner').forEach(el => {
    if (el.textContent && el.textContent.includes('불러오는')) el.style.display = 'none';
  });
  document.querySelectorAll('[class*="yearly"], [id*="yearly"]').forEach(el => {
    if (el.style.display === 'none') el.style.display = 'block';
  });
}'''
)

text = text.replace(
    '''async function loadWeeklyPage() {
  console.log('[주간리뷰] 함수 시작');''',
    '''async function loadWeeklyPage() {
  alert('주간 함수 호출됨');
  console.log('[주간리뷰] 함수 시작');'''
)

text = text.replace(
    '''async function loadMonthlyPage() {
  console.log('[월간리뷰] 함수 시작');''',
    '''async function loadMonthlyPage() {
  alert('월간 함수 호출됨');
  console.log('[월간리뷰] 함수 시작');'''
)

text = text.replace(
    '''async function loadYearlyPage() {
  console.log('[연간리뷰] 함수 시작');''',
    '''async function loadYearlyPage() {
  alert('연간 함수 호출됨');
  console.log('[연간리뷰] 함수 시작');'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done")
