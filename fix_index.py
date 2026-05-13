import codecs

path = '/Users/jaehyun/인생관리시스템/index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

# Fix garbage at EOF
idx = content.find('</body></html')
if idx != -1:
    content = content[:idx] + '</body>\n</html>\n'

# Fix loadMonthlyPage missing variables
old_monthly = """  // 통계
  const totalDone = todos.filter(t=>t.done).length;
  const totalTasks = todos.length;
  const routineDone = logs.filter(l=>l.done).length;
  const routineTotal = logs.length;
  const routineRate = routineTotal > 0 ? Math.round(routineDone/routineTotal*100) : 0;
  const reflectDays = reflects.length;"""

new_monthly = """  // 통계
  const totalDone = todos.filter(t=>t.done).length;
  const totalTasks = todos.length;
  const doneAll = totalDone;
  const totalAll = totalTasks;
  const overallRate = totalTasks > 0 ? Math.round(totalDone/totalTasks*100) : 0;
  const routineDone = logs.filter(l=>l.done).length;
  const routineTotal = logs.length;
  const routineRate = routineTotal > 0 ? Math.round(routineDone/routineTotal*100) : 0;
  const reflectDays = reflects.length;"""
content = content.replace(old_monthly, new_monthly)

old_monthly_cats = """  const catData = { work:[], job:[], growth:[], personal:[] };
  todos.forEach(t => { if (catData[t.category]) catData[t.category].push(t); });"""

new_monthly_cats = """  const cats = { work:[], job:[], growth:[], personal:[] };
  todos.forEach(t => { 
    const c = t.category || '';
    if (cats[c.toLowerCase()]) cats[c.toLowerCase()].push(t); 
  });
  let bestCat = '-', bestCatRate = -1;
  Object.entries(cats).forEach(([cat, items]) => {
    const r = items.length > 0 ? items.filter(t=>t.done).length / items.length * 100 : 0;
    if (r > bestCatRate) { bestCatRate = r; bestCat = typeof CAT_LABEL !== 'undefined' && CAT_LABEL[cat] ? CAT_LABEL[cat] : cat; }
  });
  
  const days = Array.from({length: daysInMonth}, (_,i) => {
    const d = new Date(targetYear, targetMonth, i+1);
    return { date: d, str: fmtDateStr(d), label: String(i+1) };
  });"""
content = content.replace(old_monthly_cats, new_monthly_cats)


# Fix loadYearlyPage missing variables
old_yearly = """  const totalDone = todos.filter(t=>t.done).length;
  const routineDone = logs.filter(l=>l.done).length;
  const routineTotal = logs.length;
  const routineRate = routineTotal > 0 ? Math.round(routineDone/routineTotal*100) : 0;
  const bestMonth = monthStats.reduce((b,m) => m.rate > b.rate ? m : b, monthStats[0]);"""

new_yearly = """  const totalDone = todos.filter(t=>t.done).length;
  const totalTasks = todos.length;
  const doneAll = totalDone;
  const totalAll = totalTasks;
  const overallRate = totalTasks > 0 ? Math.round(totalDone/totalTasks*100) : 0;
  const routineDone = logs.filter(l=>l.done).length;
  const routineTotal = logs.length;
  const routineRate = routineTotal > 0 ? Math.round(routineDone/routineTotal*100) : 0;
  const bestMonth = monthStats.reduce((b,m) => m.rate > b.rate ? m : b, monthStats[0]);

  const cats = { work:[], job:[], growth:[], personal:[] };
  todos.forEach(t => { 
    const c = t.category || '';
    if (cats[c.toLowerCase()]) cats[c.toLowerCase()].push(t); 
  });
  let bestCat = '-', bestCatRate = -1;
  Object.entries(cats).forEach(([cat, items]) => {
    const r = items.length > 0 ? items.filter(t=>t.done).length / items.length * 100 : 0;
    if (r > bestCatRate) { bestCatRate = r; bestCat = typeof CAT_LABEL !== 'undefined' && CAT_LABEL[cat] ? CAT_LABEL[cat] : cat; }
  });"""
content = content.replace(old_yearly, new_yearly)


content = content.replace(
    "  document.getElementById('monthly-body').innerHTML = '<div class=\"rv-spinner\">데이터 불러오는 중...</div>';\n\n  const now",
    "  const bodyEl = document.getElementById('monthly-body');\n  bodyEl.innerHTML = '<div class=\"rv-spinner\">데이터 불러오는 중...</div>';\n  try {\n  const now"
)
content = content.replace(
    "document.getElementById('monthly-body').innerHTML = html;\n}",
    "bodyEl.innerHTML = html;\n  } catch(e) {\n    console.error(e);\n    bodyEl.innerHTML = '<div style=\"padding:40px; text-align:center; color:#ef4444;\">데이터를 불러오는 중 오류가 발생했습니다.</div>';\n  }\n}"
)

content = content.replace(
    "  document.getElementById('yearly-body').innerHTML = '<div class=\"rv-spinner\">데이터 불러오는 중...</div>';\n\n  const targetYear",
    "  const bodyEl = document.getElementById('yearly-body');\n  bodyEl.innerHTML = '<div class=\"rv-spinner\">데이터 불러오는 중...</div>';\n  try {\n  const targetYear"
)
content = content.replace(
    "document.getElementById('yearly-body').innerHTML = html;\n}",
    "bodyEl.innerHTML = html;\n  } catch(e) {\n    console.error(e);\n    bodyEl.innerHTML = '<div style=\"padding:40px; text-align:center; color:#ef4444;\">데이터를 불러오는 중 오류가 발생했습니다.</div>';\n  }\n}"
)

content = content.replace(
    "  document.getElementById('weekly-body').innerHTML = '<div class=\"rv-spinner\">데이터 불러오는 중...</div>';\n\n  // 이번 주",
    "  const bodyEl = document.getElementById('weekly-body');\n  bodyEl.innerHTML = '<div class=\"rv-spinner\">데이터 불러오는 중...</div>';\n  try {\n  // 이번 주"
)
content = content.replace(
    "document.getElementById('weekly-body').innerHTML = html;\n}",
    "bodyEl.innerHTML = html;\n  } catch(e) {\n    console.error(e);\n    bodyEl.innerHTML = '<div style=\"padding:40px; text-align:center; color:#ef4444;\">데이터를 불러오는 중 오류가 발생했습니다.</div>';\n  }\n}"
)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)
print("Done")
