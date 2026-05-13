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
    
    # Check if there is data in ai_reviews
    req = urllib.request.Request(url + "/rest/v1/ai_reviews?select=*", headers={
        "apikey": key,
        "Authorization": f"Bearer {key}"
    })
    try:
        with urllib.request.urlopen(req) as res:
            data = res.read().decode('utf-8')
            print("ai_reviews data:", data)
    except Exception as e:
        if hasattr(e, 'read'):
            print("ai_reviews error body:", e.read().decode('utf-8'))
        else:
            print("ai_reviews test error:", e)

