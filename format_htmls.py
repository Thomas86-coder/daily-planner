import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def replace_html_block(text, search_start_marker, bound_start_marker, search_end_marker, new_html_template):
    start_pos = text.find(search_start_marker)
    if start_pos == -1: 
        print(f"Failed to find {search_start_marker}")
        return text
        
    bound_start = text.find(bound_start_marker, start_pos)
    if bound_start == -1:
        print(f"Failed to find {bound_start_marker}")
        return text
        
    bound_end = text.find(search_end_marker, bound_start)
    if bound_end == -1:
        print(f"Failed to find end marker {search_end_marker}")
        return text
        
    return text[:bound_start] + new_html_template + text[bound_end:]

# ----- WEEKLY -----
weekly_html = """const html = `
  <!-- 섹션 1: 주간 지표 -->
  <div style="background:#F8F9FF; border:1.5px solid #C7D2FE; border-radius:16px; padding:24px; margin-bottom:24px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
      <div style="width:36px; height:36px; border-radius:50%; background:#EDE9FE; display:flex; align-items:center; justify-content:center; font-size:18px;">📊</div>
      <h3 style="margin:0; font-size:18px; font-weight:bold; color:#111827;">주간 지표</h3>
    </div>
    
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px; margin-bottom:24px;">
      <!-- 루틴 실천율 -->
      <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
          <span>🔄</span> 루틴 실천율
        </div>
        <div style="font-size:28px; font-weight:bold; color:${routineRate === 0 ? '#EF4444' : (routineRate >= 50 ? '#10B981' : '#374151')}; margin-bottom:4px;">
          ${routineRate}%
        </div>
        <div style="font-size:13px; color:#6B7280; margin-bottom:8px;">${routineDone} / ${routineTotal} 체크</div>
        <div style="font-size:12px; color:#9CA3AF;">★모닝:-% 🌙나이트:-%</div>
      </div>
      
      <!-- 할일 완료율 -->
      <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
          <span>✅</span> 할일 완료율
        </div>
        <div style="font-size:28px; font-weight:bold; color:#374151; margin-bottom:4px;">
          ${overallRate}%
        </div>
        <div style="font-size:13px; color:#6B7280; margin-bottom:8px;">${doneAll} / ${totalAll} 완료</div>
        <div style="font-size:12px; color:#9CA3AF;">평균 일일 할일: ${Math.round(totalAll / 7)}개</div>
      </div>

      <!-- 성찰 작성일 -->
      <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
          <span>📝</span> 성찰 작성일
        </div>
        <div style="font-size:28px; font-weight:bold; color:${reflects.length === 0 ? '#EF4444' : '#374151'}; margin-bottom:4px;">
          ${reflects.length}일
        </div>
        <div style="font-size:13px; color:#6B7280; margin-bottom:8px;">${Math.round(reflects.length / 7 * 100)}% 작성률</div>
        <div style="font-size:12px; color:#9CA3AF;">7일 중 ${reflects.length}일 기록</div>
      </div>
    </div>

    <!-- 카테고리별 완료율 4칸 -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:12px;">
      ${Object.entries(cats).map(([cat, items]) => {
        const d = items.filter(t=>t.done).length;
        const tot = items.length;
        const r = tot > 0 ? Math.round(d / tot * 100) : 0;
        let cColor = '#FDE68A'; let cBg = '#FEF3C7';
        if (cat === 'job') { cColor = '#DBEAFE'; cBg = '#EFF6FF'; }
        else if (cat === 'growth') { cColor = '#D1FAE5'; cBg = '#ECFDF5'; }
        else if (cat === 'personal') { cColor = '#FCE7F3'; cBg = '#FDF2F8'; }
        
        return `<div style="background:${cBg}; border:1px solid ${cColor}; border-radius:8px; padding:12px;">
          <div style="font-size:12px; font-weight:bold; color:#4B5563; text-transform:capitalize; margin-bottom:4px;">${CAT_LABEL[cat] || cat}</div>
          <div style="font-size:16px; font-weight:bold; color:#111827; margin-bottom:2px;">${r}%</div>
          <div style="font-size:11px; color:#6B7280;">${d} / ${tot} 완료</div>
        </div>`;
      }).join('')}
    </div>
  </div>

  <!-- 섹션 2: 주간 분석 -->
  <div style="background:#FFF5F5; border:1.5px solid #FFD0D0; border-radius:16px; padding:24px; margin-bottom:24px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
      <div style="width:36px; height:36px; border-radius:50%; background:#FEE2E2; display:flex; align-items:center; justify-content:center; font-size:18px;">💡</div>
      <h3 style="margin:0; font-size:18px; font-weight:bold; color:#111827;">주간 분석</h3>
    </div>

    <!-- 실천율 카드들 -->
    <h4 style="font-size:14px; font-weight:bold; color:#374151; margin-bottom:12px;">🎯 실천율</h4>
    <div style="display:flex; flex-direction:column; gap:10px; margin-bottom:20px;">
      <div style="background:#FFFBEA; border:1px solid #FFE082; border-radius:12px; padding:14px 16px; color:#4B5563; font-size:13px; display:flex; gap:10px; align-items:center;">
        <span style="font-size:16px;color:#F97316;">!</span> <span>${overallRate >= 50 ? '할일 완료율이 양호합니다. 이 페이스를 유지해보세요!' : '할일 완료율이 다소 낮습니다. 중요한 할일부터 하나씩 차근차근 시작해보세요.'}</span>
      </div>
      <div style="background:#FFFBEA; border:1px solid #FFE082; border-radius:12px; padding:14px 16px; color:#4B5563; font-size:13px; display:flex; gap:10px; align-items:center;">
        <span style="font-size:16px;color:#F97316;">!</span> <span>${routineRate >= 50 ? '루틴 실천율이 좋습니다. 습관이 잘 형성되고 있습니다!' : '규칙적인 루틴 실천에 조금만 더 신경써보세요.'}</span>
      </div>
      <div style="background:#FFFBEA; border:1px solid #FFE082; border-radius:12px; padding:14px 16px; color:#4B5563; font-size:13px; display:flex; gap:10px; align-items:center;">
        <span style="font-size:16px;color:#F97316;">!</span> <span>${reflects.length >= 3 ? '꾸준히 성찰을 기록하고 있습니다. 자기 객관화에 큰 도움이 됩니다.' : '이번 주말에는 꼭 한 주를 되돌아보는 성찰을 기록해보세요.'}</span>
      </div>
    </div>

    <!-- 전주 대비 변화 -->
    <h4 style="font-size:14px; font-weight:bold; color:#374151; margin-bottom:12px;">↗ 전주 대비 변화</h4>
    <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06); font-size:13px; color:#9CA3AF; margin-bottom:20px; text-align:center;">
      전주 대비 큰 변화가 없습니다.
    </div>

    <!-- 주간 패턴 -->
    <h4 style="font-size:14px; font-weight:bold; color:#374151; margin-bottom:12px;">〰 주간 패턴</h4>
    ${ (() => {
      let bDay = days[0].label;
      let dN = 0, lN = 0, mMax = -1;
      days.forEach(day => {
        const dCount = todos.filter(t => t.log_date === day.str && t.done).length;
        const lCount = logs.filter(l => l.log_date === day.str && l.done).length;
        if ((dCount+lCount) > mMax) { mMax = dCount+lCount; bDay = day.label; dN = dCount; lN = lCount; }
      });
      return `<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px;">
        <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
          <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">📅 가장 활발한 요일</div>
          <div style="font-size:22px; font-weight:bold; color:#111827; margin-bottom:4px;">${bDay}요일</div>
          <div style="font-size:12px; color:#6B7280;">할일 ${dN}개, 루틴 ${lN}개 완료</div>
        </div>
        <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
          <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">🏆 가장 완료율 높은 카테고리</div>
          <div style="font-size:22px; font-weight:bold; color:#111827; margin-bottom:4px;">${bestCatRate === -1 ? '-' : bestCat}</div>
          <div style="font-size:12px; color:#6B7280;">${bestCatRate === -1 ? '0' : Math.round(bestCatRate)}% 완료</div>
        </div>
      </div>`;
    })() }
  </div>

  <!-- 섹션 3: AI 주간 성찰 -->
  <div style="background:linear-gradient(135deg,#F3E8FF,#FCE7F3); border-radius:16px; padding:24px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
      <div style="width:36px; height:36px; border-radius:50%; background:white; display:flex; align-items:center; justify-content:center; font-size:18px;">✨</div>
      <h3 style="margin:0; font-size:18px; font-weight:bold; color:#111827;">AI 주간 성찰</h3>
    </div>
    
    <div id="weekly-ai-result" style="margin-bottom:20px;">
      <div style="text-align:center; padding:20px;">
        <div style="font-size:40px; margin-bottom:12px;">✨</div>
        <div style="font-size:16px; font-weight:bold; color:#374151; margin-bottom:6px;">AI 주간 성찰이 아직 없습니다</div>
        <div style="font-size:13px; color:#6B7280;">이번 주의 활동을 분석하여 맞춤형 피드백을 제공합니다.</div>
      </div>
    </div>

    <button id="weekly-ai-btn" class="ai-review-btn" onclick="generateWeeklyAIReview('${startStr}', '${endStr}')" style="width:100%; background:#8B5CF6; color:white; border:none; padding:14px; border-radius:12px; font-weight:bold; cursor:pointer;">
      ✦ AI 성찰 생성하기
    </button>
  </div>`;
"""
text = replace_html_block(text, "async function loadWeeklyPage() {", "const html = `", "document.getElementById('weekly-body').innerHTML = html;", weekly_html)

# ----- MONTHLY -----
monthly_html = """const html = `
  <!-- 섹션 1: 월간 지표 -->
  <div style="background:#F8F9FF; border:1.5px solid #C7D2FE; border-radius:16px; padding:24px; margin-bottom:24px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
      <div style="width:36px; height:36px; border-radius:50%; background:#EDE9FE; display:flex; align-items:center; justify-content:center; font-size:18px;">📊</div>
      <h3 style="margin:0; font-size:18px; font-weight:bold; color:#111827;">월간 지표</h3>
    </div>
    
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px; margin-bottom:24px;">
      <!-- 루틴 실천율 -->
      <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
          <span>🔄</span> 루틴 실천율
        </div>
        <div style="font-size:28px; font-weight:bold; color:${routineRate === 0 ? '#EF4444' : (routineRate >= 50 ? '#10B981' : '#374151')}; margin-bottom:4px;">
          ${routineRate}%
        </div>
        <div style="font-size:13px; color:#6B7280; margin-bottom:8px;">${routineDone} / ${routineTotal} 체크</div>
        <div style="font-size:12px; color:#9CA3AF;">★모닝:-% 🌙나이트:-%</div>
      </div>
      
      <!-- 할일 완료율 -->
      <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
          <span>✅</span> 할일 완료율
        </div>
        <div style="font-size:28px; font-weight:bold; color:#374151; margin-bottom:4px;">
          ${overallRate}%
        </div>
        <div style="font-size:13px; color:#6B7280; margin-bottom:8px;">${doneAll} / ${totalAll} 완료</div>
        <div style="font-size:12px; color:#9CA3AF;">평균 일일 할일: ${Math.round(totalAll / days.length)}개</div>
      </div>

      <!-- 성찰 작성일 -->
      <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
          <span>📝</span> 성찰 작성일
        </div>
        <div style="font-size:28px; font-weight:bold; color:${reflects.length === 0 ? '#EF4444' : '#374151'}; margin-bottom:4px;">
          ${reflects.length}일
        </div>
        <div style="font-size:13px; color:#6B7280; margin-bottom:8px;">${Math.round(reflects.length / days.length * 100)}% 작성률</div>
        <div style="font-size:12px; color:#9CA3AF;">${days.length}일 중 ${reflects.length}일 기록</div>
      </div>
    </div>

    <!-- 카테고리별 완료율 4칸 -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:12px;">
      ${Object.entries(cats).map(([cat, items]) => {
        const d = items.filter(t=>t.done).length;
        const tot = items.length;
        const r = tot > 0 ? Math.round(d / tot * 100) : 0;
        let cColor = '#FDE68A'; let cBg = '#FEF3C7';
        if (cat === 'job') { cColor = '#DBEAFE'; cBg = '#EFF6FF'; }
        else if (cat === 'growth') { cColor = '#D1FAE5'; cBg = '#ECFDF5'; }
        else if (cat === 'personal') { cColor = '#FCE7F3'; cBg = '#FDF2F8'; }
        
        return `<div style="background:${cBg}; border:1px solid ${cColor}; border-radius:8px; padding:12px;">
          <div style="font-size:12px; font-weight:bold; color:#4B5563; text-transform:capitalize; margin-bottom:4px;">${CAT_LABEL[cat] || cat}</div>
          <div style="font-size:16px; font-weight:bold; color:#111827; margin-bottom:2px;">${r}%</div>
          <div style="font-size:11px; color:#6B7280;">${d} / ${tot} 완료</div>
        </div>`;
      }).join('')}
    </div>
  </div>

  <!-- 섹션 2: 월간 분석 -->
  <div style="background:#FFF5F5; border:1.5px solid #FFD0D0; border-radius:16px; padding:24px; margin-bottom:24px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
      <div style="width:36px; height:36px; border-radius:50%; background:#FEE2E2; display:flex; align-items:center; justify-content:center; font-size:18px;">💡</div>
      <h3 style="margin:0; font-size:18px; font-weight:bold; color:#111827;">월간 분석</h3>
    </div>

    <!-- 실천율 카드들 -->
    <h4 style="font-size:14px; font-weight:bold; color:#374151; margin-bottom:12px;">🎯 실천율</h4>
    <div style="display:flex; flex-direction:column; gap:10px; margin-bottom:20px;">
      <div style="background:#FFFBEA; border:1px solid #FFE082; border-radius:12px; padding:14px 16px; color:#4B5563; font-size:13px; display:flex; gap:10px; align-items:center;">
        <span style="font-size:16px;color:#F97316;">!</span> <span>${overallRate >= 50 ? '이번 달 할일 완료율이 양호합니다. 훌륭한 성과입니다!' : '할일 완료율이 낮습니다. 일정을 재점검하고 작은 것부터 시작해보세요.'}</span>
      </div>
      <div style="background:#FFFBEA; border:1px solid #FFE082; border-radius:12px; padding:14px 16px; color:#4B5563; font-size:13px; display:flex; gap:10px; align-items:center;">
        <span style="font-size:16px;color:#F97316;">!</span> <span>${routineRate >= 50 ? '규칙적인 요소를 잘 해내고 있습니다. 습관 형성이 원활하네요!' : '의식적인 노력을 통해 필수 루틴 기록에 신경을 써주세요.'}</span>
      </div>
      <div style="background:#FFFBEA; border:1px solid #FFE082; border-radius:12px; padding:14px 16px; color:#4B5563; font-size:13px; display:flex; gap:10px; align-items:center;">
        <span style="font-size:16px;color:#F97316;">!</span> <span>${reflects.length >= 10 ? '꾸준히 성찰을 기록하고 있습니다. 자기 객관화에 큰 도움이 됩니다.' : '조금 더 자주 하루를 돌아보는 성찰을 기록해보세요.'}</span>
      </div>
    </div>

    <!-- 전월 대비 변화 -->
    <h4 style="font-size:14px; font-weight:bold; color:#374151; margin-bottom:12px;">↗ 전월 대비 변화</h4>
    <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06); font-size:13px; color:#9CA3AF; margin-bottom:20px; text-align:center;">
      전월 대비 큰 변화가 없습니다.
    </div>

    <!-- 월간 패턴 -->
    <h4 style="font-size:14px; font-weight:bold; color:#374151; margin-bottom:12px;">〰 월간 패턴</h4>
    ${ (() => {
      let bDay = days[0].label;
      let dN = 0, lN = 0, mMax = -1;
      days.forEach(day => {
        const dCount = todos.filter(t => t.log_date === day.str && t.done).length;
        const lCount = logs.filter(l => l.log_date === day.str && l.done).length;
        if ((dCount+lCount) > mMax) { mMax = dCount+lCount; bDay = day.label; dN = dCount; lN = lCount; }
      });
      return `<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px;">
        <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
          <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">📅 가장 활발한 일자</div>
          <div style="font-size:22px; font-weight:bold; color:#111827; margin-bottom:4px;">${bDay}일</div>
          <div style="font-size:12px; color:#6B7280;">할일 ${dN}개, 루틴 ${lN}개 완료</div>
        </div>
        <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
          <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">🏆 가장 완료율 높은 카테고리</div>
          <div style="font-size:22px; font-weight:bold; color:#111827; margin-bottom:4px;">${bestCatRate === -1 ? '-' : bestCat}</div>
          <div style="font-size:12px; color:#6B7280;">${bestCatRate === -1 ? '0' : Math.round(bestCatRate)}% 완료</div>
        </div>
      </div>`;
    })() }
  </div>

  <!-- 섹션 3: AI 월간 성찰 -->
  <div style="background:linear-gradient(135deg,#F3E8FF,#FCE7F3); border-radius:16px; padding:24px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
      <div style="width:36px; height:36px; border-radius:50%; background:white; display:flex; align-items:center; justify-content:center; font-size:18px;">✨</div>
      <h3 style="margin:0; font-size:18px; font-weight:bold; color:#111827;">AI 월간 성찰</h3>
    </div>
    
    <div id="monthly-ai-result" style="margin-bottom:20px;">
      <div style="text-align:center; padding:20px;">
        <div style="font-size:40px; margin-bottom:12px;">✨</div>
        <div style="font-size:16px; font-weight:bold; color:#374151; margin-bottom:6px;">AI 월간 성찰이 아직 없습니다</div>
        <div style="font-size:13px; color:#6B7280;">이번 달의 활동을 분석하여 맞춤형 피드백을 제공합니다.</div>
      </div>
    </div>

    <button id="monthly-ai-btn" class="ai-review-btn" onclick="generateMonthlyAIReview('${startStr}', '${endStr}')" style="width:100%; background:#8B5CF6; color:white; border:none; padding:14px; border-radius:12px; font-weight:bold; cursor:pointer;">
      ✦ AI 성찰 생성하기
    </button>
  </div>`;
"""
text = replace_html_block(text, "async function loadMonthlyPage() {", "const html = `", "document.getElementById('monthly-body').innerHTML = html;", monthly_html)


# ----- YEARLY -----
yearly_html = """const html = `
  <!-- 섹션 1: 연간 지표 -->
  <div style="background:#F8F9FF; border:1.5px solid #C7D2FE; border-radius:16px; padding:24px; margin-bottom:24px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
      <div style="width:36px; height:36px; border-radius:50%; background:#EDE9FE; display:flex; align-items:center; justify-content:center; font-size:18px;">📊</div>
      <h3 style="margin:0; font-size:18px; font-weight:bold; color:#111827;">${targetYear}년 연간 지표</h3>
    </div>
    
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px; margin-bottom:24px;">
      <!-- 루틴 실천율 -->
      <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
          <span>🔄</span> 루틴 실천율
        </div>
        <div style="font-size:28px; font-weight:bold; color:${routineRate === 0 ? '#EF4444' : (routineRate >= 50 ? '#10B981' : '#374151')}; margin-bottom:4px;">
          ${routineRate}%
        </div>
        <div style="font-size:13px; color:#6B7280; margin-bottom:8px;">${routineDone} / ${routineTotal} 체크</div>
        <div style="font-size:12px; color:#9CA3AF;">★모닝:-% 🌙나이트:-%</div>
      </div>
      
      <!-- 할일 완료율 -->
      <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
          <span>✅</span> 할일 완료율
        </div>
        <div style="font-size:28px; font-weight:bold; color:#374151; margin-bottom:4px;">
          ${overallRate}%
        </div>
        <div style="font-size:13px; color:#6B7280; margin-bottom:8px;">${doneAll} / ${totalAll} 완료</div>
        <div style="font-size:12px; color:#9CA3AF;">평균 일일 할일: ${Math.round(totalAll / 365)}개</div>
      </div>

      <!-- 성찰 작성일 -->
      <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
          <span>📝</span> 성찰 작성일
        </div>
        <div style="font-size:28px; font-weight:bold; color:${reflects.length === 0 ? '#EF4444' : '#374151'}; margin-bottom:4px;">
          ${reflects.length}일
        </div>
        <div style="font-size:13px; color:#6B7280; margin-bottom:8px;">${Math.round(reflects.length / 365 * 100)}% 작성률</div>
        <div style="font-size:12px; color:#9CA3AF;">365일 중 ${reflects.length}일 기록</div>
      </div>
    </div>

    <!-- 카테고리별 완료율 4칸 -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:12px;">
      ${Object.entries(cats).map(([cat, items]) => {
        const d = items.filter(t=>t.done).length;
        const tot = items.length;
        const r = tot > 0 ? Math.round(d / tot * 100) : 0;
        let cColor = '#FDE68A'; let cBg = '#FEF3C7';
        if (cat === 'job') { cColor = '#DBEAFE'; cBg = '#EFF6FF'; }
        else if (cat === 'growth') { cColor = '#D1FAE5'; cBg = '#ECFDF5'; }
        else if (cat === 'personal') { cColor = '#FCE7F3'; cBg = '#FDF2F8'; }
        
        return `<div style="background:${cBg}; border:1px solid ${cColor}; border-radius:8px; padding:12px;">
          <div style="font-size:12px; font-weight:bold; color:#4B5563; text-transform:capitalize; margin-bottom:4px;">${CAT_LABEL[cat] || cat}</div>
          <div style="font-size:16px; font-weight:bold; color:#111827; margin-bottom:2px;">${r}%</div>
          <div style="font-size:11px; color:#6B7280;">${d} / ${tot} 완료</div>
        </div>`;
      }).join('')}
    </div>
  </div>

  <!-- 섹션 2: 연간 분석 -->
  <div style="background:#FFF5F5; border:1.5px solid #FFD0D0; border-radius:16px; padding:24px; margin-bottom:24px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
      <div style="width:36px; height:36px; border-radius:50%; background:#FEE2E2; display:flex; align-items:center; justify-content:center; font-size:18px;">💡</div>
      <h3 style="margin:0; font-size:18px; font-weight:bold; color:#111827;">${targetYear}년 연간 분석</h3>
    </div>

    <!-- 실천율 카드들 -->
    <h4 style="font-size:14px; font-weight:bold; color:#374151; margin-bottom:12px;">🎯 실천율</h4>
    <div style="display:flex; flex-direction:column; gap:10px; margin-bottom:20px;">
      <div style="background:#FFFBEA; border:1px solid #FFE082; border-radius:12px; padding:14px 16px; color:#4B5563; font-size:13px; display:flex; gap:10px; align-items:center;">
        <span style="font-size:16px;color:#F97316;">!</span> <span>${overallRate >= 50 ? '올 한 해 할일 완료율이 양호합니다. 훌륭한 해였습니다!' : '할일 완료율이 낮습니다. 새해에는 작은 습관부터 시작해보세요.'}</span>
      </div>
      <div style="background:#FFFBEA; border:1px solid #FFE082; border-radius:12px; padding:14px 16px; color:#4B5563; font-size:13px; display:flex; gap:10px; align-items:center;">
        <span style="font-size:16px;color:#F97316;">!</span> <span>${routineRate >= 50 ? '규칙적인 요소를 잘 해내고 있습니다. 멋진 습관 형성이네요!' : '의식적인 노력을 통해 필수 루틴 기록에 신경을 써주세요.'}</span>
      </div>
      <div style="background:#FFFBEA; border:1px solid #FFE082; border-radius:12px; padding:14px 16px; color:#4B5563; font-size:13px; display:flex; gap:10px; align-items:center;">
        <span style="font-size:16px;color:#F97316;">!</span> <span>${reflects.length >= 50 ? '꾸준히 성찰을 기록했습니다. 내적 성장이 돋보입니다.' : '내년엔 조금 더 자주 자신을 돌아보는 시간을 가져보세요.'}</span>
      </div>
    </div>

    <!-- 전년 대비 변화 -->
    <h4 style="font-size:14px; font-weight:bold; color:#374151; margin-bottom:12px;">↗ 전년 대비 변화</h4>
    <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06); font-size:13px; color:#9CA3AF; margin-bottom:20px; text-align:center;">
      전년 대비 큰 변화가 없습니다.
    </div>

    <!-- 연간 패턴 -->
    <h4 style="font-size:14px; font-weight:bold; color:#374151; margin-bottom:12px;">〰 연간 패턴</h4>
    ${ (() => {
      let bMonth = 1;
      let wMonth = 1;
      let bMax = -1;
      let wMin = 999999;
      
      const mCounts = Array(12).fill(0);
      todos.filter(t=>t.done).forEach(t => {
        const mStr = t.log_date.split('-')[1];
        if(mStr) mCounts[parseInt(mStr, 10)-1] += 1;
      });
      logs.filter(l=>l.done).forEach(l => {
        const mStr = l.log_date.split('-')[1];
        if(mStr) mCounts[parseInt(mStr, 10)-1] += 1;
      });

      for(let i=0; i<12; i++) {
        if(mCounts[i] > bMax) { bMax = mCounts[i]; bMonth = i+1; }
        if(mCounts[i] < wMin) { wMin = mCounts[i]; wMonth = i+1; }
      }

      return `<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px;">
        <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
          <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">🏆 가장 완료율 높은 카테고리</div>
          <div style="font-size:22px; font-weight:bold; color:#111827; margin-bottom:4px;">${bestCatRate === -1 ? '-' : bestCat}</div>
          <div style="font-size:12px; color:#6B7280;">${bestCatRate === -1 ? '0' : Math.round(bestCatRate)}% 완료</div>
        </div>
        <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
          <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">📅 가장 활발한 월</div>
          <div style="font-size:22px; font-weight:bold; color:#111827; margin-bottom:4px;">${bMonth}월</div>
          <div style="font-size:12px; color:#6B7280;">기록 총합 ${bMax}개 기록</div>
        </div>
        <div style="background:white; border-radius:12px; padding:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
          <div style="font-size:13px; color:#6B7280; font-weight:500; margin-bottom:8px; display:flex; align-items:center; gap:6px;">📉 개선이 필요한 월</div>
          <div style="font-size:22px; font-weight:bold; color:#EF4444; margin-bottom:4px;">${wMonth}월</div>
          <div style="font-size:12px; color:#6B7280;">기록 총합 ${wMin === 999999 ? 0 : wMin}개 기록</div>
        </div>
      </div>`;
    })() }
  </div>

  <!-- 섹션 3: AI 연간 성찰 -->
  <div style="background:linear-gradient(135deg,#F3E8FF,#FCE7F3); border-radius:16px; padding:24px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
      <div style="width:36px; height:36px; border-radius:50%; background:white; display:flex; align-items:center; justify-content:center; font-size:18px;">✨</div>
      <h3 style="margin:0; font-size:18px; font-weight:bold; color:#111827;">AI 연간 성찰</h3>
    </div>
    
    <div id="yearly-ai-result" style="margin-bottom:20px;">
      <div style="text-align:center; padding:20px;">
        <div style="font-size:40px; margin-bottom:12px;">✨</div>
        <div style="font-size:16px; font-weight:bold; color:#374151; margin-bottom:6px;">AI 연간 성찰이 아직 없습니다</div>
        <div style="font-size:13px; color:#6B7280;">올 한 해의 활동을 분석하여 맞춤형 피드백을 제공합니다.</div>
      </div>
    </div>

    <button id="yearly-ai-btn" class="ai-review-btn" onclick="generateYearlyAIReview('${startStr}', '${endStr}')" style="width:100%; background:#8B5CF6; color:white; border:none; padding:14px; border-radius:12px; font-weight:bold; cursor:pointer;">
      ✦ AI 성찰 생성하기
    </button>
  </div>`;
"""
text = replace_html_block(text, "async function loadYearlyPage() {", "const html = `", "document.getElementById('yearly-body').innerHTML = html;", yearly_html)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

