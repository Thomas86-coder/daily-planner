#!/usr/bin/env python3
"""
인생관리 시스템 - 로컬 라이브서버
실행: python3 dev.py
- http://localhost:8080 으로 자동 브라우저 열기
- index.html 변경 감지 시 브라우저 자동 새로고침 (LiveReload)
"""

import http.server
import socketserver
import threading
import webbrowser
import time
import os
import sys
from pathlib import Path

PORT = 8080
WATCH_FILES = ['index.html']
POLL_INTERVAL = 0.8  # 초

# ── LiveReload 스크립트 (브라우저에 주입) ──
LIVERELOAD_JS = b"""
<script>
(function(){
  var last = 0;
  setInterval(function(){
    fetch('/__livereload__?t=' + Date.now(), {cache:'no-store'})
      .then(r => r.text())
      .then(t => {
        var ts = parseInt(t);
        if(last > 0 && ts > last){ location.reload(); }
        last = ts;
      }).catch(()=>{});
  }, 800);
})();
</script>
</body>"""

class LiveReloadHandler(http.server.SimpleHTTPRequestHandler):
    reload_ts = int(time.time() * 1000)

    def do_GET(self):
        if self.path.startswith('/__livereload__'):
            body = str(LiveReloadHandler.reload_ts).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', len(body))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def send_response_only(self, code, message=None):
        super().send_response_only(code, message)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def log_message(self, fmt, *args):
        # /__livereload__ 요청은 로그 숨김
        if '/__livereload__' not in args[0]:
            path = args[0].split(' ')[1] if ' ' in args[0] else args[0]
            print(f"  → {path}")

    def copyfile(self, source, outputfile):
        """HTML 파일에 LiveReload 스크립트 주입"""
        content = source.read()
        if b'</body>' in content:
            content = content.replace(b'</body>', LIVERELOAD_JS)
        outputfile.write(content)


def watch_files(directory):
    """파일 변경 감지 루프"""
    mtimes = {}
    for f in WATCH_FILES:
        path = Path(directory) / f
        if path.exists():
            mtimes[f] = path.stat().st_mtime

    print(f"\n  감시 중: {', '.join(WATCH_FILES)}")
    print("  index.html 저장 시 브라우저가 자동으로 새로고침됩니다!\n")

    while True:
        time.sleep(POLL_INTERVAL)
        for f in WATCH_FILES:
            path = Path(directory) / f
            if path.exists():
                mtime = path.stat().st_mtime
                if f in mtimes and mtime != mtimes[f]:
                    mtimes[f] = mtime
                    LiveReloadHandler.reload_ts = int(time.time() * 1000)
                    print(f"  ✅ 변경 감지: {f} → 브라우저 새로고침")
                else:
                    mtimes[f] = mtime


def main():
    directory = Path(__file__).parent
    os.chdir(directory)

    # 서버 시작
    with socketserver.TCPServer(('', PORT), LiveReloadHandler) as httpd:
        print("\n" + "="*50)
        print("  🚀 인생관리 로컬 라이브서버 시작")
        print(f"  📍 http://localhost:{PORT}")
        print("  📝 index.html 저장하면 자동 새로고침")
        print("  🛑 종료: Ctrl+C")
        print("="*50)

        # 파일 감시 스레드
        watcher = threading.Thread(target=watch_files, args=(directory,), daemon=True)
        watcher.start()

        # 브라우저 자동 열기
        threading.Timer(0.8, webbrowser.open, args=(f'http://localhost:{PORT}',)).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n  서버 종료")
            sys.exit(0)


if __name__ == '__main__':
    main()
