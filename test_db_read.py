import urllib.request
import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

url_match = re.search(r"const SUPABASE_URL = '(.*?)'", content)
key_match = re.search(r"const SUPABASE_KEY = '(.*?)'", content)

if url_match and key_match:
    url = url_match.group(1)
    key = key_match.group(1)
    
    # 1. Read
    req1 = urllib.request.Request(url + "/rest/v1/ai_reviews?select=*", headers={
        "apikey": key,
        "Authorization": f"Bearer {key}"
    })
    try:
        with urllib.request.urlopen(req1) as res:
            print("READ:", res.read().decode('utf-8'))
    except Exception as e:
        if hasattr(e, 'read'):
            print("READ error:", e.read().decode('utf-8'))
        else:
            print("READ error:", e)

    # 2. Insert test
    req2 = urllib.request.Request(url + "/rest/v1/ai_reviews", method="POST", headers={
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }, data=json.dumps({"type": "weekly", "period": "test-2026-19", "content": "test content"}).encode('utf-8'))
    try:
        with urllib.request.urlopen(req2) as res:
            print("INSERT:", res.read().decode('utf-8'))
    except Exception as e:
        if hasattr(e, 'read'):
            print("INSERT error:", e.read().decode('utf-8'))
        else:
            print("INSERT error:", e)

