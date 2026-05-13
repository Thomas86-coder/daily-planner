import urllib.request
import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

url_match = re.search(r"const SUPABASE_URL = '(.*?)'", content)
key_match = re.search(r"const SUPABASE_KEY = '(.*?)'", content)

if url_match and key_match:
    url = url_match.group(1)
    key = key_match.group(1)
    
    data = json.dumps({"log_date": "2026-17_weekly", "ai_feedback": "test"}).encode('utf-8')
    req = urllib.request.Request(url + "/rest/v1/reflections", data=data, headers={
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    })
    try:
        with urllib.request.urlopen(req) as res:
            print("Insert result:", res.read().decode('utf-8'))
    except Exception as e:
        print("Insert error:", e)

