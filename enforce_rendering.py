import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# REMOVE ALERTS
text = text.replace("alert('주간 함수 호출됨');\n", "")
text = text.replace("alert('월간 함수 호출됨');\n", "")
text = text.replace("alert('연간 함수 호출됨');\n", "")

# FORCE RENDER - WEEKLY
text = text.replace(
    '''  if (bodyEl) bodyEl.innerHTML = html;

  // 강제 렌더링으로 빠른 확인 (try/catch 우회하여 100% 실행 보장)''',
    '''  if (bodyEl) {
    bodyEl.innerHTML = html;
    bodyEl.style.display = 'block';
    bodyEl.style.visibility = 'visible';
    bodyEl.style.opacity = '1';
  }

  const reviewContent = document.querySelector('#weekly-content, .weekly-content, [id*="weekly"][id*="content"], [class*="weekly"][class*="content"]');
  if (reviewContent) {
    reviewContent.style.display = 'block';
    reviewContent.style.visibility = 'visible';
    reviewContent.style.opacity = '1';
  }

  // 강제 렌더링으로 빠른 확인 (try/catch 우회하여 100% 실행 보장)'''
)

# FORCE RENDER - MONTHLY
text = text.replace(
    '''  if (bodyEl) bodyEl.innerHTML = html;

  // 강제 렌더링으로 빠른 확인''',
    '''  if (bodyEl) {
    bodyEl.innerHTML = html;
    bodyEl.style.display = 'block';
    bodyEl.style.visibility = 'visible';
    bodyEl.style.opacity = '1';
  }

  const reviewContent = document.querySelector('#monthly-content, .monthly-content, [id*="monthly"][id*="content"], [class*="monthly"][class*="content"]');
  if (reviewContent) {
    reviewContent.style.display = 'block';
    reviewContent.style.visibility = 'visible';
    reviewContent.style.opacity = '1';
  }

  // 강제 렌더링으로 빠른 확인'''
)

# FORCE RENDER - YEARLY
text = text.replace(
    '''  if (bodyEl) bodyEl.innerHTML = html;

  // 강제 렌더링으로 빠른 확인''',
    '''  if (bodyEl) {
    bodyEl.innerHTML = html;
    bodyEl.style.display = 'block';
    bodyEl.style.visibility = 'visible';
    bodyEl.style.opacity = '1';
  }

  const reviewContent = document.querySelector('#yearly-content, .yearly-content, [id*="yearly"][id*="content"], [class*="yearly"][class*="content"]');
  if (reviewContent) {
    reviewContent.style.display = 'block';
    reviewContent.style.visibility = 'visible';
    reviewContent.style.opacity = '1';
  }

  // 강제 렌더링으로 빠른 확인'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done enforcing")
