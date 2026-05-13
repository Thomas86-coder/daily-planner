import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace button onclicks
text = text.replace(
    '''<button class="nav-btn" id="nav-weekly" onclick="navigate('weekly')">''',
    '''<button class="nav-btn" id="nav-weekly" onclick="switchToWeekly()">'''
)
text = text.replace(
    '''<button class="nav-btn" id="nav-monthly" onclick="navigate('monthly')">''',
    '''<button class="nav-btn" id="nav-monthly" onclick="switchToMonthly()">'''
)
text = text.replace(
    '''<button class="nav-btn" id="nav-yearly" onclick="navigate('yearly')">''',
    '''<button class="nav-btn" id="nav-yearly" onclick="switchToYearly()">'''
)

# Replace mob tab onclicks
text = text.replace(
    '''<a id="mob-weekly" class="mob-tab" onclick="navigate('weekly')"''',
    '''<a id="mob-weekly" class="mob-tab" onclick="switchToWeekly()"'''
)
text = text.replace(
    '''<a id="mob-monthly" class="mob-tab" onclick="navigate('monthly')"''',
    '''<a id="mob-monthly" class="mob-tab" onclick="switchToMonthly()"'''
)
text = text.replace(
    '''<a id="mob-yearly" class="mob-tab" onclick="navigate('yearly')"''',
    '''<a id="mob-yearly" class="mob-tab" onclick="switchToYearly()"'''
)

# Insert the functions right after navigate function
nav_func_end = text.find('function navigate(page) {')
if nav_func_end != -1:
    script_to_add = '''
window.switchToWeekly = function() {
  const loading = document.querySelector('#page-weekly .rv-spinner');
  if (loading) loading.style.display = 'none';
  const now = new Date();
  const headerEl = document.getElementById('weekly-title');
  if (headerEl) headerEl.innerHTML = `📅 ${now.getFullYear()}년 ${now.getMonth()+1}월 주간`;
  navigate('weekly');
};

window.switchToMonthly = function() {
  const loading = document.querySelector('#page-monthly .rv-spinner');
  if (loading) loading.style.display = 'none';
  const now = new Date();
  const headerEl = document.getElementById('monthly-title');
  if (headerEl) headerEl.innerHTML = `📅 ${now.getFullYear()}년 ${now.getMonth()+1}월`;
  navigate('monthly');
};

window.switchToYearly = function() {
  const loading = document.querySelector('#page-yearly .rv-spinner');
  if (loading) loading.style.display = 'none';
  const now = new Date();
  const headerEl = document.getElementById('yearly-title');
  if (headerEl) headerEl.innerHTML = `📅 ${now.getFullYear()}년`;
  navigate('yearly');
};

'''
    text = text[:nav_func_end] + script_to_add + text[nav_func_end:]


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done")
