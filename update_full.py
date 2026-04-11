import sys

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add date input and today button to HTML
date_nav_old = """      <div class="center-date-nav dbar-today">
        <button class="date-nav-btn" onclick="changeDate(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        <div class="center-date-text">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span id="dateDisplay">2026년 4월 2일 (목)</span>
        </div>
        <button class="date-nav-btn" onclick="changeDate(1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><path d="m9 18 6-6-6-6"/></svg>
        </button>
      </div>"""

date_nav_new = """      <div class="center-date-nav dbar-today" style="position:relative;">
        <button class="date-nav-btn" onclick="changeDate(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        <div class="center-date-text" style="cursor:pointer;" onclick="document.getElementById('dateInputH')._flatpickr.open()">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span id="dateDisplay"></span>
          <input type="text" id="dateInputH" style="opacity:0; position:absolute; z-index:-1; width:1px; height:1px;">
        </div>
        <button class="date-nav-btn" onclick="changeDate(1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><path d="m9 18 6-6-6-6"/></svg>
        </button>
        <button id="btnToday" style="display:none; margin-left:12px; padding:6px 12px; font-size:13px; font-weight:600; background-color:#e0e7ff; color:#4338ca; border:none; border-radius:8px; cursor:pointer;" onclick="goToToday()">오늘로 이동</button>
      </div>
      <!-- Hidden input for task date change -->
      <input type="text" id="taskDateInputH" style="opacity:0; position:absolute; z-index:-1; width:1px; height:1px;">
"""
if date_nav_old in text:
    text = text.replace(date_nav_old, date_nav_new)
else:
    # Let's do a more robust regex-like logical string find/replace if exact missed
    print("WARNING: date_nav_old not found. Proceeding with best-effort updates.")

# 2. Update renderTodos to include the icons 📅, Copy, 🗑️
todo_item_old = """            <span style="flex:1; font-size:13.5px; ${t.done ? 'text-decoration:line-through; color:#9ca3af;' : 'color:#1f2937;'}">
              ${t.text}
            </span>
            <span onclick="deleteTodo('${t.id}')" style="cursor:pointer; color:#ef4444; padding:2px 4px; font-size:14px;">🗑️</span>"""

todo_item_new = """            <del style="flex:1; font-size:13.5px; display:${t.done ? 'block' : 'none'}; color:#9ca3af; text-decoration:line-through;">${t.text}</del>
            <span style="flex:1; font-size:13.5px; display:${t.done ? 'none' : 'block'}; color:#1f2937;">${t.text}</span>
            <div style="display:flex; gap:6px; margin-left:auto;">
              <span onclick="openTaskDate('${t.id}', '${t.log_date}')" style="cursor:pointer; font-size:14px; opacity:0.6; padding:2px;">📅</span>
              <span onclick="copyTask('${t.id}')" style="cursor:pointer; font-size:14px; opacity:0.6; padding:2px;">📋</span>
              <span onclick="deleteTodo('${t.id}')" style="cursor:pointer; color:#ef4444; padding:2px; font-size:14px;">🗑️</span>
            </div>"""

if todo_item_old in text:
    text = text.replace(todo_item_old, todo_item_new)
else:
    print("WARNING: todo_item_old not found. Make sure to update renderTodos.")

# 3. Add functionalities and date checking at the end of script
js_additions = """
// ============================================
// Additions for Date Navigation and Icons
// ============================================

window.openTaskDate = function(taskId, currentLogDate) {
  const tp = document.getElementById('taskDateInputH');
  if(!tp._flatpickr) {
    flatpickr(tp, {
      locale: 'ko',
      onChange: async function(selectedDates, dateStr) {
         if (tp.dataset.taskId && dateStr) {
           await sb.from('todos').update({ log_date: dateStr }).eq('id', tp.dataset.taskId);
           loadData();
           showToast('날짜가 변경되었습니다 📅');
         }
      }
    });
  }
  tp.dataset.taskId = taskId;
  tp._flatpickr.setDate(currentLogDate || new Date());
  tp._flatpickr.open();
};

window.copyTask = async function(id) {
  let found = null;
  for (const cat of Object.keys(todos)) {
    const t = todos[cat].find(x => x.id === id);
    if (t) { found = t; break; }
  }
  if (!found) return;

  const { error } = await sb.from('todos').insert({
    category: found.category,
    text: found.text + ' (복사본)',
    log_date: todayStr(),
    done: false,
    icon: found.icon
  });
  if (error) {
    showToast('복사 중 오류가 발생했습니다.');
  } else {
    showToast('할일이 복사되었습니다 📋');
    loadData();
  }
};

window.goToToday = async function() {
  currentDate = new Date();
  updateDateBar();
  loadData();
};

// Listen for flatpickr initialization
document.addEventListener('DOMContentLoaded', () => {
  flatpickr('#dateInputH', {
    locale: 'ko',
    defaultDate: new Date(),
    onChange: function(selectedDates) {
      if (selectedDates.length > 0) {
        currentDate = selectedDates[0];
        updateDateBar();
        loadData();
      }
    }
  });

  const originalUpdateDateBar = updateDateBar;
  window.updateDateBar = function() {
    originalUpdateDateBar();
    const btnToday = document.getElementById('btnToday');
    if (btnToday) {
      if (todayStr(currentDate) !== todayStr(new Date())) {
        btnToday.style.display = 'inline-block';
      } else {
        btnToday.style.display = 'none';
      }
    }
  };
  
  // init run
  setTimeout(()=> { window.updateDateBar(); }, 500);
});
</script>"""

text = text.replace("</script>", js_additions)

# Update routine badge style if missing
text = text.replace(
    "${t.is_recurring ? '<span style=\"font-size:10px; background:#ede9fe; color:#7c3aed; padding:2px 6px; border-radius:10px; font-weight:600;\">🔄 반복업무</span>' : ''}",
    "${t.icon === '반복업무' ? '<span style=\"font-size:10px; background:#ede9fe; color:#7c3aed; padding:2px 6px; border-radius:10px; font-weight:600;\">🔄 반복업무</span>' : ''}"
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Updates applied.")
