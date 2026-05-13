import urllib.request
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

url_match = re.search(r"const SUPABASE_URL = '(.*?)'", content)
key_match = re.search(r"const SUPABASE_KEY = '(.*?)'", content)

if url_match and key_match:
    url = url_match.group(1)
    key = key_match.group(1)
    
    req = urllib.request.Request(url + "/rest/v1/reflections?select=*&limit=1", headers={
        "apikey": key,
        "Authorization": f"Bearer {key}"
    })
    try:
        with urllib.request.urlopen(req) as res:
            print("reflections schema check:", res.read().decode('utf-8'))
    except Exception as e:
        print("error:", e)

