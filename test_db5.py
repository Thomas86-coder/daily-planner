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
    
    req = urllib.request.Request(url + "/rest/v1/ai_reviews?select=id", headers={
        "apikey": key,
        "Authorization": f"Bearer {key}"
    })
    try:
        with urllib.request.urlopen(req) as res:
            print("ai_reviews test:", res.read().decode('utf-8'))
    except Exception as e:
        if hasattr(e, 'read'):
            print("ai_reviews error body:", e.read().decode('utf-8'))
        else:
            print("ai_reviews test error:", e)

