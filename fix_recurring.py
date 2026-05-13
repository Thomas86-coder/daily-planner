import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix the error text insertion from before
text = text.replace(
'''<div class="pr-content-area">
          <p style="font-size: 13px; color: #6b7280; margin-bottom: 12px; font-weight: bold;">[안내] 오류 발생 시 콘솔을 확인해주세요</p>
          <div id="recurring-grid" class="recurring-grid">''',
'''<div class="pr-content-area">
          <div id="recurring-grid" class="recurring-grid">'''
)

# 2. Revert any old calls to window.openRecurringModal
text = text.replace(
    '''onclick="window.openRecurringModal()"''',
    '''onclick="showRecurringTaskModal()"'''
)
text = text.replace(
    '''onclick="openRecurringModal()"''',
    '''onclick="showRecurringTaskModal()"'''
)

# Replace the implementations in JS
js_to_replace = '''  window.loadRecurringTasks = async function() {
    try {
      if(!window.sb) return;
      const { data, error } = await sb.from('recurring_tasks').select('*').order('created_at', { ascending: false });
      if (error) { 
        if (error.code === 'PGRST204' || error.code === '42P01') {
          console.error("🚨 recurring_tasks 테이블이 없습니다. DB SQL을 실행하여 생성해주세요:\\nCREATE TABLE recurring_tasks (\\n  id uuid default uuid_generate_v4() primary key,\\n  title text not null,\\n  category text not null,\\n  frequency text not null,\\n  start_date date not null,\\n  end_date date not null,\\n  user_id text not null,\\n  created_at timestamp with time zone default timezone('utc'::text, now())\\n);");
        }
        return; 
      }
      window.allRecurringTasks = data || [];
      window.renderRecurringTasks();
    } catch(e) { console.error(e); }
  };'''

js_new = '''  window.loadRecurringTasks = async function() {
    try {
      if(!window.sb) return;
      const { data, error } = await sb.from('recurring_tasks').select('*').order('created_at', { ascending: false });
      if (error) { 
        console.error('recurring_tasks 오류:', error.message);
        window.allRecurringTasks = [];
        window.renderRecurringTasks();
        return; 
      }
      window.allRecurringTasks = data || [];
      window.renderRecurringTasks();
    } catch(e) { 
      console.error('recurring_tasks catch 오류:', e && e.message ? e.message : '알 수 없는 오류');
      window.allRecurringTasks = [];
      window.renderRecurringTasks();
    }
  };'''
text = text.replace(js_to_replace, js_new)

js_to_replace_modal = '''  window.openRecurringModal = function() {
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
  };'''

js_new_modal = '''  window.showRecurringTaskModal = function() {
    let existing = document.getElementById('dynamic-recurring-modal');
    if(existing) {
      existing.remove();
    }
    const tzoffset = (new Date()).getTimezoneOffset() * 60000;
    const localISOTime = (new Date(Date.now() - tzoffset)).toISOString().split('T')[0];

    const modalHtml = `
      <div id="dynamic-recurring-modal" class="modal-backdrop" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.4); display:flex; align-items:center; justify-content:center; z-index:9999;" onclick="if(event.target===this) this.remove()">
        <div style="background:white; border-radius:16px; padding:32px; width:90%; max-width:400px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
            <h3 style="margin:0; font-size:18px; color:#111827;">반복업무 추가</h3>
            <button onclick="document.getElementById('dynamic-recurring-modal').remove()" style="background:none; border:none; cursor:pointer; color:#9ca3af; font-size:20px;">×</button>
          </div>
          
          <div style="margin-bottom:16px;">
            <label style="display:block; font-size:14px; color:#374151; font-weight:500; margin-bottom:8px;">카테고리</label>
            <select id="dyn-rt-cat" style="width:100%; padding:10px; border-radius:8px; border:1px solid #d1d5db; font-size:14px;">
              <option value="work">Work</option>
              <option value="job">Job</option>
              <option value="growth">Growth</option>
              <option value="personal">Personal</option>
            </select>
          </div>

          <div style="margin-bottom:16px;">
            <label style="display:block; font-size:14px; color:#374151; font-weight:500; margin-bottom:8px;">할일</label>
            <input type="text" id="dyn-rt-text" placeholder="반복할 할일을 입력하세요" style="width:100%; padding:10px; border-radius:8px; border:1px solid #d1d5db; font-size:14px;" />
          </div>

          <div style="margin-bottom:16px;">
            <label style="display:block; font-size:14px; color:#374151; font-weight:500; margin-bottom:8px;">반복 주기</label>
            <select id="dyn-rt-cycle" style="width:100%; padding:10px; border-radius:8px; border:1px solid #d1d5db; font-size:14px;">
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

          <div style="margin-bottom:16px;">
            <label style="display:block; font-size:14px; color:#374151; font-weight:500; margin-bottom:8px;">시작일</label>
            <input type="date" id="dyn-rt-start" value="${localISOTime}" style="width:100%; padding:10px; border-radius:8px; border:1px solid #d1d5db; font-size:14px;" />
          </div>

          <div style="margin-bottom:24px;">
            <label style="display:block; font-size:14px; color:#374151; font-weight:500; margin-bottom:8px;">종료일 (선택) <span style="font-size:11px; color:#9ca3af;">(비워두면 3개월 후까지 등록)</span></label>
            <input type="date" id="dyn-rt-end" placeholder="(비워두면 3개월 후까지 등록)" style="width:100%; padding:10px; border-radius:8px; border:1px solid #d1d5db; font-size:14px;" />
          </div>

          <div style="display:flex; gap:10px;">
            <button onclick="window.saveDynRecurringTask()" style="flex:2; padding:12px; border-radius:8px; background:linear-gradient(135deg, #8B5CF6, #7C3AED); color:white; border:none; font-weight:bold; cursor:pointer;">✓ 저장</button>
            <button onclick="document.getElementById('dynamic-recurring-modal').remove()" style="flex:1; padding:12px; border-radius:8px; background:#f3f4f6; color:#374151; border:none; font-weight:bold; cursor:pointer;">취소</button>
          </div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);
  };

  window.saveDynRecurringTask = async function() {
    const rawCat = document.getElementById('dyn-rt-cat').value || 'work';
    const cat = rawCat.toLowerCase();
    const title = document.getElementById('dyn-rt-text').value.trim();
    const frequency = document.getElementById('dyn-rt-cycle').value;
    const start = document.getElementById('dyn-rt-start').value;
    let end = document.getElementById('dyn-rt-end').value;
    
    if(!title || !start) {
      if(typeof showToast === 'function') showToast('할일 내용과 시작일을 모두 입력하세요.', true);
      else alert('할일 내용과 시작일을 모두 입력하세요.');
      return;
    }

    if(!end) {
      const d = new Date(start);
      d.setMonth(d.getMonth() + 3);
      end = d.toISOString().split('T')[0];
    }
    
    try {
      const insertData = { category: cat, title, frequency, start_date: start, end_date: end, user_id: window.currentUser ? window.currentUser.id : 'mock-user' };
      const { error } = await sb.from('recurring_tasks').insert([insertData]);
      if(error) {
        console.error('recurring_tasks insert 오류:', error.message);
        if(typeof showToast === 'function') showToast('저장 중 오류가 발생했습니다.', true);
        else alert('저장 중 오류가 발생했습니다.');
        return;
      }
      if(typeof showToast === 'function') showToast('반복업무가 추가되었습니다!');
      document.getElementById('dynamic-recurring-modal').remove();
      window.loadRecurringTasks();
    } catch(e) {
      console.error('recurring_tasks catch 오류:', e && e.message ? e.message : String(e));
    }
  };'''
text = text.replace(js_to_replace_modal, js_new_modal)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done phase 1")
