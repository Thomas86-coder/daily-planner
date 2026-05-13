import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Modal HTML z-index
text = text.replace(
    '''<div id="recurring-modal" class="modal-backdrop" style="display:none;" onclick="if(event.target===this) closeRecurringModal()">''',
    '''<div id="recurring-modal" class="modal-backdrop" style="display:none; z-index: 3000;" onclick="if(event.target===this) window.closeRecurringModal()">'''
)

# Fix open btn
text = text.replace(
    '''onclick="openRecurringModal()"''',
    '''onclick="window.openRecurringModal()"'''
)

text = text.replace(
    '''onclick="saveRecurringTask()"''',
    '''onclick="window.saveRecurringTask()"'''
)
text = text.replace(
    '''onclick="closeRecurringModal()"''',
    '''onclick="window.closeRecurringModal()"'''
)


# 2. Update Modal Fields
text = text.replace(
'''          <div class="rc-field">
            <label class="modal-label">반복 주기</label>
            <select id="rt-cycle-input" class="modal-input">
              <option value="매일 (월~일)">매일(월~일)</option>
              <option value="매주 (월~금)">주중(월~금)</option>
              <option value="주말 (토~일)">주말</option>
              <option value="주 1회">매주</option>
              <option value="월 1회">매월</option>
            </select>
          </div>
          
          <div class="rc-field">
            <label class="modal-label">시작일</label>
            <input type="date" id="rt-start-input" class="modal-input" />
          </div>
          
          <div class="rc-field">
            <label class="modal-label">종료일 (선택) <span class="sub-label">(비워두면 3개월 후까지 등록)</span></label>
            <input type="date" id="rt-end-input" class="modal-input" />
          </div>''',
'''          <div class="rc-field">
            <label class="modal-label">반복 주기</label>
            <select id="rt-cycle-input" class="modal-input">
              <option value="매일 (월~일)">매일 (월~일)</option>
              <option value="주중 매일 (월~금)">주중 매일 (월~금)</option>
              <option value="주말 (토~일)">주말 (토~일)</option>
              <option value="매주 월">매주 월</option>
              <option value="매주 화">매주 화</option>
              <option value="매주 수">매주 수</option>
              <option value="매주 목">매주 목</option>
              <option value="매주 금">매주 금</option>
              <option value="매주 토">매주 토</option>
              <option value="매주 일">매주 일</option>
            </select>
          </div>
          
          <div class="rc-field">
            <label class="modal-label">시작일</label>
            <input type="date" id="rt-start-input" class="modal-input" />
          </div>
          
          <div class="rc-field">
            <label class="modal-label">종료일 (선택) <span class="sub-label" style="font-size:11px; color:#9ca3af;">(비워두면 3개월 후까지 등록)</span></label>
            <input type="date" id="rt-end-input" class="modal-input" placeholder="(비워두면 3개월 후까지 등록)" />
          </div>'''
)

# 3. Update JS Logic
old_js_start = text.find('// ===== 반복업무 로직 =====')
old_js_end = text.find('</script>', old_js_start)

new_js = '''// ===== 반복업무 로직 =====
  window.allRecurringTasks = [];

  window.openRecurringModal = function() {
    const textInput = document.getElementById('rt-text-input');
    const startInput = document.getElementById('rt-start-input');
    const endInput = document.getElementById('rt-end-input');
    if(textInput) textInput.value = '';
    const tzoffset = (new Date()).getTimezoneOffset() * 60000;
    const localISOTime = (new Date(Date.now() - tzoffset)).toISOString().split('T')[0];
    if(startInput) startInput.value = localISOTime;
    if(endInput) endInput.value = '';
    const modal = document.getElementById('recurring-modal');
    if(modal) modal.style.display = 'flex';
  };

  window.closeRecurringModal = function() {
    const modal = document.getElementById('recurring-modal');
    if(modal) modal.style.display = 'none';
  };

  window.loadRecurringTasks = async function() {
    try {
      if(!window.sb) return;
      const { data, error } = await sb.from('recurring_tasks').select('*').order('created_at', { ascending: false });
      if (error) { 
        if (error.code === 'PGRST204' || error.code === '42P01') {
          console.error("🚨 recurring_tasks 테이블이 없습니다. 아래 SQL을 실행하여 생성해주세요:\\nCREATE TABLE recurring_tasks (\\n  id uuid default uuid_generate_v4() primary key,\\n  title text not null,\\n  category text not null,\\n  frequency text not null,\\n  start_date date not null,\\n  end_date date not null,\\n  user_id text not null,\\n  created_at timestamp with time zone default timezone('utc'::text, now())\\n);");
        }
        return; 
      }
      window.allRecurringTasks = data || [];
      window.renderRecurringTasks();
    } catch(e) { console.error(e); }
  };

  function getRcCategoryIcon(cat) {
    cat = cat.toLowerCase();
    if (cat === 'work') return '💼';
    if (cat === 'job') return '👔';
    if (cat === 'growth') return '🌱';
    return '🏃';
  }

  window.renderRecurringTasks = function() {
    const grid = document.getElementById('recurring-grid');
    if (!grid) return;
    grid.innerHTML = '';
    
    if (window.allRecurringTasks.length === 0) {
      grid.innerHTML = '<div style="color:#9ca3af;text-align:center;padding:40px;grid-column:1/-1;">등록된 반복업무가 없습니다.</div>';
      return;
    }

    window.allRecurringTasks.forEach(t => {
      const startStr = t.start_date || '지정안됨';
      const endStr = t.end_date || '계속';
      
      const div = document.createElement('div');
      div.className = 'rc-card';
      div.innerHTML = `
        <button class="rc-delete" onclick="window.deleteRecurringTask('${t.id}')">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
        </button>
        <div class="rc-header">
          <div class="rc-icon-box">${getRcCategoryIcon(t.category)}</div>
          <div class="rc-info">
            <h3 style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:80%;">${t.title}</h3>
            <span class="rc-badge" style="text-transform: capitalize;">${t.category}</span>
          </div>
        </div>
        <div class="rc-divider"></div>
        <div class="rc-details">
          <span>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg>
            ${t.frequency}
          </span>
          <span>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
            ${startStr} ~ ${endStr}
          </span>
        </div>
        <button class="rc-action-btn" onclick="window.addRecurringToToday('${t.id}')">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
          오늘 할일 등록하기
        </button>
      `;
      grid.appendChild(div);
    });
  };

  window.saveRecurringTask = async function() {
    const rawCat = document.getElementById('rt-cat-input').value || 'Work';
    const cat = rawCat.toLowerCase();
    const title = document.getElementById('rt-text-input').value.trim();
    const frequency = document.getElementById('rt-cycle-input').value;
    const start = document.getElementById('rt-start-input').value;
    let end = document.getElementById('rt-end-input').value;
    
    if(!title || !start) {
      showToast('할일 내용과 시작일을 모두 입력하세요.', true);
      return;
    }

    if(!end) {
      const d = new Date(start);
      d.setMonth(d.getMonth() + 3);
      end = d.toISOString().split('T')[0];
    }
    
    try {
      // Assuming 'thomas-account' or a mock up from codebase
      const insertData = { category: cat, title, frequency, start_date: start, end_date: end, user_id: window.currentUser ? window.currentUser.id : 'mock-user' };
      const { error } = await sb.from('recurring_tasks').insert([insertData]);
      if(error) {
        if (error.code === 'PGRST204' || error.code === '42P01') {
          console.error("🚨 recurring_tasks 테이블이 없습니다. DB SQL을 실행하여 생성해주세요:\\nCREATE TABLE recurring_tasks (\\n  id uuid default uuid_generate_v4() primary key,\\n  title text not null,\\n  category text not null,\\n  frequency text not null,\\n  start_date date not null,\\n  end_date date not null,\\n  user_id text not null,\\n  created_at timestamp with time zone default timezone('utc'::text, now())\\n);");
        }
        showToast('저장 중 오류가 발생했습니다. (DB 테이블 여부를 확인하세요) 🚨', true);
        throw error;
      }
      showToast('반복업무가 추가되었습니다!');
      window.closeRecurringModal();
      window.loadRecurringTasks();
    } catch(e) {
      console.error(e);
    }
  };

  window.deleteRecurringTask = async function(id) {
    if(!confirm('해당 반복업무를 삭제하시겠습니까?')) return;
    try {
      await sb.from('recurring_tasks').delete().eq('id', id);
      showToast('삭제되었습니다.');
      window.loadRecurringTasks();
    } catch(e) { console.error(e); }
  };

  window.addRecurringToToday = async function(rtId) {
    const rc = window.allRecurringTasks.find(x => x.id === rtId);
    if (!rc) return;
    
    try {
      const dstr = currentDate.toISOString().split('T')[0];
      const { data: exist } = await sb.from('todos')
        .select('id')
        .eq('user_id', window.currentUser ? window.currentUser.id : 'mock-user')
        .eq('log_date', dstr)
        .eq('text', rc.title)
        .eq('category', rc.category)
        .eq('icon', '반복업무');
      
      if (exist && exist.length > 0) {
        showToast('오늘 같은 반복업무가 이미 등록되어 있습니다.', true);
        return;
      }
      
      const insertData = {
        user_id: window.currentUser ? window.currentUser.id : 'mock-user',
        log_date: dstr,
        text: rc.title,
        icon: '반복업무',
        category: rc.category,
        is_done: false
      };
      const { error } = await sb.from('todos').insert([insertData]);
      if(error) throw error;
      
      showToast('오늘 할일에 등록되었습니다! 👏');
      if(typeof fetchDataForDate === 'function') fetchDataForDate(currentDate);
    } catch(e) { console.error(e); showToast('등록 중 오류 발생', true); }
  };

  window.syncRecurringTasksToToday = async function() {
    if(sessionStorage.getItem('recurringSyncDone')) return;

    try {
      if(!window.sb) return;
      const todayStr = new Date().toISOString().split('T')[0];
      const { data: rcs, error } = await sb.from('recurring_tasks')
        .select('*')
        .lte('start_date', todayStr)
        .gte('end_date', todayStr);
      
      if(error || !rcs || rcs.length === 0) {
        sessionStorage.setItem('recurringSyncDone','true');
        return;
      }

      const today = new Date();
      const options = ['일','월','화','수','목','금','토'];
      const todayDowStr = options[today.getDay()];
      const isWeekday = today.getDay() >= 1 && today.getDay() <= 5;
      const isWeekend = today.getDay() === 0 || today.getDay() === 6;

      const toInsert = [];
      for(const rc of rcs) {
        let match = false;
        if(rc.frequency === "매일 (월~일)") match = true;
        else if(rc.frequency === "주중 매일 (월~금)" && isWeekday) match = true;
        else if(rc.frequency === "주말 (토~일)" && isWeekend) match = true;
        else if(rc.frequency === `매주 ${todayDowStr}`) match = true;

        if(!match) continue;

        // Check if already in today's todos
        const { data: exist } = await sb.from('todos')
          .select('id')
          .eq('log_date', todayStr)
          .eq('text', rc.title)
          .eq('category', rc.category)
          .eq('icon', '반복업무');
        
        if(!exist || exist.length === 0) {
          toInsert.push({
            user_id: rc.user_id || (window.currentUser ? window.currentUser.id : 'mock-user'),
            log_date: todayStr,
            text: rc.title,
            icon: '반복업무',
            category: rc.category,
            is_done: false
          });
        }
      }

      if(toInsert.length > 0) {
        await sb.from('todos').insert(toInsert);
        showToast(`오늘의 반복업무 ${toInsert.length}개가 자동 추가되었습니다! ✨`);
        if(typeof fetchDataForDate === 'function') fetchDataForDate(currentDate || new Date());
      }
      sessionStorage.setItem('recurringSyncDone','true');

    } catch(err) {
      console.error('syncRecurringTasksToToday fail:', err);
    }
  };

'''

text = text[:old_js_start] + new_js + text[old_js_end:]

# 4. Integrate syncRecurringTasksToToday inside DOMContentLoaded execution.
# We also want to loadRecurringTasks
text = text.replace(
'''  // init run
  setTimeout(()=> { 
    if(window.updateDateBar) window.updateDateBar(); 
    loadData(); // Initial data load
  }, 500);''',
'''  // init run
  setTimeout(()=> { 
    if(window.updateDateBar) window.updateDateBar(); 
    if(window.syncRecurringTasksToToday) window.syncRecurringTasksToToday();
    if(window.loadRecurringTasks) window.loadRecurringTasks();
    loadData(); // Initial data load
  }, 500);'''
)

text = text.replace(
'''<div class="pr-content-area">
          <div id="recurring-grid" class="recurring-grid">''',
'''<div class="pr-content-area">
          <p style="font-size: 13px; color: #6b7280; margin-bottom: 12px; font-weight: bold;">[안내] 오류 발생 시 콘솔을 확인해주세요</p>
          <div id="recurring-grid" class="recurring-grid">'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("HTML and JS updated successfully!")

